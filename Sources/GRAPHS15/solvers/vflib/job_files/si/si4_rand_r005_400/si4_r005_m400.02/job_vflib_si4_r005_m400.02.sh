#!/bin/bash 

#SBATCH -A mallet
#SBATCH --mem=2GB
#SBATCH --time=00:00:100000
#SBATCH -o /dev/null
#SBATCH -e ./error/vflib_si4_r005_m400.02.err
srun /usr/bin/time -f %e /pfs/tc1/gscratch/dpulatov/GRAPHS2015/solvers/vflib/solve_vf /gscratch/dpulatov/GRAPHS2015/instances/si/si4_rand_r005_400/si4_r005_m400.02/pattern /gscratch/dpulatov/GRAPHS2015/instances/si/si4_rand_r005_400/si4_r005_m400.02/target 100000