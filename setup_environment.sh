conda create -n xsuite-env python=3.10
conda activate cupy-env
conda install -c conda-forge cupy
pip install xsuite
pip install xwakes
pip install matplotlib
pip install h5py
pip install git+https://gitlab.cern.ch/tprebiba/beam-analysis-sandbox.git#subdirectory=beamtools
pip install nafflib
pip install pynaff
conda install conda-pack
conda-pack -p /afs/cern.ch/work/t/tprebiba/python_environments/miniconda3/envs/xsuite-env -o /eos/user/t/tprebiba/xsuite_outputs/xsuite-env.tar.gz