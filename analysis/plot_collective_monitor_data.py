#%%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
import h5py
sys.path.append('../')
from simulation_parameters import parameters as p
import glob

#%%
# Load bunch-by-bunch data using h5py
source_dir = '../output/'
files = glob.glob(source_dir+'collective_monitor*.h5')
file = files[0]
file = files[1]
bunch_data = {}
with h5py.File(file, 'r') as f:
    for bunch in f.keys():
        data = {key: f[bunch][key][()] for key in f[bunch].keys()}
        bunch_data[int(bunch)] = pd.DataFrame(data)

# %%
# Plot turn-by-turn position in x-y-z
f,axs = plt.subplots(3,1,figsize=(10,8),facecolor='white')
fontsize=15
ax = axs[0]
ax.set_xlabel('Turn', fontsize=fontsize)
ax.set_ylabel(r'Bunch $\overline{x}$ [mm]', fontsize=fontsize)
ax.tick_params(axis='both', which='major', labelsize=fontsize)
ax = axs[1]
ax.set_xlabel('Turn', fontsize=fontsize)
ax.set_ylabel(r'Bunch $\overline{x}$ [mm]', fontsize=fontsize)
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
# Plot emittance and intensity over turn
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
# %%
