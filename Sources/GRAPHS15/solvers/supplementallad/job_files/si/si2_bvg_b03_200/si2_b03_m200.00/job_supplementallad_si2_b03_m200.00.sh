#!/bin/bash 

#SBATCH -A mallet
#SBATCH --mem=2GB
#SBATCH --time=00:00:100000
#SBATCH -o /dev/null
#SBATCH -e ./error/supplementallad_si2_b03_m200.00.err
srun /usr/bin/time -f %e /pfs/tc1/gscratch/dpulatov/GRAPHS2015/solvers/supplementallad/main -p /gscratch/dpulatov/GRAPHS2015/instances/si/si2_bvg_b03_200/si2_b03_m200.00/pattern -t /gscratch/dpulatov/GRAPHS2015/instances/si/si2_bvg_b03_200/si2_b03_m200.00/target -s 100000