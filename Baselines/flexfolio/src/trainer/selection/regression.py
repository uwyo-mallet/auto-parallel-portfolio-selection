'''
Created on Nov 8, 2012

@author: manju
'''

import os
#import math
#import json
#import sys

from trainer.selection.selector import SelectorTrainer
from misc.printer import Printer
from trainer.selection.metatuner import MetaTuner

class Regression(SelectorTrainer):
    '''
       train for each algorithm and meta class (SAT/UNSAT) a regression model
       and a classifier for the meta class
    '''


    def __init__(self, save_models=True):
        '''
        Constructor
        '''
        SelectorTrainer.__init__(self, save_models)
        self.__MINIMAL_RUNTIME = 0.005
        self._UNKNOWN_CODE = -512
        self._CACHE_SIZE = 1000 # memory size of libsvm
               
    def train(self, instance_dic, solver_list, config_dic, cutoff,
              model_dir, f_indicator, n_feats):
        '''
            train models for flexfolio based on classifcation models of libsvm
            Args:
                instance_dic: instance name -> Instance()
                solver_list: list of solver names
                config_dic: solver name -> call
                cutoff: runtime captime
                model_dir: directory to save trained models
                f_indicator: indicates the use of features or set them to 
            Return:
                dictionary with all meta information to use models
        '''
        
        self._cutoff = cutoff
        
        n_solver = len(solver_list)
        
        # model per algorithm x class and class prediction model
        models, class_model = self.__collect_and_train_data(instance_dic, n_solver, cutoff)

        if self._save_models:        
            # save models
            files = self.__save_models(models, class_model, model_dir)
        else:
            files = self.__collect_models(models, class_model, model_dir)
        
        conf_dic = {}
        for solver in range(0,n_solver) :
            solver_dic = {
                          "call": config_dic[solver_list[solver]],                            
                          "backup" : "False",
                          "id" : str(solver)
                          }
            conf_dic[solver_list[solver]] = solver_dic
        selector_dic = self.__compose_config_dic(files, f_indicator, conf_dic, model_dir)
        return selector_dic
    
    def __collect_and_train_data(self, instance_dic, n_solver, cutoff):
        '''
            collects all necessary data to train a model per algorithm
            and trains pairwise svm models
            Args:
                instance_dic : instance name -> Instance()
                n_solver: number of solvers
                cutoff: cutoff time (int)
            Returns:
                models: (solver i, solver j) -> Model()
        '''
        models = {}

        # collect features
        features = {} # status -> matrix of features
        labels = {} # status -> matrix of labels
        weights = {} # status -> vector of weights
        
        # ensure same order of instances independently of memory allocation
        inst_keys = sorted(instance_dic.keys())
        for inst_name in inst_keys:
            inst  = instance_dic[inst_name]
            if inst._pre_solved:
                continue
            class_ = inst._ground_truth.get("satunsat") # TODO: Generalize
            if class_ == None or class_ == "?": # or class_ == -1:
                class_ = -1
            
            features[class_] = features.get(class_,[])
            feat_matrix = features.get(class_)

            labels[class_] = labels.get(class_,[[] for _ in range(0,n_solver)])
            label_matrix = labels.get(class_)

            weights[class_] = weights.get(class_,[])
            weight_vector = weights.get(class_)

            feat_matrix.append(inst._normed_features)
            weight_vector.append(inst._weight)
            labels_inst =  inst._transformed_cost_vec
            
            for id_solver in range(0,n_solver):
                runtime = labels_inst[id_solver]
                #label = max(runtime, self.__MINIMAL_RUNTIME)
                label_matrix[id_solver].append(runtime) 
        
        joined_feats = []
        class_labels = []
        class_weights = []
        for class_, feat_matrix in features.items():
            # class prediction data
            joined_feats.extend(feat_matrix) 
            class_labels.extend([class_]*len(feat_matrix))
            weights_class = weights[class_]
            class_weights.extend(weights_class)
            # model learning for each class x algorithm
            for id_solver in range(0, n_solver):
                labels_id = labels[class_][id_solver]
                index = 0
                for lab in labels_id:
                    if lab == self._UNKNOWN_CODE: # unknown runtime, e.g. -512
                        labels_id.pop(index)
                        weights_class.pop(index)
                        feat_matrix.pop(index)
                    else:
                        index += 1
                if index == 0:
                    Printer.print_w("No Trainings data for model - Check input data!")
                if len(set(labels_id)) == 1:
                    model = cutoff
                    #Printer.print_w("Remove algorithms with constant performance (e.g., only timeouts) or use --contr-filter 0.000001")
                else:
                    model = self._train_regression(labels_id, feat_matrix, weights_class)
                    if model is None:
                        model = cutoff
                #model = svm_train(weights_class, labels_id, feat_matrix, '-s 3 -c %f -g %f -m 1000 -q' %(c, g))
                models[(class_,id_solver)] = model
        
        # train class prediction model
        weights = [1]*len(class_labels) #TODO: adjust instance weights
        class_model = self._train_classifier(class_labels, joined_feats, weights)
        
        return models, class_model
    
    
    def _train_regression(self, y, X, weights):
        '''
            abstract method
            train the regression model
            Args:
                y: vector of labels
                X: matrix of features
                weights: weights for each observation
        '''
        
    def _train_classifier(self,y, X, weights):
        '''
            train the classification model
            Args:
                y: vector of labels
                X: matrix of features
                weights: weights for each observation
            Return:
                trainer: instance of sklearn.svm.SVC
        '''
        from sklearn.svm import SVC
        import numpy

        X = numpy.array(X)
        y = numpy.array(y)
        weights = numpy.array(weights)
        
        many_labels = numpy.any(y - min(y))
        
        if many_labels:
            tuner = MetaTuner()
            tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1, 0.5, 0.25, 0.125, 0.0625, 0.0],
                                 'C': [0.5, 1, 4, 16, 64],
                                'max_iter': [100], 'cache_size': [self._CACHE_SIZE]}]
            best_svc = tuner.tune(X, y, SVC, tuned_parameters)

            trainer = SVC(kernel=best_svc.kernel, C=best_svc.C, gamma=best_svc.gamma, probability=True, cache_size=self._CACHE_SIZE, random_state=12345)
            trainer.fit(X,y,sample_weight=weights)
        else:
            trainer = None
            
        return trainer
    
    def __save_models(self, models, class_model, model_dir):
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
        for (class_,solver_id),model in models.items():
            file_name = os.path.join(model_dir, '%d_%d.model' %(class_,solver_id))
            joblib.dump(model, file_name, compress=9)
            files.append(file_name)
            
        class_file_name = os.path.join(model_dir, 'class.model')
        joblib.dump(class_model, class_file_name, compress=9)
        files.append(class_file_name)
        return files
                
    def __collect_models(self, models, class_model, model_dir):
        '''
            collect models in a dictionary (theoretical file name -> model)
            Args:
                models: (class, solver ) -> Model()
                class_model :class prediction model
                model_dir: directory to save models
            Returns:
                list of file names for models
        '''
        
        models_dict = {}
        for (class_,solver_id),model in models.items():
            file_name = os.path.join(model_dir, '%d_%d.model' %(class_,solver_id))
            models_dict[file_name] = model
            
        class_file_name = os.path.join(model_dir, 'class.model')
        models_dict[class_file_name] = class_model
        return models_dict                 
    
    def __compose_config_dic(self, files, f_indicator, conf_dic, model_dir):
        '''
            collect all necessary information in dictionary for a config file
        '''
        
        selector_dic = {
                         "approach": {
                                     "approach" : "regression",
                                     "models" : files
                                     },
                        "normalization": {
                                          "filter" : f_indicator, 
                                          },
                        "configurations":{}
                        }
        
        selector_dic["configurations"].update(conf_dic)
        return selector_dic