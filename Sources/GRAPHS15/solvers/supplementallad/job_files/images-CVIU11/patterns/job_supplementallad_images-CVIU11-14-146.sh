#!/bin/bash 

#SBATCH -A mallet
#SBATCH --mem=2GB
#SBATCH --time=00:00:100000
#SBATCH -o /dev/null
#SBATCH -e ./error/supplementallad_images-CVIU11-14-146.err
srun /usr/bin/time -f %e /pfs/tc1/gscratch/dpulatov/GRAPHS2015/solvers/supplementallad/main -p /gscratch/dpulatov/GRAPHS2015/instances/images-CVIU11/patterns/pattern14 -t /gscratch/dpulatov/GRAPHS2015/instances/images-CVIU11/targets/target146 -s 100000