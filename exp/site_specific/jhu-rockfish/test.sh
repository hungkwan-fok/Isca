#!/bin/bash
#SBATCH --job-name=mpi_test
#SBATCH --partition=shared
#SBATCH --time=00:10:00
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --output=mpi_test_%j.out
#SBATCH --error=mpi_test_%j.err

module purge
source $GFDL_BASE/src/extra/env/jhu-rockfish

echo "Testing different MPI launch methods:"

echo "1. Using srun:"
srun --ntasks=4 hostname

echo -e "\n2. Using mpirun with fork:"
mpirun -bootstrap fork -np 4 hostname

echo -e "\n3. Using mpirun with ssh:"
mpirun -bootstrap ssh -np 4 hostname

echo -e "\n4. Using mpirun with slurm:"
mpirun -bootstrap slurm -np 4 hostname
s
echo -e "\n5. Default mpirun:"
mpirun -np 4 hostname