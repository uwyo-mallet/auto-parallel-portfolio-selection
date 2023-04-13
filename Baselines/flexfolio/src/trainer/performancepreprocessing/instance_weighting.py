'''
Created on Mar 25, 2013

@author: manju
'''
import math

from misc.printer import Printer

class InstanceWeighter(object):
    '''
        weight instances to improve learned models
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def weight_instances(self, instance_dic, metainfo):
        '''
            weight instances by the root mean squared distance to the minimal runtime       
            Args:
                metainfo: trainer.trainer_parser.coseal_reader.Metainfo()
                instance_dic: instance name -> Instance()
            Modifies: weights of all Instances() in <instance_dic>
        '''
        
        args_ = metainfo.options
        
        Printer.print_verbose("\n Instance Weighting")
        
        if args_.approx_weights == "max":
            for inst_ in instance_dic.values():
                runtimes = inst_._transformed_cost_vec
                weight = max(runtimes) - min(runtimes)
                inst_._weight = max(weight, 0.0001)# weight has to be large 0
                
        if args_.approx_weights == "rmsd":
            for inst_ in instance_dic.values():
                inst_._weight = max(self.__root_msd(inst_), 0.0001) # weight has to be large 0
    
        if args_.approx_weights == "nrmsd":
            weights = []
            inst_list = instance_dic.values()
            for inst_ in inst_list:
                weights.append(self.__root_msd(inst_))

            mean_weights, variance_weights = self.__mean_variance(weights)
            
            for inst_,weight in zip(inst_list,weights):
                normed_weight = ((weight - mean_weights) / math.sqrt(variance_weights)) + 10 
                inst_._weight = max(normed_weight, 0.0001)
    
    def __root_msd(self, inst_):
        '''
            root mean squared distance
        '''
        runtimes = inst_._transformed_cost_vec
        min_time = min(runtimes)
        mean_squared_dist = sum(list(math.pow(min_time - x,2) for x in runtimes)) / len(runtimes)
        root_msd = math.sqrt(mean_squared_dist)
        return root_msd
                
    def __mean_variance(self, list_):
        s2 = 0
        s = 0
        n = len(list_)
        for e in list_:
            s += e
            s2 += e * e
        mean = s / n
        variance = (s2 - (s*s) / n) / n
        return mean, variance
        
            