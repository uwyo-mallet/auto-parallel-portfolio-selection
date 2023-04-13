'''
Created on Nov 5, 2012

@author: manju
'''

import operator
import os

from sklearn.externals import joblib

from misc.printer import Printer
from selector import Selector

class ClassMulti(Selector):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def select_algorithms(self, se_dic, features, pwd=""):
        '''
            select algorithms
            Parameter:
                args: dictionary with attributes
                features: list of float values
                pwd: directory of flexfolio (search path for models)
            Returns:
                ordered list of configurations with their decision valuess
        '''
        
        self._set_base_args(se_dic, features)
        
        self._normalize(self._normalization["approach"], self._normalization["filter"], features)
        
        if self._features is None:    #CVSH original was: if not self._features:
            return None
        
        sorted_scores = self.__select(se_dic, pwd)    
        return sorted_scores
        
    def __select(self,se_dic, pwd):
        '''
            scores each configurations
            and returns a list (conf,score)
        '''
        
        x0 = [self._features]
        y0 = [0] # pseudo label
        

        
        conf_dic = se_dic["configurations"]
        n_solver = len(conf_dic)
        
        dic_solver_votes = dict([x,0] for x in range(0, n_solver))

        model_list =  se_dic["approach"]["models"]
        if isinstance(model_list, dict):
            # model_list is actually a dictionary -> model was not saved to file system
            model_file = model_list.keys()[0]
            model = model_list[model_file]
        else:
            # load model from file system
            model_file = se_dic["approach"]["models"][0]
            model = joblib.load(os.path.join(pwd,model_file))
            
        probs = model.predict_proba(x0)
        
        index = 0
        for class_ in model.classes_:
            if len(probs[0]) < index+1 : # if model is certain with probability 1.0 model.classes is not equal to size of prob vector
                dic_solver_votes[class_] = 1
            else:
                dic_solver_votes[class_] = 1 - probs[0][index]
                
            index += 1
        
        dic_solver_votes = self.__map_ids_2_names(dic_solver_votes, se_dic["configurations"])
        
        for name, votes in dic_solver_votes.items():
            Printer.print_verbose("%s : %.2f" %(name, votes))
        
        sorted_scores = sorted(dic_solver_votes.iteritems(),key=operator.itemgetter(1))
        
        Printer.print_nearly_verbose("\nConfiguration Scores:")
        for (solver,score) in sorted_scores:
            Printer.print_nearly_verbose("[%s]: %f" %(solver,score))
        
        return sorted_scores
        
        
    def __map_ids_2_names(self, dic_scores, conf_dic):
        '''
            map id of solver to its name
        '''
        dic_name_score = {}
        for solver_name, meta_dic in conf_dic.items():
            id = meta_dic["id"]
            dic_name_score[solver_name] = dic_scores[int(id)]
        return dic_name_score
                     
        