'''
Created on 30.05.2013

@author: manju
'''

import traceback

from sklearn.grid_search import GridSearchCV
from misc.printer import Printer

class MetaTuner(object):
    '''
       tunes the free parameter of sklearn ml techniques 
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        
    def tune(self, X, y, model, tuned_parameters):
        '''
          find instantiation of free parameters
          original implementation:
          http://scikit-learn.org/dev/auto_examples/grid_search_digits.html
          
          Args:
              X: matrix with observations
              y: vector of labels
              model: model class of sklearn ml techniques, e.g. sklearn.svm.SVC
              tuned_parameters: list of dictionaries with parameters to tune,e.g.
                      tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],
                             'C': [1, 10, 100, 1000]},
                            {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]
        '''
        
        Printer.print_nearly_verbose(">>> Tuning hyper-parameters")
        
        try:
            clf = GridSearchCV(model(), tuned_parameters, cv=5)
            clf.fit(X, y)
        except ValueError: # e.g., only one label in training data of libsvm
            traceback.print_exc()
            return model() # return default if error occured
        
        Printer.print_nearly_verbose("Best parameters set found on training set:")
        Printer.print_nearly_verbose(str(clf.best_estimator_))
        return clf.best_estimator_

        
