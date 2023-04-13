'''
Created on Jul 26, 2012

@author: manju
'''

#import math
from math import sqrt
from misc.printer import Printer
from TrainPreprocessor import TrainPreprocessor

class ZNormalizer(TrainPreprocessor):
    '''
        zscore normalization class
        uses zscore normalization to transform features to mean = 0 and variance = 1
   
    '''
    
    def __init__(self,feature_dic):
        self.__feature_dic = feature_dic
        
        # computed
        self.__means_ = []
        self.__stds_ = []
        self.__keyOrder = []
    
    def normalize_features(self):
        ''' __normalize features with min-max normalization to [0,1]
            Args:
                Implicit over constructor!
            returns:
                dictionary of instances names to normalized features 
        '''
        transposed_features = self.__transpose_dic_to_matrix(self.__feature_dic)
        self.__means_,self.__stds_ = self.__get_stastics(transposed_features)
        trans_normed_features = self.__normalize(transposed_features)
        self.__feature_dic = self.__transpose_matrix_to_dic(trans_normed_features)
        return self.__feature_dic
    
    def get_stats(self):
        return {"means":self.__means_, "stds":self.__stds_}
    
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
            get mean and variances of each row (/feature)
            Args:
                matrix: 
            Returns:
                a list of mean values and a list of variance values 
        '''
        means_ = []
        stds_ = [] 
        for line in matrix:
            x_s = []
            n = len(line)
            mean = sum(line)/n
            means_.append(mean)
            std_ = sqrt(sum((x-mean)**2 for x in line) / (n-1))
            stds_.append(max([std_,0.0001]))
        return means_,stds_
    
    def __normalize(self, matrix):
        '''
            perform z-score normalization on matrix
            previously stored means and variances are used here
            Args:
                matrix: 2d list
            Returns:
                matrix with normalized rows/features
        '''
        index = 0
        norm_matrix = []
        Printer.print_verbose("Means : "+str(self.__means_))
        Printer.print_verbose("Stds : "+str(self.__stds_))
        for row in matrix:
            new_row = []
            mean_ = self.__means_[index]
            std_ = self.__stds_[index]
            for value in row:
                new_row.append((float(value)-mean_)/std_)
            norm_matrix.append(new_row)
            index += 1
        return norm_matrix
    
    def __normalize_vector(self,vector):
        '''
            perform z-score normalization on a single vector
            previously stored means_ and variances are used here
            Args:
                vector: list
            Returns:
                list with zscore normalized values
        '''
        normed_vector = []
        index = 0
        means_ = self.__means_
        stds_ = self.__stds_
        for value in vector:
            normed_vector.append((float(value)-means_[index])/stds_[index])
            index += 1
        return normed_vector