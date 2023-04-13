#!/bin/python
'''
    sum up all runtime data for algorithm_runs.arff and feature_costs.arff
    @author: Marius Lindauer
    
'''

import os
import sys
import logging
import arff

def read_description(file_):
    cutoff = None
    steps = {}
    default_steps = []
    with open(file_) as fp:
        for line in fp:
            line = line.strip("\n")
            if line.startswith("feature_step"):
                name, feats = line.lstrip("feature_step").split(":")
                name = name.strip(" ")
                feats = map(lambda x: x.strip(" "), feats.split(","))
                steps[name] = feats
            if line.startswith("default_steps"):
                defs = line.lstrip("default_steps:")
                default_steps = map(lambda x: x.strip(" "), defs.split(","))
            if line.startswith("algorithm_cutoff_time"):
                cutoff = float(line.lstrip("algorithm_cutoff_time:").strip(" "))
                
    logging.debug("Cutoff: %.1f" %(cutoff))
    logging.debug("Steps: %s" %(str(steps)))
    logging.debug("Default Steps: %s" %(",".join(default_steps)))
    
    # find usable features of default steps
    unused_features = set()
    unused_steps = set(steps.keys()).difference(set(default_steps))
    for u_step in unused_steps:
        not_processed_features = steps[u_step]
        unused_features = unused_features.union(set(not_processed_features))
        
    all_features = set()
    for feats in steps.values():
        all_features.update(feats)
        
    used_features = set(all_features).difference(unused_features)
        
    print("Active Features: %s" %(",".join(used_features)))
                
    return cutoff, steps, default_steps, used_features
    
def read_inst(file_, cutoff):
    '''
        EXPECTED HEADER:
        @RELATION ALGORITHM_RUNS_2013-SAT-Competition

        @ATTRIBUTE instance_id STRING
        @ATTRIBUTE repetition NUMERIC
        @ATTRIBUTE algorithm STRING
        @ATTRIBUTE PAR10 NUMERIC
        @ATTRIBUTE Number_of_satisfied_clauses NUMERIC
        @ATTRIBUTE runstatus {ok, timeout, memout, not_applicable, crash, other}
    '''
    
    fp = open(file_)
    arff_dict = arff.load(fp)
    fp.close()
    
    algo_costs = 0
    for data in arff_dict["data"]:
        if data[3] is None:
            time = cutoff
        else:
            time = float(data[3])
        algo_costs += time
        
    return algo_costs

def read_costs(file_, steps):
    '''
        Expected header:
        @RELATION FEATURE_COSTS_2013-SAT-Competition

        @ATTRIBUTE instance_id STRING
        @ATTRIBUTE repetition NUMERIC
        @ATTRIBUTE preprocessing NUMERIC
        @ATTRIBUTE local_search_probing NUMERIC
    '''
    
    fp = open(file_)
    arff_dict = arff.load(fp)
    fp.close()
    
    active_indx = []
    indx = 0
    for step,_ in arff_dict["attributes"][2:]:
        if step in default_steps:
            active_indx.append(indx)
        indx += 1    
        
    cost_feats = 0
    
    for data in arff_dict["data"]:
        costs = data[2:]
        costs = [costs[idx] for idx in active_indx] #use only costs of active steps
        
        costs = map(lambda x: 0 if x is None else float(x), costs)
        costs = sum(costs)
        cost_feats += costs
    return cost_feats


#######################################

logging.basicConfig(level=logging.DEBUG)        
        
algo_runs = os.path.join(sys.argv[1], "algorithm_runs.arff")
feature_costs_file = os.path.join(sys.argv[1], "feature_costs.arff")
description = os.path.join(sys.argv[1], "description.txt")

cutoff, steps, default_steps, used_features = read_description(description)
algo_costs = read_inst(algo_runs, cutoff)
if not os.path.isfile(feature_costs_file):
    feature_costs = 0
else:
    feature_costs = read_costs(feature_costs_file, steps)

print("Algo Costs: %.2f" %(algo_costs))
print("Feature Costs: %.2f" %(feature_costs))
print("Sum Costs: %.2f" %(algo_costs + feature_costs))


