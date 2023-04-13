'''
Created on Oct 4, 2015

@author: manju
'''

import math
import os
import sys
import operator

from sklearn.externals import joblib

from misc.printer import Printer
from selector import Selector

class RegPairs(Selector):
    '''
     selects an algorithm on the base of pairwise models with regression of performance difference
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def select_algorithms(self, se_dic, features, pwd=""):
        '''
            select algorithms
            Parameter:
                args: dictionary with attributes
                features: list of float values
                pwd: directory of flexfolio (search path for models)
            Returns:
                ordered list of configurations with their decision valuess
        '''
        
        self._set_base_args(se_dic, features)
        
        self._normalize(self._normalization["approach"], self._normalization["filter"], features)
        
        if self._features is None:    #CVSH original was: if not self._features:
            return None
        
        sorted_scores = self.__select(se_dic, pwd)    
        return sorted_scores
        
    def __select(self, se_dic, pwd):
        '''
            scores each configurations
            and returns a list (conf,score)
        '''
        
        x0 = [self._features]
        y0 = [0] # pseudo label
        
        model_files = se_dic["approach"]["models"]
        
        conf_dic = se_dic["configurations"]
        n_solver = len(conf_dic)
        
        dic_solver_votes = dict([x,0] for x in range(0, n_solver))
        
        no_load = False
        if isinstance(model_files, dict): # if cv evaluation is used, the models are not saved in the file system 
            no_load = True
            model_dict = model_files
            model_files = model_files.keys()
        
        for model_file in model_files:
            base_name = os.path.basename(model_file) # format: %d_%d.model
            tuple_solvers = base_name.split(".")[0].split("_")
            i = int(tuple_solvers[0])
            j = int(tuple_solvers[1])
            if no_load:
                model = model_dict[model_file]
            else:
                model = joblib.load(os.path.join(pwd,model_file))
            p_diff = model.predict(x0) # we predict y_i - y_j
            dic_solver_votes[i] += p_diff
            dic_solver_votes[j] -= p_diff 
            
        dic_solver_votes = self.__map_ids_2_names(dic_solver_votes, se_dic["configurations"])
        
        for name, votes in dic_solver_votes.items():
            Printer.print_verbose("%s : %d" %(name, votes))
        
        sorted_scores = sorted(dic_solver_votes.iteritems(),key=operator.itemgetter(1))
        
        Printer.print_nearly_verbose("\nConfiguration Scores:")
        for (solver,score) in sorted_scores:
            Printer.print_nearly_verbose("[%s]: %f" %(solver,score))
        
        return sorted_scores
        
        
    def __map_ids_2_names(self, dic_scores, conf_dic):
        '''
            map id of solver to its name
        '''
        dic_name_score = {}
        for solver_name, meta_dic in conf_dic.items():
            id = meta_dic["id"]
            dic_name_score[solver_name] = dic_scores[int(id)]
        return dic_name_score
                     
        