'''
Created on Nov 9, 2012

@author: manju
'''

import sys
import math
import operator
import json
import copy

from selector.selectionApp import SelectionBase

from misc.printer import Printer
from tempfile import NamedTemporaryFile
from trainer.evalutor.statistical_tests.permutationtest import PermutationTest

class Stats(object):
    
    def __init__(self, max_threads, solver_list):
        '''
            Constructor
        '''
        self._MAX_THREADS = max_threads
        self.thread_time_dic = dict((i,0) for i in range(1,self._MAX_THREADS+1))
        self.thread_rmse_dic = dict((i,0) for i in range(1,self._MAX_THREADS+1))
        self.thread_timeout_dic = dict((i,0) for i in range(1,self._MAX_THREADS+1))
        self.spend_time = dict((x,0) for x in solver_list)
        self.solver_stats = dict((i,{}) for i in range(1,self._MAX_THREADS+1))
        self.inst_par10_dict = {}  #threadid -> inst_name -> perf
        self.thread_avg_dic = {}
        self.thread_par10_dic = {}
        self._test_n = 0
        self.presolved = 0
        self.unsolved = 0 # instances that are not solved by any algorithm AND not presolved
        
        self.ties = 0 # how often two or more 
        
    def print_runtime_stats(self, oracle_avg_time, oracle_spend_time_dict, oracle_par10, oracle_tos, cutoff):
        Printer.print_c("\n >>> Instances: %d <<<" %(self._test_n))
        Printer.print_c(" >>> Oracle Evaluation (w/o unsolved) <<<\n")
        Printer.print_c("Unsolved (not by any algorithm and not by feature computation): %d" %(self.unsolved))
        #TODO: maybe normalize also oracle with self.unsolved; however, perfect system can be better than oracle than
        oracle_avg_time_wo = ((oracle_avg_time * self._test_n) - (cutoff * oracle_tos)) / (self._test_n - oracle_tos)
        Printer.print_c("PAR1 time: %f (%f)" %(oracle_avg_time, oracle_avg_time_wo))
        oracle_par10_wo  = ((oracle_par10 * self._test_n) - (10* cutoff * oracle_tos)) / (self._test_n - oracle_tos)
        Printer.print_c("Par10 time: %f (%f)" %(oracle_par10, oracle_par10_wo))
        Printer.print_c("#TOs: %d (0)" %(oracle_tos))
        
        for thread, time in self.thread_time_dic.items():
            self.thread_par10_dic[thread] = time / self._test_n
            self.thread_avg_dic[thread] = self._extract_par1_from_par10(time, self.thread_timeout_dic[thread], cutoff) / self._test_n
        for thread, squared_error in self.thread_rmse_dic.items():
            self.thread_rmse_dic[thread] = math.sqrt(squared_error / self._test_n)
            #global_thread_rmse_dic[thread] = math.sqrt(math.exp(squared_error / len(instance_train_dic)))
        
        solved = dict((thread, 1 - (float(to)/self._test_n)) for thread, to in self.thread_timeout_dic.items())
        Printer.print_c("\n >>> Cross Fold Evaluation <<<\n")
        Printer.print_c("Presolved: %s" %(str(self.presolved)))
        Printer.print_c("Prediction ties: %d" %(self.ties))
        
        Printer.print_c(">>>With Unsolvable Instances")
        Printer.print_c("Timeouts (with unsolved): %d" %(self.thread_timeout_dic[1]))
        Printer.print_c("Solved (perc) (with unsolved): %.4f" %(solved[1]))
        Printer.print_c("PAR1 (with unsolved): %.2f" %(self.thread_avg_dic[1]))
        Printer.print_c("PAR10 (with unsolved): %.2f" %(self.thread_par10_dic[1]))
        
        Printer.print_c(">>>Without Unsolved Instances (depends on pre-solved in feature groups)")
        thread_timeout_dic_wo = dict([thread, to - self.unsolved] for thread, to in self.thread_timeout_dic.iteritems())
        Printer.print_c("Timeouts (without unsolved): %d" %(thread_timeout_dic_wo[1]))
        solved_wo_unsolveable = dict([thread, (solved_y * self._test_n) / (self._test_n - self.unsolved) ] for thread, solved_y in solved.iteritems())
        Printer.print_c("Solved (perc) (without unsolved): %.4f" %(solved_wo_unsolveable[1]))
        par1_wo_unsolveable = dict([thread, ((avg * self._test_n) - (cutoff * self.unsolved)) / (self._test_n - self.unsolved)] for thread, avg in self.thread_avg_dic.iteritems())
        Printer.print_c("PAR1 (without unsolved): %.2f" %(par1_wo_unsolveable[1]))
        par10_wo_unsolveable = dict([thread, ((par10 * self._test_n) - (10* cutoff * self.unsolved)) / (self._test_n - self.unsolved)] for thread, par10 in self.thread_par10_dic.iteritems())
        Printer.print_c("PAR10 (without unsolved): %.2f" %(par10_wo_unsolveable[1]))
        
        Printer.print_c("")
        #Printer.print_c("RMSE per #Thread: %s" %(str(self.thread_rmse_dic)))
        Printer.print_nearly_verbose("Solver Selection Frequencies (#Threads -> Solvers):")
        Printer.print_nearly_verbose(str(json.dumps(self.solver_stats, indent=2)))
        Printer.print_c("Time used by each solver: %s" %(str(self.spend_time)))
        Printer.print_c("Optimal Time used by each solver: %s" %(str(oracle_spend_time_dict)))
        
    def print_qual_stats(self, oracle_avg_time, maximize=False):
        Printer.print_c("\n >>> Instances: %d <<<" %(self._test_n))
        Printer.print_c(" >>> Oracle Evaluation (w/o unsolved) <<<\n")
        Printer.print_c("Unsolved (not by any algorithm and not by feature computation): %d" %(self.unsolved))
        #TODO: maybe normalize also oracle with self.unsolved; however, perfect system can be better than oracle than
        Printer.print_c("quality: %.2f " %(oracle_avg_time if maximize else -1*oracle_avg_time))
        
        for thread, time in self.thread_time_dic.items():
            self.thread_par10_dic[thread] = time / self._test_n
        
        Printer.print_c("\n >>> Cross Fold Evaluation <<<\n")
        Printer.print_c("Prediction ties: %d" %(self.ties))
        
        qual = self.thread_par10_dic[1] if maximize else -1*self.thread_par10_dic[1]
        Printer.print_c("quality: %.6f" %(qual))
        
    def _extract_par1_from_par10 (self, par10, timeouts, cutoff):
        '''
            extract the par1 score based on given par10 and number of timeouts
            at a certain cutoff
        '''
        return par10 - (timeouts * cutoff * (10-1))


class Validator(object):
    '''
        perform cross validation evaluation
    '''


    def __init__(self, update_sup, print_file):
        '''
        Constructor
        '''
        self._select = SelectionBase.select

        self._update = update_sup
        self._print_file = print_file
    
        self._MAX_THREADS = 32
        self.__RMSE_NORM = 2
        
        self._selection_stats = dict((x,0) for x in range(1,self._MAX_THREADS+1))
        
        self._aspeed_opt = False
    
    def training(self, instance_train, meta_info, config_dic, trainer):
        '''
            train model on training data
        '''
        
        # TRAINING
        selection_dic = trainer.train(meta_info, instance_train, config_dic, save_models=False)

        meta_info.options.aspeed_opt = self._aspeed_opt # restore setting in command line arguments (aspeed scheduler changes it to prevent infinite loops)
        solver_schedule = {1: {"claspfolio": meta_info.algorithm_cutoff_time}}
        
        if self._aspeed_opt or meta_info.options.pre_schedule:
            configs_dict = selection_dic["configurations"]
            for conf_name, conf_dict in configs_dict.items():
                if conf_dict.get("presolving_time"):
                    for core, pre_solve_time in conf_dict.get("presolving_time").iteritems():
                        pre_solver = conf_name
                        solver_schedule[core] = solver_schedule.get(core,{"claspfolio": meta_info.algorithm_cutoff_time})
                        solver_schedule[core]["claspfolio"] -= pre_solve_time
                        solver_schedule[core][pre_solver] = pre_solve_time
                    
        #===================================================================
        # if self._update:
        #     times_train_fp = self._write_train_dic(instance_train,solver_list)
        #     up_dic = {
        #               "runtime_file" : times_train_fp.name,
        #               "feature_file" : args_.feats,
        #               "class_file" : args_.satunsat,
        #               "runtime_update" : os.path.join(args_.model_dir,"runtime_update%d.txt" %(iteration)),
        #               "feature_update" : os.path.join(args_.model_dir,"feature_update%d.txt" %(iteration)),
        #               "class_update" : os.path.join(args_.model_dir,"class_update%d.txt" %(iteration)),
        #               "cutoff" : args_.cutoff,
        #               "n_feats": args_.n_feats,
        #               "approach" : args_.approach,
        #               "norm" : args_.norm,
        #               "svm_train" : args_.svm_train,
        #               "model_dir" : args_.model_dir,
        #               "n_new" : 0
        #               }
        #===================================================================                    
                    
        return selection_dic, solver_schedule
    
    def testing(self, instance_test, meta_info, selection_dic, solver_schedule, stats):
        '''
            testing trained model on test instances
            updates Stats object
        '''
        
        solver_list = meta_info.algorithms
        
        par10_per_set = 0
        
        for instance in instance_test.values():
            Printer.print_verbose(instance._name)
            # predict only if features available, intime computable and not presolved
            if meta_info.options.approach != "SBS": # SBS and aspeed do not need feature and therefore no time is wasted
                feature_time = instance._feature_cost_total
            else:
                feature_time = 0
            if instance._pre_solved and meta_info.options.approach != "SBS": #SBS and aspeed does not presolve anything
                thread_time_dic = dict((thread, feature_time) for thread in range(1,self._MAX_THREADS+1))
                thread_rmse_dic = dict((thread, 0) for thread in range(1,self._MAX_THREADS+1))
                thread_timeout_dic = dict((thread, 0) for thread in range(1,self._MAX_THREADS+1))
                selected_solvers = ["feature_extractor"]
                spend_time_dict = {}
                stats.presolved += 1
            else:
                if not instance._features is None and feature_time <= meta_info.options.feat_time: #TODO: does not make sense in case of feature imputation
                    list_conf_scores = self._select(meta_info.options.approach, selection_dic, copy.deepcopy(instance._features))
                else:
                    list_conf_scores = self._extract_backup_scores(selection_dic)
                
                thread_time_dic, thread_rmse_dic, thread_timeout_dic, selected_solvers, spend_time_dict = \
                    self._get_time(list_conf_scores, 
                               instance._cost_vec,
                               min(feature_time, meta_info.options.feat_time), 
                               solver_list, 
                               meta_info.algorithm_cutoff_time,
                               solver_schedule, satzilla_mode = meta_info.options.test_mode == "satzilla")
                if list_conf_scores[0][1] == list_conf_scores[1][1]:
                    stats.ties += 1
            par10_per_set += thread_time_dic[1]
            stats._test_n += 1
            stats.spend_time = dict((solver,stats.spend_time.get(solver,0)+ spend_time_dict.get(solver,0)) for solver in solver_list)
            stats.thread_time_dic = self._add_dics(stats.thread_time_dic, thread_time_dic)
            stats.thread_rmse_dic = self._add_dics(stats.thread_rmse_dic, thread_rmse_dic)
            stats.thread_timeout_dic = self._add_dics(stats.thread_timeout_dic, thread_timeout_dic)
            stats.solver_stats = self._solver_frequency(selected_solvers, stats.solver_stats)
            #TODO: bugfix if SBS exists
            #self._get_seq_selection_stat(thread_time_dic[1], instance.get_runtimes())
            for t in thread_time_dic.keys():
                stats.inst_par10_dict[t] = stats.inst_par10_dict.get(t,{})
                stats.inst_par10_dict[t][instance._name] = thread_time_dic[t]
            
            # update models
            #---------------------------------------------- if self._update:
                #------ updater = Updater(up_dic, selection_dic, None, None)
                # selection_dic = updater.update_models(thread_time_dic[1], instance.get_features(), instance.get_class(), list_conf_scores[0][0], instance)
                #-------------------------------------- up_dic["n_new"] += 1
        #------------- Printer.print_verbose(str(global_thread_timeout_dic))
        Printer.print_c("PAR10 on current test set: %.2f (%d instances)" %(par10_per_set / len(instance_test), len(instance_test)))
        #Printer.print_c("%s" %("\n".join(sorted(instance_test.keys()))))
        Printer.print_verbose(str(stats.thread_time_dic))
        #Printer.print_nearly_verbose(str(json.dumps(solver_stats, indent=2)))
    
    def make_sig_test(self, name_perf_dict):
        '''
            make a permutation test of all entries in name_perf_dict
        '''    
        permtester = PermutationTest()
        ALPHA = 0.05
        PERMUTATIONS = 10000
        name2 = max(list(name_perf_dict.keys()))
        perf2 = name_perf_dict[name2]
        for name1, perf1 in name_perf_dict.items():
                #===============================================================
                # rejected, switched, pvalue = permtester.doTest(perf1, perf2, ALPHA, PERMUTATIONS, name1, name2, noise=None)
                # if rejected and switched:
                #     Printer.print_c("%s is significantly better than %s (p-value: %f)" %(name2, name1, pvalue))
                # elif rejected and not switched:
                #     Printer.print_c("%s is significantly better than %s (p-value: %f)" %(name1, name2, pvalue))
                # elif not rejected:
                #     Printer.print_c("No evidence that %s or %s is better (p-value: %f)" %(name1, name2, pvalue))
                # 
                # # manntwhitneyu test
                #===============================================================
                from scipy.stats import mannwhitneyu
                u, prob = mannwhitneyu(perf2, perf1)
                Printer.print_c("sigtest: %s vs %s; u: %f; prob: %f" %(name2, name1, u, prob))
                    
    def evaluate_invalids(self, time_invalid_dic, backup_solver, cutoff ):
        '''
            evaluate instances with invalid features by backup solver
            backup solver = best solver in valid time dic
            Parameter:
                time_invalid_dic : dictionary  instance -> runtimes
                time_dic : dictionary instanc -> runtimes
                cutoff: runtime cutoff
        '''
        
        unsolved = 0
        par10 = 0
        for times in time_invalid_dic.values():
            time = times[backup_solver]
            if time >= cutoff:
                unsolved +=1
            par10 += time
        
        Printer.print_c(">>>>> Stats of instances with invalid feature list (no features, too few features, unknown features):")
        Printer.print_c("Number of instances: %d" %(len(time_invalid_dic)))
        Printer.print_c("Timeouts: %d" %(unsolved))
        if time_invalid_dic:
            Printer.print_c("PAR10: %f" %(par10 / len(time_invalid_dic)))
        else:
            Printer.print_c("PAR10: 0")
        return unsolved, par10
    
    def _write_train_dic(self, instance_dic, header):
        '''
            write runtimes
            writes dic_ [key] -> [list] as a csv file and returns NamedTemporaryFile
        '''
        fp_ = NamedTemporaryFile(suffix=".tmp", prefix="UpdateTrain", dir=".", delete=True)
        fp_.write(",%s\n" %(",".join(map(str,header))))
        for key_, inst in instance_dic.items():
            list_ = inst._cost_vec
            fp_.write("%s,%s\n" %(key_, ",".join(map(str,list_))))
        fp_.flush()
        return fp_
    
    def _write_csv_runtimes(self, file_name, instance_dict, inst_par10_dict, solver_list):
        '''
            write in file_name csv file with runtimes of all solvers and flexfolio per instance
            Args:
                file_name
                instance_dict: instance name -> instance()
                inst_par10_dict: instance name -> par10 of flexfolio
                solver_list: list of solver names (alignment as used in Instance())
        '''
        
        fp = open(file_name,"w")
        fp.seek(0)
        #solver_list.append("claspfolio")
        solver_list = ["claspfolio"]
        fp.write("Instance,%s\n" %(",".join(solver_list)))
        for name, _ in instance_dict.items():
            fp.write("%s,%.4f\n" %(name, inst_par10_dict[name]))
            #fp.write("%s,%s,%.4f\n" %(name, ",".join(map(str,inst_._cost_vec)), inst_par10_dict[name]))
        fp.flush()
        fp.close()
        
    def _solver_frequency(self, selected_solvers, solver_stats):
        '''
            count how often a solver was selected per Thread
        '''
        thread_index = 1
        for solver in selected_solvers:
            for t in range(thread_index, self._MAX_THREADS + 1):
                dic_freq_thread = solver_stats[t]
                if dic_freq_thread.get(solver):
                    dic_freq_thread[solver] += 1
                else:
                    dic_freq_thread[solver] = 1
            thread_index += 1
        return solver_stats
                
    def _get_time(self, list_conf_scores, times, ftime, solver_list, cutoff, solver_schedule, satzilla_mode=False):
        '''
            look for runtime of given runtimes (times) while selecting solvers from list_conf_scores
            Parameter:
                list_conf_scores: sorted list with (solver_name,score)
                times: list of runtimes
                ftime: time to compute features
                solver_list: list of solver_names (same order as times)
                cutoff: runtime cutoff
                solver_schedule : core -> solver name -> solving time
                satzilla_mode: Boolean - feature computation after schedule
            Returns:
                dictionary: #threads -> par10 time
                dictionary: #threads -> par1 time
                dictionary: #threads -> RMSE
                dictionary: #threads -> timeouts
                selected_solvers: list: index i -> solver selected with i threads 
                spend_time_dic : solver name -> spend time for solving (seq. solving)
        '''
        oracle_time = min(times)
        solver_index = 0
        #print("Runtimes: %s " %(",".join(map(str,times))))
        #print("Get Time")
        #print(solver_schedule)
        
        spend_time_dic = dict((x,0) for x in solver_list) # time solver was running

        sorted_schedules = {}
        for core, core_schedule in solver_schedule.items():
            sorted_schedules[core] = sorted(core_schedule.iteritems(), key=operator.itemgetter(1)) #
            
        max_threads = min(self._MAX_THREADS,len(list_conf_scores))
        
        thread_time_dic = {} #dict((x+1,used_time) for x in range(0,max_threads))
        thread_rmse_dic = {} #dict((x+1,rmse) for x in range(0,max_threads))
        thread_timeout_dic = {} #dict((x+1,0) for x in range(0,max_threads))
        
        # separately calculate performance for each individual thread first
        for threads in range(1, max_threads+1):
            
            if sorted_schedules.get(threads):
                sorted_schedule = sorted_schedules[threads]
            else:
                sorted_schedule = [("claspfolio", cutoff)]
            
            if satzilla_mode:# first step: schedule
                used_time = 0 
                selected = ["claspfolio"]
            else:
                if threads == 1:
                    used_time = ftime #feature time only on first core 
                    selected =  ["claspfolio", list_conf_scores[threads-1][0]]
                else:
                    used_time = 0 # first step: compute features
                    selected =  ["claspfolio"] # simplify only on the first thread
                
            for (solver_name,pre_time) in sorted_schedule: # smallest pre_solving time first
                if solver_name in selected:
                    Printer.print_verbose("Skip %s because selected with %d threads" %(solver_name, threads))
                    continue
                solver_index = solver_list.index(solver_name)
                time = times[solver_index]
                if time < pre_time and time + used_time < cutoff:
                    used_time += time
                    spend_time_dic[solver_list[solver_index]] += time
                    #rmse = math.pow(oracle_time - used_time, 2)
                    rmse = math.pow(math.log(used_time) - math.log(oracle_time), self.__RMSE_NORM)
                    thread_time_dic[threads] = used_time
                    thread_rmse_dic[threads] = rmse
                    thread_timeout_dic[threads] = 0
                    break
                    #return thread_time_dic, thread_rmse_dic, thread_timeout_dic, [solver_list[solver_index]], spend_time_dic
                else:
                    used_time += pre_time
                    spend_time_dic[solver_list[solver_index]] += pre_time
                    
            # if not solved, we invested some time
            if not thread_timeout_dic.get(threads) == 0:
                if satzilla_mode and threads == 1: #add feature time only on first core
                    used_time += ftime
                    
                if used_time < ftime: # selected solver can only ran if the feature computation was done
                    used_time = ftime 
                    #Printer.print_w("Something strange happened because pre-solving schedule was too short (Thread %d)..." %(threads))
                
                solver, _ = list_conf_scores[threads-1]
                idx = solver_list.index(solver)
                time = times[idx]
                
                complete_time = time + used_time
                
                if complete_time < cutoff:
                    thread_timeout_dic[threads] = 0
                    runtime_par10 = complete_time
                else:
                    thread_timeout_dic[threads] = 1
                    runtime_par10 = cutoff * 10
                    
                thread_time_dic[threads] = runtime_par10 
                
                if threads == 1:
                    spend_time_dic[solver] += min(cutoff-used_time, time)
            
        min_time = thread_time_dic[1]
        min_timeout = thread_timeout_dic[1]
        for thread in range(1, max_threads+1):
            min_time = min(min_time, thread_time_dic[thread])
            thread_time_dic[thread] = min_time
            
            min_timeout = min(min_timeout, thread_timeout_dic[thread])
            thread_timeout_dic[thread] = min_timeout
            
            #rmse = math.pow(math.log(min_time) - math.log(oracle_time), self.__RMSE_NORM)
            #thread_rmse_dic[thread] = rmse       
        
        return thread_time_dic, thread_rmse_dic, thread_timeout_dic, [] ,spend_time_dic

    def _add_dics(self,a,b):
        '''
            http://stackoverflow.com/questions/1031199/adding-dictionaries-in-python
        '''
        return dict( (n, a.get(n, 0)+b.get(n, 0)) for n in set(a)|set(b) )

    def _extract_backup_scores(self, selection_dict):
        '''
            extract backup solver ranking
        '''
        algorithms = selection_dict["configurations"]
        backup_score_dict = {}
        
        for algo_name, meta_info in algorithms.items():
            backup_score = meta_info["backup"]
            backup_score_dict[algo_name] = backup_score
        sorted_scores = sorted(backup_score_dict.iteritems(),key=operator.itemgetter(1))
        
        return sorted_scores
    
    def _extract_par1_from_par10 (self, par10, timeouts, cutoff):
        '''
            extract the par1 score based on given par10 and number of timeouts
            at a certain cutoff
            REMOVE - added in Stats
        '''
        return par10 - (timeouts * cutoff * (10-1))
        
    
    def _oracle_performance(self, instance_dic, solver_list, cutoff, stats=None):
        '''
            computes the performance stastics of the oralce solver (sometimes also called vbs)
            (all unsolvable instances are filtered beforehand)
            Args:
                instance_dic: instance name -> Instance()
                solver_list: list of solvers (ordering same as runtimes)
                cutoff: runtime cutoff
            Returns:
                avg_time: par1 metric
                spend_time_dict: solver name -> used runtime
                par10_time: par10 metric
                inst_par10_dict : instance name -> performance (without unsolvable instances)
                tos: number of timeouts
        '''
        spend_time_dict = dict((solver,0) for solver in solver_list)
        inst_par10_dict = {}
        
        avg_time = 0
        par10_time = 0
        tos = 0
        for instance in instance_dic.values():
            times = instance._cost_vec
            min_time = min(times)
            solver_index = times.index(min_time)
            solver_name = solver_list[solver_index]
            spend_time_dict[solver_name] += min_time
            avg_time += min_time
            if min_time >= cutoff:
                par10_score = cutoff * 10
                tos += 1
                if instance._pre_solved:
                    Printer.print_w("Oracle Problem: Unsolved but presolved instance: %s" % (instance._name))
                elif stats:
                    stats.unsolved += 1
            else:
                par10_score = min_time
            par10_time += par10_score
            
            runtime_plus_fcost = min_time #+ instance._feature_cost_total
            if runtime_plus_fcost < cutoff:
                inst_par10_dict[instance._name] = runtime_plus_fcost
        
        avg_time = avg_time / len(instance_dic)
        par10_time = par10_time / len(instance_dic)
        
        return avg_time, spend_time_dict, par10_time, inst_par10_dict, tos