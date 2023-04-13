'''
Created on Nov 5, 2012

@author: manju
'''

from misc.printer import Printer
import math
from Preprocessor import Preprocessor

class Dec(Preprocessor):
    '''
    Decimal point normalization 
    '''


    def __init__(self,decs):
        '''
        Constructor
        '''
        self.__decs = decs
    
    def normalize(self,vect):
        '''
            x / 10^d  for each x in vect
        '''
        n_vect = []
        if len(vect) == len(self.__decs):
            for x,dec_ in zip(vect,self.__decs):
                n_vect.append( x / math.pow(10,dec_))
            return n_vect
        else:
            Printer.print_w("Features: %s" % (",".join(map(str,vect))) )
            Printer.print_w("Lenght of Features does not correspond to given statistics (features: %d, stats: %d)" 
                            % (len(vect), len(self.__decs))
                            )
            return None