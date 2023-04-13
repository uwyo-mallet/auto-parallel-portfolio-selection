'''
Created on Nov 9, 2012

@author: manju
'''

import random
import copy
import json

from misc.printer import Printer
#from misc.updater import Updater
from trainer.evalutor.validator import Validator, Stats
from trainer.evalutor.plotter import Plotter

class CrossValidator(Validator):
    '''
        perform cross validation evaluation
    '''

    def __init__(self, update_sup, print_file):
        '''
        Constructor
        '''
        Validator.__init__(self, update_sup, print_file)
        self._instance_parts = []
        self._n_folds = 10

    def evaluate(self, trainer, meta_info, instance_train_dic, config_dic, threads=1):
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
        
        instance_train_dic = self._get_cross_fold(instance_train_dic, meta_info.options.cv_repetition) 
        
        self._aspeed_opt = meta_info.options.aspeed_opt
        
        self._MAX_THREADS = min(self._MAX_THREADS, len(meta_info.algorithms))
        stats = Stats(self._MAX_THREADS, meta_info.algorithms)
        
        for iteration in range(0, self._n_folds):
            Printer.print_c(">>> %d-th iteration<<<" %(iteration + 1))
            if self._n_folds > 1:
                instance_train = self.__get_train_nth_fold(iteration)
                instance_test = self._instance_parts[iteration]
            else:
                Printer.print_w("NO TRAINING TEST SPLIT!")
                instance_train = instance_train_dic
                instance_test =  instance_train_dic
            
            #TRAINING
            selection_dic, solver_schedule = self.training(instance_train, meta_info, config_dic, trainer)

            # TEST / EVALUATION
            self.testing(instance_test, meta_info, selection_dic, solver_schedule, stats)
            
            #oracle_avg_time, oracle_spend_time_dict, oracle_par10, oracle_dict, oracle_tos = \
            #self._oracle_performance(instance_test, solver_list, meta_info.algorithm_cutoff_time)
            #stats.print_stats(oracle_avg_time, oracle_spend_time_dict, oracle_par10, oracle_tos, meta_info.algorithm_cutoff_time)
            
        oracle_avg_time, oracle_spend_time_dict, oracle_par10, oracle_dict, oracle_tos = \
            self._oracle_performance(instance_train_dic, solver_list, meta_info.algorithm_cutoff_time, stats)
        
        if meta_info.performance_type[0].upper() == "RUNTIME":
            stats.print_runtime_stats(oracle_avg_time, oracle_spend_time_dict, oracle_par10, oracle_tos, meta_info.algorithm_cutoff_time)
        else:
            stats.print_qual_stats(oracle_avg_time, maximize=meta_info.maximize[0])
        
        if self._print_file:
            self._write_csv_runtimes(self._print_file, instance_train_dic, stats.inst_par10_dict[threads], solver_list)
        
        args_ = meta_info.options
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
        
        return stats.thread_par10_dic[threads], stats.inst_par10_dict[threads]

    def _get_cross_fold(self, instance_dic, rep=None):
        '''
            split the available data in __n_folds parts to perform later a cross fold validation;
        '''
        l = len(instance_dic)
        index = 0
        self._instance_parts = []
        parted_inst_dic = {}
        threshold = l / self._n_folds
        partIndex = 1
        instsList = sorted(instance_dic.keys())
        while instsList != []:
            randIndex = random.randint(0, len(instsList)-1)
            inst = instsList.pop(randIndex)
            
            if (index >= threshold): # if the fold full?
                self._instance_parts.append(parted_inst_dic)
                parted_inst_dic = {}
                l = l - index
                threshold = l / (self._n_folds - partIndex)
                partIndex += 1
                index = 0
                
            index += 1
            parted_inst_dic[inst] = instance_dic[inst]
        self._instance_parts.append(parted_inst_dic)
        return instance_dic
        
    def __get_train_nth_fold(self,n):
        '''
            returns the n-th training fold for the cross validation
            uses: __times_parts, self.__feature_parts, self.__status_parts
            Args:
                n : index of fold
            Returns:
                dictionary with instances
        '''
        instance_train = {}
        for i in range(0,self._n_folds):
            if (n == i):
                continue
            instance_train.update(copy.deepcopy(self._instance_parts[i]))
        return instance_train

    
