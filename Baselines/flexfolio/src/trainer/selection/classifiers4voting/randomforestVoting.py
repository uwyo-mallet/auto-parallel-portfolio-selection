'''
Created on 29.05.2013

@author: manju
'''

from sklearn.ensemble import RandomForestClassifier
import numpy

from trainer.selection.classifierVoter import ClassifierVoter
from trainer.selection.metatuner import MetaTuner
from misc.printer import Printer

class RandomForestVoting(ClassifierVoter):
    '''
       uses a random forest to learn pairwise models
       sklearn.ensemble.RandomForestClassifier
    '''


    def __init__(self, max_features=None, criterion=None, min_samples_leaf=None, save_models=True):
        '''
        Constructor
        '''
        ClassifierVoter.__init__(self, save_models)
        
        self.__max_features = max_features
        self.__criterion = criterion
        self.__min_samples_leaf = min_samples_leaf
    
        self.__SEED = 12345
        
    def __repr__(self):
        return "RANDOMFOREST-CLASSVOTER"
    
    def _train(self, y, X, weights):
        '''
            @overrides(ClassifierVoter)
            returns fitted model
        '''
        
        
        X = numpy.array(X)
        y = numpy.array(y)
        weights = numpy.array(weights)
        
        Printer.print_verbose("Train PairWise Classifier with RandomForest")  
        
        many_labels = numpy.any(y - min(y)) 
        if not many_labels:
            return y[0] # return simply the only label in this case
        
        if self.__criterion is None or self.__min_samples_leaf is None: # don't check max_features because it can be itentionally None
            tuner = MetaTuner()
            tuned_parameters = [{'max_features': ['sqrt','log2',None], 'criterion': ['gini','entropy'],
                             'min_samples_leaf' : [1,2,4,8,16,32]
                            }]
            best_clf = tuner.tune(X, y, RandomForestClassifier, tuned_parameters)
            max_features = best_clf.max_features
            criterion = best_clf.criterion
            min_samples_leaf = best_clf.min_samples_leaf
        else:
            max_features = self.__max_features
            criterion = self.__criterion
            min_samples_leaf = self.__min_samples_leaf
        
        trainer = RandomForestClassifier(max_features=max_features, criterion=criterion, 
                                         min_samples_leaf=min_samples_leaf, random_state=self.__SEED
                                         )
        trainer.fit(X,y,weights)
        
        #self.__plot_feature_importance(trainer)
                
        return trainer
    
    def __plot_feature_importance(self, forest):
        import numpy as np
        
        importances = forest.feature_importances_
        std = np.std([tree.feature_importances_ for tree in forest.estimators_],
                     axis=0)
        indices = np.argsort(importances)[::-1]
        
        # Print the feature ranking
        Printer.print_verbose("Feature ranking:")
        
        for f in range(10):
            Printer.print_verbose("%d. feature %d (%.2f +- %.2f)" % (f + 1, indices[f], importances[indices[f]], std[indices[f]]))
        
        #=======================================================================
        # # Plot the feature importances of the forest
        # import pylab as pl
        # pl.figure()
        # pl.title("Feature importances")
        # pl.bar(range(10), importances[indices][:10], color="r", yerr=std[indices][:10], align="center")
        # pl.xticks(range(10), indices)
        # pl.xlim([-1, 10])
        # pl.show()
        # 
        # 
        #=======================================================================