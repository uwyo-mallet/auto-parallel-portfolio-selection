'''
Created on Nov 5, 2012

@author: manju
'''

from misc.printer import Printer
from Preprocessor import Preprocessor

class Zscore(Preprocessor):
    '''
    Zscore normalization (mean = 0 and standard deviation = 1)
    '''


    def __init__(self,means,stds):
        '''
        Constructor
        '''
        self.__means = means
        self.__stds = stds
    
    def normalize(self,vect):
        '''
            (x - u)/s for each x in vect
        '''
        n_vect = []
        if len(vect) == len(self.__means) and len(vect) == len(self.__stds):
            for x,u,s in zip(vect,self.__means,self.__stds):
                if s > 0.0:
                    n_vect.append( (x - u ) / s)
                else:
                    n_vect.append(0.0)
            return n_vect
        else:
            Printer.print_w("Lenght of Features does not correspond to given statistics (features: %d, stats: %d, %d)" 
                            % (len(vect), len(self.__means), len(self.__stds))
                            )
            return None