#%%
import xtrack as xt
from xtrack.slicing import Strategy, Teapot
import json
from simulation_parameters import parameters as p

print('*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~**~*~*~**~*~*~**~*~*~*')
print('005_lattice_imperfections.py')
print('*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~**~*~*~**~*~*~**~*~*~*')

if p['slice']:
    print('Slicing line into %s slices.'%(p['nr_slices']))

    #########################################
    # Load SPS line
    #########################################
    print('Loading SPS line from sps/sps_line_thick.json.')
    line = xt.Line.from_json('sps/sps_line_thick.json')
    line.build_tracker()
    Csps = line.get_length()

    #########################################
    # Twiss thick line
    #########################################
    tw = line.twiss() # ContextCpu by default
    print('Working point of thick lattice: (Qx, Qy) = (%s, %s)'%(tw.qx, tw.qy))
    print('Chromaticity of thick lattice (not normalized - as in MAD-X): (dQx, dQy) = (%s, %s)'%(tw.dqx, tw.dqy))

    #########################################
    # Slice thick line with xsuite 
    #########################################
    slices = p['nr_slices']
    line.slice_thick_elements(
        slicing_strategies=[
            Strategy(slicing=Teapot(slices)), # default is 1
            Strategy(slicing=Teapot(slices), element_type=xt.Bend),
            Strategy(slicing=Teapot(slices), element_type=xt.Quadrupole),
        ]
    )
    print('Line sliced into %s slices with xsuite.'%(slices))

    #########################################
    # Twiss thin line
    #########################################
    tw = line.twiss()
    print('Working point of thin lattice: (Qx, Qy) = (%s, %s)'%(tw.qx, tw.qy))
    print('Chromaticity of thin lattice (not normalized - as in MAD-X): (dQx, dQy) = (%s, %s)'%(tw.dqx, tw.dqy))

    #########################################
    # (Re) Match tunes and chromaticity
    #########################################
    print('Matching tunes and chromaticity...')
    if p['chroma_mode'] == 'natural':
        print('Natural chromaticity (zero-ing sextupoles: klsfa0, klsfb0, klsda0, klsdb0), matching only tunes.')
        line.vars['klsfa0'] = 0
        line.vars['klsfb0'] = 0
        line.vars['klsda0'] = 0
        line.vars['klsdb0'] = 0
        line.vars['qph_setvalue'] = 0 # should zero out klsfa, klsfb
        line.vars['qpv_setvalue'] = 0 # should zero out klsda, klsdb
        opt = line.match(solve=False,
        vary=[
            xt.VaryList(['qh_setvalue', 'qv_setvalue'], step=1e-7), 
        ],
        targets=[
            xt.TargetSet(qx=p['qh_setvalue'], qy=p['qv_setvalue'], tol=1e-5), 
        ])
        opt.assert_within_tol=False
        opt.solve()
        print(opt.log())
    elif p['chroma_mode'] == 'default':
        print('Start matching')
        for parameterkey,twisskey in zip(['qph_setvalue', 'qpv_setvalue'],
                                        ['dqx', 'dqy']):
            print(f'{parameterkey}: keeping default value of {float(tw[twisskey])}.')
            p[parameterkey] = float(tw[twisskey])
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
    elif p['chroma_mode'] == 'manual':
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
    else:
        raise ValueError(f"Unknown mode: {p['chroma_mode']}")
    print('Matching done.')
    print('Sextupole strengths:')
    print('klsfa0: %s'%line.vars['klsfa0']._value)
    print('klsfb0: %s'%line.vars['klsfb0']._value)
    print('klsda0: %s'%line.vars['klsda0']._value)
    print('klsdb0: %s'%line.vars['klsdb0']._value)

    #########################################
    # Re-twissing and saving
    #########################################
    print('Twiss after matching:')
    tw = line.twiss()
    print('Working point of thin lattice: (Qx, Qy) = (%s, %s)'%(tw.qx, tw.qy))
    print('Chromaticity of thin lattice (not normalized - as in MAD-X): (dQx, dQy) = (%s, %s)'%(tw.dqx, tw.dqy))
    optics_at_start = {
        'betx': tw.betx[0],
        'bety': tw.bety[0],
        'gamx': tw.gamx[0],
        'gamy': tw.gamy[0],
        'alfx': tw.alfx[0],
        'alfy': tw.alfy[0],
        'dx': tw.dx[0],
        'dy': tw.dy[0],
        'gamma0': tw.gamma0,
        'beta0': tw.beta0,
        'qx': tw.qx,
        'qy': tw.qy,
        'dqx': tw.dqx,
        'dqy': tw.dqy,
    }
    print('Some optics at the start of the line:')
    print(optics_at_start)
    print('Saving to sps/optics_at_start.json.')
    with open('sps/optics_at_start.json', 'w') as f:
        json.dump(optics_at_start, f, indent=4)
    line.to_json('sps/sps_line_thin.json')
    print('Line saved to sps/sps_line_thin.json')