'''
Created on Dec 4, 2013

@author: Marius Lindauer
'''

import json

from misc.printer import Printer

class Correlator(object):
    '''
        computes correlation between algorithms
        on the base of spearman test (requires scipy.stats)
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def correlation_test(self, instance_dic, solver_list, factor=1):
        '''
            spearman correlation test between runtimes of solvers
            Args:
                solver_list: list of all used algorithm names 
                instance_dic: instance name -> Instance()
                factor: multiply with correlation score
            Returns:
                double dictionary: a1 -> a2 -> correlation \in [0,1]
        '''
        from scipy.stats import spearmanr
        
        n_solver = len(solver_list)
        
        runtime_matrix = list([] for _ in solver_list)
        for inst_ in instance_dic.values():
            times = map(lambda x: sum(inst_._cost["runtime"][x])/len(inst_._cost["runtime"][x]), solver_list)
            runtime_matrix = map(lambda (x,y): x.append(y) or x, zip(runtime_matrix,times))
        
        correlation_matrix = dict((solver,{}) for solver in solver_list)
        for index1,solver1 in zip(range(0,n_solver),solver_list):
            for index2,solver2 in zip(range(0,n_solver),solver_list):
                cor_coefficient,_ = spearmanr(runtime_matrix[index1],runtime_matrix[index2])
                correlation_matrix[solver1][solver2] = factor * cor_coefficient

        Printer.print_verbose(json.dumps(correlation_matrix, indent=2))
        return correlation_matrix

    def pairwise_contribution(self, instance_dic, solver_list, factor=1):
        '''
            compute pairwise: VBS performance - better runtime
        '''
         
        n_solver = len(solver_list)
        
        runtime_matrix = list([] for _ in solver_list)
        for inst_ in instance_dic.values():
            times = map(lambda x: sum(inst_._cost["runtime"][x])/len(inst_._cost["runtime"][x]), solver_list)
            runtime_matrix = map(lambda (x,y): x.append(y) or x, zip(runtime_matrix,times))
        
        bias_matrix = dict((solver,{}) for solver in solver_list)
        for index1,solver1 in zip(range(0,n_solver),solver_list):
            for index2,solver2 in zip(range(0,n_solver),solver_list):
                avg_s1 = sum(runtime_matrix[index1]) / len(runtime_matrix[index1])
                avg_s2 = sum(runtime_matrix[index2]) / len(runtime_matrix[index2])
                vbs_perf = map(lambda p: min(p[0],p[1]), zip(runtime_matrix[index1], runtime_matrix[index1]))
                vbs_avg = sum(vbs_perf) / len(vbs_perf)
                bias = min(avg_s1,avg_s2) - vbs_avg
                bias_matrix[solver1][solver2] = factor * bias
            bias_vec = [bias_matrix[solver1][solver2] for solver2 in solver_list]
            scaled_bias_vec = self.__min_max_scale(bias_vec)
            bias_matrix[solver1] = dict((solver2,-1*bias) for solver2,bias in zip(solver_list,scaled_bias_vec))

        Printer.print_verbose(json.dumps(bias_matrix, indent=2))
        return bias_matrix
        
    def __min_max_scale(self, list_):
        min_ = min(list_)
        max_ = max(list_)
        if min_ == max_:
            return [0 for _ in list_]
        return [((x - min_) / (max_ - min_)) for x in list_]