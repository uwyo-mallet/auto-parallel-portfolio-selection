#!/bin/bash 

#SBATCH -A mallet
#SBATCH --mem=2GB
#SBATCH --time=00:00:100000
#SBATCH -o /dev/null
#SBATCH -e ./error/supplementallad_si6_r001_m400.02.err
srun /usr/bin/time -f %e /pfs/tc1/gscratch/dpulatov/GRAPHS2015/solvers/supplementallad/main -p /gscratch/dpulatov/GRAPHS2015/instances/si/si6_rand_r001_400/si6_r001_m400.02/pattern -t /gscratch/dpulatov/GRAPHS2015/instances/si/si6_rand_r001_400/si6_r001_m400.02/target -s 100000