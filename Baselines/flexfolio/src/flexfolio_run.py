'''
Created on Nov 5, 2012

@author: manju
'''

import sys
import os
import operator
import inspect
import time

# http://stackoverflow.com/questions/279237/python-import-a-module-from-a-folder
global cmd_folder
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
cmd_folder = os.path.realpath(os.path.join(cmd_folder, ".."))
if cmd_folder not in sys.path:
    sys.path.append(cmd_folder)
#print(sys.path)

from input_parser.cmd_parser import Parser
from executor.executor import Executor
from executor.executorClaspmt import ExecutorClaspmt
from misc.printer import Printer

# feature extraction imports
from featureExtractor.claspre import Claspre
from featureExtractor.satzilla import SatZilla
from featureExtractor.claspre2 import Claspre2

from selector.selectionApp import SelectionBase

#from misc.updater import Updater

class Flexfolio(object):
    '''
        main class of claspfolio
        execution plan:
            1. parse command line arguments (and config file)
            2. use featureExtractor to compute instance features of given instance
            3. select algorithms to execute (selector)
            4. execute algorithms
    '''

    extractor = {"CLASPRE" : Claspre, "CLASPRE2" : Claspre2, "SATZILLA": SatZilla}
    
    def __init__(self):
        ''' Constructor '''
        self._parser = Parser()
        self._executor = Executor()
        
    def main(self,sys_argv):
        '''
            main method of claspfolio, is directly called
            Parameter:
                sys_argv: command line arguments
        '''     
        
        entire_time_start = time.time() #@UnusedVariable

        instance, ex_dic, se_dic, al_dic, features_stop, values_stop, up_dic, ori_config_file, o_dir, env_, clause_sharing = \
            self._parser.parse_command_line(sys_argv)
        
        if not o_dir: # normal mode
            self.normal_mode(instance, ex_dic, se_dic, al_dic, features_stop, values_stop, up_dic, ori_config_file, env_, clause_sharing)
        else:
            self.oracle_mode( ex_dic, se_dic, o_dir)

    def normal_mode(self, instance, ex_dic, se_dic, al_dic, features_stop, values_stop, up_dic, ori_config_file, env_, clause_sharing, exit_=True):
        '''
            normal mode:
                1. feature prediction
                2. algorithm selection
                3. run solver
            Args:
                instance: fp to file
                ex_dic: extractor dictionary
                se_dic: selection dictionary
                al_dic: algorithm dictionary 
                features_stop: terminate after feature computation
                values_stop: terminate after decision value computation
                up_dic: update dicationary
                ori_config_file: original configuration file (includes ex_dic, se_dic and al_dic)
                env: system environment
                clause_sharing: enable clause sharing by replacing executor
                exit_: exit after stop?
        '''

        features = Flexfolio.extractor[ex_dic["class"].upper()]().run_extractor(ex_dic,instance)
        
        if features_stop and exit_:
            Printer.print_c("Features: %s" % (",".join(map(str,features))))
            sys.exit(0)
        if not features and not se_dic["normalization"]["impute"]: # if feature were imputed, we can still use them
            if exit_:
                self.run_backup_solvers(al_dic, se_dic, instance, env_, quit_ = (up_dic == None))
            else:
                return None
            
        pwd = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
        pwd = os.path.realpath(os.path.join(pwd, ".."))
            
        selector_name = se_dic["approach"]["approach"].upper()
        list_conf_scores = SelectionBase.select(selector_name, se_dic, features, pwd)
        if not list_conf_scores:
            if exit_:
                self.run_backup_solvers(al_dic, se_dic, instance, env_, quit_ = (up_dic == None))
            else:
                return None
        
        if values_stop and exit_:
            sys.exit(0)
        
        if values_stop and not exit_:
            return list_conf_scores
        
        if clause_sharing: # replace executor for clause sharing with clasp mt
            self._executor = ExecutorClaspmt()
            
        runtime, solver, status = self._executor.execute(al_dic["threads"], 
                                                         se_dic["configurations"], 
                                                         list_conf_scores, 
                                                         instance, 
                                                         env_, 
                                                         quit_ = (up_dic == None))
        
        if up_dic and runtime != -1: # update models
            self.update_models(features, runtime, status, solver, instance, up_dic, se_dic, ex_dic, ori_config_file)

    def oracle_mode(self, ex_dic, se_dic, o_dir):
        '''
            oralce mode:
                for all isntances in o_dir:
                    1. feature computation
                    2. scoring of algorithms
                Aggregate solver scores
            Args:
                ex_dic: extractor dictionary
                se_dic: selection dictionary
                o_dir: dictionary with files 
        '''

        pwd = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
        pwd = os.path.realpath(os.path.join(pwd, ".."))
        
        solver_score_dic = {}
        for r,d,files_ in os.walk(o_dir):
            for file_ in files_:
                instance = open(os.path.join(r,file_),"r")
                Printer.print_c("\n"+instance.name)
                features = Flexfolio.extractor[ex_dic["class"].upper()]().run_extractor(ex_dic, instance)
                if not features:
                    continue
                
                selector_name = se_dic["approach"]["approach"].upper()
                list_conf_scores = SelectionBase.select(selector_name, se_dic, features, pwd)
                if not list_conf_scores:
                    continue
                for solver,score in list_conf_scores:
                    if solver_score_dic.get(solver):
                        solver_score_dic[solver] += score
                    else:
                        solver_score_dic[solver] = score
        sorted_scores = sorted(solver_score_dic.iteritems(),key=operator.itemgetter(1))
        
        Printer.print_c("\n >>> Algorithm Scores <<<\n")
        
        index = 1
        for solver,score in sorted_scores:
            Printer.print_c("%d-th ranked solver: \t %s" %(index, solver))
            Printer.print_c("Call: \t\t %s" %( se_dic["configurations"][solver]["call"]))
            Printer.print_c("Score: \t\t %d\n" %(score))
            index += 1
            
    def run_backup_solvers(self, al_dic, se_dic, instance, env_, quit_):
        '''
            run backup solver if feature computation failed
        '''
        conf_score_dic = {}
        for name,solver in se_dic["configurations"].items():
            backup_rank = solver["backup"]
            conf_score_dic[name] = backup_rank
            
        sorted_scores = sorted(conf_score_dic.iteritems(),key=operator.itemgetter(1))
        self._executor.execute(al_dic["threads"], se_dic["configurations"], sorted_scores, instance, env_, quit_)
        
        
    def update_models(self, features, runtime, status, solver, instance, up_dic, se_dic, ex_dic, ori_config_file):
        '''
            adds new information to training files and retrains models
            Parameter:
                features: list of features
                runtime: __time to solver instance
                solver: used solver to solve instance (resp. fastest solver)
                up_dic: Dictionary with all necessary meta information for training
                sel_dic: selection dictionary of config file
                ex_dic: feature extraction dictionary 
        '''
        #updater = Updater(up_dic, se_dic, ex_dic, ori_config_file)
        #updater.update_models(runtime, features, status, solver, instance)
        
            
        
    #def old_style(self,se_dic,al_dic):
    #    print("@means: %s" % (",".join(map(str,se_dic["normalization"]["means"]))))
    #    print("@stds: %s" % (",".join(map(str,se_dic["normalization"]["stds"]))))
    #    print("")
    #    for solver,conf in se_dic["configurations"].items():
    #        print("[%s]: %s" %(conf["id"],conf["call"]))
    
              
if __name__ == '__main__':
    Printer.print_c("flexfolio")
    Printer.print_c("published under GPLv2")
    Printer.print_c("https://bitbucket.org/mlindauer/xfolio")
    xfolio = Flexfolio()
    xfolio.main(sys.argv[1:])
    