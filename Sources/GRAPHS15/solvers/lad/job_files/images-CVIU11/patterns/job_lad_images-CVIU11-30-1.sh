#!/bin/bash 

#SBATCH -A mallet
#SBATCH --mem=2GB
#SBATCH --time=00:00:100000
#SBATCH -o /dev/null
#SBATCH -e ./error/lad_images-CVIU11-30-1.err
srun /usr/bin/time -f %e /pfs/tc1/gscratch/dpulatov/GRAPHS2015/solvers/lad/main -p /gscratch/dpulatov/GRAPHS2015/instances/images-CVIU11/patterns/pattern30 -t /gscratch/dpulatov/GRAPHS2015/instances/images-CVIU11/targets/target1 -s 100000