#!/bin/bash 

#SBATCH -A mallet
#SBATCH --mem=2GB
#SBATCH --time=00:00:100000
#SBATCH -o /dev/null
#SBATCH -e ./error/vflib_si2_m4D_m256.01.err
srun /usr/bin/time -f %e /pfs/tc1/gscratch/dpulatov/GRAPHS2015/solvers/vflib/solve_vf /gscratch/dpulatov/GRAPHS2015/instances/si/si2_m4D_m4D_256/si2_m4D_m256.01/pattern /gscratch/dpulatov/GRAPHS2015/instances/si/si2_m4D_m4D_256/si2_m4D_m256.01/target 100000