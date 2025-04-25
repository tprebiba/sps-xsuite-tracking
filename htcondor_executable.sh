#!/bin/bash
echo "uname -r:" `uname -r`

#source /usr/local/xsuite/miniforge3/bin/activate xsuite
pwd


current_directory=/afs/cern.ch/user/t/tprebiba/workspace/psb-xsuite-tracking/sftpro/fb_qx62_qy58_100b_2100kMP_2p4e13_wakesx10
cp -r $current_directory/sps .
cp -r $current_directory/input .
cp -r $current_directory/output .
cp -r $current_directory/lib .
cp -r $current_directory/wakes .
cp $current_directory/*.py .
cp $current_directory/*.sh .

export PYTHONNOUSERSITE=1
unset PYTHONPATH
unset CONDA_PYTHON_EXE
unset LD_LIBRARY_PATH
unset SHLIB_PATH
unset CMAKE_INCLUDE_PATH
unset SRM_PATH
unset MODULES_RUN_QUARANTINE
unset MANPATH
export PATH=/usr/bin:/bin
mkdir my_env
tar -xvzf xsuite-env.tar.gz -C my_env
source my_env/bin/activate
echo "Using Python: $(which python)"
echo $PYTHONPATH
unset PYTHONPATH
echo $PYTHONPATH
echo "Files: $(ls)"
for f in *.zip; do
  echo "Unzipping $f"
  unzip "$f"
done

echo "which python:" `which python`

date
#python runSPS.py
my_env/bin/python runSPS.py
date
