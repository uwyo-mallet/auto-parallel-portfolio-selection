'''
Created on 10.03.2014

@author: lindauer
'''

import os,sys
import unittest
import random

cmd_folder = "/ihome/lindauer/workspace/claspfolio-2.0/src/"
if cmd_folder not in sys.path:
    sys.path.append(cmd_folder)
print(sys.path)

from selector.Ensemble import Ensemble
from misc.printer import Printer

class Test(unittest.TestCase):


    def test_portfolio_construction(self):
        
        ens = Ensemble()
        Printer.verbose = 2
        
        # sample portfolio scores
        SOLVERS = 4
        SCORES = list(range(0,SOLVERS)) 
        SAMPLES = 10
        REPS = 1000
        
        for _ in range(0,REPS):
            solver_score_dict = {}
            for i in range(0,SOLVERS):
                solver = "s%d" %(i)
                solver_score_dict[solver] = []
                for _ in range(0,SAMPLES):
                    solver_score_dict[solver].append(random.random()*SOLVERS)
                
            portfolio_develop_stats = ens._greedy_construction(solver_score_dict.keys(), solver_score_dict)
            Printer.print_verbose("Mean development: \t%s" %("->".join(map(str,portfolio_develop_stats["means"]))))
            
            s = 1000
            for m in portfolio_develop_stats["means"]:
                assert s >= m
                s = m
            
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_portfolio_construction']

    unittest.main()