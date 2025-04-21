#%%
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#%%
png_dir = './'
source_dir = '../output/'
source_dir = '/home/tprebiba/afs/temp/'
files = glob.glob(source_dir+'*.json')

#%%
df = {}
for file in files[0:15]:
    #print(file)
    #turn = int(file.split('/')[-1].split('_')[-1][0:5])
    df[file] = pd.read_json(file)

#%%
for file in files[-2:-1]:
    print(file)

    try:
         turn = int(file.split('_')[-1].split('.')[0])
    except:
         turn = '00'
    df[file] = df[file][df[file]['state']>0] # keep only active particles
    x = df[file]['x']
    y = df[file]['y']
    xp = df[file]['px']
    yp = df[file]['py']
    z = df[file]['zeta']
    dE = df[file]['ptau']*df[file]['p0c']/1e6
    print('number of particles in turn ', turn, 'is ', len(x))

    bins=100 #500
    my_cmap = plt.cm.jet
    my_cmap.set_under('w',0.1)
    #f, axs = plt.subplots(2,2,figsize=(10,8),facecolor='white')
    #fontsize=15
    f, axs = plt.subplots(2,2,figsize=(7,5),facecolor='white')
    fontsize=10
    f.suptitle('Turn %s'%turn, fontsize=fontsize)
    vmin = 0.1 # the smaller it is, the less sensitive is the colormap
    ax = axs[0,0]
    ax.hist2d(x*1000., xp*1000.,bins=bins, cmap=my_cmap, vmin=vmin)
    #ax.plot(x*1000., xp*1000.,ms=0.5,color='blue')
    ax.set_xlabel('x [mm]')
    ax.set_ylabel('xp [mrad]')
    ax.set_xlim(-22,22)
    ax.set_ylim(-7,7)
    ax = axs[0,1]
    ax.hist2d(y*1000., yp*1000.,bins=bins, cmap=my_cmap, vmin=vmin)
    #ax.plot(y*1000., yp*1000.,ms=0.5,color='blue')
    ax.set_xlabel('y [mm]')
    ax.set_ylabel('yp [mrad]')
    ax.set_xlim(-22,22)
    ax.set_ylim(-7,7)
    ax = axs[1,0]
    ax.hist2d(x*1000., y*1000.,bins=bins, cmap=my_cmap, vmin=vmin)
    #ax.plot(x*1000., y*1000.,ms=0.5,color='blue')
    ax.set_xlabel('x [mm]')
    ax.set_ylabel('y [mm] ')
    ax.set_xlim(-22,22)
    ax.set_ylim(-22,22)
    ax = axs[1,1]
    ax.hist2d(z, dE,bins=bins, cmap=my_cmap, vmin=vmin)
    #ax.plot(z, dE, '.', c='blue')
    ax.set_xlabel('z [m]')
    ax.set_ylabel('dE [MeV] ')
    #ax.set_ylim(-2,2)
    #ax.set_xlim(-50,50)
    for ax in axs.flatten():
            ax.xaxis.label.set_size(fontsize)
            ax.yaxis.label.set_size(fontsize)
            ax.tick_params(labelsize=fontsize)
    #plt.suptitle('turn %s'%turn, fontsize=fontsize)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()
    #plt.savefig('%s/phasespace_%s.png'%(png_dir, turn), dpi=100)
    #plt.close(f)
# %%
