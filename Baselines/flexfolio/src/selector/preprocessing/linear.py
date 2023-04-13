'''
Created on Nov 5, 2012

@author: manju
'''

from misc.printer import Printer
from Preprocessor import Preprocessor

class Linear(Preprocessor):
    '''
    Linear normalization: [0,1]
    '''


    def __init__(self,mins,maxs):
        '''
        Constructor
        '''
        self.__mins = mins
        self.__maxs = maxs
    
    def normalize(self,vect):
        '''
            (x - min)/ (max - min)  for each x in vect
        '''
        n_vect = []
        if len(vect) == len(self.__mins) and len(vect) == len(self.__maxs):
            for x,mini,maxi in zip(vect,self.__mins,self.__maxs):
                if mini - maxi != 0.0:
                    n_vect.append( (x - mini ) / (maxi - mini))
                else:
                    n_vect.append(0.0)
            return n_vect
        else:
            Printer.print_w("Features %s" % (vect) )
            Printer.print_w("Lenght of Features does not correspond to given statistics (features: %d, stats: %d, %d)" 
                            % (len(vect), len(self.__mins), len(self.__maxs))
                            )
            return None