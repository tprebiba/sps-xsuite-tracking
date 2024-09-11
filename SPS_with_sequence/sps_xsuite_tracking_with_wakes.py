import xtrack as xt
import xpart as xp
import xobjects as xo
import xfields as xf
from xpart.longitudinal.rf_bucket import RFBucket
from xpart.longitudinal.rfbucket_matching import RFBucketMatcher, ThermalDistribution
from scipy.constants import m_p , c
from dataclasses import dataclass
from tqdm import tqdm
import os
import h5py
import numpy as np
from cpymad.madx import Madx
#xt.enable_pyheadtail_interface()

# Saving function


def monitor_to_h5(particles_to_save, filename, compression_opts=4,  readwrite_opts='a',context='ContextCpu', verbose=False, collapse_into_avr=True):

    not_first_time = os.path.exists(filename)
    with h5py.File(filename, readwrite_opts) as hs:

        excluded_stuff=['XoStruct','extra_sources','add_particles']
        tracked_vars=['x','y','px','py']#,'delta','energy','kin_ps','kin_px','kin_py','kin_xprime','kin_yprime','ptau','pzeta','rpp','rvv','zeta'
        attrs=[a for a in dir(particles_to_save) if not (a.startswith('_')  or a in excluded_stuff )]

        for kk in tracked_vars:

            if verbose: print('Writing '+kk)
            dat=getattr(particles_to_save , kk)
            if context == 'ContextCpu':
                 dat_cpu=dat
            else:
                dat_cpu=dat.get()
            if not_first_time:
                if  kk in tracked_vars:
                    if collapse_into_avr:
                        dat_cpu=np.mean(dat_cpu,axis=0)
                    

                    hs[kk].resize( hs[kk].shape[0]+1, axis=0) 
                    hs[kk][-1,...] = dat_cpu

            else:
                if True:#isinstance(dat, np.ndarray ):

                    if collapse_into_avr:
                        dat_cpu=np.mean(dat_cpu,axis=0)     
                      
                    maxshape=tuple([None]*len(np.array([dat_cpu]).shape))
                    
                    dset = hs.create_dataset(kk, shape=np.array([dat_cpu]).shape, dtype=dat_cpu.dtype, maxshape=maxshape , compression='gzip', compression_opts=compression_opts)
                    dset[...] = dat_cpu
                else:
                    try:
                        hs[kk] = dat
                    except:
                        pass
    hs.close()

#Settings
average_values=True
gpu_device = 0
seq_name = "sps"

#target_dqy = -1.3
qx=26.13
qy=26.18
target_dqx = 0.2


p0c = 26e9


use_wakes = True
n_slices_wakes = 300

limit_z = 0.7
bunch_intensity = 2.5e10

bl_val_ns=3.2
sigma_z = bl_val_ns*1.e-9*c/4

nemitt_x=1.5e-6
nemitt_y=1.5e-6

n_part=int(1e3)
num_turns=6000
num_spacecharge_interactions = 540

# modes : frozen, quasi-frozen , pic
mode = 'frozen'

#########################################
# Load line
#########################################
mad = Madx()
#mad.chdir('sps')
mad.call('misc/sps_lhc_q26_gitlab.madx') 
mad.beam()
mad.use(seq_name)

# Select context 
context = xo.ContextCpu()
#context = xo.ContextCupy()


#Building line
line = xt.Line.from_madx_sequence(sequence=mad.sequence[seq_name],
           deferred_expressions=True, install_apertures=True,
           apply_madx_errors=False)


#Declaring reference particle

line.particle_ref = xt.Particles(p0c=p0c, q0=1.0 ,mass0=xt.PROTON_MASS_EV)

# Initializing RF cavity voltages

for el in line.elements:
    if isinstance(el, xt.Cavity):
        el.voltage = 4.5e6/24.
        el.frequency = 200266000.0
        el.lag = 180



#line.build_tracker()
tw = line.twiss()
line.unfreeze()

#Space-charge effects

# lprofile = xf.LongitudinalProfileQGaussian(
#        number_of_particles=bunch_intensity,
#        sigma_z=sigma_z,
#        z0=0.,
#        q_parameter=1.)

# xf.install_spacecharge_frozen(line=line,
#                   particle_ref=line.particle_ref,
#                   longitudinal_profile=lprofile,
#                   nemitt_x=nemitt_x, nemitt_y=nemitt_y,
#                   sigma_z=sigma_z,
#                   num_spacecharge_interactions=num_spacecharge_interactions,
#                   )


# Switch to PIC or quasi-frozen
if mode == 'frozen':
   pass # Already configured in line
elif mode == 'quasi-frozen':
   xf.replace_spacecharge_with_quasi_frozen(
                                   line,
                                   update_mean_x_on_track=True,
                                   update_mean_y_on_track=True)
elif mode == 'pic':
   pic_collection, all_pics = xf.replace_spacecharge_with_PIC(
       _context=context, line=line,
       n_sigmas_range_pic_x=8,
       n_sigmas_range_pic_y=8,
       nx_grid=256, ny_grid=256, nz_grid=100,
       n_lims_x=7, n_lims_y=3,
       z_range=(-3*sigma_z, 3*sigma_z))
else:
   raise ValueError(f'Invalid mode: {mode}')

if use_wakes:

   bucket_length_m = 12*sigma_z
   wake_table_filename = 'SPS_Q26.wake'
   
   wake_file_columns = ['time', 'dipole_x', 'dipole_y',
                     'quadrupole_x', 'quadrupole_y']
   waketable=xf.Wakefield.table_from_headtail_file( wake_table_filename, wake_file_columns, flag_pyht_units=True)
   
   waketable['time']*=-1
   waketable['dipole_x']*= -54.65/tw['betx'][0]
   waketable['dipole_y']*=-54.51/tw['bety'][0]
   waketable['quadrupole_x']*=-54.65/tw['betx'][0]
   waketable['quadrupole_y']*=-54.65/tw['bety'][0]



   use_components=['dipole_x', 'dipole_y', 'quadrupole_x', 'quadrupole_y']
   wakefield = xf.Wakefield.from_table(
    waketable,use_components,
    #use_components=['dipole_x', 'dipole_y','quadrupole_x', 'quadrupole_y'],
    zeta_range=(-0.5*bucket_length_m, 0.5*bucket_length_m),
    num_slices=n_slices_wakes,
    num_turns=5.,
    circumference=line.get_length()
)

   # Specity that the wakefield element needs to run on CPU and that lost
   # particles need to be hidden for this element (required by PyHEADTAIL)
   wakefield.needs_cpu = True
   wakefield.needs_hidden_lost_particles = True

   # Insert element in the line
   line.insert_element(element=wakefield,name="wakefield", at_s=0)


   # Set chromaticities
qpvs=np.linspace(0,-2,20)

for qpv in qpvs:

   line.match(
      vary=[
         xt.Vary('qph_setvalue', step=0.001),
         xt.Vary('qpv_setvalue', step=0.001),
      ],
      targets = [
         xt.Target('dqx', target_dqx*qx, tol=1e-4),
         xt.Target('dqy', qpv*qy, tol=1e-4)
      ],
      method='4d')

   # We need to unfreeze the line to make adjustments


   line.unfreeze()


   #building tracker
   line.build_tracker(_context=context)


   #Matching particle distribution
   line_sc_off = line.filter_elements(exclude_types_starting_with='SpaceCh')

   particles = xp.generate_matched_gaussian_bunch(_context=context,
         num_particles=n_part, total_intensity_particles=bunch_intensity,
         nemitt_x=nemitt_x, nemitt_y=nemitt_y, sigma_z=sigma_z,
         particle_ref=line.particle_ref, line=line_sc_off)

   particles.circumference = line.get_length() # Needed by pyheadtail


   #tracking


   filename=f'sps_q26_qpv{qpv}_avr.h5'

   print(f'Running qpv: {qpv}')
   
   for i_turn in tqdm(range(num_turns), desc = "SPS tracking: "):
      if i_turn == 0: 
        particles.y += 0
      line.track(particles, num_turns=1)
   
      monitor_to_h5(particles,filename,collapse_into_avr=True, context=str(context))
      

   del(particles)

