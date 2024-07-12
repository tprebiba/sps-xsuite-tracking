#!/bin/bash
echo "uname -r:" `uname -r`

#source /usr/local/xsuite/miniforge3/bin/activate xsuite
pwd


current_directory=/home/tprebiba/eos/Fellowship/03_Xsuite/sps-xsuite-tracking
cp -r $current_directory/sps .
cp -r $current_directory/input .
cp -r $current_directory/output .
cp -r $current_directory/lib .
cp -r $current_directory/time_tables .
cp $current_directory/*.py .
cp $current_directory/*.sh .

echo "which python:" `which python`

date
python runSPS.py
date
