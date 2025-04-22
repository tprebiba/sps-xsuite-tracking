#%%
import numpy as np
import pylab as plt
from scipy.interpolate import griddata
from PyNAFF import naff
from resonance_lines import resonance_lines
import matplotlib.gridspec as gridspec
import json

# Simple linear fit with errors
def linfit_with_errors(X, Y, X_threshold=None, x_fit_nr=100):
    X = np.array(X)
    Y = np.array(Y)
    if X_threshold != None:
        i = np.where(np.array(X)>X_threshold)
        X = X[i]
        Y = Y[i]

    p,e = np.polyfit(X, Y, 1, cov=True)
    pe=np.sqrt(np.diag(e))
    x_fit = np.linspace(np.min(X), np.max(X), x_fit_nr)
    y_fit = [p[0]*xx+p[1] for xx in x_fit]

    return p, pe, x_fit, y_fit

#%%
# Load particle tunes (calculated as 1-turn phase advance)
qx_pic = np.load('qx_pic.npy')
qy_pic = np.load('qy_pic.npy')
jx_pic = np.load('jx_pic.npy')
jy_pic = np.load('jy_pic.npy')
qxnew = np.copy(qx_pic)
qynew = np.copy(qy_pic)
jxnew = np.copy(jx_pic)*1e6
jynew = np.copy(jy_pic)*1e6
qxnew[np.where(qx_pic<0)] += 1
qynew[np.where(qy_pic<0)] += 1
qxnew = qxnew+26
qynew = qynew+26

#%%
# Plot tune spread
my_cmap = plt.cm.jet
my_cmap.set_under('w',1)
fontsize=18
bins = 100
vmin = 20
#vmin = 1
# qxlims = [26.616,26.624]
# qylims = [26.576,26.584]
# qxlims = [26.60,26.64]
# qylims = [26.56,26.60]
qxlims = [26.53,26.69]
qylims = [26.49,26.65]
qx0 = 26.62
qy0 = 26.58

r=resonance_lines(qxlims, qylims, [1,2,3,4], 6)
fig = plt.figure(figsize=(10,8), facecolor='w')
gs = gridspec.GridSpec(6, 6)
ax = plt.subplot(gs[1:6, 0:4])
ax.set_xlim(qxlims[0], qxlims[1])
ax.set_ylim(qylims[0], qylims[1])
ax.set_xticks(np.linspace(qxlims[0]+0.001, qxlims[1]-0.001, 5))
ax.set_yticks(np.linspace(qylims[0]+0.001, qylims[1]-0.001, 5))
ax.xaxis.set_major_formatter(plt.FormatStrFormatter('%.3f'))
ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%.3f'))
ax_xDist = plt.subplot(gs[0, 0:4],sharex=ax)
ax_yDist = plt.subplot(gs[1:6, 4],sharey=ax)

H, xedges, yedges = np.histogram2d(qxnew, qynew, bins=bins, range=[qxlims, qylims])
H_masked = np.where(H >= vmin, H, 0)
xproj = H_masked.sum(axis=1)  # sum along y: gives x distribution
yproj = H_masked.sum(axis=0)  # sum along x: gives y distribution
pcm = ax.pcolormesh(xedges, yedges, H_masked.T, cmap=my_cmap, vmin=vmin)
#ax.plot(qx0, qy0, '*', ms=20, color='k', zorder=1e5)

# Plot resonance lines on top of colormesh
r.plot_resonance(ax=ax)
ax.set_xlabel('$\mathrm{Q_x}$', fontsize=fontsize)
ax.set_ylabel('$\mathrm{Q_y}$', fontsize=fontsize)
ax.tick_params(axis='both', labelsize=fontsize)

ax_xDist.bar((xedges[:-1] + xedges[1:]) / 2, xproj, width=(xedges[1]-xedges[0]), color='black')
ax_xDist.tick_params(axis='x', labelleft=False, labelright=False, labeltop=False, labelbottom=False)
ax_xDist.tick_params(axis='y', labelleft=False, labelright=False, labeltop=False, labelbottom=False)
nsigmas = 0.5
ax_xDist.axvline(np.mean(qxnew)-nsigmas*np.std(qxnew), color='red', ls='-')
ax_xDist.axvline(np.mean(qxnew)+nsigmas*np.std(qxnew), color='red', ls='-')
print('Total tune spread in x: ', nsigmas*np.std(qxnew)*2)

ax_yDist.barh((yedges[:-1] + yedges[1:]) / 2, yproj, height=(yedges[1]-yedges[0]), color='black')
ax_yDist.tick_params(axis='x', labelleft=False, labelright=False, labeltop=False, labelbottom=False)
ax_yDist.tick_params(axis='y', labelleft=False, labelright=False, labeltop=False, labelbottom=False)
nsigmas = 1
ax_yDist.axhline(np.mean(qynew)-nsigmas*np.std(qynew), color='red', ls='-')
ax_yDist.axhline(np.mean(qynew)+nsigmas*np.std(qynew), color='red', ls='-')
print('Total tune spread in y: ', nsigmas*np.std(qynew)*2)

fig.tight_layout()
#fig.savefig('tunespread_natChroma_onMomentum_noOctupoles_epsx_12p0_epsy_4p0.png', dpi=300)
#fig.savefig('tunespread_setChroma_onMomentum_noOctupoles_epsx_12p0_epsy_4p0.png', dpi=300)
#fig.savefig('tunespread_natChroma_onMomentum_setOctupoles_epsx_12p0_epsy_4p0.png', dpi=300)
#fig.savefig('tunespread_natChroma_fullBunch_noOctupoles_epsx_12p0_epsy_4p0.png', dpi=300)
#fig.savefig('tunespread_setChroma_fullBunch_setOctupoles_epsx_12p0_epsy_4p0.png', dpi=300)

# %%
# Plot tune versus amplitude (action)
f,axs = plt.subplots(2, 1, figsize=(12, 6), facecolor='w')
fontsize=20

ax = axs[0]
ax.set_ylabel(r'$Q_x$', fontsize=fontsize)
ax.set_xlabel(r'$J_x$ [mm mrad]', fontsize=fontsize)
ax.tick_params(labelsize=fontsize)
ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%.3f'))
ax.plot(jxnew, qxnew, '.', markersize=1, c='black')
p, pe, x_fit, y_fit = linfit_with_errors(jxnew, qxnew)
ax.plot(x_fit, y_fit, 'r-', lw=2, label='slope = %.4f' % p[0])
ax.set_ylim(qxlims[0], qxlims[1]) 
ax.grid(True)
ax.legend(fontsize=fontsize, loc=0)

ax = axs[1]
ax.set_ylabel(r'$Q_y$', fontsize=fontsize)
ax.set_xlabel(r'$J_y$ [mm mrad]', fontsize=fontsize)
ax.tick_params(labelsize=fontsize)
ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%.3f'))
ax.plot(jynew, qynew, 'o', markersize=1, c='black')
p, pe, x_fit, y_fit = linfit_with_errors(jynew, qynew)
ax.plot(x_fit, y_fit, 'r-', lw=2, label='slope = %.4f' % p[0])
ax.set_ylim(qylims[0], qylims[1])
ax.grid(True)
ax.legend(fontsize=fontsize, loc=0)

f.tight_layout()
#fig.savefig('amplitude_detuning_natChroma_onMomentum_noOctupoles_epsx_12p0_epsy_4p0.png', dpi=300)
#fig.savefig('amplitude_detuning_setChroma_onMomentum_noOctupoles_epsx_12p0_epsy_4p0.png', dpi=300)
#fig.savefig('amplitude_detuning_natChroma_onMomentum_setOctupoles_epsx_12p0_epsy_4p0.png', dpi=300)
#fig.savefig('amplitude_detuning_natChroma_fullBunch_noOctupoles_epsx_12p0_epsy_4p0.png', dpi=300)
#fig.savefig('amplitude_detuning_setChroma_fullBunch_setOctupoles_epsx_12p0_epsy_4p0.png', dpi=300)
# %%
