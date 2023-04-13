'''
Created on Nov 9, 2012

@author: manju
'''
from trainer.selection.selector import SelectorTrainer
import os

class NearestNeighbourTrainer(SelectorTrainer):
    '''
        trainer for nearest neighbour classification
    '''


    def __init__(self,save_models=True):
        '''
            Constructor
        '''
        SelectorTrainer.__init__(self, save_models)
        self._cutoff = 900
        self._norm_approach = "Zscore"
        
        self._UNKNOWN_CODE = -512
   
    def __repr__(self):
        return "NN"
   
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
        
        inst_solver_dic = self.__find_best_solver(instance_dic, solver_list, cutoff)
        model_name = self.__write_arff(instance_dic, inst_solver_dic, solver_list, model_dir, n_feats)
        
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
                                "approach" : "NN",
                                "model" : model_name
                                },
                   "normalization" : {
                                      "filter"  : f_indicator                           
                                 },
                   "configurations":conf_dic                        
                   }
        return sel_dic
        
        
    def __find_best_solver(self, instance_dic, solver_list, cutoff):
        '''
            matches instance name with best performing solver
            Args:
                instance_dic: instance name -> Instance()
                solver_list: list of solver names
                cutoff: runtime cutoff
        '''
        
        inst_solver_dic = {}
        
        def filter_unknown(x): return x != self._UNKNOWN_CODE and x < cutoff
        
        for name,instance in instance_dic.items():
            if instance._pre_solved:
                continue
            times = instance._transformed_cost_vec
            times_filt = filter(filter_unknown, times) # filter all unknown runtimes and runtimes equal or larger than cutoff
            if times_filt == []: 
                continue
            best_time = min(times_filt)
            solver_index = times.index(best_time)
            best_solver = solver_list[solver_index]
            inst_solver_dic[name] = best_solver
            
        return inst_solver_dic
    
        
    
    def __write_arff(self,instance_dic, inst_solver_dic, solver_list, model_dir, n_feats):
        '''
            write nn models as arff files to be compatible with ME-ASP
        '''
        model_name = os.path.join(model_dir,"model_nn.arff")
        fp = open(model_name,"w")
        
        fp.write("@relation dataset-weka.filters.unsupervised.attribute.Remove-R1\n\n")
        
        for i in range(0,n_feats):
            fp.write("@attribute feature_%d numeric\n" % (i))
        
        fp.write("@attribute weight numeric\n")
        fp.write("@attribute class {%s}\n\n" % (",".join(solver_list)))
        
        fp.write("@data\n")
        for instance,solver in inst_solver_dic.items():
            if instance_dic[instance]._pre_solved:
                continue
            fp.write("%s,%f,%s\n" % (",".join(map(str,instance_dic[instance]._normed_features)), instance_dic[instance]._weight, solver))
        
        fp.close()
        
        return model_name 
    
    