'''
Created on 29.05.2013

@author: manju
'''

from sklearn.svm import SVR
import numpy

from trainer.selection.snnap import SNNAPTrainer
from trainer.selection.metatuner import MetaTuner
from misc.printer import Printer

class SVRRegressorSNNAP(SNNAPTrainer):
    '''
       uses a SVR (libsvm) to learn model for each algorithm
       sklearn.svm.SVR
       
       http://scikit-learn.org/dev/modules/generated/sklearn.svm.SVR.html#sklearn.svm.SVR
    '''


    def __init__(self, k, best_n=3, gamma=None, C=None, epsilon=None, save_models=True):
        '''
        Constructor
        '''
        SNNAPTrainer.__init__(self, k, best_n, save_models)
        self.__gamma = gamma
        self.__C = C         
        self.__epsilon = epsilon
          
        self.__SEED = 12345
    
    def __repr__(self):
        return "SVR-SNNAP"
    
    def _train_regression(self, y, X, weights):
        '''
            @overrides(ClassifierVoter)
            returns fitted model
        '''

        X = numpy.array(X)
        y = numpy.array(y)
        weights = numpy.array(weights)
        
        Printer.print_verbose("Train Regression Model with SVR")
        
        if self.__gamma is None or self.__C  is None or self.__epsilon is None:
            tuner = MetaTuner()
            tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1, 0.5, 0.25, 0.125, 0.0625],
                                 'C': [0.5, 1, 4, 16, 64], 'epsilon': [0.003,0.015,0.0625,0.25,0.5,1.0], 
                                'cache_size': [self._CACHE_SIZE]}] #'max_iter': [100],
            best_svr = tuner.tune(X, y, SVR, tuned_parameters)
            gamma = best_svr.gamma
            C = best_svr.C
            epsilon = best_svr.epsilon
        else:
            gamma = self.__gamma
            C = self.__C
            epsilon = self.__epsilon
            
        trainer = SVR(kernel='rbf', C=C, gamma=gamma, epsilon=epsilon,
                      cache_size=self._CACHE_SIZE, random_state=self.__SEED)
        trainer.fit(X,y,sample_weight=weights)
        
        return trainer
        
        