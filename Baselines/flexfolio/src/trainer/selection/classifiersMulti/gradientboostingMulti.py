'''
Created on 29.05.2013

@author: manju
'''

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.multiclass import OneVsRestClassifier

import numpy

from trainer.selection.classifierMulti import ClassifierMulti
from trainer.selection.metatuner import MetaTuner
from misc.printer import Printer
import math


class GradientBoostingMulti(ClassifierMulti):
    '''
       uses a SVM (libsvm) to learn pairwise models
       sklearn.svm.SVC
    '''


    def __init__(self, max_depth=None, min_samples_leaf=None, max_features=None, save_models=True):
        '''
        Constructor
        '''
        ClassifierMulti.__init__(self, save_models)
        self.__max_depth = max_depth
        self.__min_samples_leaf = min_samples_leaf
        self.__max_features = max_features     
        
        self.__SEED = 12345
    
    def __repr__(self):
        return "GRADIENTBOOSTING-CLASSMULTI"
    
    def _train(self, y, X, weights):
        '''
            @overrides(ClassifierVoter)
            returns fitted model
        '''
        
        X = numpy.array(X)
        y = numpy.array(y)
        weights = numpy.array(weights)
        
        sqrt_n = max(1,int(math.sqrt(X.shape[1])))
        log2_n = max(1,int(math.log(X.shape[1],2)))

        # will be automatically translated in the next sklearn version
        if self.__max_features == "sqrt":
            self.__max_features = sqrt_n
        if self.__max_features == "log2":
            self.__max_features = log2_n
        
        Printer.print_verbose("Train OneVsRest Classifier with Gradientboosting")  
        
        if self.__max_depth is None or self.__min_samples_leaf is None: # don't check max_features because it can be itentionally None
            estimator = GradientBoostingClassifier()
        else:
            estimator = GradientBoostingClassifier(max_depth = self.__max_depth, 
                                             min_samples_leaf = self.__min_samples_leaf,
                                             max_features = self.__max_features,
                                             random_state=self.__SEED
                                             ) 
        
        trainer = OneVsRestClassifier(estimator=estimator)
        
        trainer.fit(X,y)
        
        return trainer
        
        