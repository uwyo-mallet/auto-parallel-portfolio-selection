'''
Created on Nov 5, 2012

@author: manju
'''
from selector import Selector
from misc.printer import Printer

import math
import operator
import os

class NearestNeighbor(Selector):
    '''
        nearestNeighborhood selection
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    
    def select_algorithms(self, args, features, pwd=""):
        ''' select nearest neighbors '''
        
        self._set_base_args(args, features)
        
        self._normalize(self._normalization["approach"], self._normalization["filter"], features)
        
        if not self._features:
            return None
        
        model_file = args["approach"]["model"]
        
        solver_score_dic = self.__find_nearest_solver(model_file, self._features, pwd )

        sorted_scores = sorted(solver_score_dic.iteritems(),key=operator.itemgetter(1))
        
        Printer.print_nearly_verbose("\nConfiguration Scores:")
        for (solver,score) in sorted_scores:
            Printer.print_nearly_verbose("[%s]: %f" %(solver,score))
        
        return sorted_scores
        
    def __find_nearest_solver(self, model_file, features, pwd):
        '''
            look through all training instances and remember for each encountered solver the nearest distance
        '''
        fp = open(os.path.join(pwd,model_file),"r")
        solver_minDist_dic = {}
        
        for line in fp:
            line = line.replace("\n","")
            if not line.startswith("@") and line != "":
                splitted = line.split(",")
                inst_features = map(float,splitted[:-2]) # all but not last two elements (weight, solver)
                solver = splitted[-1]
                weight = float(splitted[-2])
                # weights are decreased to decrease the influence,
                # hence, 1/weight increases the distance
                distance = self.__get_euclidean_dist(features,inst_features) * (1/weight) 
                if distance < 0.00001:
                    Printer.print_w("I may encountered the given instance previously!")
                    Printer.print_w(str(features))
                    Printer.print_w(str(inst_features))
                if solver_minDist_dic.get(solver):
                    solver_minDist_dic[solver] = min(solver_minDist_dic[solver],distance)
                else:
                    solver_minDist_dic[solver] = distance
        fp.close()
        return solver_minDist_dic
                
    def __get_euclidean_dist(self,vect1, vect2):
        squares = list( math.pow(f1-f2,2) for f1,f2 in zip(vect1,vect2))
        sum_squares = sum(squares)
        return math.sqrt(sum_squares)
            