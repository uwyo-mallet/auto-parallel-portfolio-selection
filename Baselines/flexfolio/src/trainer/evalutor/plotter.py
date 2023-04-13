'''
Created on May 16, 2013

@author: manju
'''
import os

class Plotter(object):
    '''
        plots some graphs with matplotlib
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    def plot_mulithreading(self, thread_perf_dic, oracle_perf, instance_set, metric="PAR10"):
        '''
            plots number of threads vs. performance 
            and adds at the lower bound the oracle speed
        '''
        
        import matplotlib.pyplot as plt
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        
        optimal_speedup = []
        x = []
        y = []
        for i in range(1,len(thread_perf_dic)+1):
            perf = thread_perf_dic[i]
            if perf <= 0:
                break
            else:
                x.append(i)
                y.append(perf)
                optimal_speedup.append(thread_perf_dic[1]/i)
        
        #t_line = ax.plot(list(thread_perf_dic.keys()),list(thread_perf_dic.values()), color="k", label="claspfolio")
        ax.plot(x,y, color="k", marker="+", markersize=15, label="flexfolio")
        ax.plot(x,optimal_speedup, color="k", marker="*", markersize=15, label="optimal speedup")
        ax.plot(x,[oracle_perf]*len(x), color="k", label="oracle")
        
        ax.set_xlabel("Number of Threads")
        ax.set_ylabel(metric)
        
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels)
        
        instances = os.path.basename(instance_set).strip(" ").replace(".csv","").replace(".arff","")
        plt.savefig("./BenchScripts/plots/"+instances+"-mt.pdf",format='pdf')
        #plt.show()
        
    def plot_spend_times(self, selected_solver_times, oracle_time, instance_set):
        '''
            plot how many runtime each solver got
            and the optimal distribution of runtimes
        '''
        
        import matplotlib.pyplot as plt
        import numpy as np
        width = 0.35
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        solvers = selected_solver_times.keys()
        indexes = np.arange(len(solvers))+0.5
        flexfolio = list(selected_solver_times[s] for s in solvers)
        oracle = list(oracle_time[s] for s in solvers)

        ax.bar(indexes,flexfolio, width, color="r", label="actual times spend")
        ax.bar(indexes+width, oracle, width, color="y", label="optimal times spend")
        
        ax.set_xticks(indexes+width)
        ax.set_xticklabels(solvers)
        
        ax.set_ylabel("Time in Sec.")
        
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels)
        instances = os.path.basename(instance_set).strip(" ").replace(".csv","").replace(".arff","")
        plt.savefig("./BenchScripts/plots/"+instances+"-spend.pdf",format='pdf')
        
    def plot_classes(self, dict_class_frac_tos, instance_set):
        '''
            plot the fraction of timeouts for each classes 
            Args:
                dict_class_frac_tos: class name -> faction of timeouts
                instance_set: name of instance set (base of output files)
        '''
        
        import matplotlib.pyplot as plt
        import numpy as np
        width = 0.35
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        classes_ = dict_class_frac_tos.keys()
        indexes = np.arange(len(classes_))

        fractions = list(dict_class_frac_tos.values())

        ax.bar(indexes,fractions, width, color="r")
        
        indexes = np.arange(1,len(classes_)+1,5)
        ax.set_xticks(indexes)
        #ax.set_xticklabels(classes_)
        #for ticks in ax.get_xticklabels():
        #    ticks.set_rotation(30)
        
        ax.set_ylabel("Fraction of Timeouts")
        
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels)
        
        #plt.setp(plt.xticks()[1], rotation=30)
        fig.autofmt_xdate()
        
        instances = os.path.basename(instance_set).strip(" ").replace(".csv","").replace(".arff","")
        plt.savefig("./BenchScripts/plots/"+instances+"-classes.pdf",format='pdf')
        
        