'''
Created on Mar 27, 2013

@author: manju
'''

import os

from trainer.selection.selector import SelectorTrainer

import sys

class ClassifierMulti(SelectorTrainer):
    '''
       trainer with multiclass svm models
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
            train models for flexfolio based on multi class classifcation models of libsvm
            Args:
                instance_dic: instance name -> Instance()
                solver_list: list of solver names
                config_dic: solver name -> call
                norm_approach: normalization approach 
                cutoff: runtime captime
                model_dir: directory to save trained models
                f_indicator: indicates the use of features or set them to
            Return:
                dictionary with all meta information to use models
        '''
        
        self._cutoff = cutoff
        
        n_solver = len(solver_list)
        
        # multiclass svm learning
        model = self.__collect_and_train_data(instance_dic, n_solver, cutoff)
        if self._save_models:
            # save models
            files = self.__save_model(model, model_dir)
        else:
            files = self.__collect_model(model, model_dir)
        
        conf_dic = {}
        for solver in range(0,n_solver):
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
            collects all necessary data for multiclass classification
            and trains pairwise svm models
            Args:
                instance_dic : instance name -> Instance()
                n_solver: number of solvers
                cutoff: cutoff time (int)
            Returns:
                models: (solver i, solver j) -> Model()
        '''
        def replace_unknown(y): y = sys.maxint if y==self._UNKNOWN_CODE else y; return y
        
        feats = []
        labels = []
        weights = []
        # ensure same order of instances independently of memory allocation
        inst_keys = sorted(instance_dic.keys())
        for inst_name in inst_keys:
            inst  = instance_dic[inst_name]
            if inst._pre_solved:
                continue
            f = inst._normed_features
            runtimes = inst._transformed_cost_vec
            weight = inst._weight
            min_runtime = reduce(lambda x,y: min(x,replace_unknown(y)), runtimes)
            if min_runtime >= cutoff: # no information in instances with only timeouts
                continue
            best_solver_index = runtimes.index(min_runtime)
            labels.append(best_solver_index)
            feats.append(f)
            weights.append(weight)
        
        model = self._train(labels, feats, weights)
        return model
    
    #@abc.abstractmethod
    def _train(self, y, X, weights):
        '''
            trains the actual model
            dummy implementation - override in subclasses
        '''
        return
    
    def __save_model(self, model, model_dir):
        '''
            save model to files
            Args:
                models: (solver i, solver j) -> Model()
                model_dir: directory to save models
            Returns:
                list of file names for models
        '''
        from sklearn.externals import joblib
        
        files = []
        file_name = os.path.join(model_dir, 'multiclass.model')
        joblib.dump(model, file_name, compress=9)
        files.append(file_name)
        return files
    
    def __collect_model(self, model, model_dir):
        '''
            collect models in a dictionary 
            Args:
                models: Model()
                model_dir: directory to save models
            Returns:
                dict: theoretical file  name -> model
        '''
        
        model_dict = {}
        file_name = os.path.join(model_dir, 'multiclass.model')
        model_dict[file_name] = model
        return model_dict
                        
    def __compose_config_dic(self, files, f_indicator, conf_dic, model_dir):
        '''
            collect all necessary information in dictionary for a config file
        '''
        
        selector_dic = {
                        "approach": {
                                     "approach" : "classmulti",
                                     "models" : files
                                     },
                        "normalization": {
                                          "filter" : f_indicator, 
                                          },
                        "configurations":{}
                        }
        
        
        selector_dic["configurations"].update(conf_dic)
        return selector_dic