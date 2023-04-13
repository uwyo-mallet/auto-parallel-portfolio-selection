'''
Created on Mai 30, 2014

@author: manju
'''

import random
import copy
import json

from misc.printer import Printer
#from misc.updater import Updater
from trainer.evalutor.validator import Validator, Stats
from trainer.evalutor.plotter import Plotter

class TrainTestValidator(Validator):
    '''
        perform cross validation evaluation
    '''

    def __init__(self, update_sup, print_file):
        '''
        Constructor
        '''
        Validator.__init__(self, update_sup, print_file)

    def evaluate(self, trainer, meta_info, instance_train_dic, config_dic):
        '''
            cross fold evaluation
            Parameter:
                trainer : Trainer object
                args_: command line arguments parsed via argparse
                instance_train_dic : instance name -> Instance()
                config_dic : solver alias -> command line
            Returns
                dictionary with all generated files and meta informations
                inst_par10_dict: flexfolio performance : instance name -> par10 runtime
        '''
        seed = meta_info.options.seed
        folds = meta_info.options.crossfold
        solver_list = meta_info.algorithms
        
        random.seed(seed)
        
        self._n_folds = folds
        
        self._aspeed_opt = meta_info.options.aspeed_opt
        
        stats = Stats(self._MAX_THREADS, meta_info.algorithms)
        
        instance_train, instance_test = self.__get_test_train(instance_train_dic, meta_info.options.train_set, meta_info.options.test_set)
        Printer.print_c("Size Training Set: %d" %(len(instance_train)))
        Printer.print_c("Size Test Set: %d" %(len(instance_test)))
            
        #TRAINING
        selection_dic, solver_schedule = self.training(instance_train, meta_info, config_dic, trainer)

        # TEST / EVALUATION
        self.testing(instance_test, meta_info, selection_dic, solver_schedule, stats)
            
        oracle_avg_time, oracle_spend_time_dict, oracle_par10, oracle_dict, oracle_tos = \
            self._oracle_performance(instance_test, solver_list, meta_info.algorithm_cutoff_time)
        
        if meta_info.performance_type[0].upper() == "RUNTIME":
            stats.print_runtime_stats(oracle_avg_time, oracle_spend_time_dict, oracle_par10, oracle_tos, meta_info.algorithm_cutoff_time)
        else:
            stats.print_qual_stats(oracle_avg_time, maximize=meta_info.maximize[0])
        
        if self._print_file:
            self._write_csv_runtimes(self._print_file, instance_test, stats.inst_par10_dict[1], solver_list)
        
        args_ = meta_info.options
        
        if args_.smac:
            par10 = stats.thread_par10_dic[1]
            if meta_info.performance_type[0].upper() == "RUNTIME":
                cut = meta_info.algorithm_cutoff_time
                par10_wo_unsolvable = (par10*len(instance_test) - cut*10*oracle_tos) # without average normalization
            else:
                par10_wo_unsolvable = par10
            print("Result for SMAC: %f" %(par10_wo_unsolvable))
        
        if args_.table_format:
            name = args_.approach
            if args_.approach == "REGRESSION":
                name += "-"+args_.regressor
            if args_.approach == "CLASSVOTER":
                name += "-"+args_.classifier
            if args_.approach == "CLASSMULTI":
                name += "-"+args_.classifiermulti
            if args_.approach == "CLUSTERING":
                name += "-"+args_.cluster_algo       
            # SET & Approach & Normalization & contr.-filter & weigthing  & aspeed-opt & PAR1 & PAR10 & TO & RMSE & oralce
            print("SET & FEATURES & Approach & Normalization & contr.-filter & weigthing  & aspeed-opt & PAR1 & PAR10 & TO & RMSE & oralce")
            print("%s & %s & %s & %s & %.2f & %r & %r & %.2f & %.2f & %d & %.2f & %.2f" %(
                                                            args_.times, args_.feats, name, args_.norm, args_.contributor_filter,
                                                            args_.approx_weights, 
                                                            args_.aspeed_opt,
                                                            stats.thread_avg_dic[1],
                                                            stats.thread_par10_dic[1],
                                                            stats.thread_timeout_dic[1],
                                                            stats.thread_rmse_dic[1],
                                                            oracle_avg_time
                                                            ))
        
        if args_.plot_mt:
            plotter = Plotter()
            plotter.plot_mulithreading(stats.thread_par10_dic, oracle_avg_time, args_.times, "PAR10")
            plotter.plot_spend_times(stats.spend_time, oracle_spend_time_dict, args_.times)
        
        if args_.sigtest_threads:
            sig_dict = {}
            instances = oracle_dict.keys()
            for name, inst_perf_dict in stats.inst_par10_dict.items():
                if len(inst_perf_dict) > stats.presolved:
                    sig_dict[name] = [inst_perf_dict[inst_] for inst_ in instances] # throw away instane names
            par10_dict = dict((name, sum(par10)/len(par10)) for name, par10 in sig_dict.items())
            Printer.print_c("PAR10 without unsolvable: %s" %(json.dumps(par10_dict)))
            self.make_sig_test(sig_dict)
        
        return stats.thread_par10_dic[1], stats.inst_par10_dict[1]

        
    def __get_test_train(self,instance_dict, train_tuples, test_tuples):
        '''
            returns the n-th training fold for the cross validation
            uses: __times_parts, self.__feature_parts, self.__status_parts
            Args:
                instance_dict : name -> Instance()
                train_tuples: (#rep,#fold),(#rep,#fold)... 
            Returns:
                two dictionary with training and test instances
        '''
        test_set = {}
        train_set = {}
        for name, inst_ in instance_dict.items():
            for (rep,fold) in train_tuples:
                if inst_._fold[rep] == fold:
                    train_set[name] = inst_
                    break
            for (rep,fold) in test_tuples:
                if inst_._fold[rep] == fold:
                    test_set[name] = inst_
                    break
        # check whether these sets are disjunct
        trains = set(train_set.keys())
        tests = set(test_set.keys())
        if trains.intersection(tests):
            Printer.print_w("Training and Test set are not disjunct.")
                
        return train_set, test_set
            
                    
            


    
