#%%
import xtrack as xt
import pandas as pd
import xdeps as xd
from simulation_parameters import parameters as p

print('*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~**~*~*~**~*~*~**~*~*~*')
print('002_match_tune_chroma.py')
print('*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~**~*~*~**~*~*~**~*~*~*')

# %%
#########################################
# Load SPS line and inspect mad-x default settings
#########################################
print('Loading SPS line from sps/sps_line_thick_madx-default.json')
line = xt.Line.from_json('sps/sps_line_thick_madx-default.json')
line_table = line.get_table()
#line_table.rows[:12]
line.element_names
#line.element_dict
print('Twiss default settings:')
tw = line.twiss() # ContextCpu by default
print('Working point of thick lattice: (Qx, Qy) = (%s, %s)'%(tw.qx, tw.qy))
print('Chromaticity of thick lattice (not normalized - as in MAD-X): (dQx, dQy) = (%s, %s)'%(tw.dqx, tw.dqy))
print('Chromaticity is close but not exactly equal to the MAD-X value (dQx, dQy) = (0, 2.658)')
print(line.vars['qh_setvalue']._value)
print(line.vars['qh_setvalue']._info(limit=None))

# %%
#########################################
# Match tunes and chromaticity
#########################################
print('Matching tunes and chromaticity...')
for parameterkey,twisskey in zip(['qh_setvalue', 'qv_setvalue', 'qph_setvalue', 'qpv_setvalue'],
                                 ['qx', 'qy', 'dqx', 'dqy']):
    if p[parameterkey] is None:
        print(f'{parameterkey} is None, keeping default value of {float(tw[twisskey])}.')
        p[parameterkey] = float(tw[twisskey])
    else:
        print(f'{parameterkey} is {p[parameterkey]}.')
print('Start matching')
opt = line.match(solve=False,
    vary=[
        xt.VaryList(['qh_setvalue', 'qv_setvalue'], step=1e-7), 
        xt.VaryList(['qph_setvalue', 'qpv_setvalue'], step=1e-7), 
    ],
    targets=[
        xt.TargetSet(qx=p['qh_setvalue'], qy=p['qv_setvalue'], tol=1e-5), 
        xt.TargetSet(dqx=p['qph_setvalue'], dqy=p['qpv_setvalue'], tol=1e-5), 
    ])
opt.assert_within_tol=False
opt.solve()
print(opt.log())

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
print('Betax, Betay, Gammax, Gammay, Dispx, Dispy, gammarel, betarel:',
      tw.betx[0], tw.bety[0], tw.gamx[0], tw.gamy[0],
      tw.dx[0], tw.dy[0], tw.gamma0, tw.beta0)
line.to_json('sps/sps_line_thick.json')
print('Line saved to sps/sps_line_thick.json')
# %%
