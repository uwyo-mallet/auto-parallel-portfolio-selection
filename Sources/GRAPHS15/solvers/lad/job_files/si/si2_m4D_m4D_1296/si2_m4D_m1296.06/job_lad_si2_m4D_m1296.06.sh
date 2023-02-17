#!/bin/bash 

#SBATCH -A mallet
#SBATCH --mem=2GB
#SBATCH --time=00:00:100000
#SBATCH -o /dev/null
#SBATCH -e ./error/lad_si2_m4D_m1296.06.err
srun /usr/bin/time -f %e /pfs/tc1/gscratch/dpulatov/GRAPHS2015/solvers/lad/main -p /gscratch/dpulatov/GRAPHS2015/instances/si/si2_m4D_m4D_1296/si2_m4D_m1296.06/pattern -t /gscratch/dpulatov/GRAPHS2015/instances/si/si2_m4D_m4D_1296/si2_m4D_m1296.06/target -s 100000