#!/bin/bash 

#SBATCH -A mallet
#SBATCH --mem=2GB
#SBATCH --time=00:00:100000
#SBATCH -o /dev/null
#SBATCH -e ./error/vflib_si4_m4Dr4_m1296.00.err
srun /usr/bin/time -f %e /pfs/tc1/gscratch/dpulatov/GRAPHS2015/solvers/vflib/solve_vf /gscratch/dpulatov/GRAPHS2015/instances/si/si4_m4D_m4Dr4_1296/si4_m4Dr4_m1296.00/pattern /gscratch/dpulatov/GRAPHS2015/instances/si/si4_m4D_m4Dr4_1296/si4_m4Dr4_m1296.00/target 100000