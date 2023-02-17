#!/bin/bash 

#SBATCH -A mallet
#SBATCH --mem=2GB
#SBATCH --time=00:00:100000
#SBATCH -o /dev/null
#SBATCH -e ./error/vflib_si4_r001_m600.04.err
srun /usr/bin/time -f %e /pfs/tc1/gscratch/dpulatov/GRAPHS2015/solvers/vflib/solve_vf /gscratch/dpulatov/GRAPHS2015/instances/si/si4_rand_r001_600/si4_r001_m600.04/pattern /gscratch/dpulatov/GRAPHS2015/instances/si/si4_rand_r001_600/si4_r001_m600.04/target 100000