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
    cvs = []
    for x in xrange(0,10):
        cvs.append([])
    for data in arff_dict["data"]:
        inst_name = data[0]
        split = int(data[2])
        cvs[split-1].append(inst_name)
    return cvs    

def sample_test_val_train(cvs):

    inner_cv = {}
    for index in xrange(1,11):
        train = set()
        for r_split, inner_index in zip(cvs, range(1,11)):
            if index != inner_index:
                train = train.union(set(r_split))
        inner_cv[index] = sample_cv(train)
    return inner_cv

def sample_cv(train_set, folds=10):
    train_set = copy.copy(train_set)
    inst_fold_dict = {}
    for i in range(0,folds):
        fold = random.sample(train_set, int(len(train_set)*1/(folds-i)))
        #sys.stderr.write("Fold: %d Size: %d\n" %(i, len(fold)))
        train_set.difference_update(fold)
        for inst_ in fold:
            inst_fold_dict[inst_] = i+1
    return inst_fold_dict
    
def write_cv(cvs, inner_cv):
    '''
        first repetition: 1: test, 2: training
        second repetition: -1: not applicable, 0-9: folds for training set
    '''
    print("@relation R_data_frame")

    print("@attribute instance_id string")
    print("@attribute repetition numeric")
    print("@attribute fold numeric")
    
    print("@data")
    for split, index in zip(cvs, range(1,11)):    
        for inst in split:
            print("%s, 1, %d" %(inst, index))
            for inner in xrange(1,11):
                inner_id = inner_cv[inner].get(inst)
                if inner_id is None:
                    inner_id = -1
                print("%s, %d, %d" %(inst, inner+1, inner_id))
FOLDS = 10

if len(sys.argv) != 2:
    print("Usage: python generate_outer_cv_coseal.py <cv.arff>")
    sys.exit(1)
    
cvs = read_inst(sys.argv[1])
#print("Insts: %d" %(len(insts)))
inner_cv = sample_test_val_train(cvs)

write_cv(cvs, inner_cv)
