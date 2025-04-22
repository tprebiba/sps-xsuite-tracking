#%%
import numpy as np
import pylab as plt
import nafflib
import json

# %%
# Load turn-by-turn data, format [i,j]: i-th particle, j-th turn
x=np.load('x.npy')
y=np.load('y.npy')
px = np.load('px.npy')
py = np.load('py.npy')
state = np.load('state.npy')
nr_particles = len(x)
with open('../../sps/optics_at_start.json', 'r') as f:
    optics = json.load(f)

# %%
# Calculate tunes and action
Jx = 0.5*(optics['gamx']*x**2 + 2*optics['alfx']*x*px + optics['betx']*px**2)*1e6 # in mm mrad
Jy = 0.5*(optics['gamy']*y**2 + 2*optics['alfy']*y*py + optics['bety']*py**2)*1e6 # in mm mrad
Jx = Jx.mean(axis=1)
Jy = Jy.mean(axis=1)
qx = np.zeros(nr_particles)
qy = np.zeros(nr_particles)
tol = 1e-3
for i in range(nr_particles):
    if all(x == 1 for x in state[i]): # particle was not lost
        _qx = nafflib.tune(x[i], -px[i], window_order=2, window_type='hann')
        _qy = nafflib.tune(y[i], -py[i], window_order=2, window_type='hann')
        if abs(_qx)>tol:
            qx[i] = _qx
        else:
            qx[i] = np.nan
        if abs(_qy)>tol:
            qy[i] = _qy
        else:
            qy[i] = np.nan
    else: # particle was lost
        qx[i] = np.nan
        qy[i] = np.nan

#%%
# Plot amplitude detuning
f,axs = plt.subplots(2, 1, figsize=(12, 6), facecolor='w')
fontsize=20

ax = axs[0]
ax.set_ylabel(r'$Q_x$', fontsize=fontsize)
ax.set_xlabel(r'$J_x$ [mm mrad]', fontsize=fontsize)
ax.tick_params(labelsize=fontsize)
ax.plot(Jx, 1-qx, 'o', markersize=1, c='black')
#ax.set_ylim(0.6, 0.64)
ax.set_ylim(0.6, 0.65)

ax = axs[1]
ax.set_ylabel(r'$Q_y$', fontsize=fontsize)
ax.set_xlabel(r'$J_y$ [mm mrad]', fontsize=fontsize)
ax.tick_params(labelsize=fontsize)
ax.plot(Jy, 1-qy, 'o', markersize=1, c='black')
#ax.set_ylim(0.56, 0.60)
ax.set_ylim(0.54, 0.60)

f.tight_layout()
#f.savefig('ampl_det_natChroma_onMomentum_noOctupoles.png', dpi=300)
#f.savefig('ampl_det_setChroma_onMomentum_noOctupoles.png', dpi=300)
#f.savefig('ampl_det_setChroma_onMomentum_setOctupoles.png', dpi=300)
# %%
