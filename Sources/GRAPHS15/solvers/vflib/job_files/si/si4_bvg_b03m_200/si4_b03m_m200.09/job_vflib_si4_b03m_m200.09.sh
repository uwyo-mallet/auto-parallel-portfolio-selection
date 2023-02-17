#!/bin/bash 

#SBATCH -A mallet
#SBATCH --mem=2GB
#SBATCH --time=00:00:100000
#SBATCH -o /dev/null
#SBATCH -e ./error/vflib_si4_b03m_m200.09.err
srun /usr/bin/time -f %e /pfs/tc1/gscratch/dpulatov/GRAPHS2015/solvers/vflib/solve_vf /gscratch/dpulatov/GRAPHS2015/instances/si/si4_bvg_b03m_200/si4_b03m_m200.09/pattern /gscratch/dpulatov/GRAPHS2015/instances/si/si4_bvg_b03m_200/si4_b03m_m200.09/target 100000