#!/bin/sh

#SBATCH --account=mallet
#SBATCH --time=7-00:00:00
#SBATCH --partition=teton
#SBATCH --job-name=distance_target_features
#SBATCH --output=./distance_target_features.out
#SBATCH --error=./distance_target_features.error

module load gcc/7.3.0
module load singularity/3.8.1
module load boost/1.72.0 
DIR="/gscratch/hkashgar/BatchScripts/GRAPHS2015/instances"
FILE="/gscratch/hkashgar/BatchScripts/GRAPHS2015/instances_gscratch.txt"

cd "/gscratch/hkashgar/BatchScripts/GRAPHS2015/instances/features/distance_target"

ExecFile="/gscratch/hkashgar/BatchScripts/GRAPHS2015/instances/features/graph_stats/graph_stats"

while read instance pattern target num
do
	echo $target
	echo "$target.t"
	echo "$target.f"
        ts=$(date +%s%N)
	/usr/bin/time -o "$instance.t" $ExecFile --distance $target > "$instance.f"
        tt=$((($(date +%s%N) - $ts)/1000000))
	echo $tt >> "$instance.t"
done < $FILE
