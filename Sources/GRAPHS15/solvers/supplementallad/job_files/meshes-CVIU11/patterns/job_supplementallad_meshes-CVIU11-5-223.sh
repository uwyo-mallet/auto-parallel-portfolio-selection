#!/bin/bash 

#SBATCH -A mallet
#SBATCH --mem=2GB
#SBATCH --time=00:00:100000
#SBATCH -o /dev/null
#SBATCH -e ./error/supplementallad_meshes-CVIU11-5-223.err
srun /usr/bin/time -f %e /pfs/tc1/gscratch/dpulatov/GRAPHS2015/solvers/supplementallad/main -p /gscratch/dpulatov/GRAPHS2015/instances/meshes-CVIU11/patterns/pattern5 -t /gscratch/dpulatov/GRAPHS2015/instances/meshes-CVIU11/targets/target223 -s 100000