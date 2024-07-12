#%%
from cpymad.madx import Madx
import xtrack as xt
import xpart as xp
from simulation_parameters import parameters as p

print('*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~**~*~*~**~*~*~**~*~*~*')
print('001_get_SPS_line.py')
print('*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~**~*~*~**~*~*~**~*~*~*')

#%%
#########################################
# Load line
#########################################
mad = Madx()
mad.globals.thin = 0 # if > 0 madx makes all elements thin
mad.globals.slices = 0
mad.globals.QH = p['qx_ini']
mad.globals.QV = p['qy_ini']
mad.chdir('sps')
mad.call('sps_lhc_q26.madx') # note that a single cavity is installed close to the main one (br.c02)
line= xt.Line.from_madx_sequence(mad.sequence['sps'],
                                 deferred_expressions=True,
                                 install_apertures=True,
                                 #enable_field_errors=True, # field errors are not yet supported for thick elements
                                 enable_align_errors=True,
                                 allow_thick=True,
                                 )
print('SPS line loaded.')
print('Line length: ', line.get_length())

# %%
#########################################
# Add reference particle
#########################################
line.particle_ref=xp.Particles(mass0=xp.PROTON_MASS_EV,gamma0=mad.sequence.sps.beam.gamma)
print('Reference particle added at gamma0=%s.'%(mad.sequence.sps.beam.gamma))

#%%
#########################################
# Configure bends if thick
#########################################
if mad.globals.thin == 0:
    line.configure_bend_model(core='full', edge='full') # switch to exact model for bends (PTC-like, appropriate for small rings) 
    #line.configure_bend_model(core='expanded', edge='full')
    print('Bend model configured for thick elements.')


#########################################
# Inspect elements, twiss and save
#########################################
line_table = line.get_table()
#line_table.rows[:12]
line.element_names
#line.element_dict
line.twiss_default['method'] = '4d' # no cavity
tw = line.twiss() # ContextCpu by default
tw.to_pandas().to_pickle('sps/sps_twiss_thick.pkl')
print('Twiss computed and saved to sps/sps_twiss_thick.pkl.')
print('Working point of thick lattice: (Qx, Qy) = (%s, %s)'%(tw.qx, tw.qy))
line.to_json('sps/sps_line_thick.json')
print('Line saved to sps/sps_line_thick.json')