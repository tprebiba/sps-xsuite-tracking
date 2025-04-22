import xtrack as xt
import pandas as pd
import xdeps as xd
from simulation_parameters import parameters as p

print('*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~**~*~*~**~*~*~**~*~*~*')
print('005_lattice_imperfections.py')
print('*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~**~*~*~**~*~*~**~*~*~*')

#########################################
# Load SPS line
#########################################
# print('Loading SPS line from sps/sps_line_thick.json.')
# line = xt.Line.from_json('sps/sps_line_thick.json')
# line.build_tracker()
# Csps = line.get_length()