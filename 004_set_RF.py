import xtrack as xt
import pandas as pd
import xdeps as xd
from simulation_parameters import parameters as p

print('*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~**~*~*~**~*~*~**~*~*~*')
print('004_set_RF.py')
print('*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~**~*~*~**~*~*~**~*~*~*')

#########################################
# Load SPS line
#########################################
print('Loading SPS line from sps/sps_line_thick.json.')
line = xt.Line.from_json('sps/sps_line_thick.json')
line.build_tracker()
Csps = line.get_length()

#########################################
# Set 200 MHz RF cavities
#########################################
print('Setting 200 MHz RF cavities.')
print('Put everything in a single cavity; to be improved later.')
line.element_refs['actcse.31632'].voltage = 1e6#p['v200'] # in V
line.element_refs['actcse.31632'].frequency = p['freq200'] # in Hz
line.element_refs['actcse.31632'].lag = p['lag200'] # in degrees
print('SPS circumference: %s m'%Csps)
frev = 0.99776*2.99792458e8/Csps # revolution frequency in Hz0
print('SPS revolution frequency at 14 GeV/c: %s Hz'%frev)
print('Harmonic number h for 200 MHz RF cavity: %s'%(200e6/frev))

#########################################
# Set 800 MHz RF cavities
#########################################
print('Setting 800 MHz RF cavities.')
print('Skipping for now.')

#########################################
# Check if 6D twiss works and save line
#########################################
print('Switching to 6D twiss.')
line.twiss_default['method'] = '6d'
print('Twissing')
try:
    tw = line.twiss() # ContextCpu by default
    print('Twiss computed.')
    tw.to_pandas().to_pickle('sps/sps_twiss_thick.pkl')
    print('Twiss computed and saved to sps/sps_twiss_thick.pkl.')
    print('Synchrotron tune: %s'%tw.qs)
    line.to_json('sps/sps_line_thick.json')
    print('Line saved to sps/sps_line_thick.json')
except Exception as e:
    print('Exception: %s'%e)
    print('Twiss failed. Check if the line is built correctly.')
    raise