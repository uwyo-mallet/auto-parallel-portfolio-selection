'''
Created on 29.05.2013

@author: manju
'''

from sklearn.ensemble import RandomForestClassifier
from sklearn.multiclass import OneVsRestClassifier

import numpy

from trainer.selection.classifierMulti import ClassifierMulti
from trainer.selection.metatuner import MetaTuner
from misc.printer import Printer


class RandomForestMulti(ClassifierMulti):
    '''
       uses a SVM (libsvm) to learn pairwise models
       sklearn.svm.SVC
    '''


    def __init__(self, max_features=None, criterion=None, min_samples_leaf=None, save_models=True):
        '''
        Constructor
        '''
        ClassifierMulti.__init__(self, save_models)
        self.__max_features = max_features
        self.__criterion = criterion
        self.__min_samples_leaf = min_samples_leaf  
        
        self.__SEED = 12345    
        
    def __repr__(self):
        return "RANDOMFORREST-CLASSMULTI"  
    
    def _train(self, y, X, weights):
        '''
            @overrides(ClassifierVoter)
            returns fitted model
        '''
        
        X = numpy.array(X)
        y = numpy.array(y)
        weights = numpy.array(weights)
        
        Printer.print_verbose("Train OneVsRest Classifier with RandomForest")         
        
        if self.__criterion is None or self.__min_samples_leaf is None: # don't check max_features because it can be itentionally None
            estimator = RandomForestClassifier()
        else:
            estimator = RandomForestClassifier(max_features=self.__max_features, criterion=self.__criterion, 
                                               min_samples_leaf=self.__min_samples_leaf, random_state=self.__SEED)
        
        trainer = OneVsRestClassifier(estimator=estimator)
        trainer.fit(X,y)
        
        return trainer
        
        