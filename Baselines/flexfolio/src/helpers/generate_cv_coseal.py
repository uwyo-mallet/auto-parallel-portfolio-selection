#!/bin/python

import sys
import os
import arff
import random
import copy

def read_inst(file_):
    fp = open(file_)
    arff_dict = arff.load(fp)
    fp.close()
    insts = []
    for data in arff_dict["data"]:
        inst_name = data[0]
        insts.append(inst_name)
    return insts    

def sample_test_val_train(insts, test, train):
    insts = set(insts)
    test_nr = int(len(insts) * test)
    tests_set = random.sample(insts, test_nr)
    train_set = insts.difference(tests_set)
    return tests_set, train_set

def sample_cv(train_set, folds):
    train_set = copy.copy(train_set)
    inst_fold_dict = {}
    for i in range(0,folds):
        fold = random.sample(train_set, int(len(train_set)*1/(folds-i)))
        sys.stderr.write("Fold: %d Size: %d\n" %(i, len(fold)))
        train_set.difference_update(fold)
        for inst_ in fold:
            inst_fold_dict[inst_] = i+1
    return inst_fold_dict
    
def write_cv(tests_set, train_set, inst_fold_dict):
    '''
        first repetition: 1: test, 2: training
        second repetition: -1: not applicable, 0-9: folds for training set
    '''
    print("@relation R_data_frame")

    print("@attribute instance_id string")
    print("@attribute repetition numeric")
    print("@attribute fold numeric")
    
    print("@data")
    for inst_ in tests_set:
        print("%s, 1, 1" %(inst_)) 
        print("%s, 2, -1" %(inst_))

       
    for inst_ in train_set:
        print("%s, 1, 2" %(inst_))
        print("%s, 2, %d" %(inst_, inst_fold_dict[inst_]))  
    
        
FOLDS = 10
# Test, Train
TEST = 0.3
#VAL = 0.21
TRAIN = 0.7

if len(sys.argv) != 2:
    print("Usage: python generate_cv_coseal.py <feature_values.arff>")
    sys.exit(1)
    
insts = read_inst(sys.argv[1])
#print("Insts: %d" %(len(insts)))
tests_set, train_set = sample_test_val_train(insts, test=TEST, train=TRAIN)
sys.stderr.write("Test: %d, Train: %d\n" %(len(tests_set), len(train_set)))

inst_fold_dict = sample_cv(train_set, FOLDS)

write_cv(tests_set, train_set, inst_fold_dict)
