#!/bin/bash 

#SBATCH -A mallet
#SBATCH --mem=2GB
#SBATCH --time=00:00:100000
#SBATCH -o /dev/null
#SBATCH -e ./error/supplementallad_si4_b09_m800.00.err
srun /usr/bin/time -f %e /pfs/tc1/gscratch/dpulatov/GRAPHS2015/solvers/supplementallad/main -p /gscratch/dpulatov/GRAPHS2015/instances/si/si4_bvg_b09_800/si4_b09_m800.00/pattern -t /gscratch/dpulatov/GRAPHS2015/instances/si/si4_bvg_b09_800/si4_b09_m800.00/target -s 100000