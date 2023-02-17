#!/bin/bash 

#SBATCH -A mallet
#SBATCH --mem=2GB
#SBATCH --time=00:00:100000
#SBATCH -o /dev/null
#SBATCH -e ./error/lad_si2_r005_m600.02.err
srun /usr/bin/time -f %e /pfs/tc1/gscratch/dpulatov/GRAPHS2015/solvers/lad/main -p /gscratch/dpulatov/GRAPHS2015/instances/si/si2_rand_r005_600/si2_r005_m600.02/pattern -t /gscratch/dpulatov/GRAPHS2015/instances/si/si2_rand_r005_600/si2_r005_m600.02/target -s 100000