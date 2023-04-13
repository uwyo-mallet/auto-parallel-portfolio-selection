'''
Created on Jun 28, 2013

@author: manju
'''
import numpy
from sklearn.cluster import KMeans

from trainer.selection.Clustering import ClusteringTrainer
from misc.printer import Printer


class KMeansTrainer(ClusteringTrainer):
    '''
        see http://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html#sklearn.cluster.KMeans.fit_predict
    '''
    
    def __init__(self, max_clusters='log', plot_cluster=False, save_models=True):
        '''
            constructor
        '''
        ClusteringTrainer.__init__(self, max_clusters, plot_cluster, save_models)
        
        self.__SEED = 12345
        
    def __repr__(self):
        return "KMEANS"
        
    def _train(self,X, Y, n_clusters):
        '''
            @overrides(ClusteringTrainer)
            returns fitted model
        '''
        
        X = numpy.array(X)
        
        Printer.print_verbose("Train Clustering with KMEANS")  
        
        trainer = KMeans(n_clusters=n_clusters,n_init=self._REPETITIONS,random_state=self.__SEED)
        
        labels = trainer.fit_predict(X)
        
        return labels