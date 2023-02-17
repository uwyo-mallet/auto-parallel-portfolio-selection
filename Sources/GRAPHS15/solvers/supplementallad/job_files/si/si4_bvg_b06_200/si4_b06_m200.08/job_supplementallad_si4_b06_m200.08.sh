#!/bin/bash 

#SBATCH -A mallet
#SBATCH --mem=2GB
#SBATCH --time=00:00:100000
#SBATCH -o /dev/null
#SBATCH -e ./error/supplementallad_si4_b06_m200.08.err
srun /usr/bin/time -f %e /pfs/tc1/gscratch/dpulatov/GRAPHS2015/solvers/supplementallad/main -p /gscratch/dpulatov/GRAPHS2015/instances/si/si4_bvg_b06_200/si4_b06_m200.08/pattern -t /gscratch/dpulatov/GRAPHS2015/instances/si/si4_bvg_b06_200/si4_b06_m200.08/target -s 100000