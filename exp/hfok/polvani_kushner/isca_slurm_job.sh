#!/bin/bash -l
#
#SBATCH --job-name=polvani_kushner_py
#SBATCH --partition=parallel          # or “short”, “long”, …
#SBATCH --time=06:00:00           # wall-clock limit
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32      # Rockfish = 48 cores / node
#SBATCH --cpus-per-task=1
#SBATCH --output=slurm_%j.out
#SBATCH --error=slurm_%j.err

echo "Running on host $(hostname)"
echo "Start time: $(date)"
echo "Working dir: $(pwd)"

########################## 1  Modules / env ##########################

source "$HOME/.bashrc"
source $GFDL_BASE/src/extra/env/jhu-rockfish

########################## 2  Launch ##########################
# Run the Python driver that compiles (if needed) and then executes.
# -- Assuming the script is the standard test-case provided by Isca:
$HOME/.conda/envs/isca_env/bin/python $GFDL_BASE/exp/hfok/polvani_kushner/polvani_kushner.py

########################## 3  Book-keeping ##########################
echo "End   time: $(date)"
