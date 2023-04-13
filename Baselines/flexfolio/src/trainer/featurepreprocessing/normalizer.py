'''
Created on Aug 29, 2013

@author: Marius Schneider
'''

from trainer.featurepreprocessing.ZscoreNormalizer import ZNormalizer
from trainer.featurepreprocessing.LinearNormalizer import LNormalizer
from trainer.featurepreprocessing.DecimalNormalizer import DNormalizer
from trainer.featurepreprocessing.PCAPreprocessorSklearn import PCAPreprocessor

import numpy as np
import copy

class Normalizer(object):
    '''
        normalize features
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def normalize(self, inst_dict, norm, f_indicator=None, pca_dims=2):
        '''
            normalize inst_.__features to inst_.__normed_features according to <norm> strategy
        '''
                #extract dictionary instance name -> feature list
        feature_dic = {}
        for name, inst in inst_dict.items():
            feature_dic[name] = inst._features
        
        stats_ = {}
        normed_feature_dic = copy.deepcopy(feature_dic)
        # 1. normalization of features
        if norm == "zscore":
            normalizer = ZNormalizer(feature_dic)
        if norm == "linear":
            normalizer = LNormalizer(feature_dic)
        if norm == "dec":
            normalizer = DNormalizer(feature_dic)            
        if norm == "pca":
            normalizer = PCAPreprocessor(feature_dic, pca_dims) 

        if norm != "none":
            normed_feature_dic = normalizer.normalize_features()
            stats_ = normalizer.get_stats()

        zero_var = self.__get_invariant_features(normed_feature_dic)

        if f_indicator:
            f_indicator = map(lambda (x,y): -1 if x else y, zip(zero_var, f_indicator))
        else:
            f_indicator = map(lambda x: -1 if x else 0, zero_var == 0)

        for name, feature_list in normed_feature_dic.items():
            for index in reversed(range(0,len(f_indicator))):
                indicator = f_indicator[index]
                if indicator != 1:
                    #feature_list[index] = 0
                    feature_list.pop(index)
            normed_feature_dic[name] = feature_list
                    

        for name, inst in inst_dict.items():
            inst._normed_features = normed_feature_dic[name]

        #print(f_indicator)
        return inst_dict, stats_, f_indicator
    
    def __get_invariant_features(self, normed_feature_dic):
        '''
            remove features without variance
        '''
        
        feature_matrix = np.array(list(normed_feature_dic.values()), dtype=np.float64)
        variances = np.var(feature_matrix, axis=0)
        return variances == 0
        