#!/bin/bash 

#SBATCH -A mallet
#SBATCH --mem=2GB
#SBATCH --time=00:00:100000
#SBATCH -o /dev/null
#SBATCH -e ./error/supplementallad_si6_m4D_m625.09.err
srun /usr/bin/time -f %e /pfs/tc1/gscratch/dpulatov/GRAPHS2015/solvers/supplementallad/main -p /gscratch/dpulatov/GRAPHS2015/instances/si/si6_m4D_m4D_625/si6_m4D_m625.09/pattern -t /gscratch/dpulatov/GRAPHS2015/instances/si/si6_m4D_m4D_625/si6_m4D_m625.09/target -s 100000