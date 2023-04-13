'''
Created on Nov 5, 2012

@author: manju
'''
import operator
import math
import sys
import json
import random
import copy
import itertools
import numpy

from selector import Selector
from misc.printer import Printer

#prevent cyclic import ... super ugly
if not sys.modules.get("selector.selectionApp"):
    from selector.selectionApp import SelectionBase
else: 
    SelectionBase = sys.modules.get("selector.selectionApp").SelectionBase
    
class Ensemble(Selector):
    '''
        ensemble selection (ask all selection models and give each solver scores corresponding to their ranks in the prediction)
    '''


    def __init__(self):
        '''
        Constructor
        '''

        self._sample = False

        self._numberof_models = -1
        self._opt_base = "ranks" # scores
    
        self._SAMPLES = 1000
        self._opt_Q = 75
    
    def select_algorithms(self, args, features, pwd=""):
        ''' select  
            Args:
                args: selection_dic
                features: list of features
                pwd: directory of flexfolio (search path for models)
        '''
        
        self._set_base_args(args, features)
        
        self._opt_Q = args["approach"]["Q"]
        self._opt_base = args["approach"]["base"]
        
        if not self._features:
            return None
        
        # find all solver names:
        solver_list = list(args["configurations"].keys())
        n_solver = len(solver_list)
        
        trainer_dict = args["approach"]["trainer"]
        solver_score_dict = {}
        self._numberof_models = len(trainer_dict)
        for name, trainer_meta in trainer_dict.items():
            name = name.split("-")[0] # format <trainer name>-<index>
            trainer_args = args.copy() #copy.copy(args)
            trainer_args["approach"] = trainer_meta["approach"]
            trainer_args["normalization"] = trainer_meta["normalization"]
            
            #self._normalize(self._normalization["approach"], self._normalization["filter"], features)
            
            Printer.print_nearly_verbose("Ask %s:" %(name))
            sorted_scores = SelectionBase.select(name, trainer_args, copy.deepcopy(features), pwd)
            sorted_solvers = map(lambda x: x[0], sorted_scores)

            for solver in solver_list:
                if self._opt_base == "ranks":
                    try: 
                        new_score  = sorted_solvers.index(solver)
                    except:
                        new_score = n_solver
                elif self._opt_base == "scores":
                    new_score = reduce(lambda x,y: y[1] if y[0] == solver else x, sorted_scores, sys.maxint)
                solver_score_dict[solver] = solver_score_dict.get(solver, [])
                solver_score_dict[solver].append(new_score)

        portfolio = self._greedy_construction(solver_list, solver_score_dict)
        
        sorted_scores = zip(portfolio, range(0, len(portfolio)))

        Printer.print_nearly_verbose("\nConfiguration Scores (Ensemble):")
        for (solver,score) in sorted_scores:
            Printer.print_nearly_verbose("[%s]: %f" %(solver,score))
        
        return sorted_scores
    
    def _greedy_construction(self, solver_list, solver_score_dict):
        '''
            constructs the portfoloio in a greedy fashion.
        '''
        # greedy approach to find portfolio
        portfolio = [] # solver names
        remaining_solvers = copy.deepcopy(solver_list) # unused solvers
        portfolio_develop_stats = []
        while remaining_solvers:
            stats = []
            for s in remaining_solvers:
                new_portfolio = portfolio[:]
                new_portfolio.append(s)
                portfolio_score_dict = dict((solver, solver_score_dict[solver]) for solver in new_portfolio)
                q_score = self._get_portfolio_stats(portfolio_score_dict)
                stats.append(q_score)
            # 1. optimize mean
            index_best, cur_stats = self.__select_next_component(stats)
            if index_best is None:
                Printer.print_w("Current Portfolio of size %d selected" %(len(portfolio)))
                break
            portfolio.append(remaining_solvers[index_best])
            remaining_solvers.remove(remaining_solvers[index_best])
            #Printer.print_verbose("Portfolio mean (t: %d) : \t %f (%s)" %(len(portfolio), min_means, ",".join(portfolio)))
            portfolio_develop_stats.append(cur_stats)
        Printer.print_verbose("->".join(map(str,portfolio_develop_stats)))

        return portfolio
        #return portfolio_develop_stats
    
    def _get_portfolio_stats(self, portfolio_score_dict):
        '''
            get a portfolio distribution statistic
            1. sample scores per solver
            2. save minima in list
            3. compute mean and variance of porfolio distribution
            Args:
                portfolio_score_dict : solver -> [scores]
            Returns
                returns minima statistic of portfolio performance
        '''
        if self._sample:
            # sample approach
            portfolio_scores = []
            for _ in range(0, self._SAMPLES):
                run_scores = []
                for scores in portfolio_score_dict.values():
                    #print(random.choice(scores))
                    run_scores.append(random.choice(scores))
                portfolio_scores.append(min(run_scores))
        else:
            # per model approach
            portfolio_scores = []
            for i in range(0, self._numberof_models):
                run_scores = [scores[i] for scores in portfolio_score_dict.values()]
                portfolio_scores.append(min(run_scores))
            
        # too cost intensive
        #=======================================================================
        # portfolio_scores = list(reduce(lambda x,y: [min(xx, yy) for xx in x for yy in y], portfolio_score_dict.values()))
        # try:
        #     portfolio_scores = map(lambda x: min(x), portfolio_scores)
        # except TypeError: # in first iteration
        #     pass
        #=======================================================================
        
        return numpy.percentile(portfolio_scores, self._opt_Q)
    
    def __select_next_component(self, stats):
        '''
            select the next component for the portfolio given the distribution <stats> 
            with respect of the <thresholds>
            and the selection <self._criterion>
            Returns:
                index of next component of remaining algorithms (None if nothing was selected)
                statistics of selected portfolio (None if nothing was selected)
        '''
        sorted_stats = sorted(stats)
        min_index = stats.index(sorted_stats[0])
        return min_index, stats[min_index]
