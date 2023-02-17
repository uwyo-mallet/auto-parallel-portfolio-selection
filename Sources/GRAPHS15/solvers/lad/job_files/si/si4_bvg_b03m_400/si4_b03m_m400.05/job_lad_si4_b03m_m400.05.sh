#!/bin/bash 

#SBATCH -A mallet
#SBATCH --mem=2GB
#SBATCH --time=00:00:100000
#SBATCH -o /dev/null
#SBATCH -e ./error/lad_si4_b03m_m400.05.err
srun /usr/bin/time -f %e /pfs/tc1/gscratch/dpulatov/GRAPHS2015/solvers/lad/main -p /gscratch/dpulatov/GRAPHS2015/instances/si/si4_bvg_b03m_400/si4_b03m_m400.05/pattern -t /gscratch/dpulatov/GRAPHS2015/instances/si/si4_bvg_b03m_400/si4_b03m_m400.05/target -s 100000