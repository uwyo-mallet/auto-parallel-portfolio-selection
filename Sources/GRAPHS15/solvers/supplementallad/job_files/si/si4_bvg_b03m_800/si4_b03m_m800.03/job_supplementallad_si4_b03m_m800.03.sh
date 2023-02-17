#!/bin/bash 

#SBATCH -A mallet
#SBATCH --mem=2GB
#SBATCH --time=00:00:100000
#SBATCH -o /dev/null
#SBATCH -e ./error/supplementallad_si4_b03m_m800.03.err
srun /usr/bin/time -f %e /pfs/tc1/gscratch/dpulatov/GRAPHS2015/solvers/supplementallad/main -p /gscratch/dpulatov/GRAPHS2015/instances/si/si4_bvg_b03m_800/si4_b03m_m800.03/pattern -t /gscratch/dpulatov/GRAPHS2015/instances/si/si4_bvg_b03m_800/si4_b03m_m800.03/target -s 100000