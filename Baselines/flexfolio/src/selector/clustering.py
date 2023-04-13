'''
Created on Jun 28, 2013

@author: manju
'''
from selector import Selector
from misc.printer import Printer

from sklearn.externals import joblib
import math
import operator


class Clustering(Selector):
    '''
        nearestNeighborhood selection
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    
    def select_algorithms(self, args, features, pwd=""):
        ''' selection based on nearest neighbor of clusters'''
        
        self._set_base_args(args, features)
        
        self._normalize(self._normalization["approach"], self._normalization["filter"], features)
        
        if not self._features:
            return None
        
        best_solver_list = args["approach"]["solvermapping"]
        center_list = args["approach"]["centers"]
        

        solver_score_dic = self.__find_nearest_solver(center_list, best_solver_list, self._features )
        sorted_scores = sorted(solver_score_dic.iteritems(),key=operator.itemgetter(1))
        
        Printer.print_nearly_verbose("\nConfiguration Scores:")
        for (solver,score) in sorted_scores:
            Printer.print_nearly_verbose("[%s]: %f" %(solver,score))
        
        return sorted_scores
        
    def __find_nearest_solver(self, center_list, best_solver_list, features):
        '''
            look through all training instances and remember for each encountered solver the nearest distance
        '''
        
        solver_minDist_dic = {}
        
        for center, solver in zip(center_list,best_solver_list):
            distance = self.__get_euclidean_dist(features,center)
            if distance < 0.00001:
                Printer.print_w("I may encountered the given instance previously!")
                Printer.print_w(str(features))
                Printer.print_w(str(center))
            if solver_minDist_dic.get(solver):
                solver_minDist_dic[solver] = min(solver_minDist_dic[solver],distance)
            else:
                solver_minDist_dic[solver] = distance
        
        return solver_minDist_dic
                
    def __get_euclidean_dist(self,vect1, vect2):
        squares = list( math.pow(f1-f2,2) for f1,f2 in zip(vect1,vect2))
        sum_squares = sum(squares)
        return math.sqrt(sum_squares)
            