'''
Created on Jul 26, 2012

@author: manju
'''

import numpy as np
from sklearn.preprocessing import Imputer as SKImputer

class Imputer(object):
    '''
        linear normalization class
        uses min-max normalization to transform features to [0,1]
    
    __feature_dic = {}
    
    # computed
    __mins_ = []
    __maxs_ = []
    __keyOrder = []
    
    '''
    
    def __init__(self, strategy):
        # computed
        self.__keyOrder = []
        self.__strategy = strategy
    
    def impute(self, inst_dic, n_feats):
        ''' __normalize features with min-max normalization to [0,1]
            Args:
                Implicit over constructor!
            returns:
                dictionary of instances names to normlized features 
        '''
        matrix = self.__transform_dic_to_matrix(inst_dic, n_feats)
        matrix, imp = self.__impute(matrix)
        inst_dic = self.__transform_matrix_to_dic(matrix, inst_dic)
        return inst_dic, imp
    
    def __transform_dic_to_matrix(self, inst_dic, n_feats):
        '''
            transform a dictionary with names to features into an matrix;
            saves the keys internally 
            Args:
                dic: dictionary with string -> int list
            Returns:
                2d matrix (2d list); one instance per row and one feature per coloumn
        '''
        matrix = []
        for name,inst in inst_dic.items():
            self.__keyOrder.append(name)
            if not inst._features:
                inst._features = [None]*n_feats
            matrix.append(inst._features)
        return matrix
    
    def __transform_matrix_to_dic(self, matrix, inst_dic):
        '''
            transpose a matrix to its corresponding dictionary;
            inverse method of __transpose_dic_to_matrix;
            uses internally saved keys!
            Args:
                matrix: 2d lists
            Returns:
                dictionary: string -> int list
        '''
        for feats, name in zip(matrix, self.__keyOrder):
            inst_dic[name]._features = feats.tolist()
        return inst_dic
    
    def __impute(self, matrix):
        '''
            impute feature values by???
            Args:
                matrix:
            Returns:
                matrix with imputed rows (/features)
        '''
        if self.__strategy == "-512":
            np_matrix = np.array(matrix)
            np_matrix = np.where(np_matrix == np.array(None), -512, np_matrix)
            return np_matrix, -512
        else:
            imp = SKImputer(missing_values='NaN', strategy=self.__strategy, axis=0)
            np_matrix = np.array(matrix)
            imp.fit(np_matrix)
            return imp.transform(np_matrix), imp
