#!/bin/bash 

#SBATCH -A mallet
#SBATCH --mem=2GB
#SBATCH --time=00:00:100000
#SBATCH -o /dev/null
#SBATCH -e ./error/vflib_si6_b09_m400.06.err
srun /usr/bin/time -f %e /pfs/tc1/gscratch/dpulatov/GRAPHS2015/solvers/vflib/solve_vf /gscratch/dpulatov/GRAPHS2015/instances/si/si6_bvg_b09_400/si6_b09_m400.06/pattern /gscratch/dpulatov/GRAPHS2015/instances/si/si6_bvg_b09_400/si6_b09_m400.06/target 100000