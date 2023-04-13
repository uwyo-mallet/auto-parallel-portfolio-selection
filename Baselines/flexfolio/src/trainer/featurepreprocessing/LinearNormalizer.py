'''
Created on Jul 26, 2012

@author: manju
'''

from TrainPreprocessor import TrainPreprocessor

class LNormalizer(TrainPreprocessor):
    '''
        linear normalization class
        uses min-max normalization to transform features to [0,1]
    
    __feature_dic = {}
    
    # computed
    __mins_ = []
    __maxs_ = []
    __keyOrder = []
    
    '''
    
    def __init__(self, feature_dic):
        self.__feature_dic = feature_dic
        
        # computed
        self.__mins_ = []
        self.__maxs_ = []
        self.__keyOrder = []
    
    
    def normalize_features(self):
        ''' __normalize features with min-max normalization to [0,1]
            Args:
                Implicit over constructor!
            returns:
                dictionary of instances names to normlized features 
        '''
        transposed_features = self.__transpose_dic_to_matrix(self.__feature_dic)
        self.__maxs_,self.__mins_ = self.__get_stastics(transposed_features)
        trans_normed_features = self.__normalize(transposed_features)
        self.__feature_dic = self.__transpose_matrix_to_dic(trans_normed_features)
        return self.__feature_dic
    
    def get_stats(self):
        return {"maxs":self.__maxs_, "mins":self.__mins_}
    
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
        maxs = []
        mins = [] 
        for row in matrix:
            maxs.append(max(row))
            mins.append(min(row))
        return maxs,mins
    
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
            max_ = self.__maxs_[index]
            min_ = self.__mins_[index]
            for value in row:
                if (max_ == min_):
                    new_row.append(0.0)
                else:
                    new_row.append(((value-min_) /(max_-min_)))
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
        mini = self.__mins_
        maxi = self.__maxs_
        for value in vector:
            if (mini[index] != maxi[index]):
                normed_vector.append((float(value)-mini[index])/(maxi[index] - mini[index]))
            else:
                normed_vector.append(0.0)
            index += 1
        return normed_vector