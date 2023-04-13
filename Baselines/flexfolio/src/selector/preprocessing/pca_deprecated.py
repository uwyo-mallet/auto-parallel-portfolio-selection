'''
Created on Nov 5, 2012

@author: manju
'''

from misc.printer import Printer
from Preprocessor import Preprocessor

class PCA_OLD(Preprocessor):
    '''
      pca normalization
      DEPRECATED
    '''


    def __init__(self,resMat, mean, std):
        '''
        Constructor
        '''
        self.__resMat = resMat
        self.__mean = mean
        self.__std = std
    
    def normalize(self,vect):
        '''
            pca transformation
            Args:
                vect: list of features
            Returns
                list of transformed features
        '''
        
        import numpy as np
        
        #Printer.print_c(">>> Running Feature Transformation! <<<")
        #print "vect ", vect
        vect = np.matrix(vect)
        #print "vect ", vect
        
        vect -= self.__mean
        vect /= np.where( self.__std, self.__std, 1. )
        
        matr = np.dot(self.__resMat,vect.T).T
        #print np.squeeze(np.asarray(matr))
        #return vect
        return list(np.squeeze(np.asarray(matr)))
        
        
