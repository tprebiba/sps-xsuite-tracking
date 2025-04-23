#%%
import xtrack as xt
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec

#%%
# Load line
print('Loading SPS line from ../../sps/sps_line_thick.json.')
line = xt.Line.from_json('../../sps/sps_line_thick.json')

#%% Twiss and get aperture
tw1 = line.twiss4d()
aper = line.get_aperture_table(dx=1e-3, dy=1e-3,
                               x_range=(-0.1, 0.1), y_range=(-0.1, 0.1))

#%% Check minimum apertures
mask_min_x_high = np.where(aper['x_aper_high_discrete']==np.nanmin(aper['x_aper_high_discrete']))
mask_min_x_low = np.where(abs(aper['x_aper_low_discrete'])==np.nanmin(np.abs(aper['x_aper_low_discrete'])))
mask_min_y_high = np.where(aper['y_aper_high_discrete']==np.nanmin(aper['y_aper_high_discrete']))
mask_min_y_low = np.where(abs(aper['y_aper_low_discrete'])==np.nanmin(np.abs(aper['y_aper_low_discrete'])))
elements_at_min_x_high = aper['name'][mask_min_x_high]
elements_at_min_x_low = aper['name'][mask_min_x_low]
elements_at_min_y_high = aper['name'][mask_min_y_high]
elements_at_min_y_low = aper['name'][mask_min_y_low]
print('Elements with minimum aperture:')
print('Positive x: %s at locations %s m with apertures %s mm'%(aper['name'][mask_min_x_high], aper['s'][mask_min_x_high], aper['x_aper_high_discrete'][mask_min_x_high]*1e3))
print('Negative x: %s at locations %s m with apertures %s mm'%(aper['name'][mask_min_x_low], aper['s'][mask_min_x_low], aper['x_aper_low_discrete'][mask_min_x_low]*1e3))
print('Positive y: %s at locations %s m with apertures %s mm'%(aper['name'][mask_min_y_high], aper['s'][mask_min_y_high], aper['y_aper_high_discrete'][mask_min_y_high]*1e3))
print('Negative y: %s at locations %s m with apertures %s mm'%(aper['name'][mask_min_y_low], aper['s'][mask_min_y_low], aper['y_aper_low_discrete'][mask_min_y_low]*1e3))

#%% Plotting
f = plt.figure(figsize=(15, 5), facecolor='w')
gs = gridspec.GridSpec(2, 1, height_ratios=[1, 4])
fontsize = 16

ax_lattice = f.add_subplot(gs[0])
tw1.plot(ax=ax_lattice, lattice_only=True, grid=False)
ax_lattice.legend().remove()
ax_lattice.tick_params(axis='both',labelsize=0)
ax_lattice.set_xlabel('')

ax = f.add_subplot(gs[1], sharex=ax_lattice)
ax.plot(aper.s, aper.x_aper_low*1e3, 'k-', lw=1)
ax.plot(aper.s, aper.x_aper_high*1e3, 'k-', lw=1)
# ax.plot(aper.s, aper.x_aper_low_discrete*1e3, '.k')
ax.plot(aper.s, aper.y_aper_low*1e3, 'r-', lw=1)
ax.plot(aper.s, aper.y_aper_high*1e3, 'r-', lw=1)

ax.tick_params(labelsize=fontsize, labelbottom=True)
ax.set_xlabel('s [m]', fontsize=fontsize)
ax.set_ylabel('Aperture [mm]', fontsize=fontsize)
ax.set_ylim(-60, 60)

f.tight_layout()
#f.savefig('aper.png', dpi=300)

# %%
# Plot particle
f, ax = plt.subplots(1, 1, figsize=(15, 5), facecolor='w')
fontsize = 16

#ax.plot(aper.s, aper.x_aper_low*1e3, 'k-', lw=1)
#ax.plot(aper.s, aper.x_aper_high*1e3, 'k-', lw=1)
# ax.plot(aper.s, aper.x_aper_low_discrete*1e3, '.k')
#ax.plot(aper.s, aper.y_aper_low*1e3, 'r-', lw=1)
ax.plot(aper.s, aper.y_aper_high*1e3, 'r-', lw=1)

epsy = 2e-6
ax.plot(tw1.s, np.sqrt(tw1.bety*epsy)*1e3, color='blue', label='Particle at $\epsilon_y$ = 3e-6 m')
epsy = 4e-6
ax.plot(tw1.s, np.sqrt(tw1.bety*epsy)*1e3, color='orange', label='Particle at $\epsilon_y$ = 4e-6 m')
epsy = 6e-6
ax.plot(tw1.s, np.sqrt(tw1.bety*epsy)*1e3, color='green', label='Particle at $\epsilon_y$ = 5e-6 m')

ax.tick_params(labelsize=fontsize, labelbottom=True)
ax.set_xlabel('s [m]', fontsize=fontsize)
ax.set_ylabel('Vertical aperture [mm]', fontsize=fontsize)
ax.set_ylim(10, 25)
ax.set_xlim(0, 1000)
ax.legend(loc=0, fontsize=fontsize)

f.tight_layout()
#f.savefig('aper_particle.png', dpi=300)

# %%
