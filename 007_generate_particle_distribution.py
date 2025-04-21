#%%
import xtrack as xt
import json
import numpy as np
import xpart as xp
import xobjects as xo
from simulation_parameters import parameters as p
from lib.parabolic_longitudinal_distribution import parabolic_longitudinal_distribution

print('*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~**~*~*~**~*~*~**~*~*~*')
print('007_generate_particle_distribution.py')
print('*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~**~*~*~**~*~*~**~*~*~*')

#%%
#########################################
# Load SPS line
#########################################
print('Loading SPS line from sps/sps_line_thick.json.')
line = xt.Line.from_json('sps/sps_line_thick.json')
line.build_tracker()
Csps = line.get_length()

#%%
#########################################
# Generate particle distribution
#########################################
print('Generating particles...')
context = xo.ContextCpu()
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

# Add injection missteering
particles.x += p['injection_missteering_x']
particles.y += p['injection_missteering_y']

with open('input/particles_initial.json', 'w') as fid:
    json.dump(particles.to_dict(), fid, cls=xo.JEncoder)
print('Number of macroparticles: ', p['n_part'])
print('Particles generated and saved to inputs/particles_initial.json.')
# %%
