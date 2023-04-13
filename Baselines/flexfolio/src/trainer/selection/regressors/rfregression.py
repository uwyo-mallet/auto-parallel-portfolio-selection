'''
Created on 29.05.2013

@author: manju
'''

from sklearn.ensemble import RandomForestRegressor
import numpy

from trainer.selection.regression import Regression
from trainer.selection.metatuner import MetaTuner
from misc.printer import Printer

class RandomForrestRegression(Regression):
    '''
       uses a ridge regression for each algorihm
       sklearn.linear_model.Ridge
       
       http://scikit-learn.org/0.13/modules/generated/sklearn.linear_model.Ridge.html
    '''


    def __init__(self, max_features=None, min_samples_leaf=None, save_models=True):
        '''
        Constructor
        '''
        Regression.__init__(self, save_models)
        self.__max_features = max_features
        self.__min_samples_leaf = min_samples_leaf
    
        self.__SEED = 12345
    
    def __repr__(self):
        return "RANDOM-FOREST-REGRESSION"
    
    def _train_regression(self, y, X, weights):
        '''
            @overrides(ClassifierVoter)
            returns fitted model
        '''
        
        X = numpy.array(X)
        y = numpy.array(y)
        weights = numpy.array(weights)        
        
        Printer.print_verbose("Train Regression Model with RANDOM FOREST Regression")  
        
        if self.__min_samples_leaf is None: # don't check max_features because it can be itentionally None
            tuner = MetaTuner()
            tuned_parameters = [{'max_features': ['sqrt','log2',None],
                                 'min_samples_leaf' : [1,2,4,8,16,32]
                                 }]
            best_reg = tuner.tune(X, y, RandomForestRegressor, tuned_parameters)
            max_features = best_reg.max_features
            min_samples_leaf = best_reg.min_samples_leaf
        else:
            max_features = self.__max_features
            min_samples_leaf = self.__min_samples_leaf
        
        trainer = RandomForestRegressor(max_features=max_features,
                                         min_samples_leaf=min_samples_leaf, random_state=self.__SEED)
        trainer.fit(X,y,weights)
        
        return trainer
        
        