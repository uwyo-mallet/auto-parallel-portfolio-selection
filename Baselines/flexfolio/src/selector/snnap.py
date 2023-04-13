'''
Created on Nov 5, 2012

@author: manju
'''

import os
import operator
import json

from sklearn.externals import joblib
from sklearn.neighbors import NearestNeighbors 

from misc.printer import Printer
from selector import Selector

try: # hack for asp competition 2013
    from binaries.libsvm_weights_312.svmutil import *
except:
    pass

class SNNAP(Selector):
    '''
      1. predicts (normalized) performance for each solver
      2. uses k-NN on predicted performance 
      3. selects best solver on k-neighbors 
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
        
    def __select(self,se_dic, pwd):
        '''
            scores each configurations
            and returns a list (conf,score)
        '''
        
        x0 = [self._features]
        k = se_dic["approach"]["k"] 
        best_n = se_dic["approach"]["best_n"]
        
        model_files = se_dic["approach"]["models"]
        
        conf_dic = se_dic["configurations"]
        n_solver = len(conf_dic)
        
        # prediction of scaled runtimes
        
        if isinstance(model_files, list): # if cv evaluation is used, the models are not saved in the file system 
            models = model_files
            knn_data = model_files = se_dic["approach"]["knn_data"]
        else:
            models = []
            with open(os.path.join(pwd,knn_data)) as fp:
                knn_data = json.load(fp)
            for model_file in model_files:
                model = joblib.load(os.path.join(pwd,model_file))
                models.append(model)
        
        perf_features = []
        for model in models:
            p = model.predict(x0)[0]
            perf_features.append(p)
            
        # nearest neighbors
        
        knn_train = map(lambda x: x[0], knn_data)
        dist, nn_index = self.__kneighbors(perf_features, knn_train, k, best_n)
    
        solver_perfs = [0] * n_solver
        for neighbor in nn_index:
            perfs = knn_data[neighbor][1] #unscaled performance data
            solver_perfs = map(lambda x: x[0]+x[1], zip(solver_perfs, perfs))

        dic_solver_scores = self.__map_ids_2_names(solver_perfs, conf_dic)
        
        Printer.print_verbose(str(dic_solver_scores))
        sorted_scores = sorted(dic_solver_scores.iteritems(),key=operator.itemgetter(1))
        
        for (solver,score) in sorted_scores:
            Printer.print_nearly_verbose("[%s]: %f" %(solver,score))
        
        return sorted_scores
        
    def __kneighbors(self, X, train, k, best_n=3):
        distances = []
        best_on_X = set(self.__get_n_min(X, best_n))
        for vec in train:
            best_on_v = set(self.__get_n_min(vec, best_n))
            Printer.print_nearly_verbose("Best on y: %s" %(str(best_on_v)))
            Printer.print_nearly_verbose("Best on x: %s" %(str(best_on_X)))
            dist = 1 - (len(set.intersection(best_on_X, best_on_v)) / len(set.union(best_on_X, best_on_v)))
            distances.append(dist)
            #print(dist)
        sorted_data = sorted(enumerate(distances), key=lambda x: x[1])
        sorted_indx = map(lambda x: x[0], sorted_data)
        sorted_dists = map(lambda x: x[1], sorted_data)
        return sorted_dists[:k], sorted_indx[:k]
            
    def __get_n_min(self, vec, n):
        sorted_vec = sorted(vec)[:n]
        min_indx = []
        for v in sorted_vec:
            for indx, v_o in enumerate(vec):
                if v_o == v and indx not in min_indx:
                    min_indx.append(indx)
        return min_indx
        
    def __map_ids_2_names(self, dic_scores, conf_dic):
        '''
            map id of solver to its name
        '''
        dic_name_score = {}
        for solver_name, meta_dic in conf_dic.items():
            id = meta_dic["id"]
            dic_name_score[solver_name] = dic_scores[int(id)]
        return dic_name_score
                     
        