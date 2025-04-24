#%%
import xtrack as xt
import xfields as xf
from simulation_parameters import parameters as p

print('*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~**~*~*~**~*~*~**~*~*~*')
print('006_wakes.py')
print('*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~**~*~*~**~*~*~**~*~*~*')

#if p['install_wakes']:
if False: # For now; will do it from runSPS.py, WakeFromTable does not yet have .to_dict() method
    print('Installing wakes')

    #########################################
    # Load SPS line
    #########################################
    print('Loading SPS line from sps/sps_line_thick.json.')
    line = xt.Line.from_json('sps/sps_line_thick.json')
    line.build_tracker()
    Csps = line.get_length()

    #########################################
    # Load waketable and inspect
    #########################################
    import xwakes as xw
    waketable = xw.read_headtail_file(p['wakes_file_name'],p['wake_file_columns'])
    for col in p['use_components']:
        waketable[col] = waketable[col] * p['wake_scaling_factor']

    #########################################
    # Install wakes
    #########################################
    wf = xw.WakeFromTable(waketable, columns=p['use_components'])
    wf.configure_for_tracking(zeta_range=(-p['bucket_length']/2, p['bucket_length']/2),
                            num_slices=p['num_slices_wakes'],
                            bunch_spacing_zeta=p['bunch_spacing_m'],
                            filling_scheme=p['filling_scheme'],
                            num_turns=p['num_turns_wakes'],
                            circumference=Csps
                            )
    line.discard_tracker()
    line.insert_element(index=-1, element=wf, name='wakefield')
    line.build_tracker()
    print('Wakes installed at the end of the line.')

    #########################################
    # Saving line
    #########################################
    line.to_json('sps/sps_line_thick.json')
    print('Line saved to sps/sps_line_thick.json')