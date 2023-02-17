#!/bin/bash

DIR="/gscratch/hkashgar/BatchScripts/GRAPHS2015/instances"
FILE="/gscratch/hkashgar/BatchScripts/GRAPHS2015/instances/features/lad_features/lad_probs.txt"
PATH="/gscratch/hkashgar/BatchScripts/GRAPHS2015/instances/features/lad_features/"
cd "/gscratch/hkashgar/BatchScripts/GRAPHS2015/instances/features/lad_features"
ExecFile="/gscratch/hkashgar/BatchScripts/GRAPHS2015/instances/features/lad_stats/LADpreprocessing"

#module load gcc/7.3.0
while read instance pattern target num
do
	ts=$(/usr/bin/date +%s%N)
        $ExecFile -p $pattern -t $target > "$instance.f"
        tt=$((($(/usr/bin/date +%s%N) - $ts)/1000000))
        echo $tt > "$instance.t"
done < $FILE
