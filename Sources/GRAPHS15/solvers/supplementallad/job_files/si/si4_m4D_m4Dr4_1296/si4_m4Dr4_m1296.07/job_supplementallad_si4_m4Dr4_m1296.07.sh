#!/bin/bash 

#SBATCH -A mallet
#SBATCH --mem=2GB
#SBATCH --time=00:00:100000
#SBATCH -o /dev/null
#SBATCH -e ./error/supplementallad_si4_m4Dr4_m1296.07.err
srun /usr/bin/time -f %e /pfs/tc1/gscratch/dpulatov/GRAPHS2015/solvers/supplementallad/main -p /gscratch/dpulatov/GRAPHS2015/instances/si/si4_m4D_m4Dr4_1296/si4_m4Dr4_m1296.07/pattern -t /gscratch/dpulatov/GRAPHS2015/instances/si/si4_m4D_m4Dr4_1296/si4_m4Dr4_m1296.07/target -s 100000