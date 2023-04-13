'''
Created on Jun 28, 2013

@author: manju
'''
import numpy
from sklearn.mixture import GMM

from trainer.selection.Clustering import ClusteringTrainer
from misc.printer import Printer


class GMTrainer(ClusteringTrainer):
    '''
        see http://scikit-learn.org/stable/modules/generated/sklearn.mixture.GMM.html
    '''
    
    def __init__(self, max_clusters='log', plot_cluster=False, save_models=True):
        '''
            constructor
        '''
        ClusteringTrainer.__init__(self, max_clusters, plot_cluster, save_models)
    
        self.__SEED = 12345
        
    def __repr__(self):
        return "GM"
        
    def _train(self,X, Y, n_clusters):
        '''
            @overrides(ClusteringTrainer)
            returns fitted model
        '''
        
        X = numpy.array(X)
        
        Printer.print_verbose("Train Clustering with GM")  
        
        trainer = GMM(n_components=n_clusters, n_init=self._REPETITIONS, random_state=self.__SEED)
        
        model = trainer.fit(X)
        labels = model.predict(X)
        
        return labels