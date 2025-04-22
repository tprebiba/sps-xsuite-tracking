import xobjects as xo
import numpy as np

p = {} 

# Tracking parameters
p['num_turns'] = 1200 # number of turns to track
p['turns2saveparticles'] = [1,2,10,50, p['num_turns']-1] # turns to save particles object
p['turns2plot'] = [] # turns to plot phase space (while tracking)

# Beam intensity and emittance
p['gamma0'] = 14.953 # gamma relativistic for SFTPRO flat-bottom
p['n_part'] = int(1e5) # number of macroparticles
p['bunch_intensity'] = 1.5e13/2100 # number of particles per bunch
p['macrosize'] = p['bunch_intensity']/p['n_part'] # number of charges per macroparticle
p['nemitt_x'] = 12e-6 # normalized emittance in x
p['nemitt_y'] = 4e-6# normalized emittance in y
p['sigma_z'] = (5/4)*0.99776*0.3 # bunch length in m (2.5ns based on Giulia's measurements, is it 4 sigma?)
p['longitudinal_shape'] = 'gaussian' # 'parabolic' or 'coasting' or 'gaussian'

# Lattice: tunes, chromaticity, octupoles, imperfections, ...
# I prefer the (x,y) notation instead of (h,v) but I will keep the same name
# as the original line knobs
# Tunes
p['qh_setvalue'] = 26.62 # 26.29
p['qv_setvalue'] = 26.58 # 26.22
# Chromaticity (Qprime i.e. d Q / d delta);
# chroma_mode controls both chromaticities (for now)
# can be: 'natural' (no sextupoles) or 'default' (madx default) or 'manual' (user defined)
p['chroma_mode'] = 'manual' 
p['qph_setvalue'] = 0.6727 # used only if p['chroma_mode'] == 'manual'
p['qpv_setvalue'] = -0.624 # used only if p['chroma_mode'] == 'manual'
# Injection misteering
p['injection_missteering_x'] = 0.0 # in m
p['injection_missteering_y'] = 0.0 # in m
# RF
p['prepare_acceleration'] = 1 # if 0 all cavities will be switched off
p['v200'] = 1e6 # total RF voltage in V
p['freq200'] = 200e6 # RF frequency in Hz
p['lag200'] = 0#180 # RF phase
# Octupoles
p['klof'] = 0.8986 # focusing octupole strength in 1/m^4 (not integrated)
p['klod'] = -0.9117 # defocusing octupole strength in 1/m^4 (not integrated)

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