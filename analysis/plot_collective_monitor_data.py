#%%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
import h5py
sys.path.append('../')
from simulation_parameters import parameters as p
import glob
import matplotlib.cm as cm
import matplotlib.colors as mcolors

#%%
#################################################
# Load bunch-by-bunch data using h5py
source_dir = '../output/'
files = glob.glob(source_dir+'collective_monitor*bunches.h5')
file = files[0]
bunch_data = {}
with h5py.File(file, 'r') as f:
    for bunch in f.keys():
        data = {key: f[bunch][key][()] for key in f[bunch].keys()}
        bunch_data[int(bunch)] = data #pd.DataFrame(data)

# %%
# Plot turn-by-turn position in x-y-z for all slices and bunches
f,axs = plt.subplots(3,1,figsize=(10,8),facecolor='white')
fontsize=15
ax = axs[0]
ax.set_xlabel('Turn', fontsize=fontsize)
ax.set_ylabel(r'Bunch $\overline{x}$ [mm]', fontsize=fontsize)
ax.tick_params(axis='both', which='major', labelsize=fontsize)
ax = axs[1]
ax.set_xlabel('Turn', fontsize=fontsize)
ax.set_ylabel(r'Bunch $\overline{y}$ [mm]', fontsize=fontsize)
ax.tick_params(axis='both', which='major', labelsize=fontsize)
ax = axs[2]
ax.set_xlabel('Turn', fontsize=fontsize)
ax.set_ylabel(r'Bunch $\overline{z}-<\overline{z}>$ [m]', fontsize=fontsize)
ax.tick_params(axis='both', which='major', labelsize=fontsize)
for bunch in bunch_data.keys():
    axs[0].plot(bunch_data[bunch]['mean_x']*1e3, '-', lw=1)
    axs[1].plot(bunch_data[bunch]['mean_y']*1e3, '-', lw=1)
    axs[2].plot((bunch_data[bunch]['mean_zeta']-np.mean(bunch_data[bunch]['mean_zeta'])), '-', lw=1)
f.tight_layout()

# %%
# Plot emittance and intensity over turn for all slices and bunches
f, axs = plt.subplots(3,1,figsize=(10,8))
fontsize=15
ax = axs[0]
ax.tick_params(axis='both', which='major', labelsize=fontsize)
ax.set_ylabel('Intensity per bunch', fontsize=fontsize)
ax.set_xlabel('Turn', fontsize=fontsize)
ax = axs[1]
ax.tick_params(axis='both', which='major', labelsize=fontsize)
ax.set_ylabel(r'$\epsilon_x$ [mm mrad]', fontsize=fontsize)
ax.set_xlabel('Turn', fontsize=fontsize)
ax = axs[2]
ax.tick_params(axis='both', which='major', labelsize=fontsize)
ax.set_ylabel(r'$\epsilon_y$ [mm mrad]', fontsize=fontsize)
ax.set_xlabel('Turn', fontsize=fontsize)
for bunch in bunch_data.keys():
    axs[0].plot(bunch_data[bunch]['num_particles'], '-', lw=1)
    axs[1].plot(bunch_data[bunch]['epsn_x']*1e6, '-', lw=1)
    axs[2].plot(bunch_data[bunch]['epsn_y']*1e6, '-', lw=1)

plt.tight_layout()
plt.show()


#%%
#################################################
# Load slice-by-slice data using h5py
source_dir = '../output/'
files = glob.glob(source_dir+'collective_monitor*slices.h5')
file = files[0]
bunch_data = {}
with h5py.File(file, 'r') as f:
    for bunch in f.keys():
        data = {key: f[bunch][key][()] for key in f[bunch].keys()}
        bunch_data[int(bunch)] = data #pd.DataFrame(data)


# %%
# Plot turn-by-turn intrabunch motion for one bunch (dipolar)
f, axs = plt.subplots(3, 1, figsize=(10, 8), facecolor='white')
fontsize = 15
labels = [r'X pickup [a.u.]', r'Y pickup [a.u.]', r'Z pickup [a.u.]']
for ax, label in zip(axs, labels):
    ax.set_xlabel('Slice', fontsize=fontsize)
    ax.set_ylabel(label, fontsize=fontsize)
    ax.tick_params(axis='both', which='major', labelsize=fontsize)

bunch = 0
num_turns = len(bunch_data[bunch]['mean_x'])
turns = np.arange(num_turns)
cmap = cm.viridis
norm = mcolors.Normalize(vmin=turns.min(), vmax=turns.max())
colors = cmap(norm(turns))
for turn, color in zip(turns, colors):
    w = bunch_data[bunch]['num_particles'][turn] / 1e6
    axs[0].plot(bunch_data[bunch]['mean_x'][turn]*w, '-', lw=1, color=color)
    axs[1].plot(bunch_data[bunch]['mean_y'][turn]*w, '-', lw=1, color=color)
    axs[2].plot(bunch_data[bunch]['mean_zeta'][turn]*w, '-', lw=1, color=color)

sm = cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = f.colorbar(sm, ax=axs, orientation='vertical')
cbar.set_label('Turn', fontsize=fontsize)
cbar.ax.tick_params(labelsize=fontsize)
#f.tight_layout()

# %%
# Plot turn-by-turn intrabunch motion for one bunch (quadrupolar)
f, axs = plt.subplots(3, 1, figsize=(10, 8), facecolor='white')
fontsize = 15
labels = [r'$\sigma_x$ pickup [a.u.]', r'$\sigma_y$ pickup [a.u.]', r'$\sigma_{zeta}$ pickup']
for ax, label in zip(axs, labels):
    ax.set_xlabel('Slice', fontsize=fontsize)
    ax.set_ylabel(label, fontsize=fontsize)
    ax.tick_params(axis='both', which='major', labelsize=fontsize)

bunch = 0
num_turns = len(bunch_data[bunch]['mean_x'])
turns = np.arange(num_turns)
cmap = cm.viridis
norm = mcolors.Normalize(vmin=turns.min(), vmax=turns.max())
colors = cmap(norm(turns))
for turn, color in zip(turns, colors):
    w =  bunch_data[bunch]['num_particles'][turn] / 1e6
    axs[0].plot(bunch_data[bunch]['sigma_x'][turn]*w, '-', lw=1, color=color)
    axs[1].plot(bunch_data[bunch]['sigma_y'][turn]*w, '-', lw=1, color=color)
    axs[2].plot(bunch_data[bunch]['sigma_zeta'][turn]*w, '-', lw=1, color=color)

sm = cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = f.colorbar(sm, ax=axs, orientation='vertical')
cbar.set_label('Turn', fontsize=fontsize)
cbar.ax.tick_params(labelsize=fontsize)
#f.tight_layout()

# %%
