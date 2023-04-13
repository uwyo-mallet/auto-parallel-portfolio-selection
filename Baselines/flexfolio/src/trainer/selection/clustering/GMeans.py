'''
Created on Jun 28, 2013

@author: manju
'''
import numpy
from trainer.selection.clustering.gmeans_base import GMeans

from trainer.selection.Clustering import ClusteringTrainer
from misc.printer import Printer


class GMeansTrainer(ClusteringTrainer):
    '''
        gmeans implementation by Matthias Feurer
    '''
    
    def __init__(self, max_clusters='log', plot_cluster=False, save_models=True):
        '''
            constructor
        '''
        ClusteringTrainer.__init__(self, max_clusters, plot_cluster, save_models)
        
        self.__SEED = 12345
        
    def __repr__(self):
        return "GMEANS"
        
    def _train(self,X, Y, n_clusters):
        '''
            @overrides(ClusteringTrainer)
            returns fitted model
        '''
        
        X = numpy.array(X)
        
        Printer.print_verbose("Train Clustering with GMEANS")  
        
        trainer = GMeans(n_init=self._REPETITIONS,random_state=self.__SEED, restarts=1, minimum_samples_per_cluster=10)
        
        labels = trainer.fit_predict(X)
        
        return labels