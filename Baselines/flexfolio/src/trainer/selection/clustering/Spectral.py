'''
Created on Jun 28, 2013

@author: manju
'''
import numpy
from sklearn.cluster import SpectralClustering

from trainer.selection.Clustering import ClusteringTrainer
from misc.printer import Printer


class SpectralTrainer(ClusteringTrainer):
    '''
        see http://scikit-learn.org/stable/modules/generated/sklearn.cluster.SpectralClustering.html
    '''
    
    def __init__(self, max_clusters='log', plot_cluster=False, save_models=True):
        '''
            constructor
        '''
        ClusteringTrainer.__init__(self, max_clusters, plot_cluster, save_models)
    
        self.__SEED = 12345
    
    def __repr__(self):
        return "SpectralClustering"
        
    def _train(self,X, Y, n_clusters):
        '''
            @overrides(ClusteringTrainer)
            returns fitted model
        '''
        
        X = numpy.array(X)
        
        Printer.print_verbose("Train Clustering with GM")  
        
        trainer = SpectralClustering(n_clusters=n_clusters, n_init=self._REPETITIONS, random_state=self.__SEED)
        
        try:
            labels = trainer.fit_predict(X)
        except numpy.linalg.linalg.LinAlgError: # in case matrix is not semi positive definite; try to fix it with some constant
            try:
                labels = trainer.fit_predict(X + 0.00001)
            except:
                Printer.print_e("Feature Matrix is not semi positive definite", 1)
            
        return labels