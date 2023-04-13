'''
Created on Dec 5, 2013

@author: Marius Lindauer
'''

from misc.printer import Printer

class CorrelationPostProcessing(object):
    '''
        adds correlation scores to selector's scores
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def modify_score(self, list_conf_score, correlation_dic):
        '''
            adds correlation scores to selector's scores
            Args:
                list_conf_score: [(solver,score)]
                correlation_dic: solver -> solver -> correlation score \in [0,1]
            Returns:
                new list of (solver,scores)
                
        '''
        
        from numpy import argmin
        
        scores = map(float,[score for (_,score) in list_conf_score])
        solvers = [solver for (solver,_) in list_conf_score]
        
        scaled_scores = self.__min_max_scale(scores)
        scaled_scores_dict = dict((solver,score) for solver,score in zip(solvers, scaled_scores))
        
        new_scores = [(list_conf_score[0][0],scaled_scores[0])] # initial new scores with best element in list_conf_score
        unused_solvers = solvers[:]
        used_solvers = set([list_conf_score[0][0]])
        unused_solvers.remove(list_conf_score[0][0])
        
        while unused_solvers:
            step_scores = []
            for s in unused_solvers:
                correlations = [correlation_dic[s][used_s] for used_s in used_solvers]
                max_corr = max(correlations)
                scaled_score = scaled_scores_dict[s]
                step_scores.append(scaled_score + max_corr)
            solver_index = argmin(step_scores)
            solver = unused_solvers[solver_index]
            new_scores.append((solver,step_scores[solver_index]))
            used_solvers.add(solver)
            unused_solvers.remove(solver)
            

        Printer.print_verbose("Scores after Correlation Modification: %s" %(str(new_scores)))
        #print(list_conf_score)        
        #print(new_scores)
        return new_scores
    
    def __min_max_scale(self, list_):
        min_ = min(list_)
        max_ = max(list_)
        if min_ == max_:
            return [0 for _ in list_]
        return [((x - min_) / (max_ - min_)) for x in list_]
                
                
         