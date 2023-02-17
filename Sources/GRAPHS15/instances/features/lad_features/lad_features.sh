#!/bin/sh

#SBATCH --account=mallet
#SBATCH --time=7-00:00:00
#SBATCH --partition=teton
#SBATCH --job-name=lad_features
#SBATCH --output=./lad_features.out
#SBATCH --error=./lad_features.error

module load gcc/7.3.0
module load singularity/3.8.1
#module load boost/1.72.0 

DIR="/gscratch/hkashgar/BatchScripts/GRAPHS2015/instances"
FILE="/gscratch/hkashgar/BatchScripts/GRAPHS2015/instances_gscratch.txt"
PATH="/gscratch/hkashgar/BatchScripts/GRAPHS2015/instances/features/lad_features/"
cd "/gscratch/hkashgar/BatchScripts/GRAPHS2015/instances/features/lad_features"
ExecFile="/gscratch/hkashgar/BatchScripts/GRAPHS2015/instances/features/lad_stats/LADpreprocessing"

while read instance pattern target num
do
	ts=$(date +%s%N)
	singularity run my-container.sif $ExecFile -p $pattern -t $target > "$instance.f"
        tt=$((($(date +%s%N) - $ts)/1000000))
	echo $tt >> "$instance.t"
done < $FILE
