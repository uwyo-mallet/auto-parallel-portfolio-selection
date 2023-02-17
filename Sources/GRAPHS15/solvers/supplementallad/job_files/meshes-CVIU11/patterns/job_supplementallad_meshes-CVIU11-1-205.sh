#!/bin/bash 

#SBATCH -A mallet
#SBATCH --mem=2GB
#SBATCH --time=00:00:100000
#SBATCH -o /dev/null
#SBATCH -e ./error/supplementallad_meshes-CVIU11-1-205.err
srun /usr/bin/time -f %e /pfs/tc1/gscratch/dpulatov/GRAPHS2015/solvers/supplementallad/main -p /gscratch/dpulatov/GRAPHS2015/instances/meshes-CVIU11/patterns/pattern1 -t /gscratch/dpulatov/GRAPHS2015/instances/meshes-CVIU11/targets/target205 -s 100000