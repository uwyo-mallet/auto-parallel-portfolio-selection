'''
Created on Nov 20, 2012

@author: manju
'''
from misc.printer import Printer
from selector import SelectorTrainer
import numpy

import os
import math

class ClusteringTrainer(SelectorTrainer):
    '''
        Trainer for KMeans Algorithm Selector (inspired by 3S)
         1. Cluster in instances with KMEANS according to distance in feature space
         2. Get best solver for each instance cluster
         3. Save Model as NN approach
    '''


    def __init__(self, max_clusters='log', plot_cluster=False, save_models=True):
        '''
        Constructor
            Args:
                k_tuning: try to find the optimal number of clusters or not
                max_clusters: maximal number of solvers: 
                        log: log half of the number of instances
                        sqrt: sqrt half of the number of instances
                        solver: equal to the number of solvers
        '''
        SelectorTrainer.__init__(self, save_models)
        self.__max_clusters = max_clusters
        self.__plot_cluster = plot_cluster
        
        self._UNKNOWN_CODE = -512
        self._REPETITIONS = 100
        self.__SEED = 12345
    
    def train(self, instance_dic, solver_list, config_dic, cutoff, model_dir, f_indicator, n_feats):
        '''
            train model
            Args:
                instance_dic: instance name -> Instance()
                solver_list: list of solvers
                norm_approach: normalization approach
                cutoff: runtime cutoff
                model_dir: directory to save model
                f_indicator: of used features
                n_feats: number of features
        '''
        
        self._cutoff = cutoff
        
        feature_dic = {}
        weight_dic = {}
        
        # ensure same order of instances independently of memory allocation
        inst_keys = sorted(instance_dic.keys())
        for name in inst_keys:
            inst = instance_dic[name]
            if inst._pre_solved:
                continue
            feature_dic[name] = inst._normed_features
            weight_dic[name] = inst._weight
        
        if self.__max_clusters == 'log':
            maximal_clusters = int(math.log(len(feature_dic)/2))
            Printer.print_verbose("Using log half many clusters: %d" %(maximal_clusters))
        elif self.__max_clusters == 'sqrt':
            maximal_clusters = int(math.sqrt(len(feature_dic)/2))
            Printer.print_verbose("Using sqrt half many clusters: %d" %(maximal_clusters))
        elif self.__max_clusters == 'solvers':
            maximal_clusters = len(solver_list)
            Printer.print_verbose("Using as many clusters as solvers: %d" %(maximal_clusters))
        else:
            Printer.print_e("Unknown maximal number of clusters")
        
        feats = []
        instances = []
        performances = []
        inst_keys = sorted(instance_dic.keys())
        for name in inst_keys:
            inst = instance_dic[name]
            if inst._pre_solved:
                continue
            f = inst._normed_features
            p = inst._transformed_cost_vec
            feats.append(f)
            performances.append(p)
            instances.append(name)
            
        clusters = self._train(feats, performances, maximal_clusters) # list of clusters in the same order as input data
        
        #clusters = kMeanClusterer.doCluster(seed = self.__SEED, feature_dic = feature_dic, weight_dic = weight_dic,
        #                                    reps=self.__REPETITIONS, clus = maximal_clusters, 
        #                                    crossfolds=self.__CROSSFOLD)
        
        # map instance name to cluster
        maximal_clusters = max(maximal_clusters, max(clusters)+1)
        instance_cluster_list = []
        for _ in range(0,maximal_clusters):  instance_cluster_list.append([])
        for name, cluster in zip(instances, clusters):
            instance_cluster_list[cluster].append(name)
            
        centers = self.__find_centers(instance_cluster_list, instance_dic)
            
        best_solver_index  = self.__find_best_cluster_solver(instance_cluster_list, instance_dic)
        
        if self.__plot_cluster:
            self.__plot_clusters(instance_dic, instance_cluster_list, best_solver_index, solver_list, centers)
        
        best_solver = [solver_list[x] for x in best_solver_index]
        
        return self.__build_selection_dic(config_dic, solver_list, centers, best_solver, f_indicator)
    

    def _train(self,X, n_cluster):
        '''
            abstract function, will be overridden in subclasses
            Args:
                X: array-like matrix, shape=(n_samples, n_features)
                n_cluster: number of clusters
        '''

    def __save_model(self, model, model_dir):
        '''
            save model to files
            Args:
                models: clustering model
                model_dir: directory to save models
            Returns:
                list of file names for models
        '''
        from sklearn.externals import joblib
        
        files = []
        file_name = os.path.join(model_dir, 'clustering.model')
        joblib.dump(model, file_name, compress=9)
        files.append(file_name)
        return files
    
    def __find_centers(self, instance_cluster_list, inst_dic):
        '''
            find the centers of each cluster
            Args:
                instance_cluster_list: lists of lists of isntance names (one list per cluster)
                inst_dic: instance name -> Instance()
        '''
        n_feats = len(inst_dic[instance_cluster_list[0][0]]._normed_features) # not nice, but n_feats has not the correct number if pca was used
        centers = []
        for cluster in instance_cluster_list:
            n_samples = len(cluster)#
            center = numpy.array([0]*n_feats)
            for inst in cluster:
                inst_obj = inst_dic[inst]
                center = center + numpy.array(inst_obj._normed_features)
            center = center / n_samples
            centers.append(list(center))
        return centers
        
    
    def __collect_model(self, model, model_dir):
        '''
            collect models in a dictionary 
            Args:
                models: (solver i, solver j) -> Model()
                model_dir: directory to save models
            Returns:
                dict: theoretical file  name -> model
        '''
        
        model_dict = {}
        file_name = os.path.join(model_dir, 'clustering.model')
        model_dict[file_name] = model
        return model_dict

    def __find_best_cluster_solver(self, cluster_list, instance_dic):
        '''
            look for best solver for each cluster
            Args:
                cluster_list: list of list of instance names
                instance dic: instance name -> Instance()
            Returns:
                list of best solvers (index) in the same alignment as cluster_list
        '''
        
        n_solver = len(instance_dic.values()[0]._transformed_cost_vec)
        
        solver_cluster = []
        for cluster in cluster_list:
            if not cluster: # filter empty cluster
                continue
            performances = [0] * n_solver
            weigth_sums = [0] * n_solver
            sum_weights = 0
            for inst in cluster:
                times = instance_dic[inst]._transformed_cost_vec
                weight = instance_dic[inst]._weight
                sum_weights += weight
                # weight the instances -> lower weights => lower influence on best solver
                index = -1
                for time in times:
                    index += 1
                    if time == self._UNKNOWN_CODE:
                        continue
                    performances[index] += time*weight
                    weigth_sums[index] += weight
            performances = [performances[index]/weigth_sums[index] for index in range(0,n_solver)]
            best_perf = min(performances)
            best_index = performances.index(best_perf)
            solver_cluster.append(best_index)
        return solver_cluster
    
    def __plot_clusters(self, instance_dic, instance_clusters, best_solver_index, solver_list, centers):
        '''
            plot clusters in the first two dimensions of the features space
            Args:
                instance_dic: instance name -> Instance()
                instance_clusters: list of lists of instance names for each cluster
                centroids: list of centroids coordinates
                best_solver_index: list of indexes of best solver for each cluster 
                solver_list: list of solver names
        '''
        import numpy as np
        import matplotlib.pyplot as plt

        markers = {1: 'o', -1: 'x'}
        
        n_clusters = len(instance_clusters)
        colormap = plt.cm.gist_ncar
        colors = [colormap(i) for i in np.linspace(0, 0.9, max(best_solver_index)+1)]
        for cluster_index in range(0,n_clusters):
            ax = plt.subplot(1,1,1)
            x = {} # status -> x points
            y = {} # status -> y points
            cluster_insts = instance_clusters[cluster_index]
            center = centers[cluster_index]
            for inst_name in cluster_insts:
                coord = instance_dic[inst_name]._normed_features
                status = instance_dic[inst_name]._ground_truth["satunsat"] #TODO: generalize
                x[status] = x.get(status,[])
                y[status] = y.get(status,[])
                x[status].append(coord[0])
                y[status].append(coord[1])
            for status in x.keys():
                ax.scatter(x[status],y[status],marker=markers[status], s=30, c=colors[best_solver_index[cluster_index]], label=solver_list[best_solver_index[cluster_index]])
            #ax.scatter(center[0],center[1], marker='o', s=500, linewidth=2, c='none')
            #ax.scatter(center[0],center[1], marker='x', s=500, linewidth=2)
        
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
            
        # prevent from adding legends many times
        handles, labels = ax.get_legend_handles_labels()
        already_seen = set()
        labels_set = []
        handles_set = []
        for handle,label in zip(handles,labels):
            if not label in already_seen:
                already_seen.add(label)
                labels_set.append(label)
                handles_set.append(handle)
                
        ax.legend(handles_set[::-1], labels_set[::-1], loc='center left', bbox_to_anchor=(1, 0.5))
        
        plt.show()
    
    def __build_selection_dic(self, config_dic, solver_list, centers, best_solver_index, f_indicator):
        '''
            see function name
        '''
        
        conf_dic = {}
        for solver,cmd in config_dic.items():
                    solver_dic = {
                          "call": cmd,                  
                          "id" : solver_list.index(str(solver))          
                          }
                    conf_dic[solver] = solver_dic
        sel_dic = {
                   "approach": {
                                "approach" : "KMEANS",
                                "solvermapping" : best_solver_index,
                                "centers" : centers
                                },
                   "normalization" : {
                                      "filter"  : f_indicator                           
                                 },
                   "configurations":conf_dic                        
                   }
        return sel_dic