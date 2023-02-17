#!/bin/bash 

#SBATCH -A mallet
#SBATCH --mem=2GB
#SBATCH --time=00:00:100000
#SBATCH -o /dev/null
#SBATCH -e ./error/vflib_si2_r001_m200.02.err
srun /usr/bin/time -f %e /pfs/tc1/gscratch/dpulatov/GRAPHS2015/solvers/vflib/solve_vf /gscratch/dpulatov/GRAPHS2015/instances/si/si2_rand_r001_200/si2_r001_m200.02/pattern /gscratch/dpulatov/GRAPHS2015/instances/si/si2_rand_r001_200/si2_r001_m200.02/target 100000