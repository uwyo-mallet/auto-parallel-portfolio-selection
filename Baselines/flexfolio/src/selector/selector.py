'''
Created on Nov 5, 2012

@author: manju
'''

import numpy as np
from types import UnicodeType
import pickle

from misc.printer import Printer
#normalizations
from preprocessing.zscore import Zscore
from preprocessing.linear import Linear
from preprocessing.dec import Dec
from preprocessing.pcaSklearn import PCATransformer

#selections
from abc import ABCMeta, abstractmethod
import copy

class Selector(object):
    '''
     abstract class for algorithm selection
    '''
    __metaclass__ = ABCMeta

    def __init__(self):
        '''
        Constructor
        '''
        self._normalization = ""
        self._configurations = {}
        self._features = []
        
    def _set_base_args(self,args,features):
        ''' set internal attributes according to command line arguments
            Parameter:
                args: dictionary with attributes
                features: list of float values
        '''
        self._normalization = args["normalization"]
        self._configurations = args["configurations"]
        self._features = features
        
    def _normalize (self, approach, f_indicator, features):
        '''
            normalize features according a selected method
            Parameter:
                approach: choice ["zscore"]
                features: vector with instance features 
        '''
        # 0. impute missing values
        if self._normalization["impute"]:
            if self._normalization["impute"] == -512:
                features = np.where(features == np.array(None), -512, features)
            else:
                if type(self._normalization["impute"]) is UnicodeType:
                    impute_file = open(self._normalization["impute"], "r")
                    self._normalization["impute"] = pickle.load(impute_file)
                    impute_file.close()
                    
                features = self._normalization["impute"].transform(features)[0].tolist() #TODO: if features = None, this could crash?
       
        # 1. normalization of features
        if approach["name"] == "zscore":
            if "means" in self._normalization and "stds" in self._normalization:
                normalizer = Zscore(self._normalization["means"],self._normalization["stds"])
            else:
                Printer.print_e("Missing Statistics for zscore (means and stds) in config file")
            
        if approach["name"] == "linear":
            if "maxs" in self._normalization and "mins" in self._normalization:
                normalizer = Linear(self._normalization["mins"],self._normalization["maxs"])
            else:
                Printer.print_e("Missing Statistics for linear norm. (mins and maxs) in config file")       
                
        if approach["name"] == "dec":
            if "decs" in self._normalization:
                normalizer = Dec(self._normalization["decs"])
            else:
                Printer.print_e("Missing Statistics for dec. norm. (d) in config file")    
        
        if approach["name"] == "pca":
            #if "mean" in self._normalization and "std" in self._normalization and "resMat" in self._normalization:
            #    normalizer = PCA(self._normalization["resMat"], self._normalization["mean"], self._normalization["std"])
            if "n_components" in self._normalization and "components" in self._normalization and "mean" in self._normalization \
	        and "mean_scaler" in self._normalization and "std_scaler" in self._normalization:
                normalizer = PCATransformer(self._normalization["components"], self._normalization["n_components"], self._normalization["mean"],
                                            self._normalization["mean_scaler"], self._normalization["std_scaler"]
                                            )
            else:
                Printer.print_e("Missing Statistics for PCA (mean, components and n_components) in config file")
                                
        # TODO: add additional normalization methods
        
        if approach["name"] != "none":
            self._features = normalizer.normalize(features)
        else:
            self._features = copy.deepcopy(features)
        
        if f_indicator and self._features is not None:
            for index in reversed(range(0,len(f_indicator))):
                if f_indicator[index] != 1:
                    self._features.pop(index)
                    
        if self._features is not None:    #CVSH original was: if self._features:
            Printer.print_verbose("Normed Features: "+",".join(map(str,self._features )))
        
    @abstractmethod
    def select_algorithms(self,args,features, pwd=""):
        '''
            select algorithms
            Parameter:
                args: dictionary with attributes
                features: list of float values
                pwd: directory of flexfolio (search path for models)
            Returns:
                ordered list of configurations with their decision values
        '''
        
        
