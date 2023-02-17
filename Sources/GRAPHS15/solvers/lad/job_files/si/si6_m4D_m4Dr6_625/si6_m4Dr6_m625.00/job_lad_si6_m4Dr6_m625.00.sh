#!/bin/bash 

#SBATCH -A mallet
#SBATCH --mem=2GB
#SBATCH --time=00:00:100000
#SBATCH -o /dev/null
#SBATCH -e ./error/lad_si6_m4Dr6_m625.00.err
srun /usr/bin/time -f %e /pfs/tc1/gscratch/dpulatov/GRAPHS2015/solvers/lad/main -p /gscratch/dpulatov/GRAPHS2015/instances/si/si6_m4D_m4Dr6_625/si6_m4Dr6_m625.00/pattern -t /gscratch/dpulatov/GRAPHS2015/instances/si/si6_m4D_m4Dr6_625/si6_m4Dr6_m625.00/target -s 100000