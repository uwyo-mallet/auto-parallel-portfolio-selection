'''
Created on 29.05.2013

@author: manju
'''

from sklearn.linear_model import Ridge
import numpy

from trainer.selection.regressionPairs import RegressionPairs
from trainer.selection.metatuner import MetaTuner
from misc.printer import Printer
from misc import printer

class RidgeRegressionPairs(RegressionPairs):
    '''
       uses a ridge regression for each algorihm
       sklearn.linear_model.Ridge
       
       http://scikit-learn.org/0.13/modules/generated/sklearn.linear_model.Ridge.html
    '''


    def __init__(self, alpha=None, save_models=True):
        '''
        Constructor
        '''
        RegressionPairs.__init__(self, save_models)
        self.__alpha = alpha
    
    def __repr__(self):
        return "RIDGE-REGRESSIONPAIRS"
    
    def _train_regression(self, y, X, weights):
        '''
            @overrides(ClassifierVoter)
            returns fitted model
        '''
        
        X = numpy.array(X)
        y = numpy.array(y)
        weights = numpy.array(weights)        
        
        Printer.print_verbose("Train Regression Model with Ridge Regression")  
        
        if self.__alpha is None:
            tuner = MetaTuner()
            tuned_parameters = [{'alpha': [16, 8, 4, 2, 1, 0.5, 0.125], 'max_iter': [100]}]
            best_reg = tuner.tune(X, y, Ridge, tuned_parameters)
            alpha = best_reg.alpha
        else:
            alpha = self.__alpha
        
        trainer = Ridge(alpha = alpha)
        try:
            trainer.fit(X,y,weights)
            return trainer
        except UnboundLocalError: #error in sklearn 14.1
            Printer.print_w("Regularization parameter alpha probably too small. Training failed. Return statically cutoff.")
            return None
        
        