'''
Created on Feb, 2013

@author: manju
'''

import os
import math
import abc

from trainer.selection.selector import SelectorTrainer
from misc.printer import Printer

class ClassifierVoter(SelectorTrainer):
    '''
       trainer with pairwise comparison classification models
    '''


    def __init__(self, save_models=True):
        '''
        Constructor
        '''
        SelectorTrainer.__init__(self, save_models)
        self._UNKNOWN_CODE = -512
        self._CACHE_SIZE = 1000 # memory size of libsvm
                       
    def train(self, instance_dic, solver_list, config_dic, cutoff,
              model_dir, f_indicator, n_feats):
        '''
            train models for flexfolio 
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
        
        # pairwise weighted svm learning
        models = self.__collect_and_train_data(instance_dic, n_solver, cutoff)

        if self._save_models:
            # save models
            files = self.__save_models(models, model_dir)
        else:
            files = self.__collect_models(models, model_dir)
        
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
            collects all necessary data for a pairwise comparison
            and trains pairwise classification models
            Args:
                instance_dic : instance name -> Instance()
                n_solver: number of solvers
                cutoff: cutoff time (int)
            Returns:
                models: (solver i, solver j) -> Model()
        '''
        models = {}
        # ensure same order of instances independently of memory allocation
        inst_keys = sorted(instance_dic.keys())
        for i in range(0,n_solver):
            for j in range(i+1,n_solver):
                # collect labels
                feats = []
                labels = []
                weights = []
                for inst_name in inst_keys:
                    inst = instance_dic[inst_name]
                    if inst._pre_solved:
                        continue
                    f = inst._normed_features
                    y_i = inst._transformed_cost_vec[i]
                    y_j = inst._transformed_cost_vec[j]
                    if (y_i >= cutoff and y_j >= cutoff): # useless if both solver have timeout
                        continue
                    if (y_i == self._UNKNOWN_CODE or y_j == self._UNKNOWN_CODE): # one of the solvers has an unkown runtime, comparison not possible
                        continue
                    else: 
                        feats.append(f)
                        # penalize timouts
                        if y_i >= cutoff:
                            y_i *= 10 
                        if y_j >= cutoff:
                            y_j *= 10 
                        penalized_weight = inst._weight 
                        weights.append(math.fabs(y_i - y_j) * penalized_weight)
                        if y_i > y_j:
                            labels.append(1)
                        else:
                            labels.append(0)
                # train model
                if not labels:
                    Printer.print_w("At least one pair of solvers never solved an instance. Use --contr-filter 0.00001 to filter them out.")
                    model = -1 # not applicable -> not used later on at voting
                else: 
                    model = self._train(labels, feats, weights)
                
                models[(i,j)] = model
        return models
    
    #@abc.abstractmethod
    def _train(self, y, X, weights):
        '''
            trains the actual model
            dummy implementation - override in subclasses
        '''
        return
        
    
    def __save_models(self, models, model_dir):
        '''
            save models to files
            Args:
                models: (solver i, solver j) -> Model()
                model_dir: directory to save models
            Returns:
                list of file names for models
        '''
        from sklearn.externals import joblib
        
        files = []
        for (i,j),model in models.items():
            file_name = os.path.join(model_dir, '%d_%d.model' %(i,j))
            joblib.dump(model, file_name, compress=9)
            files.append(file_name)
        return files
    
    def __collect_models(self, models, model_dir):
        '''
            collect models in a dictionary (theoretical file name -> model)
            Args:
                models: (solver i, solver j) -> Model()
                model_dir: directory to save models
            Returns:
                dict: theoretical file name -> model
        '''
        models_dict = {}
        for (i,j),model in models.items():
            file_name = os.path.join(model_dir, '%d_%d.model' %(i,j))
            models_dict[file_name] = model
        return models_dict
                
    def __compose_config_dic(self, files, f_indicator, conf_dic, model_dir):
        '''
            collect all necessary information in dictionary for a config file
        '''
        
        selector_dic = {
                        "approach": {
                                     "approach" : "classvoter",
                                     "models" : files
                                     },
                        "normalization": {
                                          "filter" : f_indicator, 
                                          },
                        "configurations":{}
                        }
        
        selector_dic["configurations"].update(conf_dic)
        return selector_dic