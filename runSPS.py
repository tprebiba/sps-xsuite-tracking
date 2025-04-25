#%%
import xtrack as xt
import xobjects as xo
import xfields as xf
import xpart as xp
import numpy as np
import json
import time
import os
from lib.statisticalEmittance import StatisticalEmittance as stE
from lib.online_plotting import plot_phasespace

#########################################
# Load parameters
#########################################
from simulation_parameters import parameters as p
source_dir = os.getcwd() + '/'

#%%
#########################################
# Load SPS line
#########################################
context = p['context']
line = xt.Line.from_json(source_dir+'sps/sps_line_thick.json')
Csps = line.get_length() # 6911.52
print('Loaded SPS line from sps/sps_line_thick.json.')

#%%
#########################################
# Install space charge nodes
#########################################
if p['install_space_charge']:
    mode = p['space_charge_mode']
    print(f'Installing space charge in {mode} mode')
    # install nodes in lattice frozen-like (exact parameters do not matter if pic is used)
    lprofile = xf.LongitudinalProfileQGaussian(number_of_particles=p['bunch_intensity'], 
                                            sigma_z=p['sigma_z'], 
                                            z0=0, q_parameter=1.)
    xf.install_spacecharge_frozen(line=line,
                    particle_ref=line.particle_ref,
                    longitudinal_profile=lprofile,
                    nemitt_x=p['nemitt_x'], nemitt_y=p['nemitt_y'],
                    sigma_z=p['sigma_z'],
                    num_spacecharge_interactions=p['num_spacecharge_interactions'],
                    delta_rms=1e-3
                    )
    if mode == 'frozen':
        pass # Already configured in line
    # switch to pic or quasi-frozen
    elif mode == 'quasi-frozen':
        xf.replace_spacecharge_with_quasi_frozen(line,
                                        update_mean_x_on_track=True,
                                        update_mean_y_on_track=True)
    elif mode == 'pic':
        pic_collection, all_pics = xf.replace_spacecharge_with_PIC(
            _context=context, line=line,
            n_sigmas_range_pic_x=8, # to be reviewed
            n_sigmas_range_pic_y=8, # to be reviewed
            nx_grid=128, ny_grid=128, nz_grid=64, # to be reviewed
            n_lims_x=7, n_lims_y=5,#3,
            z_range=(-3*p['sigma_z'], 3*p['sigma_z']), 
            #z_range=(-Csps/2, Csps/2), 
            solver=p['pic_solver'],
            )
    else:
        raise ValueError(f'Invalid mode: {mode}')
    print('Space charge installed')
else:
     print('Skipping space charge...')

#%%
#########################################
# Install multi-bunch monitor
#########################################
if p['collective_monitor']:
    print('Installing collective monitor')
    import xwakes as xw
    monitor = xw.CollectiveMonitor(
        base_file_name=p['base_file_name'],
        backend='hdf5', # 'json' or 'hdf5'
        monitor_bunches=p['monitor_bunches'],
        monitor_slices=p['monitor_slices'],
        monitor_particles=p['monitor_particles'],
        num_slices=p['num_slices_wakes'],
        flush_data_every=p['flush_data_every'],
        zeta_range=(-p['bucket_length']/2, p['bucket_length']/2), # for each bunch
        filling_scheme=p['filling_scheme'],
        bunch_spacing_zeta=p['bunch_spacing_m'],
    )
    line.discard_tracker()
    line.insert_element(index=0, element=monitor, name='collective_monitor')
    line.build_tracker()
    print('Collective monitor installed at the beginning of the line.')

#%%
#########################################
# Install wakes
#########################################
if p['install_wakes']:
    import xwakes as xw
    waketable = xw.read_headtail_file(p['wakes_file_name'],p['wake_file_columns'])
    for col in p['use_components']:
        waketable[col] = waketable[col] * p['wake_scaling_factor']

    wf = xw.WakeFromTable(waketable, columns=p['use_components'])
    wf.configure_for_tracking(zeta_range=(-p['bucket_length']/2, p['bucket_length']/2),
                            num_slices=p['num_slices_wakes'],
                            bunch_spacing_zeta=p['bunch_spacing_m'],
                            filling_scheme=p['filling_scheme'],
                            num_turns=p['num_turns_wakes'],
                            circumference=Csps
                            )
    line.discard_tracker()
    line.insert_element(index=-1, element=wf, name='wakefield')
    line.build_tracker()
    print('Wakes installed at the end of the line.')

#%%
#########################################
# Build tracker
#########################################
line.build_tracker(_context=context)
print('Tracker built')
#line_sc_off = line.filter_elements(exclude_types_starting_with='SpaceCh') # to remove space charge
#print('Keeping line_sc_off: line without space charge knobs.')

#%%
#########################################
# Setup particles for injection
#########################################
with open(source_dir+'input/particles_initial.json', 'r') as fid:
    particles = xp.Particles.from_dict(json.load(fid), _context=context)
print('Loaded particles from input/particles_initial.json.')
particles.reorganize() # to run on GPU in case particles are generated on CPU

#%%
#########################################
# Last configs
#########################################
if p['prepare_acceleration'] == 0:
    # Switching all RF cavities OFF
    print('Switching off all cavities.')
    line_table = line.get_table()
    element_mask = np.where(line_table['element_type']=='Cavity')[0]
    for i in element_mask:
        cav_name = line_table['name'][i]
        line.element_refs[cav_name].voltage = 0
        line.element_refs[cav_name].frequency = 0
    print('All cavities switched off.')
    line.twiss_default['method'] = '4d'
    print('Twiss method set to 4d.')
line.enable_time_dependent_vars = False
#line.dt_update_time_dependent_vars = 3e-6 # approximately every 3 turns
line.vars.cache_active = False
line.vars['t_turn_s'] = 0.0
output = []
if p['GPU_FLAG']:
    r = stE(context='GPU')
else:
    r = stE(context='CPU')
output=[]
intensity = []
if ((p['collective_monitor']==False) and (p['install_space_charge']==False)):
    print('Nocollective elements installed, optimizing line for tracking.')
    line.optimize_for_tracking()
    print('Line optimized for tracking.')

#%%
#########################################
# Start tracking
# To be improved
#########################################
num_turns = p['num_turns']
print('Now start tracking...')
start = time.time()
for ii in range(num_turns):
    print(f'Turn {ii} out of {num_turns}')

    # keep particles within the ring circumference
    particles.zeta = (particles.zeta+Csps/2)%Csps-Csps/2

    # track one turn
    #line.track(particles, turn_by_turn_monitor=True)
    line.track(particles, num_turns=1)

    # update output
    bunch_moments=r.measure_bunch_moments(particles)
    if p['GPU_FLAG']:
        output.append([len(r.coordinate_matrix[0]),bunch_moments['nemitt_x'].tolist(),bunch_moments['nemitt_y'].tolist(),bunch_moments['emitt_z'].tolist(), np.mean((particles.x).get()), np.mean((particles.y).get()), np.mean((particles.zeta).get()), np.mean((particles.delta).get())])
    else:
        output.append([len(r.coordinate_matrix[0]),bunch_moments['nemitt_x'].tolist(),bunch_moments['nemitt_y'].tolist(),bunch_moments['emitt_z'].tolist(), np.mean(particles.x), np.mean(particles.y), np.mean(particles.zeta), np.mean(particles.delta)])

    # save every some turns
    if ii in p['turns2saveparticles']:
        print(f'Saving turn {ii}')
        with open(source_dir+f'output/particles_turn_{ii:05d}.json', 'w') as fid:
            json.dump(particles.to_dict(), fid, cls=xo.JEncoder)
            print(f'Particles saved to output/particles_turn_{ii:05d}.json.')
        #np.save(source_dir+'output/distribution_'+str(int(ii)), r.coordinate_matrix)
        #print(f'Distribution saved to output/distribution_{ii}.npy.')
        ouput=np.array(output)
        np.save(source_dir+'output/emittances', output)
        print(f'Emittances saved to output/emittances.npy.')
    
    # plot every some turns
    if ii in p['turns2plot']:
        plot_phasespace(particles, ii, png_dir=source_dir+'output/', bins=600, vmin=2, GPU_FLAG=p['GPU_FLAG'])
        print(f'Phase space plot saved to output/turn_{ii:05d}.png.')

end = time.time()
print('Tracking finished.')
print('Total seconds = ', end - start)
np.save(source_dir+'output/emittances', output)
print(f'Emittances saved to output/emittances.npy.')
