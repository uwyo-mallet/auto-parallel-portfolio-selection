'''
Created on Nov 20, 2012

@author: manju
'''
from abc import abstractmethod, ABCMeta

class Preprocessor(object):
    '''
        parent class for all normalization classes
    '''

    __metaclass__ = ABCMeta

    def __init__(self):
        '''
        Constructor
        '''
    
    @abstractmethod    
    def normalize(self,vect):
        '''
            normalize vector (vect) 
            Returns
                normalized vector
        '''