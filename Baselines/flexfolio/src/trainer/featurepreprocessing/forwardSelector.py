'''
Created on Nov 20, 2012

@author: manju
'''
import sys
import random

from misc.printer import Printer
from trainer.evalutor.crossValidator import CrossValidator


class ForwardSelector(object):
    '''
        selects a subset of features wrt to a minimized crossfold performances
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.__FOLDS = 3
        self.__THRESHOLD_IMPROVEMENT = 10 # do not use floats!

        self.__instance_dic = None        
        self.__meta_info = None
        self.__trainer = None
        self.__solver_list = None
        self.__config_dic = None
        
    
    def select_features(self, trainer, instance_dic, feature_indicator_in, config_dic, meta_info):
        '''
            selects features and returns a new dictionary of features
            Args:
                trainer: Trainer()
                instance_dic: name -> Instance()
                feature_indicator_in: list \in {-1,0,1}
                config_dic: solver name -> solver call
                meta_info: meta information 
            Returns:
                list of {-1,0,1}: 0 -> set feature to 0, 1 -> use feature
                (e.g. [1,1,0,1]: features at position 0,1,3 are used, 
                feature at position 2 is set to 0 for all instances)

        '''
        
        seed = meta_info.options.seed
        solver_list = meta_info.algorithms
        args_ = meta_info.options
        
        self.__trainer = trainer
        self.__instance_dic = instance_dic
        self.__solver_list = solver_list
        self.__config_dic = config_dic
        self.__meta_info = meta_info
        
        Printer.print_c("\n>>> Running Feature Selection! <<<\n")
        
        
        best_feature_indicator = None
        best_performance = sys.maxint
        
        for _ in range(0,args_.feat_sel_restarts):
        
            n_feats = len(meta_info.features)
            if args_.feat_sel == "forward":
                feature_indicator = [0]*n_feats
                forward = True
            elif args_.feat_sel == "backward":
                feature_indicator = [1]*n_feats
                forward = False
            elif args_.feat_sel == "random":
                feature_indicator = [0]*n_feats
                feature_indicator.extend([1]*n_feats)
                feature_indicator = random.sample(feature_indicator,n_feats)
                if sum(feature_indicator) > n_feats/2:
                    forward = False
                else:
                    forward = True
                    
            #override indicators of features without variance
            feature_indicator = map(lambda (x,y): -1 if x==-1 else y, zip(feature_indicator_in, feature_indicator))
            
            Printer.print_c("Initial Feature Distribution:")
            Printer.print_c(" ".join(map(str,feature_indicator)))
            
            evaluator = CrossValidator(args_.update_sup, None)
            performance = sys.maxint
            new_performance = sys.maxint - self.__THRESHOLD_IMPROVEMENT
            while performance - new_performance >= self.__THRESHOLD_IMPROVEMENT:
                performance = new_performance
                feature_indicator, new_performance = self.__feature_selection(feature_indicator, new_performance, n_feats, evaluator, foward=forward)
                feature_indicator, new_performance = self.__feature_selection(feature_indicator, new_performance, n_feats, evaluator, foward=(not forward))
            
            if new_performance < best_performance:
                best_feature_indicator = feature_indicator
                selected_features = filter(lambda x,y: True if y else False, zip(best_feature_indicator, meta_info.features))
                Printer.print_c("Selected: %s" %(selected_features))
            
        return best_feature_indicator
        
    def __feature_selection(self, feature_indicator, performance, n_feats, evaluator, foward):
        ''' feature selection_
            Args:
                feature_indicator : start list of feature indictators
                performance: performance of current feature_indicators
                n_feats: number of features
                evaluator: CrossValidator() object
                foward: Boolean (True: Forward Selection, False: Backward Elimination)
        '''
        self.__meta_info.options.feat_sel = False
        if foward:
            Printer.print_c(">>> Forward Selection<<<\n")
        else:
            Printer.print_c(">>> Backward Elimination<<<\n")
        
        for index in range(0, n_feats):
            if feature_indicator[index] == int(not foward):
                feature_indicator[index] = int(foward)
                        
                Printer.disable_printing = False        
                Printer.print_c("Examine Feature %d" % (index))
                Printer.disable_printing = True
                    
                self.__meta_info.options.feature_indicator = feature_indicator
                
                performance2, cf_inst_par10 = \
                        evaluator.evaluate(self.__trainer, self.__meta_info, self.__instance_dic, self.__config_dic)
                
                Printer.disable_printing = False      
                Printer.print_c(" -> Performance: %f" % (performance2))
                    
                if performance2 < performance:
                    performance = performance2            
                    Printer.print_c(" -> permanent changing Feature %d" % (index))        
                else:
                    feature_indicator[index] = int(not foward)

        Printer.print_c("Performance after selection: %s" %(performance))
        Printer.print_c("Selected Features:")
        Printer.print_c(" ".join(map(str,feature_indicator)))
        
        self.__meta_info.options.feature_indicatorr = None
        self.__meta_info.options.feat_sel = True
        return feature_indicator, performance
        
