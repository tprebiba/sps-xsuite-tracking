#%%
import xwakes as xw
import matplotlib.pyplot as plt

#%%
# Import wakes
wakes_file_name = '../../wakes/SPS_Q26.wake'
wake_file_columns = ['time', 'dipole_x', 'dipole_y', 'quadrupole_x', 'quadrupole_y']
waketable = xw.read_headtail_file(wakes_file_name,wake_file_columns)

#%%
# Plot wakes in linear scale
f,axs = plt.subplots(2, 1, figsize=(8, 5))
fontsize=10
ax = axs[0]
ax.set_xlabel('Time [ns]', fontsize=fontsize)
ax.set_ylabel('Dipolar wake [V/pC/mm]', fontsize=fontsize)
ax.tick_params(axis='both', which='major', labelsize=fontsize)
ax.plot(waketable['time']*1e9, waketable['dipole_x']*1e-15, label='H')
ax.plot(waketable['time']*1e9, waketable['dipole_y']*1e-15, label='V')
ax.set_xlim(-0.1, 20)
ax.legend(fontsize=fontsize)
for i in range(10):
    ax.axvline(i*5, color='k', linestyle='--', alpha=0.5)

ax = axs[1]
ax.set_xlabel('Time [ns]', fontsize=fontsize)
ax.set_ylabel('Quadrupolar wake [V/pC/mm]', fontsize=fontsize)
ax.tick_params(axis='both', which='major', labelsize=fontsize)
ax.plot(waketable['time']*1e9, waketable['quadrupole_x']*1e-15, label='H')
ax.plot(waketable['time']*1e9, waketable['quadrupole_y']*1e-15, label='V')
ax.set_xlim(-0.1, 20)
ax.legend(fontsize=fontsize)
for i in range(10):
    ax.axvline(i*5, color='k', linestyle='--', alpha=0.5)

f.tight_layout()

#%%
# Plot wakes in log scale
f,axs = plt.subplots(2, 1, figsize=(8, 5))
fontsize=10
ax = axs[0]
ax.set_xlabel('Time [ns]', fontsize=fontsize)
ax.set_ylabel('Dipolar wake [V/pC/mm]', fontsize=fontsize)
ax.tick_params(axis='both', which='major', labelsize=fontsize)
ax.plot(waketable['time']*1e9, abs(waketable['dipole_x']*1e-15), label='H')
ax.plot(waketable['time']*1e9, abs(waketable['dipole_y']*1e-15), label='V')
ax.set_xlim(-0.1, 2000)
ax.legend(fontsize=fontsize)
#for i in range(10):
#    ax.axvline(i*5, color='k', linestyle='--', alpha=0.5)
ax.set_yscale('log')

ax = axs[1]
ax.set_xlabel('Time [ns]', fontsize=fontsize)
ax.set_ylabel('Quadrupolar wake [V/pC/mm]', fontsize=fontsize)
ax.tick_params(axis='both', which='major', labelsize=fontsize)
ax.plot(waketable['time']*1e9, abs(waketable['quadrupole_x']*1e-15), label='H')
ax.plot(waketable['time']*1e9, abs(waketable['quadrupole_y']*1e-15), label='V')
ax.set_xlim(-0.1, 2000)
ax.legend(fontsize=fontsize)
#for i in range(10):
#    ax.axvline(i*5, color='k', linestyle='--', alpha=0.5)
ax.set_yscale('log')

f.tight_layout()
# %%
