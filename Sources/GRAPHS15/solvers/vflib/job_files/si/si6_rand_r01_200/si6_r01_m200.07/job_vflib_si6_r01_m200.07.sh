#!/bin/bash 

#SBATCH -A mallet
#SBATCH --mem=2GB
#SBATCH --time=00:00:100000
#SBATCH -o /dev/null
#SBATCH -e ./error/vflib_si6_r01_m200.07.err
srun /usr/bin/time -f %e /pfs/tc1/gscratch/dpulatov/GRAPHS2015/solvers/vflib/solve_vf /gscratch/dpulatov/GRAPHS2015/instances/si/si6_rand_r01_200/si6_r01_m200.07/pattern /gscratch/dpulatov/GRAPHS2015/instances/si/si6_rand_r01_200/si6_r01_m200.07/target 100000