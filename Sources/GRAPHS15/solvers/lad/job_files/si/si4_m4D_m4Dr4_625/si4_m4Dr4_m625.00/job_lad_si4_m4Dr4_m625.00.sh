#!/bin/bash 

#SBATCH -A mallet
#SBATCH --mem=2GB
#SBATCH --time=00:00:100000
#SBATCH -o /dev/null
#SBATCH -e ./error/lad_si4_m4Dr4_m625.00.err
srun /usr/bin/time -f %e /pfs/tc1/gscratch/dpulatov/GRAPHS2015/solvers/lad/main -p /gscratch/dpulatov/GRAPHS2015/instances/si/si4_m4D_m4Dr4_625/si4_m4Dr4_m625.00/pattern -t /gscratch/dpulatov/GRAPHS2015/instances/si/si4_m4D_m4Dr4_625/si4_m4Dr4_m625.00/target -s 100000