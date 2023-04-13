'''
Created on Nov 5, 2012

@author: manju
'''
import os, sys
from abc import ABCMeta, abstractmethod
from misc.printer import Printer

class FeatureExtractor(object):
    '''
      abstract class to extract feature of given instance
    '''
    #TODO: add runtime cutoff!

    __metaclass__ = ABCMeta
    
    
    def __init__(self):
        '''
        Constructor
        '''

    def _set_args(self,args_dic,instance):
        '''
            set internal attributes according to parsed input arguments
            Parameter:
                args_dic : dictionary with options
                instance : instance to solve
        '''
        
        self._cmd = args_dic["path"].split(" ")
        if not os.path.isfile(self._cmd[0]):
            extended = os.path.join(sys.path[-1],self._cmd[0]) #TODO: Hack to get path to flexfolio installation
            if os.path.isfile(extended):
                self._cmd[0] = extended
            else:
                Printer.print_e("Have not found feature extractor: %s" %(self._cmd[0]), exit_code=23)
                
                                        
        self._maxTime = args_dic["maxTime"]
        self._instance = instance
        
    @abstractmethod
    def run_extractor(self,args_dic,instance):
        '''
            run extractor and look for instance features
            Parameter:
                args_dic : dictionary with options
                instance : instance to solve
        '''
    
    def _timeout(self, p):
        if p.poll() == None:
            Printer.print_w("Feature computation could not finished! Use of backup solvers")
            p.terminate()
        