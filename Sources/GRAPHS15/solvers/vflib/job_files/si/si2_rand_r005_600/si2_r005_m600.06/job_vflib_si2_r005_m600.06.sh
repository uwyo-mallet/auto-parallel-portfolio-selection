#!/bin/bash 

#SBATCH -A mallet
#SBATCH --mem=2GB
#SBATCH --time=00:00:100000
#SBATCH -o /dev/null
#SBATCH -e ./error/vflib_si2_r005_m600.06.err
srun /usr/bin/time -f %e /pfs/tc1/gscratch/dpulatov/GRAPHS2015/solvers/vflib/solve_vf /gscratch/dpulatov/GRAPHS2015/instances/si/si2_rand_r005_600/si2_r005_m600.06/pattern /gscratch/dpulatov/GRAPHS2015/instances/si/si2_rand_r005_600/si2_r005_m600.06/target 100000