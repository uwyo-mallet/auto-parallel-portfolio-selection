#!/bin/bash 

#SBATCH -A mallet
#SBATCH --mem=2GB
#SBATCH --time=00:00:100000
#SBATCH -o /dev/null
#SBATCH -e ./error/supplementallad_g43-g78.err
srun /usr/bin/time -f %e /pfs/tc1/gscratch/dpulatov/GRAPHS2015/solvers/supplementallad/main -p /gscratch/dpulatov/GRAPHS2015/instances/LV/g43 -t /gscratch/dpulatov/GRAPHS2015/instances/largerGraphs/g78 -s 100000