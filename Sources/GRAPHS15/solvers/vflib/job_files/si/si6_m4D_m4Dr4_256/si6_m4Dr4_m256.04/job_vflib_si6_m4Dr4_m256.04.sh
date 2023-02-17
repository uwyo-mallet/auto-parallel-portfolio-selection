#!/bin/bash 

#SBATCH -A mallet
#SBATCH --mem=2GB
#SBATCH --time=00:00:100000
#SBATCH -o /dev/null
#SBATCH -e ./error/vflib_si6_m4Dr4_m256.04.err
srun /usr/bin/time -f %e /pfs/tc1/gscratch/dpulatov/GRAPHS2015/solvers/vflib/solve_vf /gscratch/dpulatov/GRAPHS2015/instances/si/si6_m4D_m4Dr4_256/si6_m4Dr4_m256.04/pattern /gscratch/dpulatov/GRAPHS2015/instances/si/si6_m4D_m4Dr4_256/si6_m4Dr4_m256.04/target 100000