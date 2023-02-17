#!/bin/bash 

#SBATCH -A mallet
#SBATCH --mem=2GB
#SBATCH --time=00:00:100000
#SBATCH -o /dev/null
#SBATCH -e ./error/lad_si4_m4D_m625.01.err
srun /usr/bin/time -f %e /pfs/tc1/gscratch/dpulatov/GRAPHS2015/solvers/lad/main -p /gscratch/dpulatov/GRAPHS2015/instances/si/si4_m4D_m4D_625/si4_m4D_m625.01/pattern -t /gscratch/dpulatov/GRAPHS2015/instances/si/si4_m4D_m4D_625/si4_m4D_m625.01/target -s 100000