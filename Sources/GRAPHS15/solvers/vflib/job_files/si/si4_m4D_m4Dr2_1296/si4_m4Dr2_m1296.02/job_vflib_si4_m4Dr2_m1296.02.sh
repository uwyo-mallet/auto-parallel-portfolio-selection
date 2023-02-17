#!/bin/bash 

#SBATCH -A mallet
#SBATCH --mem=2GB
#SBATCH --time=00:00:100000
#SBATCH -o /dev/null
#SBATCH -e ./error/vflib_si4_m4Dr2_m1296.02.err
srun /usr/bin/time -f %e /pfs/tc1/gscratch/dpulatov/GRAPHS2015/solvers/vflib/solve_vf /gscratch/dpulatov/GRAPHS2015/instances/si/si4_m4D_m4Dr2_1296/si4_m4Dr2_m1296.02/pattern /gscratch/dpulatov/GRAPHS2015/instances/si/si4_m4D_m4Dr2_1296/si4_m4Dr2_m1296.02/target 100000