#!/bin/bash

# This script prepares the simulation directory for the simulation

# Pull sps lattice from acc-models-sps repository on gitlab.cern.ch
pull_acc_models_sps_files=false
if [ "$pull_acc_models_sps_files" = true ]; then
    echo "Pulling sps lattice from acc-models-sps repository on gitlab.cern.ch"
    cd sps
    echo "Current directory: $(pwd)"
    source pull_acc-models-sps_files.sh
    echo "Pulled."
    cd ..
    echo "Current directory: $(pwd)"
fi

# Translates the lattice from MAD-X to Xsuite
convert_line=false
if [ "$convert_line" = true ]; then
    python 001_get_SPS_line.py
fi

# Match tune and chroma
python 002_match_tune_chroma.py

# Set octupoles
python 003_set_octupoles.py

# Set RF
python 004_set_RF.py

# Lattice imperfections
python 005_lattice_imperfections.py

# Wakes
python 006_wakes.py

# Generate particle distribution
python 007_generate_particle_distribution.py

# Configure paths on htcondor_executable for submission to htcondor
echo "Configuring paths on htcondor_executable for submission to htcondor"
current_directory=$(pwd)
htcondor_executable_file="htcondor_executable.sh"
if [ -e "$htcondor_executable_file" ]; then
    sed -i "8s|.*|current_directory=$current_directory|" "$htcondor_executable_file"
    echo "Current directory $current_directory written to $htcondor_executable_file."
else
    echo "Error: $htcondor_executable_file does not exist."
fi