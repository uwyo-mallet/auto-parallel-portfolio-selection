'''
Created on Nov 9, 2012

@author: manju
'''
from trainer.selection.selector import SelectorTrainer

class SBSTrainer(SelectorTrainer):
    '''
        always select the best solver
        TODO: Change Name of class, misleading!
    '''


    def __init__(self, save_models=True):
        ''' 
            Constructor
        '''
        SelectorTrainer.__init__(self, save_models)
        self._cutoff = 900
        self._norm_approach = "Zscore"
        
        self._UNKNOWN_CODE = -512
        
    def __repr__(self):
        return "SBS"        
   
    def train(self, instance_dic, solver_list, config_dic, cutoff, model_dir, f_indicator, n_feats):
        '''
            train model
            Args:
                instance_dic: instance name -> Instance()
                solver_list: list of solvers
                cutoff: runtime cutoff
                model_dir: directory to save model
                f_indicator: of used features
                n_feats: number of features
        '''
        
        self._cutoff = cutoff
        
        sorted_solvers = self.__find_best_solver(instance_dic, solver_list, cutoff)
        
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
                                "approach" : "Majority",
                                "solver" : sorted_solvers
                                },
                   "normalization" : {
                                      "filter"  : f_indicator                           
                                 },
                   "configurations":conf_dic                        
                   }
        return sel_dic
        
        
    def __find_best_solver(self, instance_dic, solver_list, cutoff):
        '''
            finds best solver over all instances (majority voting)
            Args:
                instance_dic: instance name -> Instance()
                solver_list: list of solver names
                cutoff: runtime cutoff
        '''
        
        par10_solver_list = [0]*len(solver_list)
        known_times_list = [0]*len(solver_list)
        
        #sum up all knwon runtimes
        for instance in instance_dic.values():
#            if instance._pre_solved:
#                continue
            times = instance._transformed_cost_vec
            solver_index = 0
            for t in times:
                if t != self._UNKNOWN_CODE:
                    if t >= cutoff:
                        par10_solver_list[solver_index] += cutoff * 10
                    else:
                        par10_solver_list[solver_index] += t
                    known_times_list[solver_index] += 1
                solver_index += 1
                
        #average runtime
        par10_solver_list = map(lambda (x,y): x/y ,zip(par10_solver_list,known_times_list))
        par10_solver_dict = dict(zip(par10_solver_list, solver_list))

        sorted_solvers = []
        while par10_solver_list:
            min_time = min(par10_solver_list)
            sorted_solvers.append(par10_solver_dict[min_time])
            par10_solver_list.remove(min_time)
                    
        return sorted_solvers
