'''
Created on Nov 9, 2012

@author: manju
'''
import os
import sys

from trainer.selection.selector import SelectorTrainer
from trainer.evalutor.crossValidator import CrossValidator
from misc.printer import Printer

class KNNTrainer(SelectorTrainer):
    '''
        trainer for k-nearest neighbour classification
         %TODO: Further techniques to improve performance is weighting and clustering
        in S. Kadioglu, Y. Malitsky, A. Sabharwal, H. Samulowitz and M. Sellmann. Algorithm Selection and Scheduling
    '''


    def __init__(self, k=-1, save_models=True):
        '''
            Constructor
        '''
        SelectorTrainer.__init__(self, save_models)
        self._cutoff = 900
        self._norm_approach = "Zscore"
        
        self.k = k
        
        self._UNKNOWN_CODE = -512
        self._MAX_K = 32
   
    def __repr__(self):
        return "k-NN"
   
    def train(self, instance_dic, solver_list, config_dic, cutoff, model_dir, f_indicator, n_feats, 
                meta_info, trainer):
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
        
        if self.k == -1:
            self.k = self.__guessK(meta_info, instance_dic, trainer, config_dic)
        
        Printer.print_nearly_verbose("Chosen k: %d" %(self.k))
        
        if self._save_models:
            model_name = self.__write_arff(instance_dic, solver_list, model_dir, n_feats)
        else:
            model_name = self.__create_save(instance_dic)
        
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
                                "model" : model_name
                                },
                   "normalization" : {
                                      "filter"  : f_indicator                           
                                 },
                   "configurations":conf_dic                        
                   }
        return sel_dic
    
    def __guessK(self, meta_info, instance_dic, trainer, config_dic):
        '''
            guess k on PAR10 by cross validation
        '''
        evaluator = CrossValidator(meta_info.options.update_sup, None)
        
        k = 1
        best_par10 = sys.maxint
        best_k = 1
        while k <= self._MAX_K and k < len(instance_dic):
            meta_info.options.knn = k
            Printer.disable_printing = True
            par10, _ = evaluator.evaluate(trainer, meta_info, instance_dic, config_dic)
            Printer.disable_printing = False
            Printer.print_nearly_verbose("k: %d \t par10: %f" %(k, par10))
            if best_par10 > par10:
                best_par10 = par10
                best_k = k
            k *= 2
        return best_k
        
    def __write_arff(self, instance_dic, solver_list, model_dir, n_feats):
        '''
            write nn models as arff files
        '''
        model_name = os.path.join(model_dir,"model_knn.arff")
        fp = open(model_name,"w")
        
        fp.write("@relation knn set\n\n")
        
        for i in range(0,n_feats):
            fp.write("@attribute feature_%d numeric\n" % (i))
        
        fp.write("@attribute weight numeric\n")
        
        for s in solver_list:
            fp.write("@attribute %s NUMERIC\n" % (s))
        
        fp.write("@data\n")
        for inst_ in instance_dic.values():
            if inst_._pre_solved:
                continue
            fp.write("%s,%f,%s\n" % (",".join(map(str,inst_._normed_features)), inst_._weight, (",".join(map(str,inst_._transformed_cost_vec)))))
        fp.close()
        
        return model_name 
    
    def __create_save(self, instance_dic):
        save_list =  []
        
        for inst_ in instance_dic.values():
            if inst_._pre_solved:
                continue
            point = {"features" : inst_._normed_features,
                     "weight" : inst_._weight,
                     "perfs" : inst_._transformed_cost_vec
                     }
            save_list.append(point)
            
        return save_list
        
        
        
    
    