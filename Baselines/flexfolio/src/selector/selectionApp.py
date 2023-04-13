'''
Created on Dec 5, 2013

@author: Marius Lindauer
'''

from score_postprocessing.correlation_postprocessing import CorrelationPostProcessing

class SelectionBase(object):
    
    
    @staticmethod
    def select(selector_name, se_dic, features, pwd=""):
        '''
            static method
            select algorithms and returns a list of scores for each algorithm
            (removes dependencies to flexfolio.selector from the outside
            and allows post processing of the scores)
            Args:
                selector_name: name of the selection approach
                se_dic: selection dict of the learned models
                features: feature vector
        '''
        
        # algorithm selection methods import
        from regression import Regression
        from regPairs import RegPairs
        from NN import NearestNeighbor
        from SBS import SBS
        from Ensemble import Ensemble
        from classVoting import ClassVoter
        from classMulti import ClassMulti
        from clustering import Clustering
        from snnap import SNNAP
        from KNN import KNearestNeighbor
        
        selector = {"CLASSVOTER": ClassVoter,
                "CLASSMULTI": ClassMulti,
                "REGRESSION" : Regression,
                "REGRESSIONPAIRS" : RegPairs,
                "NN": NearestNeighbor, 
                "kNN": KNearestNeighbor,
                "CLUSTERING": Clustering, 
                "SNNAP": SNNAP,
                "SBS": SBS,
                "ENSEMBLE": Ensemble
                }
        
        list_conf_scores = selector[selector_name]().select_algorithms(se_dic, features, pwd)

        if list_conf_scores is None:
            return None

        if se_dic["approach"].get("correlation"):
            postprocessor = CorrelationPostProcessing()
            list_conf_scores = postprocessor.modify_score(list_conf_scores, se_dic["approach"].get("correlation"))
        
        # ensure that every solver gets a score
        solvers = set(se_dic["configurations"].keys())
        scored_solvers = map(lambda x: x[0], list_conf_scores)
        unscored_solvers = solvers.difference(scored_solvers)
        for unscored in unscored_solvers:
            list_conf_scores.append((unscored,99999999999999999999999999))
        
        return list_conf_scores