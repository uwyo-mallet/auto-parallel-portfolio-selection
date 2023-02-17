#!/bin/sh

#SBATCH --account=mallet
#SBATCH --time=7-00:00:00
#SBATCH --partition=teton
#SBATCH --job-name=distance_pattern_features
#SBATCH --output=./distance_pattern_features.out
#SBATCH --error=./distance_pattern_features.error

module load gcc/7.3.0
module load singularity/3.8.1
module load boost/1.72.0 
DIR="/gscratch/hkashgar/BatchScripts/GRAPHS2015/instances"
FILE="/gscratch/hkashgar/BatchScripts/GRAPHS2015/instances_gscratch.txt"

cd "/gscratch/hkashgar/BatchScripts/GRAPHS2015/instances/features/distance_pattern"

ExecFile="/gscratch/hkashgar/BatchScripts/GRAPHS2015/instances/features/graph_stats/graph_stats"

while read instance pattern target num
do
	echo $pattern 
	echo "$pattern.t"
	echo "$pattern.f"
        ts=$(date +%s%N)
	/usr/bin/time -o "$instance.t" $ExecFile --distance $pattern > "$instance.f"
        tt=$((($(date +%s%N) - $ts)/1000000))
	echo $tt >> "$instance.t"
done < $FILE
