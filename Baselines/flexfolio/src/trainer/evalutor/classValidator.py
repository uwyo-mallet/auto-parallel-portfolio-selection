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

class ClassValidator(Validator):
    '''
        WARNING: NOT WORKING RIGHT NOW
        perform validation evaluation based on the given problem classes
    '''


    def __init__(self, update_sup, print_file):
        '''
        Constructor
        '''
        Validator.__init__(self, update_sup, print_file)
        self.__instance_parts = []

    def evaluate(self, trainer, args_, instance_train_dic, solver_list, config_dic, seed):
        '''
            class evaluation
            Parameter:
                trainer : Trainer object
                args_: command line arguments parsed via argparse
                instance_train_dic : instance name -> Instance()
                solver_list : list with solver aliases
                config_dic : solver alias -> command line
                seed: random seed
            Returns
                dictionary with all generated files and meta informations
                inst_par10_dict: flexfolio performance : instance name -> par10 runtime
        '''
        
        random.seed(seed)
        
        dict_class_inst = self.__get_class_fold(instance_train_dic)
        classes = dict_class_inst.keys()
        n_classes = len(dict_class_inst)
        Printer.print_c("Number of found classes: %d" %(n_classes))
        
        self._aspeed_opt = args_.aspeed_opt
        
        global_thread_time_dic = dict((i,0) for i in range(1,self._MAX_THREADS+1))
        global_thread_rmse_dic = dict((i,0) for i in range(1,self._MAX_THREADS+1))
        global_thread_timeout_dic = dict((i,0) for i in range(1,self._MAX_THREADS+1))
        global_spend_time = dict((x,0) for x in solver_list)
        solver_stats = dict((i,{}) for i in range(1,self._MAX_THREADS+1))
        inst_par10_dict = {}
        
        dict_class_frac_tos = {}
        
        for iteration in range(0, n_classes):
            Printer.print_c(">>> %d-th iteration: %s<<< " %(iteration + 1, classes[iteration]))
            
            instance_train = self.__get_train_nth_class(iteration)
            instance_test = self.__instance_parts[iteration]
            
            # TRAINING
            selection_dic = trainer.train(args_, instance_train, solver_list, config_dic, save_models=False)

            args_.aspeed_opt = self._aspeed_opt # restore setting in command line arguments (aspeed scheduler changes it to prevent infinite loops)
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
                times_train_fp = self._write_train_dic(instance_train,solver_list)
                up_dic = {
                          "runtime_file" : times_train_fp.name,
                          "feature_file" : args_.feats,
                          "class_file" : args_.satunsat,
                          "runtime_update" : os.path.join(args_.model_dir,"runtime_update%d.txt" %(iteration)),
                          "feature_update" : os.path.join(args_.model_dir,"feature_update%d.txt" %(iteration)),
                          "class_update" : os.path.join(args_.model_dir,"class_update%d.txt" %(iteration)),
                          "cutoff" : args_.cutoff,
                          "n_feats": args_.n_feats,
                          "approach" : args_.approach,
                          "norm" : args_.norm,
                          "svm_train" : args_.svm_train,
                          "model_dir" : args_.model_dir,
                          "n_new" : 0
                          }
            
            
            local_thread_time_dic = dict((i,0) for i in range(1,self._MAX_THREADS+1))
            local_thread_rmse_dic = dict((i,0) for i in range(1,self._MAX_THREADS+1))
            local_thread_timeout_dic = dict((i,0) for i in range(1,self._MAX_THREADS+1))
            
            # TEST / EVALUATION
            for instance in instance_test.values():
                if not instance._features is None and instance._feature_cost_total < args_.feat_time:
                    list_conf_scores = self._select(args_.approach, selection_dic, instance._features)
                else:
                    list_conf_scores = self._extract_backup_scores(selection_dic)
                
                thread_time_dic, thread_rmse_dic, thread_timeout_dic, selected_solvers, spend_time_dict = \
                    self._get_time(list_conf_scores, 
                               instance._cost_vec,
                               min(instance._feature_cost_total, args_.feat_time), 
                               solver_list, 
                               args_.cutoff,
                               solver_schedule)
                global_spend_time = dict((solver, global_spend_time.get(solver,0) + spend_time_dict.get(solver,0)) for solver in solver_list)
                
                local_thread_time_dic = self._add_dics(local_thread_time_dic, thread_time_dic)
                local_thread_rmse_dic = self._add_dics(local_thread_rmse_dic, thread_rmse_dic)
                local_thread_timeout_dic = self._add_dics(local_thread_timeout_dic, thread_timeout_dic)
                solver_stats = self._solver_frequency(selected_solvers, solver_stats)
                #TODO: bugfix if SBS exists
                #self._get_seq_selection_stat(thread_time_dic[1], instance.get_runtimes())
                inst_par10_dict[instance._name()] = thread_time_dic[1]
                
                # update models
                #---------------------------------------------- if self._update:
                    #------ updater = Updater(up_dic, selection_dic, None, None)
                    # selection_dic = updater.update_models(thread_time_dic[1], instance.get_features(), instance.get_class(), list_conf_scores[0][0], instance)
                    #-------------------------------------- up_dic["n_new"] += 1
                    
            Printer.print_c("Number of Training instances: %d" %(len(instance_train)))
            Printer.print_c("Number of Test instances: %d\n" %(len(instance_test)))
                    
            Printer.print_c("Sum of runtimes: %s" %(str(local_thread_time_dic)))
            Printer.print_c("RMSE: %s" % (str(local_thread_rmse_dic)))
            Printer.print_c("Timeouts: %s\n" % (str(local_thread_timeout_dic)))
            
            dict_class_frac_tos["%s (%d/%d)" %(classes[iteration], local_thread_timeout_dic[1], len(instance_test))] = local_thread_timeout_dic[1] / float(len(instance_test)) 
            
            global_thread_time_dic = self._add_dics(global_thread_time_dic, local_thread_time_dic)
            global_thread_rmse_dic = self._add_dics(global_thread_rmse_dic, local_thread_rmse_dic)
            global_thread_timeout_dic = self._add_dics(global_thread_timeout_dic, local_thread_timeout_dic)

        oracle_avg_time, oracle_spend_time_dict = self._oracle_performance(instance_train_dic, solver_list)
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
            global_thread_par10_dic[thread] = time / len(instance_train_dic)
            global_thread_avg_dic[thread] = self._extract_par1_from_par10(time, global_thread_timeout_dic[thread], args_.cutoff) / len(instance_train_dic)
        for thread, squared_error in global_thread_rmse_dic.items():
            global_thread_rmse_dic[thread] = math.sqrt(squared_error / len(instance_train_dic))
            #global_thread_rmse_dic[thread] = math.sqrt(math.exp(squared_error / len(instance_train_dic)))
        Printer.print_c("PAR1 per #Thread: %s" %(str(global_thread_avg_dic)))
        Printer.print_c("PAR10 per #Thread: %s" %(str(global_thread_par10_dic)))
        Printer.print_c("RMSE per #Thread: %s" %(str(global_thread_rmse_dic)))
        Printer.print_nearly_verbose("Solver Selection Frequencies (#Threads -> Solvers):")
        Printer.print_nearly_verbose(str(json.dumps(solver_stats, indent=2)))
        Printer.print_c("Time used by each solver: %s" %(str(global_spend_time)))
        Printer.print_c("Optimal Time used by each solver: %s" %(str(oracle_spend_time_dict)))
        
        if self._print_file:
            self._write_csv_runtimes(self._print_file, instance_train_dic, inst_par10_dict, solver_list)
        
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
            print("SET & Approach & Normalization & contr.-filter & weigthing  & aspeed-opt & PAR1 & PAR10 & TO & RMSE & oralce")
            print("%s & %s & %s & %.2f & %r & %r & %.2f & %.2f & %d & %.2f & %.2f" %(
                                                            args_.times, name, args_.norm, args_.contributor_filter,
                                                            args_.approx_weights, 
                                                            args_.aspeed_opt,
                                                            global_thread_avg_dic[1],
                                                            global_thread_par10_dic[1],
                                                            global_thread_timeout_dic[1],
                                                            global_thread_rmse_dic[1],
                                                            oracle_avg_time
                                                            ))
        
        if args_.plot_mt:
            plotter = Plotter()
            plotter.plot_mulithreading(global_thread_par10_dic, oracle_avg_time, args_.times, "PAR10")
            plotter.plot_spend_times(global_spend_time, oracle_spend_time_dict, args_.times)
            
        Printer.print_c(json.dumps(dict_class_frac_tos, indent=2))
            
        if args_.plot_classes:
            plotter = Plotter()
            plotter.plot_classes(dict_class_frac_tos, args_.times)
        
        return global_thread_par10_dic[1], inst_par10_dict

    def __get_class_fold(self, instance_dic):
        '''
            split the available data (features, runtimes and status) in class parts to perform later a class validation;
            the classes are extracted by the path of the instances
            fills:  __instance_parts
        '''
        
        # find all classes and build dictionary
        dict_class_inst = {}
        for name,inst_ in instance_dic.items():
            class_ = os.path.dirname(name)
            dict_class_inst[class_] = dict_class_inst.get(class_,{})
            dict_class_inst[class_][name] = inst_
            
        self.__instance_parts = list(dict_class_inst.values())
        
        return dict_class_inst
        
    def __get_train_nth_class(self,n):
        '''
            returns the training data except for the n-th class for the validation
            uses: __times_parts, self.__feature_parts, self.__status_parts
            Args:
                n : index of fold
            Returns:
                times_train: training set of runtimes (dictionary) 
                features_train: training set of features (dictionary) 
                status_train: training set of status (dictionary) 
        '''
        instance_train = {}
        for i in range(0,len(self.__instance_parts)):
            if (n == i):
                continue
            instance_train.update(self.__instance_parts[i])
        return instance_train

    