'''
Created on Nov 9, 2012

@author: manju
'''
import random
import copy
import traceback

from trainer.selection.selector import SelectorTrainer
from misc.printer import Printer
from tempfile import mkdtemp
import json
import math


class Ensemble(SelectorTrainer):
    '''
        trainer for nearest neighbour classification
    '''


    def __init__(self, subsample_size=0.7, num_models=[0,3,0,0,3,3], bootstrapping=True, ensemble_mfeatures=0.9, save_models=True):
        '''
            Constructor
            Args:
                subsample_size: fraction of original data size used for training
                num_models: number of trained models for <REGRESSION>,<CLASSVOTER>,<CLASSMULTI>,<NN>,<KMEANS>
        '''
        SelectorTrainer.__init__(self, save_models)
        self.__subsample_size = subsample_size # fraction of original data size
        self.__num_models = num_models #

        trainer_names = ["REGRESSION","CLASSVOTER","CLASSMULTI","NN","kNN","CLUSTERING"]
        self._num_trainer = zip(trainer_names, num_models)
        
        self.__bootstraping = bootstrapping
        
        self._n_sample_features = ensemble_mfeatures
    
    def __repr__(self):
        return "ENSEMBLE"
   
    def train(self, instance_dic, solver_list, config_dic, cutoff, model_dir, f_indicator, n_feats, dict_of_trainer, meta_info, trainer):
        '''
            train model
            Args:
                instance_dic: instance name -> Instance()
                solver_list: list of solvers
                cutoff: runtime cutoff
                model_dir: directory to save model
                f_indicator: of used features
                n_feats: number of features
                dict_of_trainer: dictionary of trainer (/selector) 
                meta_info : meta_info of selection task (including args_)
                trainer: pointer to main_train.Trainer() to recall the train procedure
        '''
        
        name_approach_dict = {}
        
        for trainer_name, num_models in self._num_trainer:
            if num_models > 0:
                n_a_dict, _ = self._train_on_subset(trainer_name,
                                                          num_models, 
                                                          instance_dic, 
                                                          solver_list, 
                                                          config_dic, 
                                                          model_dir, 
                                                          f_indicator,
                                                          meta_info,
                                                          trainer)
                if n_a_dict is not None:
                    name_approach_dict.update(n_a_dict)
        if not name_approach_dict:
            Printer.print_w("No model were trained for all approaches.")
                
        conf_dic = {}
        for solver,cmd in config_dic.items():
            solver_dic = {
                          "call": cmd,                  
                          "id" : solver_list.index(str(solver))          
                          }
            conf_dic[solver] = solver_dic
        sel_dic = {
                   "approach": {
                                "approach"   : "ENSEMBLE",
                                "trainer"    : name_approach_dict,
                                "base"       : meta_info.options.ensemble_base,
                                "Q"          : meta_info.options.ensemble_q
                                },
                   "normalization" : {
                                      "filter"  : f_indicator                           
                                 },
                   "configurations":conf_dic                        
                   }
        return sel_dic


    def _train_on_subset(self, trainer_name, num_models, instance_dic, solver_list, 
                         config_dic, model_dir, f_indicator, meta_info, trainer):
        '''
            train given ml approach "trainer" on a subset of the given instances in "instance_dic" 
            and the remaining given parameters
            Args:
                trainer_name: name of the selection approach
                num_models: number of trained models
                instance_dic: instance name -> Instance()
                solver_list: list of solvers
                model_dir: directory to save model
                f_indicator: of used features
        '''
        name_approach_dict = {}
        for i in range(0,num_models):
            subset = self._subsample_instances(instance_dic)
            model_dir_tmp = mkdtemp(dir=model_dir)

            # adjust arguments
            meta_info_copy = copy.deepcopy(meta_info)
            args_copy = meta_info_copy.options
            args_copy.approach = trainer_name
            args_copy.model_dir = model_dir_tmp
            args_copy.contributor_filter = 0 # no further contribution filtering
            args_copy.approx_weights = False # no reweighting
            args_copy.feat_sel = False # no feature selection a second time
            args_copy.aspeed_opt = False # no recursion in aspeed scheduling
            sub_f_indicator = self._deactivate_sampled_features(f_indicator)
            try:
                # create a Trainer object
                sel_dic = trainer.train(meta_info_copy, subset, config_dic, sub_f_indicator, self._save_models, recursive=True)
                sub_dic = sel_dic
                del sub_dic["configurations"]
                name_approach_dict[trainer_name+"-"+str(i)] = sub_dic
            except:
                traceback.print_exc()
                Printer.print_w("Skip model training because of exception!")
                
        if not name_approach_dict:
            Printer.print_w("No model were trained.")
            return None, None
                
        return name_approach_dict, sel_dic
    
    def _subsample_instances(self, instance_dic):
        '''
            sample a subset of instances for training (with replacement)
            Args:
                instance_dic: instance name -> instance()
            Returns:
                subset: instance name -> instance() (subset of instances of instance_dic)
        '''
        n_data = len(instance_dic)
        instance_names = list(instance_dic.keys())
        n_samples = int(n_data * self.__subsample_size)
        
        subset = {}
        removed = 1
        for indx in range(0,n_samples):
            rand_index = random.randint(0,n_data-removed)
            sampled_instance_name = instance_names[rand_index]
            sampled_instances = copy.deepcopy(instance_dic[sampled_instance_name])
            new_name = sampled_instance_name +"-"+str(indx)
            sampled_instances._name = new_name
            subset[new_name] = sampled_instances
            
            if not self.__bootstraping:
                removed += 1
                instance_names.pop(rand_index)
                
        return subset
    
    def _deactivate_sampled_features(self, f_indicator):
        '''
            reduce the number the number of active feature according to self._sample_features
        '''
        import numpy as np
        changeables_indx = np.where(np.array(f_indicator) == 1)[0].tolist()
        n_chan = len(changeables_indx)
        n_samples = n_chan - int(n_chan * self._n_sample_features)
        f_indicator = copy.deepcopy(f_indicator)
        to_deactivate = random.sample(changeables_indx,n_samples)
        for to_deact in to_deactivate:
            f_indicator[to_deact] = 0
        #print(f_indicator)
        return f_indicator
        
        
