'''
Created on Nov 5, 2012

@author: manju
'''
from selector import Selector
import operator
from misc.printer import Printer

class SBS(Selector):
    '''
        single best solver (best solver on the training set wrt. PAR10)
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    
    def select_algorithms(self, args, features, pwd=""):
        ''' select majority voted algorithm '''
        
        self._set_base_args(args, features)
        
        #self._normalize(self._normalization["approach"], self._normalization["filter"], features)
        
        #if not self._features:
        #    return None
        
        sorted_solvers = args["approach"]["solver"]
        
        solver_score_dic = dict(zip(sorted_solvers, range(len(sorted_solvers))))

        sorted_scores = sorted(solver_score_dic.iteritems(),key=operator.itemgetter(1))
        
        Printer.print_nearly_verbose("\nConfiguration Scores:")
        for (solver,score) in sorted_scores:
            Printer.print_nearly_verbose("[%s]: %f" %(solver,score))
        
        return sorted_scores
