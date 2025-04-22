import xtrack as xt
import numpy as np
import time
import os
from simulation_parameters import parameters as p

source_dir = os.getcwd() + '/'
context = p['context']
line = xt.Line.from_json(source_dir+'sps/sps_line_thick.json')
Csps = line.get_length() # 157.08 m
print('Loaded SPS line from sps/sps_line_thick.json.')
line.build_tracker(_context=context)

xymin = 0.1e-3
xymax = 20e-3
xystep = 0.1e-3
particles = line.build_particles(
    x=np.arange(xymin, xymax, xystep),
    y=np.arange(xymin, xymax, xystep),
    zeta=0, delta=0,
)

num_turns = 500
print('Now start tracking...')
start = time.time()
line.track(particles, num_turns=num_turns, turn_by_turn_monitor=True)
print('Tracking finished')
end = time.time()
print('Time taken for tracking: ', end-start)
# Format: [i,j]: i-th particle, j-th turn
np.save(source_dir+'test/amplitudeDetuning/x.npy', line.record_last_track.x)
np.save(source_dir+'test/amplitudeDetuning/y.npy', line.record_last_track.y)
np.save(source_dir+'test/amplitudeDetuning/px.npy', line.record_last_track.px)
np.save(source_dir+'test/amplitudeDetuning/py.npy', line.record_last_track.py)
np.save(source_dir+'test/amplitudeDetuning/zeta.npy', line.record_last_track.zeta)
np.save(source_dir+'test/amplitudeDetuning/delta.npy', line.record_last_track.delta)
np.save(source_dir+'test/amplitudeDetuning/state.npy', line.record_last_track.state)