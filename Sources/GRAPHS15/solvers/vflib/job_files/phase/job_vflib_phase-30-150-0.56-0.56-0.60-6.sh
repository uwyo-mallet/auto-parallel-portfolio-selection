#!/bin/bash 

#SBATCH -A mallet
#SBATCH --mem=2GB
#SBATCH --time=00:00:100000
#SBATCH -o /dev/null
#SBATCH -e ./error/vflib_phase-30-150-0.56-0.56-0.60-6.err
srun /usr/bin/time -f %e /pfs/tc1/gscratch/dpulatov/GRAPHS2015/solvers/vflib/solve_vf /gscratch/dpulatov/GRAPHS2015/instances/phase/phase-30-150-0.56-0.56-0.60-6-pattern /gscratch/dpulatov/GRAPHS2015/instances/phase/phase-30-150-0.56-0.56-0.60-6-target 100000