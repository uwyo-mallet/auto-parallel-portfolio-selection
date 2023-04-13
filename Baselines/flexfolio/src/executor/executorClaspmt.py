'''
Created on Nov 5, 2012

@author: manju
'''

from executor import Executor
from misc.printer import Printer

from tempfile import NamedTemporaryFile
import os, sys

class ExecutorClaspmt(Executor):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        Executor.__init__(self)
        
    def _build_cmd_list(self, threads, pre_solving_schedule):
        '''
            @Overrides parent method
            merges all command line arguments in a portfolio file and pass it to claspmt
            Preconditions:
                * all calls belong to clasp
                * all configurations include only thread parameters (no global parameters)
            Args:
                threads: number of threads to use
                pre_solving_schedule: name of pre solver (not used)
            Return:
                list of command line calls
                boolean to indicate whether pre-solver is already selected
        '''
        cmd_list = []
        portfolio_file = NamedTemporaryFile(suffix=".txt", prefix="portfolio", dir=".", delete=True) 
        solver_bin = ""
        Printer.print_c("Add to portfolio:")
        for t in range(0, min(len(self._confs_scores), threads)): # we cannot run more solvers than available in our models
            conf_2_exec = self._confs_scores[t][0]
            score = self._confs_scores[t][1]
            call = self._configurations[conf_2_exec]["call"]
            call = call.strip(" ")

            cmd = call.split(" ")
            conf = cmd[1:]
            solver_bin = cmd[0]
            if not os.path.isfile(solver_bin):
                extended = os.path.join(sys.path[-1],solver_bin) #TODO: Hack to get path to claspfolio2 installation
                if os.path.isfile(extended):
                    solver_bin = extended
                else:
                    Printer.print_e("Have not found solver: %s" %(solver_bin), exit_code=22)
                    
            portfolio_file.write("[%s (%.2f)]: %s\n" %(conf_2_exec, score, " ".join(conf)))
            Printer.print_c("   [%s (%.2f)]: %s" %(conf_2_exec, score, " ".join(conf)))
            
        portfolio_file.flush()
        cmd = [solver_bin, "-t", str(min(len(self._confs_scores), threads)), "-p", portfolio_file.name]
        cmd_list.append(("Portfolio", -1, cmd))
        pre_solving_schedule = None # disable pre solving
        return cmd_list, pre_solving_schedule
        
