'''
Created on Nov 5, 2012

@author: manju
'''
from misc.printer import Printer
from Preprocessor import Preprocessor


class PCATransformer(Preprocessor):
    '''
      pca normalization
    '''


    def __init__(self,component, n_components, mean, mean_scaler, std_scaler):
        '''
        Constructor
        '''
        self.__n_components = n_components
        self.__components = component
        self.__mean = mean
        self.__mean_scaler = mean_scaler
        self.__std_scaler = std_scaler
    
    def normalize(self,vect):
        '''
            pca transformation
            Args:
                vect: list of features
            Returns
                list of transformed features
        '''
        import numpy
        from sklearn.decomposition import PCA
        from sklearn.preprocessing import StandardScaler
                
        # z score normalization
        scaler = StandardScaler()
        scaler.mean_ = numpy.array(self.__mean_scaler)
        scaler.std_ = numpy.array(self.__std_scaler)
        znormed_vect = scaler.transform(vect)
        
        #PCA
        pca = PCA(n_components=self.__n_components)
        pca.components_ = numpy.array(self.__components)
        pca.mean_ = numpy.array(self.__mean)
        
        normalized_vect = pca.transform(znormed_vect)
        
        return normalized_vect.tolist()[0]
        
