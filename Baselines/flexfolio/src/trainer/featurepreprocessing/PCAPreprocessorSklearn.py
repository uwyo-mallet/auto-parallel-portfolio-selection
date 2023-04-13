'''
Created on Jul 26, 2012

@author: manju
'''
from misc.printer import Printer
from TrainPreprocessor import TrainPreprocessor


class PCAPreprocessor(TrainPreprocessor):
    '''
        decimal normalization class
        uses decimal point normalization to transform features to x' < 1
    
    __feature_dic = {}
    
    # computed
    __decs_ = []
    __keyOrder = []
    
    '''
    
    def __init__(self, feature_dic, n_components=8):
        self.__feature_dic = feature_dic
        
        self.__COMPONENTS = None
        self.__MEAN = None
        self.__MEAN_SCALER = None
        self.__STD_SCALER = None
        self.__n_components = n_components
        

    def normalize_features(self):
        ''' __normalize features with min-max normalization to [0,1]
            Args:
                Implicit over constructor!
            returns:
                dictionary of instances names to normlized features 
        '''
        
        #import numpy
        from sklearn.decomposition import PCA
        from sklearn.preprocessing import StandardScaler
        
        instance_order = list(self.__feature_dic.keys())
        A = []
        for name in instance_order:
            vect = self.__feature_dic[name]
            if len(vect) < self.__n_components: # cannot reduce the feature space, because it is already to small
                return self.__feature_dic
            A.append(vect)

        # zscore normalization
        scaler = StandardScaler()
        A = scaler.fit_transform(A)
        self.__MEAN_SCALER = scaler.mean_.tolist()
        self.__STD_SCALER = scaler.std_.tolist()
            
        # PCA
        pca = PCA(n_components=self.__n_components)
        transformed_A = pca.fit_transform(A).tolist()
        
        self.__COMPONENTS = pca.components_.tolist()
        self.__MEAN = pca.mean_.tolist()
        
        
        normalized_feature_dic = {}
        index = 0
        for name in instance_order:
            normalized_feature_dic[name] = transformed_A[index]
            index += 1
            
        return normalized_feature_dic 
  
    def get_stats(self):
        return {"n_components" : self.__n_components,
                "components" : self.__COMPONENTS,
                "mean" : self.__MEAN,
                "mean_scaler" : self.__MEAN_SCALER,
                "std_scaler" : self.__STD_SCALER
                }
    
 
