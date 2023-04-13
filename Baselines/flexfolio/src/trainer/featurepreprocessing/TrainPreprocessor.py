'''
Created on Nov 20, 2012

@author: manju
'''
from abc import abstractmethod, ABCMeta

class TrainPreprocessor(object):
    '''
       parent class to normalize a feature matrix
    '''
    
    __metaclass__ = ABCMeta

    def __init__(self, feature_dic):
        '''
        Constructor
        '''
        self.__feature_dic = feature_dic
        
    @abstractmethod
    def normalize_features(self):
        '''
            normalize self.__feature_dic and returns normalized version it
        '''