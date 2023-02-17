#!/bin/bash 

#SBATCH -A mallet
#SBATCH --mem=2GB
#SBATCH --time=00:00:100000
#SBATCH -o /dev/null
#SBATCH -e ./error/vflib_si2_b03m_m800.03.err
srun /usr/bin/time -f %e /pfs/tc1/gscratch/dpulatov/GRAPHS2015/solvers/vflib/solve_vf /gscratch/dpulatov/GRAPHS2015/instances/si/si2_bvg_b03m_800/si2_b03m_m800.03/pattern /gscratch/dpulatov/GRAPHS2015/instances/si/si2_bvg_b03m_800/si2_b03m_m800.03/target 100000