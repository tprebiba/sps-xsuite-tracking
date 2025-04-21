import xobjects as xo
import numpy as np

p = {} 

# Tracking parameters
p['num_turns'] = 100 # number of turns to track
p['turns2saveparticles'] = [1,10,50, p['num_turns']-1] # turns to save particles object
p['turns2plot'] = [] # turns to plot phase space (while tracking)

# Beam intensity and emittance
p['n_part'] = int(5e3) # number of macroparticles
p['bunch_intensity'] = 40.0e10 # number of particles per bunch
p['macrosize'] = p['bunch_intensity']/p['n_part'] # number of charges per macroparticle
p['nemitt_x'] = 1.5e-6 # normalized emittance in x
p['nemitt_y'] = 1.5e-6 # normalized emittance in y
p['sigma_z'] = (5/4)*0.999*0.3 # bunch length in m
p['longitudinal_shape'] = 'gaussian' # 'parabolic' or 'coasting' or 'gaussian'

# Lattice: tunes, chromaticity, octupoles, imperfections, ...
# I prefer the (x,y) notation instead of (h,v) but I will keep the same name
# as the original line knobs
# Tunes
p['qh_setvalue'] = 26.62
p['qv_setvalue'] = 26.58
# Chromaticity (Qprime i.e. d Q / d delta);
p['qph_setvalue'] = 1.078 # if None, the default MAD-X value is used
p['qpv_setvalue'] = 0.347 # if None, the default MAD-X value is used
# Injection misteering
p['injection_missteering_x'] = 0.0 # in m
p['injection_missteering_y'] = 0.0 # in m
# RF
p['prepare_acceleration'] = 1 # if 0 all cavities will be switched off
p['v200'] = 1e6 # total RF voltage in V
p['freq200'] = 200e6 # RF frequency in Hz
p['lag200'] = 0#180 # RF phase
# Octupoles
p['klof'] = 2.5 # focusing octupole strength in 1/m^4 (not integrated)
p['klod'] = -2.5 # defocusing octupole strength in 1/m^4 (not integrated)

# Setup slicing and line cycling
p['slices'] = 3 # number of slices in thin lattice
# To have the starting point of the lattice at a different location, None otherwise
# Relevant ONLY when using simulated particle distribution
p['element_to_cycle'] = None # line starts at the start of the 1st sector (NOT at the stripping foil)

# Setup space charge calculation
p['install_space_charge'] = False # if True, space charge is installed
p['space_charge_mode'] = 'pic' # 'frozen' or 'pic' or 'quasi-frozen'
p['num_spacecharge_interactions'] = 160 # space charge interactions per turn
p['pic_solver'] = 'FFTSolver2p5D' # `FFTSolver2p5DAveraged` or `FFTSolver2p5D` or 'FFTSolver3D'

# Setup resources
p['GPU_FLAG'] = False # if True, GPU is used
if p['GPU_FLAG']:
    p['context'] = xo.ContextCupy()
else:
    p['context'] = xo.ContextCpu()

parameters = p