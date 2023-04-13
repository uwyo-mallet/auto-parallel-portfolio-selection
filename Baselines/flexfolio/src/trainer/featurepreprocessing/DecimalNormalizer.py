'''
Created on Jul 26, 2012

@author: manju
'''
import math
from decimal import Decimal, ROUND_UP
from TrainPreprocessor import TrainPreprocessor

class DNormalizer(TrainPreprocessor):
    '''
        decimal normalization class
        uses decimal point normalization to transform features to x' < 1
    
    __feature_dic = {}
    
    # computed
    __decs_ = []
    __keyOrder = []
    
    '''
    
    def __init__(self, feature_dic):
        self.__feature_dic = feature_dic
        
        # computed
        self.__decs_ = []
        self.__keyOrder = []
    
    
    def normalize_features(self):
        ''' __normalize features with min-max normalization to [0,1]
            Args:
                Implicit over constructor!
            returns:
                dictionary of instances names to normlized features 
        '''
        transposed_features = self.__transpose_dic_to_matrix(self.__feature_dic)
        self.__decs_ = self.__get_stastics(transposed_features)
        trans_normed_features = self.__normalize(transposed_features)
        self.__feature_dic = self.__transpose_matrix_to_dic(trans_normed_features)
        return self.__feature_dic
    
    def get_stats(self):
        return {"decs":self.__decs_}
    
    def __transpose_dic_to_matrix(self, dic):
        '''
            transpose a dictionary with names to features into an matrix;
            saves the keys internally 
            Args:
                dic: dictionary with string -> int list
            Returns:
                transposed 2d matrix (2d list); one instance per coloumn (outer lists) and one feature per row (inner lists)
        '''
        transposed_matrix = []
        for key,row in dic.items():
            self.__keyOrder.append(key)
            index = 0
            for value in row:
                try:
                    transposed_matrix[index].append(value)
                except LookupError:
                    transposed_matrix.append([value])
                index += 1
        return transposed_matrix
    
    def __transpose_matrix_to_dic(self, matrix):
        '''
            transpose a matrix to its corresponding dictionary;
            inverse method of __transpose_dic_to_matrix;
            uses internally saved keys!
            Args:
                matrix: 2d lists
            Returns:
                dictionary: string -> int list
        '''
        dic = {}
        for row in matrix:
            index = 0
            for value in row:
                try:
                    dic[self.__keyOrder[index]].append(value)
                except LookupError:
                    dic[self.__keyOrder[index]] = [value]
                index += 1
        return dic
    
    def __get_stastics(self, matrix):
        '''
            get min and maximal values of each row (/feature)
            Args:
                matrix: 
            Returns:
                a list of maximal values and a list of minimal values 
        '''
        decs = []
        for row in matrix:
            d = 0
            maxi = max(row)
            if maxi > 0.0:
                d = int(Decimal(math.log(maxi,10)).quantize(Decimal('1.'), rounding=ROUND_UP)) 
            else:
                d = 0
            decs.append(d)
        return decs
    
    def __normalize(self, matrix):
        '''
            min-max normalization to [0,1] (linear transformation)
            uses internally saved min and max values
            Args:
                matrix:
            Returns:
                matrix with normalized rows (/features)
        '''
        index = 0
        normed_matrix = []
        for row in matrix:
            new_row = []
            dec_ = self.__decs_[index]
            for value in row:
                new_row.append( value / math.pow(10,dec_))
            normed_matrix.append(new_row)
            index += 1
        return normed_matrix
    
    def __normalize_vector(self, vector):
        '''
            normalize a single vector wrt. to previously extracted min and max values (private) to [0,1]
            Args:
                vector:
            Returns:
                normalized vector with each entry in [0,1]
        '''
        normed_vector = []
        index = 0
        for value in vector:
            dec_ = self.__decs_[index]
            normed_vector.append( value / math.pow(10,dec_))
            index += 1
        return normed_vector