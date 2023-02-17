#!/bin/bash 

#SBATCH -A mallet
#SBATCH --mem=2GB
#SBATCH --time=00:00:100000
#SBATCH -o /dev/null
#SBATCH -e ./error/vflib_si2_b09_m400.07.err
srun /usr/bin/time -f %e /pfs/tc1/gscratch/dpulatov/GRAPHS2015/solvers/vflib/solve_vf /gscratch/dpulatov/GRAPHS2015/instances/si/si2_bvg_b09_400/si2_b09_m400.07/pattern /gscratch/dpulatov/GRAPHS2015/instances/si/si2_bvg_b09_400/si2_b09_m400.07/target 100000