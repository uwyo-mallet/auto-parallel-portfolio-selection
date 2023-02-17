#!/bin/bash 

#SBATCH -A mallet
#SBATCH --mem=2GB
#SBATCH --time=00:00:100000
#SBATCH -o /dev/null
#SBATCH -e ./error/vflib_meshes-CVIU11-1-34.err
srun /usr/bin/time -f %e /pfs/tc1/gscratch/dpulatov/GRAPHS2015/solvers/vflib/solve_vf /gscratch/dpulatov/GRAPHS2015/instances/meshes-CVIU11/patterns/pattern1 /gscratch/dpulatov/GRAPHS2015/instances/meshes-CVIU11/targets/target34 100000