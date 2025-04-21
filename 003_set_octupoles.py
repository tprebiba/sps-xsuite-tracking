#%%
import xtrack as xt
import pandas as pd
import xdeps as xd
from simulation_parameters import parameters as p

print('*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~**~*~*~**~*~*~**~*~*~*')
print('003_set_octupoles.py')
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
# Check octupoles
#########################################
_check_octupoles = False
if _check_octupoles:
    print('Checking octupoles.')
    
    # Check if there are any octupoles in the line
    octupole_elements = {name: elem for name, elem in line.element_dict.items() if isinstance(elem, xt.elements.Octupole)}
    if len(octupole_elements) == 0:
        print('No octupoles found in the line.')
    else:
        print(f'Found {len(octupole_elements)} octupoles in the line.')


    # Check octupole types and their strengths (just check one of them)
    selected_octupoles = {}
    for key in ['lod', 'lof', 'loe']:
        for name, elem in octupole_elements.items():
            if key in name.lower():
                selected_octupoles[name] = elem
                break
    for name,elem in selected_octupoles.items():
        print(f'Octupole {name} strength is defined as:')
        print(line.element_refs[name].knl[3]._info())
   
    # Check initial octupole settings
    #allvars = line.vars.get_table()
    #print('Initial octupole settings:')
    #print(allvars.rows['.*lof*'])
    #print(allvars.rows['.*lod*'])
    print(line.vars['klod']._info(limit=None))
    print(line.vars['klof']._info(limit=None))
    #print(line.vars['kloe']._info(limit=None))

#%%
#########################################
# Set octupoles
#########################################
print('Setting octupoles.')
# Set octupole strengths
line.vars['klod'] = p['klod']*100
line.vars['klof'] = p['klof']*100

#%%
########################################
# Get amplitude detuning coefficients
########################################
_check_detuning = False
if _check_detuning:
    print('Getting amplitude detuning coefficients.')
    
    # Parameters:
    # nemitt_x (float) – Normalized emittance in the x-plane. Default is 1e-6.
    # nemitt_y (float) – Normalized emittance in the y-plane. Default is 1e-6.
    # num_turns (int) – Number of turns for tracking. Default is 256.
    # a0_sigmas (float) – Amplitude of the first particle (in sigmas). Default is 0.01.
    # a1_sigmas (float) – Amplitude of the second particle (in sigmas). Default is 0.1.
    # a2_sigmas (float) – Amplitude of the third particle (in sigmas). Default is 0.2.
    # Returns:
    # det_xx (float) – Amplitude detuning coefficient dQx / dJx.
    # det_yy (float) – Amplitude detuning coefficient dQy / dJy.
    # det_xy (float) – Amplitude detuning coefficient dQx / dJy.
    # det_yx (float) – Amplitude detuning coefficient dQy / dJx.
    dtc = line.get_amplitude_detuning_coefficients(nemitt_x=p['nemitt_x'], nemitt_y=p['nemitt_y'], num_turns=256, 
                                                   a0_sigmas=0.01, a1_sigmas=0.1, a2_sigmas=3)
    print('Amplitude detuning coefficients:')
    print(dtc)

# %%
#########################################
# Re-twissing and saving
#########################################
print('Twiss after matching:')
tw = line.twiss() # ContextCpu by default
print('Working point of thick lattice: (Qx, Qy) = (%s, %s)'%(tw.qx, tw.qy))
print('Chromaticity of thick lattice (not normalized - as in MAD-X): (dQx, dQy) = (%s, %s)'%(tw.dqx, tw.dqy))
tw.to_pandas().to_pickle('sps/sps_twiss_thick.pkl')
print('Twiss computed and saved to sps/sps_twiss_thick.pkl.')
line.to_json('sps/sps_line_thick.json')
print('Line saved to sps/sps_line_thick.json')