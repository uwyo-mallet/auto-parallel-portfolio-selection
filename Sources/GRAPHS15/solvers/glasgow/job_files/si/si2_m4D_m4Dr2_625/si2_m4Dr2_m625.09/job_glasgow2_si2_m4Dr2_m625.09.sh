#!/bin/bash 

#SBATCH -A mallet
#SBATCH --mem=2GB
#SBATCH --time=00:00:100000
#SBATCH -o /dev/null
#SBATCH -e ./error/glasgow2_si2_m4Dr2_m625.09.err
#SBATCH --partition=teton
module load swset/2018.05
module load gcc/7.3.0
module load boost/1.72.0
srun /usr/bin/time -f %e /pfs/tc1/gscratch/dpulatov/GRAPHS2015/solvers/glasgow2/solve_subgraph_isomorphism glasgow2 /gscratch/dpulatov/GRAPHS2015/instances/si/si2_m4D_m4Dr2_625/si2_m4Dr2_m625.09/pattern /gscratch/dpulatov/GRAPHS2015/instances/si/si2_m4D_m4Dr2_625/si2_m4Dr2_m625.09/target