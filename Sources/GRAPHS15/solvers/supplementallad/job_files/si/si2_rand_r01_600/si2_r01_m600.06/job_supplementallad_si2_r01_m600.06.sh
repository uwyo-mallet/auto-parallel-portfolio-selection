#!/bin/bash 

#SBATCH -A mallet
#SBATCH --mem=2GB
#SBATCH --time=00:00:100000
#SBATCH -o /dev/null
#SBATCH -e ./error/supplementallad_si2_r01_m600.06.err
srun /usr/bin/time -f %e /pfs/tc1/gscratch/dpulatov/GRAPHS2015/solvers/supplementallad/main -p /gscratch/dpulatov/GRAPHS2015/instances/si/si2_rand_r01_600/si2_r01_m600.06/pattern -t /gscratch/dpulatov/GRAPHS2015/instances/si/si2_rand_r01_600/si2_r01_m600.06/target -s 100000