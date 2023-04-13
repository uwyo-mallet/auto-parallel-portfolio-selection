'''
Created on Aug 29, 2013

@author: Marius Schneider
'''

import math
import numpy
import copy

class PerformanceTransformator(object):
    '''
        applies performance transformation to input data
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def transform(self, inst_dic, metainfo):
        '''
            transform inst_.runtimes depending on args_.perf_trans
        '''
        
        args_ = metainfo.options
        
        if args_.perf_trans == "log":
            for inst_ in inst_dic.values():
                runtimes = inst_._cost_vec
                runtimes = map(math.log,runtimes)
                inst_._transformed_cost_vec = runtimes
        elif args_.perf_trans == "zscore":
            for inst_ in inst_dic.values():
                runtimes = inst_._cost_vec
                mean_ = float(numpy.mean(runtimes))
                std_ = float(numpy.std(runtimes))
                if std_ == 0:
                    std_ = 1 
                runtimes = map(lambda x: (x-mean_)/std_, runtimes)
                inst_._transformed_cost_vec = runtimes
        else:
            for inst_ in inst_dic.values():
                inst_._transformed_cost_vec = copy.deepcopy(inst_._cost_vec)
        