#!/bin/bash 

#SBATCH -A mallet
#SBATCH --mem=2GB
#SBATCH --time=00:00:100000
#SBATCH -o /dev/null
#SBATCH -e ./error/lad_si2_b09m_m400.03.err
srun /usr/bin/time -f %e /pfs/tc1/gscratch/dpulatov/GRAPHS2015/solvers/lad/main -p /gscratch/dpulatov/GRAPHS2015/instances/si/si2_bvg_b09m_400/si2_b09m_m400.03/pattern -t /gscratch/dpulatov/GRAPHS2015/instances/si/si2_bvg_b09m_400/si2_b09m_m400.03/target -s 100000