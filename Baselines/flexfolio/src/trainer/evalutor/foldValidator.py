'''
Created on Nov 9, 2012

@author: manju
'''

import json
import os
import random
import math

from misc.printer import Printer
#from misc.updater import Updater
from trainer.evalutor.validator import Validator
from trainer.evalutor.plotter import Plotter

class FoldValidator(Validator):
    '''
        DEPRECATED
        performs only one fold of a cross validation evaluation
        needed for tuning with SMAC
    '''


    def __init__(self, update_sup, print_file):
        '''
        Constructor
        '''
        Validator.__init__(self, update_sup, print_file)
        self.__instance_parts = []
        self.__n_folds = 10

    def evaluate(self, trainer, args_, folds, instance_train_dic, solver_list, config_dic, seed):
        '''
            cross fold evaluation
            Parameter:
                trainer : Trainer object
                args_: command line arguments parsed via argparse
                folds: number of folds to perform
                instance_train_dic : instance name -> Instance()
                solver_list : list with solver aliases
                config_dic : solver alias -> command line
                seed: random seed
            Returns
                dictionary with all generated files and meta informations
                inst_par10_dict: flexfolio performance : instance name -> par10 runtime
                global_sbs_inst_par10_dict: sbs performance : instance name -> par10 runtime
        '''
        
        random.seed(seed)
        
        self.__n_folds = folds
        
        if self.__n_folds > 0:
            self.__get_cross_fold(instance_train_dic) # fills __times_parts, self.__feature_parts, self.__status_parts
        
        self._aspeed_opt = args_.aspeed_opt
        
        global_thread_time_dic = dict((i,0) for i in range(1,self._MAX_THREADS+1))
        global_thread_rmse_dic = dict((i,0) for i in range(1,self._MAX_THREADS+1))
        global_thread_timeout_dic = dict((i,0) for i in range(1,self._MAX_THREADS+1))
        global_spend_time = dict((x, 0) for x in solver_list)
        solver_stats = dict((i, {}) for i in range(1, self._MAX_THREADS + 1))
        inst_par10_dict = {}
        
        fold = args_.fold
    
        Printer.print_c(">>> %d-th iteration<<<" % (fold + 1))
        instance_train = self.__get_train_nth_fold(fold)
        instance_test = self.__instance_parts[fold]
        
        # TRAINING
        selection_dic = trainer.train(args_, instance_train, solver_list, config_dic, save_models=False)

        args_.aspeed_opt = self._aspeed_opt  # restore setting in command line arguments (aspeed scheduler changes it to prevent infinite loops)
        solver_schedule = {"claspfolio": args_.cutoff}
        
        if self._aspeed_opt:
            configs_dict = selection_dic["configurations"]
            for conf_name, conf_dict in configs_dict.items():
                if conf_dict.get("presolving_time"):
                    pre_solver = conf_name
                    pre_solve_time = conf_dict.get("presolving_time")
                    solver_schedule["claspfolio"] -= pre_solve_time
                    solver_schedule[pre_solver] = pre_solve_time
        
        if self._update:
            times_train_fp = self._write_train_dic(instance_train, solver_list)
            up_dic = {
                      "runtime_file" : times_train_fp.name,
                      "feature_file" : args_.feats,
                      "class_file" : args_.satunsat,
                      "runtime_update" : os.path.join(args_.model_dir, "runtime_update%d.txt" % (fold)),
                      "feature_update" : os.path.join(args_.model_dir, "feature_update%d.txt" % (fold)),
                      "class_update" : os.path.join(args_.model_dir, "class_update%d.txt" % (fold)),
                      "cutoff" : args_.cutoff,
                      "n_feats": args_.n_feats,
                      "approach" : args_.approach,
                      "norm" : args_.norm,
                      "svm_train" : args_.svm_train,
                      "model_dir" : args_.model_dir,
                      "n_new" : 0
                      }
        
        # oracle performance
        oracle_avg_time, oracle_spend_time_dict = self._oracle_performance(instance_test, solver_list)
        
        # TEST / EVALUATION
        for instance in instance_test.values():
            Printer.print_verbose(instance.get_name())
            if not instance.get_features() is None and instance.get_feature_time() < args_.feat_time:
                list_conf_scores = self._select(args_.approach, selection_dic, instance.get_features())
            else:
                list_conf_scores = self._extract_backup_scores(selection_dic)
            
            thread_time_dic, thread_rmse_dic, thread_timeout_dic, selected_solvers, spend_time_dict = \
                self._get_time(list_conf_scores, 
                               instance.get_runtimes(),
                               min(instance.get_feature_time(), args_.feat_time), 
                               solver_list, 
                               args_.cutoff,
                               solver_schedule)
            global_spend_time = dict((solver, global_spend_time.get(solver, 0) + spend_time_dict.get(solver, 0)) for solver in solver_list)
            global_thread_time_dic = self._add_dics(global_thread_time_dic, thread_time_dic)
            global_thread_rmse_dic = self._add_dics(global_thread_rmse_dic, thread_rmse_dic)
            global_thread_timeout_dic = self._add_dics(global_thread_timeout_dic, thread_timeout_dic)
            solver_stats = self._solver_frequency(selected_solvers, solver_stats)
            # TODO: bugfix if SBS exists
            # self._get_seq_selection_stat(thread_time_dic[1], instance.get_runtimes())
            inst_par10_dict[instance.get_name()] = thread_time_dic[1]
            
            # update models
            #-------------------------------------------------- if self._update:
                #---------- updater = Updater(up_dic, selection_dic, None, None)
                # selection_dic = updater.update_models(thread_time_dic[1], instance.get_features(), instance.get_class(), list_conf_scores[0][0], instance)
                #------------------------------------------ up_dic["n_new"] += 1
        Printer.print_verbose(str(global_thread_timeout_dic))
        Printer.print_verbose(str(global_thread_time_dic))
        # Printer.print_nearly_verbose(str(json.dumps(solver_stats, indent=2)))

        Printer.print_c("\n >>> Oracle Evaluation <<<\n")
        Printer.print_c("average time: %f" %(oracle_avg_time))
        Printer.print_c("(all unsolvable instances were filtered while reading data)")
        
        Printer.print_c("\n >>> Cross Fold Evaluation <<<\n")
        Printer.print_c("Timeouts per #Thread: %s" %(str(global_thread_timeout_dic)))
        Printer.print_c("Time (PAR10) per #Thread: %s" %(str(global_thread_time_dic)))
        Printer.print_c("Selection Positions : %s" %(str(self._selection_stats)))
        global_thread_avg_dic = {}
        global_thread_par10_dic = {}
        for thread, time in global_thread_time_dic.items():
            global_thread_par10_dic[thread] = time / len(instance_test)
            global_thread_avg_dic[thread] = self._extract_par1_from_par10(time, global_thread_timeout_dic[thread], args_.cutoff) / len(instance_test)
        for thread, squared_error in global_thread_rmse_dic.items():
            #global_thread_rmse_dic[thread] = math.sqrt(squared_error / len(instance_test))
            global_thread_rmse_dic[thread] = math.sqrt(math.exp(squared_error / len(instance_test)))
        Printer.print_c("PAR1 per #Thread: %s" %(str(global_thread_avg_dic)))
        Printer.print_c("PAR10 per #Thread: %s" %(str(global_thread_par10_dic)))
        Printer.print_c("RMSE per #Thread: %s" %(str(global_thread_rmse_dic)))
        Printer.print_nearly_verbose("Solver Selection Frequencies (#Threads -> Solvers):")
        Printer.print_nearly_verbose(str(json.dumps(solver_stats, indent=2)))
        Printer.print_c("Time used by each solver: %s" %(str(global_spend_time)))
        Printer.print_c("Optimal Time used by each solver: %s" %(str(oracle_spend_time_dict)))
        
        if self._print_file:
            self._write_csv_runtimes(self._print_file, instance_test, inst_par10_dict, solver_list)
        
        if args_.table_format:
            # SET & Approach & Normalization & contr.-filter & weigthing  & aspeed-opt & PAR1 & PAR10 & TO & RMSE & oralce
            print("SET & Approach & Normalization & contr.-filter & weigthing  & aspeed-opt & PAR1 & PAR10 & TO & RMSE & oralce")
            print("%s & %s & %s & %.2f & %r & %r & %.2f & %.2f & %d & %.2f & %.2f" %(
                                                            args_.times, args_.approach, args_.norm, args_.contributor_filter,
                                                            args_.approx_weights, 
                                                            args_.aspeed_opt,
                                                            global_thread_avg_dic[1],
                                                            global_thread_par10_dic[1],
                                                            global_thread_timeout_dic[1],
                                                            global_thread_rmse_dic[1],
                                                            oracle_avg_time
                                                            ))
        
        if args_.smac:
            if args_.metric == "PAR10":
                print("Result for SMAC: %f" % (global_thread_par10_dic[1]))
            elif args_.metric == "RMSE":
                print("Result for SMAC: %f" % (global_thread_rmse_dic[1]))
            elif args_.metric == "PAR1":
                print("Result for SMAC: %f" % (global_thread_avg_dic[1]))
        
        return global_thread_par10_dic[1], inst_par10_dict

    def __get_cross_fold(self, instance_dic):
        '''
            split the available data (features, runtimes and status) in __n_folds parts to perform later a cross fold validation;
            fills:  __times_parts, self.__feature_parts, self.__status_parts
        '''
        l = len(instance_dic)
        index = 0
        self.__instance_parts = []
        parted_inst_dic = {}
        threshold = l / self.__n_folds
        partIndex = 1
        instsList = instance_dic.keys()
        while instsList != []:
            randIndex = random.randint(0, len(instsList)-1)
            inst = instsList.pop(randIndex)
            
            if (index >= threshold): # if the fold full?
                self.__instance_parts.append(parted_inst_dic)
                parted_inst_dic = {}
                l = l - index
                threshold = l / (self.__n_folds - partIndex)
                partIndex += 1
                index = 0
                
            index += 1
            parted_inst_dic[inst] = instance_dic[inst]
        self.__instance_parts.append(parted_inst_dic)
        
    def __get_train_nth_fold(self,n):
        '''
            returns the n-th fold for the cross validation
            uses: __times_parts, self.__feature_parts, self.__status_parts
            Args:
                n : index of fold
            Returns:
                times_train: training set of runtimes (dictionary) 
                features_train: training set of features (dictionary) 
                status_train:  set of status (dictionary) 
        '''
        instance_train = {}
        for i in range(0,self.__n_folds):
            if (n == i):
                continue
            instance_train.update(self.__instance_parts[i])
        return instance_train

    
