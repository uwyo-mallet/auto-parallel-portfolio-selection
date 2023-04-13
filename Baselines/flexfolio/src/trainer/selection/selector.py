'''
Created on Nov 8, 2012

@author: manju
'''
from abc import ABCMeta, abstractmethod


class SelectorTrainer(object):
    '''
     abstract class to train models for flexfolio
    '''
    __metaclass__ = ABCMeta

    def __init__(self, save_models=True):
        '''
        Constructor
        '''
        
        self._norm_approach = None
        self._cutoff = None
        self._save_models = save_models
        
    
    def set_backup_solver(self, selection_dic, ranks):
        '''
            set flag for backup solver in selection dic
            Args:
                selection_dic : dictionary with meta informations
        '''
        for solver_dic in selection_dic["configurations"].values():
            solver_dic["backup"] = ranks[int(solver_dic["id"])]
        return selection_dic
        
        
    @abstractmethod
    def train(self, instance_dic, solver_list, config_dic, cutoff, model_dir, f_indicator):
        '''
            abstract method for training
            Parameter:
                instance_dic : name -> Instance() 
                solver_list: list of solver names (alignment important!)
                cutoff: runtime cutoff
                model_dir: directory to save trained models
                f_indicator: indicator list to set features to 0
        '''
