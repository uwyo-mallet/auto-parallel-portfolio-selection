'''
Created on Jun 30, 2015

@author: manju
'''
import numpy
import sys
from sklearn.cluster import KMeans

from trainer.selection.Clustering import ClusteringTrainer
from misc.printer import Printer


class CSHCTrainer(ClusteringTrainer):
    '''
        Cost sensitive hierarchical clustering
    '''
    
    def __init__(self, max_clusters='log', plot_cluster=False, save_models=True):
        '''
            constructor
        '''
        ClusteringTrainer.__init__(self, max_clusters, plot_cluster, save_models)
        
        self.__SEED = 12345
        
        self._MIN_CLUSTER_SAMPLES = 10
        
    def __repr__(self):
        return "CSHC"
        
    def _train(self,X, Y, max_clusters):
        '''
            @overrides(ClusteringTrainer)
            returns fitted model
        '''
        
        X = numpy.array(X)
        Y = numpy.array(Y)
        
        Printer.print_verbose("Train Clustering with CSHC")

        clusters = [range(X.shape[0])] # init: all instances are in the same cluster
        n_clusters = 1 # init: only 1 cluster
        loss_per_cluster = [sys.maxint] # associate a loss to each cluster (has to be minimized!)
        
        
        while n_clusters < max_clusters:

            # get cluster with worst loss and at least n samples
            insts = None
            for worst_cluster in numpy.argsort(loss_per_cluster)[::-1]:
                insts = clusters[worst_cluster]
                if len(insts) > self._MIN_CLUSTER_SAMPLES:
                    break
                
            if insts is None:
                break # all clusters are already too small!
            
            best_loss = sys.maxint
            best_split = (None, None)
            best_loss_split = (None, None)
            
            # find best splitting
            for inst in insts:
                for col in xrange(X.shape[1]):
                    # try all possible axis-parallel splits
                    split_value = X[inst,col]
                    
                    set_1, set_2 = [], []
                    for inst_in in insts:
                        if X[inst_in,col] >= split_value:
                            set_1.append(inst_in)
                        else:
                            set_2.append(inst_in)
                
                    y_set1 = Y[set_1]
                    y_set2 = Y[set_2]
                    
                    if len(set_1) < self._MIN_CLUSTER_SAMPLES or len(set_2) < self._MIN_CLUSTER_SAMPLES: # also after split each cluster has to respect the minimal sample size
                        continue
            
                    loss_set1 = self._get_loss(y_set1)
                    loss_set2 = self._get_loss(y_set2)
                    
                    if loss_set1 + loss_set2 < best_loss:
                        best_loss = loss_set1 + loss_set2
                        best_split = (set_1, set_2)
                        best_loss_split= (loss_set1, loss_set2) 
            
            if best_loss == sys.maxint:
                break # no splits found
        
            del clusters[worst_cluster]
            del loss_per_cluster[worst_cluster]
            clusters.append(best_split[0])
            clusters.append(best_split[1])
            loss_per_cluster.append(best_loss_split[0])
            loss_per_cluster.append(best_loss_split[1])
            
            n_clusters += 1 
            Printer.print_verbose("Clusters sizes: %s" %(str(map(lambda x: len(x), clusters))))
            Printer.print_verbose("Clusters loss: %s" %(str(loss_per_cluster)))
        
        labels = [0]*Y.shape[0]
        
        for id, clust in enumerate(clusters):
            for inst in clust:
                labels[inst] = id 

        return labels
    
    def _get_loss(self, Y):
        return numpy.min(numpy.sum(Y, axis=0)) - numpy.sum(numpy.min(Y, axis=1))
        
        