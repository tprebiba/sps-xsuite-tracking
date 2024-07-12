import xobjects as xo
import numpy as np

p = {} 

# Tracking parameters
p['num_turns'] = 100 # number of turns to track
p['turns2saveparticles'] = [1,10,20, p['num_turns']-1] # turns to save particles object
p['turns2plot'] = [] # turns to plot phase space (while tracking)

# Beam intensity and emittance
p['n_part'] = int(1e3) # number of macroparticles
p['bunch_intensity'] = 40.0e10 # number of particles per bunch
p['macrosize'] = p['bunch_intensity']/p['n_part'] # number of charges per macroparticle
p['nemitt_x'] = 1e-6 # normalized emittance in x
p['nemitt_y'] = 1e-6 # normalized emittance in y
p['sigma_z'] = (400/4)*0.525*0.3 # bunch length in m
p['longitudinal_shape'] = 'gaussian' # 'parabolic' or 'coasting' or 'gaussian'

# Tunes (at injection), chromaticity, imperfections
p['qx_ini'] = 26.13
p['qy_ini'] = 26.18

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