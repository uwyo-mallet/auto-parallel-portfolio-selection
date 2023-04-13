'''
Created on Feb 13, 2013

@author: Marius Lindauer
'''

import heapq

from misc.printer import Printer

class ContributorFilter(object):
    '''
         filters all algorithms which does not contribute at least n percent to the VBS 
    '''


    def __init__(self, threshold):
        '''
        Constructor
        '''
        self.__threshold = threshold + 1
        
    def filter(self, instance_dic, solver_list, config_dic):
        '''
            main method of this class (see class description)
            Args:
                instance_dic: instance name -> Instance()
                solver_list: list of solver names (in the same order as saved runtimes in Instance()
                config_dic: solver name -> solver call
        '''
        
        
        #while True:
        while len(solver_list) > 2: # CVSH FIX: Don't remove all solvers... that will cause a crash. Leave at least 2 to decide between.
            contributions = self.__calc_contributions(instance_dic, len(solver_list))
            min_contr = min(contributions)
            if min_contr < self.__threshold:
                # remove algorithms with minimal contribution
                min_index = contributions.index(min_contr) 
                self.__remove_minimal_contributor(instance_dic, min_index)
                solver_name = solver_list[min_index]
                config_dic.pop(solver_name)
                solver_list.pop(min_index)
            else:
                break
        Printer.print_c(" ")
        Printer.print_c("Remaining algorithms after contributor filtering:")
        Printer.print_c(",".join(solver_list))
        Printer.print_c(" ")
        return instance_dic, solver_list, config_dic
    
    def __calc_contributions(self, instance_dic, n_solver):
        '''
            gets the marginal contribution of each algorithms
            Args:
                instance_dic: instance name -> Instance()
                n_solver: number of solvers
            Returns:
                list of contributions per algorithm
        '''
        contributions = n_solver*[0]
        oracle = 0
        
        for inst in instance_dic.values():
            times = inst._cost_vec[:]
            min1, min2 = heapq.nsmallest(2, times)
            oracle += min1
            contribution = min2 - min1
            contributor = times.index(min1)
            contributions[contributor] += contribution
            
        perc_contributions = map((lambda contr: self.__percent_contribution(contr,oracle)), contributions)
        return perc_contributions
    
    def __percent_contribution(self, contribution, oracle):
        return (contribution+oracle) / oracle
    
    def __remove_minimal_contributor(self, instance_dic, min_index):
        '''
            remove algorithm with minimal contribution to oralce from data set
            Args:
                instance_dic: instance name -> Instance()
                min_index: minimal contributor index
        '''
        
        for inst in instance_dic.values():
            #print("%s: %d (t) vs %d (m)" %(inst.get_name(),len(times), min_index))
            inst._cost_vec.pop(min_index)
            inst._transformed_cost_vec.pop(min_index)
        
