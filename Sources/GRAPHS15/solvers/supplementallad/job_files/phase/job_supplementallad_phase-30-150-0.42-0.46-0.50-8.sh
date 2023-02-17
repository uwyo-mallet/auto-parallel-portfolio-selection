#!/bin/bash 

#SBATCH -A mallet
#SBATCH --mem=2GB
#SBATCH --time=00:00:100000
#SBATCH -o /dev/null
#SBATCH -e ./error/supplementallad_phase-30-150-0.42-0.46-0.50-8.err
srun /usr/bin/time -f %e /pfs/tc1/gscratch/dpulatov/GRAPHS2015/solvers/supplementallad/main -p /gscratch/dpulatov/GRAPHS2015/instances/phase/phase-30-150-0.42-0.46-0.50-8-pattern -t /gscratch/dpulatov/GRAPHS2015/instances/phase/phase-30-150-0.42-0.46-0.50-8-target -s 100000