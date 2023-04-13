'''
Created on 29.05.2013

@author: manju
'''

from sklearn.ensemble import GradientBoostingClassifier
import numpy

from trainer.selection.classifierVoter import ClassifierVoter
from trainer.selection.metatuner import MetaTuner
from misc.printer import Printer
import math

class GradientBoostingVoting(ClassifierVoter):
    '''
       uses a Gradient Boosting to learn pairwise models
       sklearn.ensemble.GradientBoostingClassifier
    '''


    def __init__(self, max_depth=None, min_samples_leaf=None, max_features=None, save_models=True):
        '''
        Constructor
        '''
        ClassifierVoter.__init__(self, save_models)
        
        self.__max_depth = max_depth
        self.__min_samples_leaf = min_samples_leaf
        self.__max_features = max_features
        
        self.__SEED = 12345
    
    def __repr__(self):
        return "GRADIENTBOOSTING-CLASSVOTER"
    
    def _train(self, y, X, weights):
        '''
            @overrides(ClassifierVoter)
            cannot use weights!
            returns fitted model
        '''
        X = numpy.array(X)
        y = numpy.array(y)
        weights = numpy.array(weights)

        many_labels = numpy.any(y - min(y)) 
        if not many_labels:
            return y[0] # return simply the only label in this case

        sqrt_n = max(1,int(math.sqrt(X.shape[1])))
        log2_n = max(1,int(math.log(X.shape[1],2)))

        # will be automatically translated in the next sklearn version
        if self.__max_features == "sqrt":
            self.__max_features = sqrt_n
        if self.__max_features == "log2":
            self.__max_features = log2_n

        Printer.print_verbose("Train PairWise Classifier with GradientBoosting")  

        if self.__max_depth is None or self.__min_samples_leaf is None: # don't check max_features because it can be itentionally None
            tuner = MetaTuner()
            tuned_parameters = [{'max_depth': [1,2,3,4,5,6], 'min_samples_leaf': [1,2,4,8,16,32],
                                 'max_features': [sqrt_n,log2_n,None]
                                 }]
            best_clf = tuner.tune(X, y, GradientBoostingClassifier, tuned_parameters)
            max_depth = best_clf.max_depth
            min_samples_leaf = best_clf.min_samples_leaf
            max_features = best_clf.max_features
        else:
            max_depth = self.__max_depth
            min_samples_leaf = self.__min_samples_leaf
            max_features = self.__max_features
            
        trainer = GradientBoostingClassifier(max_depth = max_depth, 
                                             min_samples_leaf = min_samples_leaf,
                                             max_features = max_features,
                                             random_state = self.__SEED
                                             )
        trainer.fit(X,y)
        
        return trainer
        
        