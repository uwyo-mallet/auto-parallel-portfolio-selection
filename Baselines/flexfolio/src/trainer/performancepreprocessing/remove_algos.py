'''
Created on Dec 10, 2014

@author: Marius Lindauer
'''
from misc.printer import Printer

class AlgoRemover(object):
    '''
        removes algorithms from training data
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
    def remove_algo(self, instance_dic, solver_list, config_dic, to_keep):
        '''
            removes all algorithms from <instance_dic>, <solver_list> and <config_dic> except <to_keep>
        '''

        if set(to_keep).difference(solver_list):
            Printer.print_e("List of Algorithms is not included in available algorithms: %s" %(str(set(to_keep).difference(solver_list))))
        
        to_removed = set(solver_list).difference(to_keep)
        for algo in to_removed:
            indx_algo = solver_list.index(algo)
            solver_list.pop(indx_algo)
            config_dic.pop(algo)
            for inst in instance_dic.values():
                inst._cost_vec.pop(indx_algo)
                inst._transformed_cost_vec.pop(indx_algo)
            
        return instance_dic, solver_list, config_dic
