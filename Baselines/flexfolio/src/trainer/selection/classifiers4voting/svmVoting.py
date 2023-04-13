'''
Created on 29.05.2013

@author: manju
'''

from sklearn.svm import SVC
import numpy

from trainer.selection.classifierVoter import ClassifierVoter
from trainer.selection.metatuner import MetaTuner
from misc.printer import Printer

class SVMVoting(ClassifierVoter):
    '''
       uses a SVM (libsvm) to learn pairwise models
       sklearn.svm.SVC
    '''


    def __init__(self, gamma=None, C=None, save_models=True):
        '''
        Constructor
        '''
        ClassifierVoter.__init__(self, save_models)
        self.__gamma = gamma
        self.__C = C
        self.__SEED = 12345
        
    def __repr__(self):
        return "SVM-CLASSVOTER"
    
    def _train(self, y, X, weights):
        '''
            @overrides(ClassifierVoter)
            returns fitted model
        '''
        
        X = numpy.array(X)
        y = numpy.array(y)
        weights = numpy.array(weights)
        
        many_labels = numpy.any(y - min(y)) # libsvm cannot deal with data with only one label
        
        if not many_labels:
            return y[0] # return simply the only label in this case
        
        Printer.print_verbose("Train PairWise Classifier with SVM")  
        
        if self.__gamma is None or self.__C  is None:
            tuner = MetaTuner()
            tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1, 0.5, 0.25, 0.125, 0.0625, 0.0],
                                 'C': [0.5, 1, 4, 16, 64],
                                 'max_iter': [100], 'cache_size': [self._CACHE_SIZE]}]
            best_svm = tuner.tune(X, y, SVC, tuned_parameters)
            gamma = best_svm.gamma
            C = best_svm.C
        else:
            gamma = self.__gamma
            C = self.__C
        
        trainer = SVC(gamma=gamma, C=C, cache_size=self._CACHE_SIZE, random_state=self.__SEED)
        trainer.fit(X,y,sample_weight=weights)
        
        return trainer
        
        