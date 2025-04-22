import xtrack as xt
import xpart as xp
import numpy as np
import time
import os
from simulation_parameters import parameters as p
from lib.parabolic_longitudinal_distribution import parabolic_longitudinal_distribution
from lib.space_charge_helpers import get_particle_tunes

source_dir = os.getcwd() + '/'
context = p['context']
line = xt.Line.from_json(source_dir+'sps/sps_line_thick.json')
Csps = line.get_length() # 157.08 m
print('Loaded SPS line from sps/sps_line_thick.json.')
line.build_tracker(_context=context)

p['n_part'] = int(1e5)
if p['longitudinal_shape'] == 'gaussian':
    particles = xp.generate_matched_gaussian_bunch(_context=context, num_particles=p['n_part'],
                            total_intensity_particles=p['bunch_intensity'],
                            nemitt_x=p['nemitt_x'], nemitt_y=p['nemitt_y'], sigma_z=p['sigma_z'],
                            particle_ref=line.particle_ref,
                            line=line
                            )
    print('Gaussian longitudinal distribution.')
elif p['longitudinal_shape'] == 'parabolic':
    particles = parabolic_longitudinal_distribution(_context=context, num_particles=p['n_part'],
                                total_intensity_particles=p['bunch_intensity'],
                                nemitt_x=p['nemitt_x'], nemitt_y=p['nemitt_y'], sigma_z=p['sigma_z'],
                                particle_ref=line.particle_ref,
                                line=line
                                )
    print('Parabolic longitudinal distribution.')
elif p['longitudinal_shape'] == 'coasting':
    # To be improved...
    # Generate particles
    particles = parabolic_longitudinal_distribution(_context=context, num_particles=p['n_part'],
                                total_intensity_particles=p['bunch_intensity'],
                                nemitt_x=p['nemitt_x'], nemitt_y=p['nemitt_y'], sigma_z=p['sigma_z'],
                                particle_ref=line.particle_ref,
                                line=line,
                                #line=line_sc_off
                                )
    # "Force" coasting beam
    particles.zeta = np.random.uniform(-Csps/2, Csps/2, p['n_part'])
    #particles.delta = np.random.uniform(-1.36e-3, 1.36e-3, n_part) # not parabolic
    print("'Forcing' coasting beam using numpy (uniform zeta).")

# removing longitudinal motion
#particles.delta = 0
#particles.zeta = 0
line_sc_off = line.filter_elements(exclude_types_starting_with='SpaceCh')
tw = line_sc_off.twiss(particle_ref=line.particle_ref,  at_elements=[0])

num_turns = 1
start = time.time()
particles0 = particles.copy()
print('Now start tracking for one turn...')
line.track(particles, num_turns=num_turns, turn_by_turn_monitor=False)
print('Tracking done')
end = time.time()
print(f'Tracking took {end-start} s')
particles1 = particles.copy()

if particles1._num_lost_particles == 0: # no particles were lost
    _qx, _Jx = get_particle_tunes(particles0.x, particles0.px, particles1.x, particles1.px, tw['betx'][0], tw['alfx'][0],
                                  tw['dx'][0], tw['dpx'][0], particles0.delta)
    _qy, _Jy = get_particle_tunes(particles0.y, particles0.py, particles1.y, particles1.py, tw['bety'][0], tw['alfy'][0],
                                  tw['dy'][0], tw['dpy'][0], particles0.delta)
np.save('test/tuneSpread/qx_pic',_qx)
np.save('test/tuneSpread/qy_pic',_qy)
np.save('test/tuneSpread/jx_pic.npy',_Jx)
np.save('test/tuneSpread/jy_pic.npy',_Jy)
print('Tune spread calculated and saved to test/tuneSpread/qx_pic, test/tuneSpread/qy_pic, test/tuneSpread/jx_pic.npy, test/tuneSpread/jy_pic.npy')