import xobjects as xo
import numpy as np
from scipy.constants import c

p = {} 

# Tracking parameters
p['num_turns'] = 1200 # number of turns to track
p['turns2saveparticles'] = [1,2,10,50, 100, 200, 300, 400, 500, p['num_turns']-1] # turns to save particles object
p['turns2plot'] = [] # turns to plot phase space (while tracking)

# Collective monitor
p['collective_monitor'] = True # if True, a collective monitor is installed in the line
p['flush_data_every'] = 5 # flush data every n turns
p['base_file_name'] = 'output/collective_monitor_10' # base file name for the collective monitor
p['monitor_bunches'] = True # if True, the monitor will save data for all bunches
p['monitor_slices'] = True # if True, the monitor will save data for all slices
p['monitor_particles'] = False # if True, the monitor will save data for all particles (HEAVY)

# Beam intensity and emittance
p['gamma0'] = 14.953 # gamma relativistic for SFTPRO flat-bottom at 14 GeV/c
p['beta0'] = 0.99776 # beta relativistic for SFTPRO flat-bottom at 14 GeV/c
p['n_part'] = int(1e5) # total number of macroparticles
p['number_of_bunches'] = 100 #420*5 # number of bunches
p['total_intensity'] = 2.4e13*p['number_of_bunches']/2100 # total number of particles in the ring
p['bunch_intensity'] = p['total_intensity']/p['number_of_bunches'] # number of particles per bunch
p['bunch_spacing_m'] = 5e-9*p['beta0']*c # bunch spacing in m (5ns bucket length)
p['macrosize'] = p['bunch_intensity']/p['n_part'] # number of charges per macroparticle
p['nemitt_x'] = 12e-6 # normalized emittance in x
p['nemitt_y'] = 4e-6# normalized emittance in y
p['sigma_z'] = (2.5e-9/4)*p['beta0']*c # bunch length in m (2.5ns based on Giulia's measurements, is it 4 sigma?)
p['longitudinal_shape'] = 'gaussian' # 'parabolic' or 'coasting' or 'gaussian'; used only if 1 bunch

# Lattice: tunes, chromaticity, octupoles, imperfections, ...
# I prefer the (x,y) notation instead of (h,v) but I will keep the same name
# as the original line knobs
# Tunes
p['qh_setvalue'] = 26.62 # 26.29
p['qv_setvalue'] = 26.58 # 26.22
# Chromaticity (Qprime i.e. d Q / d delta) (mind: LSA settings are in normalized units Qprime/Q)
# chroma_mode controls both chromaticities (for now)
# can be: 'natural' (no sextupoles) or 'default' (madx default) or 'manual' (user defined)
p['chroma_mode'] = 'manual' 
qph_measured = -0.05*p['qh_setvalue'] # Measured https://logbook.cern.ch/elogbook-server/GET/showEventInLogbook/4243321; LSA setting 0.6727
qpv_measured = -0.10*p['qv_setvalue'] # Measured https://logbook.cern.ch/elogbook-server/GET/showEventInLogbook/4243321; LSA setting -0.624
p['qph_setvalue'] = qph_measured # used only if p['chroma_mode'] == 'manual'
p['qpv_setvalue'] = qpv_measured # used only if p['chroma_mode'] == 'manual'
# Injection misteering
p['injection_missteering_x'] = 0.0 # in m
p['injection_missteering_y'] = 0.0 # in m
# RF
p['prepare_acceleration'] = 1 # if 0 all cavities will be switched off
p['v200'] = 1.8e6 # 0.8e6 total RF voltage in V
p['freq200'] = 200e6 # RF frequency in Hz
p['lag200'] = 0#180 # RF phase
p['h'] = 4621 # harmonic number freq200/frev
p['bucket_length'] = 5e-9*p['beta0']*c # bucket length in m (5ns bucket length)
p['filling_scheme'] = np.zeros(p['h'], dtype=int)
# gap between injections is 210 buckets
p['filling_scheme'][0:p['number_of_bunches']] = 1 # each element holds a one if the slot is filled.
# Octupoles
p['klof'] = 0.8986 # focusing octupole strength in 1/m^4 (not integrated)
p['klod'] = -0.9117 # defocusing octupole strength in 1/m^4 (not integrated)

# Setup slicing and line cycling
#p['slices'] = 3 # number of slices in thin lattice
# To have the starting point of the lattice at a different location, None otherwise
# Relevant ONLY when using simulated particle distribution
#p['element_to_cycle'] = None # line starts at the start of the 1st sector (NOT at the stripping foil)

# Setup space charge calculation
p['install_space_charge'] = False # if True, space charge is installed
p['space_charge_mode'] = 'frozen' # 'frozen' or 'pic' or 'quasi-frozen'
p['num_spacecharge_interactions'] = 200 # space charge interactions per turn
p['pic_solver'] = 'FFTSolver2p5D' # `FFTSolver2p5DAveraged` or `FFTSolver2p5D` or 'FFTSolver3D'

# Setup wakefields
p['install_wakes'] = False # if True, wakes are installed
p['wakes_file_name'] = 'wakes/SPS_Q26.wake'
p['wake_file_columns'] = ['time', 'dipole_x', 'dipole_y', 'quadrupole_x', 'quadrupole_y']
p['use_components'] = ['dipole_x', 'dipole_y', 'quadrupole_x', 'quadrupole_y'] # columns to use from the wake table
p['wake_scaling_factor'] = 1
p['num_slices_wakes'] = 20 # 100number of bunch slices
p['num_turns_wakes'] = 7 # number of turns to apply wakes

# Setup resources
p['GPU_FLAG'] = False # if True, GPU is used
if p['GPU_FLAG']:
    p['context'] = xo.ContextCupy()
else:
    p['context'] = xo.ContextCpu()

parameters = p