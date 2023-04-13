'''
Created on Nov 9, 2012

@author: manju
'''

import random
import copy

from misc.printer import Printer
#from misc.updater import Updater
from trainer.evalutor.validator import Validator, Stats
from trainer.evalutor.plotter import Plotter
from trainer.evalutor.crossValidator import CrossValidator

class CrossValidatorGiven(CrossValidator):
    '''
        perform cross validation evaluation with given splits
    '''

    def _get_cross_fold(self, instance_dic, rep=None):
        '''
            uses the splits given by cv.arff
            (restriction: only first repetition used)
        '''
        new_inst_dic = {} # in case that not all instances are considered in folds, e.g., fold index < 1
        Printer.print_c("Use given CV of %d-th repetition" %(rep))
        fold_index = 1
        found = True
        self._instance_parts = []
        while found:
            part_dict = {}
            for name, inst_ in instance_dic.items():
                if inst_._fold[rep] == fold_index:
                    part_dict[name] = inst_
                    new_inst_dic[name] = inst_
            if part_dict:
                self._instance_parts.append(part_dict)
                found = True
                fold_index += 1
            else:
                found = False
        self._n_folds = fold_index - 1 
        
        return new_inst_dic
        