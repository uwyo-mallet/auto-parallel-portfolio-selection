#!/bin/bash 

#SBATCH -A mallet
#SBATCH --mem=2GB
#SBATCH --time=00:00:100000
#SBATCH -o /dev/null
#SBATCH -e ./error/vflib_si6_m4Dr4_m625.06.err
srun /usr/bin/time -f %e /pfs/tc1/gscratch/dpulatov/GRAPHS2015/solvers/vflib/solve_vf /gscratch/dpulatov/GRAPHS2015/instances/si/si6_m4D_m4Dr4_625/si6_m4Dr4_m625.06/pattern /gscratch/dpulatov/GRAPHS2015/instances/si/si6_m4D_m4Dr4_625/si6_m4Dr4_m625.06/target 100000