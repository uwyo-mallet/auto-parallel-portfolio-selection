#!/bin/bash 

#SBATCH -A mallet
#SBATCH --mem=2GB
#SBATCH --time=00:00:100000
#SBATCH -o /dev/null
#SBATCH -e ./error/vflib_si6_b03m_m400.05.err
srun /usr/bin/time -f %e /pfs/tc1/gscratch/dpulatov/GRAPHS2015/solvers/vflib/solve_vf /gscratch/dpulatov/GRAPHS2015/instances/si/si6_bvg_b03m_400/si6_b03m_m400.05/pattern /gscratch/dpulatov/GRAPHS2015/instances/si/si6_bvg_b03m_400/si6_b03m_m400.05/target 100000