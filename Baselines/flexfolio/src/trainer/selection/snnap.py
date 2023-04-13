'''
Created on Nov 9, 2012

@author: manju
'''
import os
import sys
import json

import numpy
from sklearn.preprocessing import StandardScaler

from trainer.selection.selector import SelectorTrainer
from misc.printer import Printer



class SNNAPTrainer(SelectorTrainer):
    '''
        trainer for SNNAPP:
          1. learn regression models for each solver: features -> (z-score) performance
        Run:
          1. predict for each solver: features -> performance
          2. use predicted performances for k-NN
    '''


    def __init__(self, k=1, best_n=3, save_models=True):
        '''
            Constructor
        '''
        SelectorTrainer.__init__(self, save_models)
        self._cutoff = 900
        self._norm_approach = "Zscore"
        
        self.k = k
        self.best_n = best_n
        
        if self.k < 1:
            Printer.print_e("k has to be > 0", 88)
        
        self._UNKNOWN_CODE = -512
        self._CACHE_SIZE = 1000 # memory size of libsvm
   
    def __repr__(self):
        return "SNNAP"
   
    def train(self, instance_dic, solver_list, config_dic, cutoff, model_dir, f_indicator, n_feats):
        '''
            train model
            Args:
                instance_dic: instance name -> Instance()
                solver_list: list of solvers
                norm_approach: normalization approach
                cutoff: runtime cutoff
                model_dir: directory to save model
                f_indicator: of used features
                n_feats: number of features
        '''
        
        self._cutoff = cutoff
        
        Printer.print_nearly_verbose("Chosen k: %d" %(self.k))
        
        # first scale performance data with z-score on each instance
        scaler = StandardScaler()
        knn_data = [] # pair: scaled perf, unscaled perf
        train_data_dict = [{"x":[], "y":[]} for s in solver_list] # solver -> (features x perf)
        for inst in instance_dic.itervalues():
            perf_vec = inst._transformed_cost_vec
            perf_vec = scaler.fit_transform(perf_vec)
            knn_data.append((perf_vec.tolist(), inst._transformed_cost_vec))
            features = inst._normed_features
            for indx, perf in enumerate(perf_vec):
                train_data_dict[indx]["x"].append(features)
                train_data_dict[indx]["y"].append(perf)

        models = [] #in order of solver_list
        for train_data in train_data_dict:    
            model = self._train_regression(train_data["y"], train_data["x"], [1]*len(train_data["x"]))
            if model is None:
                model = cutoff
            models.append(model)
        
        if self._save_models:
            files, knn_data_file_name = self.__save_models(models, knn_data, model_dir)
        else:
            files = models
            knn_data_file_name = knn_data
        
        # build selection_dic
        conf_dic = {}
        for solver,cmd in config_dic.items():
                    solver_dic = {
                          "call": cmd,                  
                          "id" : solver_list.index(str(solver))          
                          }
                    conf_dic[solver] = solver_dic
        sel_dic = {
                   "approach": {
                                "approach" : "kNN",
                                "k" : self.k,
                                "best_n" : self.best_n,
                                "models" : files,
                                "knn_data" : knn_data_file_name
                                },
                   "normalization" : {
                                      "filter"  : f_indicator                           
                                 },
                   "configurations":conf_dic                        
                   }
        return sel_dic
   
    def __save_models(self, models, knn_data, model_dir):
        '''
            save models to files
            Args:
                models: (class, solver ) -> Model()
                class_model :class prediction model
                model_dir: directory to save models
            Returns:
                list of file names for models
        '''
        from sklearn.externals import joblib
        
        files = []
        for solver_id,model in enumerate(models):
            file_name = os.path.join(model_dir, '%d.model' %(solver_id))
            joblib.dump(model, file_name, compress=9)
            files.append(file_name)
            
        knn_data_file_name = os.path.join(model_dir, 'knn_data.model')
        with open(knn_data_file_name, "w") as fp:
            json.dump(knn_data, fp, indent=2)
        return files, knn_data_file_name
        
    def _train_regression(self, y, X, weights):
        '''
            abstract method
            train the regression model
            Args:
                y: vector of labels
                X: matrix of features
                weights: weights for each observation
        '''    