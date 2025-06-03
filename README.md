# Realistic Super Proton Synchrotron (SPS) Beam Dynamics Simulation with Xsuite

This repository provides a full simulation pipeline for realistic modeling of beam dynamics in CERN’s Super Proton Synchrotron (SPS) using [Xsuite](https://xsuite.readthedocs.io/en/latest/).  

It includes tools for:
- Lattice generation (tune & chromaticity matching)
- Octupole and RF settings  
- Machine imperfections  
- Wakefields and space charge effects  
- Tracking and output analysis  
- Scripts for submittion to [HTCondor](https://abpcomputing.web.cern.ch/computing_resources/cernbatch/) (CPU or GPU)

**Contact for corrections & suggestions**: [tirsi.prebibaj@cern.ch](mailto:tirsi.prebibaj@cern.ch)  
With inputs from: D. Amorim, F. Asvesta, H. Bartosik, Elena De La Fuente Garcia, I. Mases Sole.

---

## Structure

The simulation is organized in two main parts:

### Part I: Preparing the Simulation

- Generate the desired lattice and particle distribution (lattice setup, beam transverse and longitudinal characteristics, ...).
- All settings are controlled via `simulation_parameters.py`.
- Execution:
    ```
    . 000_prepare_simulation.sh 
    ```
- Will generate the lattice and machine settings in `sps/` and the initial particle distribution in `input/`


### Part II: Tracking

- Perform beam tracking (configured also via `simulation_parameters.py`).
- Local execution:
    ```
    python -m runSPS.py 
    ```
    or execution in HTCondor with GPU
    ```
    condor_submit htcondor_submission_gpu.sub
    ```
- An option to run with a one-turn-map instead of the full SPS lattice is possible with:
    ```
    python -m runSPS_OTM.py
    ```
- All the outputs (turn-by-turn beam data, beam profiles, ...) are saved in `output/`.