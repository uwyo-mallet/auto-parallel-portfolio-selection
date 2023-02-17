#!/bin/bash 

#SBATCH -A mallet
#SBATCH --mem=2GB
#SBATCH --time=00:00:100000
#SBATCH -o /dev/null
#SBATCH -e ./error/supplementallad_F.10.err
srun /usr/bin/time -f %e /pfs/tc1/gscratch/dpulatov/GRAPHS2015/solvers/supplementallad/main -p /gscratch/dpulatov/GRAPHS2015/instances/scalefree/F.10/pattern -t /gscratch/dpulatov/GRAPHS2015/instances/scalefree/F.10/target -s 100000