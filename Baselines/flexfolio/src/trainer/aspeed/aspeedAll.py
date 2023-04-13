'''
Created on Nov 29, 2012

@author: manju
'''
import os
from tempfile import NamedTemporaryFile
from subprocess import PIPE, Popen
import heapq

from misc.printer import Printer
from trainer.evalutor.crossValidator import CrossValidator
import operator

class AspeedAll(object):
    '''
       compute algorithm schedule based on given runtime data
    '''


    def __init__(self, clasp, gringo, runsolver, enc,
                 time_limit=900, mem_limit=4000, num_solvers=3, opt_mode=1, max_pre_slice=100000,
                 threads=1):
        '''
        Constructor
        '''
        self.__CLASP = clasp
        self.__GRINGO = gringo
        self.__ENC = enc
        self.__RUNSOLVER = runsolver
        self.__MEM_LIMIT = str(mem_limit) # memory limit of gringo and clasp in mb
        self.__TIME_LIMIT = str(time_limit) # captime of gringo and clasp in sec.
        self.__MAX_SLICE_OTHERS = max_pre_slice
        self.__DELETE = True
        self.__THREADS = threads 
        
        self.__max_feat_time = None
        self.write_tmp = None
        
        self.__NUM_SOLVERS = str(num_solvers) # exclusive flexfolio (if it is not selected, it gets nevertheless the unused time)
        self.__OPTMODE = str(opt_mode) # third optimization criterion (see encoding)
        
        if not os.path.isfile(self.__CLASP):
            Printer.print_e("[Aspeed] Not found: %s" % (self.__CLASP))
        
        if not os.path.isfile(self.__GRINGO):
            Printer.print_e("[Aspeed] Not found: %s" % (self.__GRINGO))
            
        if not os.path.isfile(self.__RUNSOLVER):
            Printer.print_e("[Aspeed] Not found: %s" % (self.__RUNSOLVER))
            
    def optimize_schedule(self, trainer, meta_info, instance_dict, config_dict):
        '''
            optimze schedule of backup solver and claspfolio 
            Args: 
                trainer: Trainer() object
                args_ : command line arguments
                instance_dict: instance name -> Instance() [Training set]
                solver_list: list with solver names
                config_dict: solver name -> call
                seed: random seed
        '''
        solver_list = meta_info.algorithms
        args_ = meta_info.options
        
        self.__max_feat_time = max(args_.feat_time,0)
        
        self.write_tmp = args_.model_dir
        
        Printer.print_c("\n>>> Algorithm Scheduler: Aspeed <<<\n")
        
        evaluator = CrossValidator(False,None)
        
        folds_back = meta_info.options.crossfold 
        meta_info.options.aspeed_opt = False #prevent infinite loop
        meta_info.options.crossfold = 10
        
        if args_.approach != "SBS":
            _, cf_inst_par10_dict = \
                    evaluator.evaluate(trainer, meta_info, instance_dict, config_dict, threads=self.__THREADS)
        else:
            cf_inst_par10_dict = None
        
        fact_file = self.__write_facts(cf_inst_par10_dict, instance_dict, meta_info.algorithm_cutoff_time)
        
        core_solver_time_dict = self.__call_solver(fact_file, solver_list)
        
        try:
            fact_file.close()
        except OSError:
            Printer.print_w("Failed to close file: %s" %(fact_file.name))
        
        if args_.approach != "SBS": 
            core_solver_time_dict = self.__fillup_schedule(core_solver_time_dict, instance_dict, solver_list)
        else:
            core_solver_time_dict = self.__fillup_schedule(core_solver_time_dict, instance_dict, solver_list, 
                                                           max_time=meta_info.algorithm_cutoff_time,
                                                           fill_all=True)
        
        # time not used by pre-solving schedule goes to selection module ("claspfolio")
        for solver_time_dict in core_solver_time_dict.values():
            delta = meta_info.algorithm_cutoff_time - sum(solver_time_dict.values())
            solver_time_dict["claspfolio"] += delta
        
        Printer.print_c("\nSchedule %s\n" % (str(core_solver_time_dict)))
        
        if args_.aspeed_concentrate:
            self.__mark_solved_instances(instance_dict, solver_list, core_solver_time_dict)

        Printer.print_c(">>> End of Algorithm Scheduler <<<\n")        
        
        # restore config
        args_.aspeed_opt = True
        args_.crossfold = folds_back
        
        return core_solver_time_dict
            
    def __write_facts(self, cf_dict, instance_dict, cutoff):
        '''
            write asp facts of solver runtimes
            Args:
                cf_dict: claspfolio performance: instance name -> par10
                instance_dict: instance name -> Instance()
                cutoff: captime for measured runtimes
        '''
        
        fp = NamedTemporaryFile(suffix=".facts", prefix="ASPEED", dir=self.write_tmp, delete=self.__DELETE)
        
        fp.write("kappa(%d).\n" %(int(cutoff)))
        
        instances = list(instance_dict.keys())
        
        #claspfolio time; solver c0
        if cf_dict:
            inst_index = 0
            for inst_name in instances:
                time =  cf_dict[inst_name]
                discrete_time = int(round(time + 0.4999999))
                fp.write("time(i%d,c%d,%d).\n" %(inst_index, 0, discrete_time))
                inst_index += 1
        
        #other solvers
        inst_index = 0
        for inst_name in instances:
            inst = instance_dict[inst_name]
            times = inst._cost_vec
            solver_index = 1
            for t in times:
                if t >= cutoff:
                    t = cutoff * 10
                discrete_time = int(round(t + 0.4999999))
                if discrete_time >= cutoff:
                    discrete_time = cutoff * 10 
                fp.write("time(i%d,c%d,%d).\n" %(inst_index, solver_index, discrete_time))
                solver_index += 1
            inst_index += 1
        
        fp.flush()
                
        return fp
                
    def __call_solver(self, fact_file, solver_list):
        '''
            call solver with given fact_file
            Args:
                fact_file: all asp facts for self.__ENC
        '''
        
        #TODO: number of maxsolvers has to be >= cores!
        
        gringo_options = ["-c","maxsolver="+str(self.__NUM_SOLVERS), 
                          "-c", "optMode="+str(self.__OPTMODE), 
                          "-c", "maxPreSlice="+str(self.__MAX_SLICE_OTHERS), 
                          "-c", "cores="+str(self.__THREADS),
                          "-c", "featTime="+str(self.__max_feat_time)]
        cmd_gringo = [self.__RUNSOLVER, "-w", "/dev/null", "-M", self.__MEM_LIMIT, "-W", self.__TIME_LIMIT, self.__GRINGO, self.__ENC, fact_file.name]
        cmd_gringo.extend(gringo_options)
        Printer.print_c(" ".join(cmd_gringo))
        ground_file = NamedTemporaryFile(suffix=".gr", prefix="GROUND", dir=self.write_tmp, delete=self.__DELETE)
        popen_gringo = Popen(cmd_gringo,stdout=ground_file)
        popen_gringo.communicate()
        
        
        cmd_clasp = [self.__RUNSOLVER, "-w", "/dev/null", "-M", self.__MEM_LIMIT, "-W", self.__TIME_LIMIT, self.__CLASP, ground_file.name,"--quiet=1,1"]
        Printer.print_c(" ".join(cmd_clasp))
        output_file = NamedTemporaryFile(suffix=".out", prefix="CLASP", dir=self.write_tmp, delete=self.__DELETE)
        popen_clasp = Popen(cmd_clasp, stdout=output_file)
        popen_clasp.communicate()
        
        return self.__parse_output(output_file, solver_list)
        
    def __parse_output(self, output_file, solver_list):
        '''
            parse output of clasp 
            assumption: clasp call with --quiet=1,1
            Args:
                output file of clasp (stdout)
        '''
        output_file.seek(0)
        
        core_solver_time_dict = dict([(idx,{"claspfolio": 0}) for idx in range(1,self.__THREADS+1)])
        
        for line in output_file:
            line = line.replace("\n","")
            Printer.print_nearly_verbose(line)
            if "slice" in line:
                slices = line.split(" ")
                for slice_ in slices:
                    slice_ = slice_.lstrip("slice(")
                    slice_ = slice_.rstrip(")")
                    core, solver, time = slice_.split(",")
                    solver = solver.lstrip("c")
                    if solver == "0":
                        solver = "claspfolio"
                    else:
                        solver = solver_list[int(solver) - 1]
                    core_solver_time_dict[int(core)][solver] = int(time)
        
        return core_solver_time_dict
    
    def __fillup_schedule(self, core_solver_time_dict, instance_dict, solver_list, max_time=None, fill_all=False):
        '''
            fill presolving schedule such that cores > 1 use at least self.max_feat_time
            Args:
                core_solver_time_dict: thread->solver->time slice
                instance_dic: instance name -> Instance()
                solver_list: list of solvers
        '''
        
        if not max_time:
            max_time = self.__max_feat_time
        
        if fill_all:
            min_threads = 1
        else:
            min_threads = 2
        
        if self.__THREADS > 1 or fill_all:
            
            # find fill up algorithms in case a core is not yet used
            #===================================================================
            # used_solvers = set()
            # for so_ti_dict in core_solver_time_dict.values():
            #     used_solvers.update(so_ti_dict.keys())
            # used_solvers.remove("claspfolio")
            # contributions = self.__calc_contributions(instance_dict, len(solver_list))
            # sol_contr = dict(zip(solver_list, contributions))
            # for used_solver in used_solvers:
            #     del sol_contr[used_solver]
            # sol_contr = sorted(sol_contr.items(), key=operator.itemgetter(1))
            #===================================================================
            
            for t in range(min_threads, self.__THREADS+1):
                solver_time_dict = core_solver_time_dict[t]
                used_time = sum(solver_time_dict.values())
                #if used_time == 0: # in case core is not yet used
                #    solver_time_dict[sol_contr.pop(0)[0]] = self.__max_feat_time
                if used_time > 0 and used_time < max_time:
                    delta = max_time - used_time
                    for solver, slice_ in solver_time_dict.items():
                        ratio = slice_ / float(used_time)
                        extra = ratio*delta
                        solver_time_dict[solver] = solver_time_dict[solver] + extra
                    
        return core_solver_time_dict
    
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
    
    def __mark_solved_instances(self, inst_dict, solver_list, core_solver_time_dict):
        '''
            set flag Instance.__pre_solved if it was solved by pre-solver schedule
            Args:
                sel_dict: dictionary with meta information about learned models
                solver_list: list of solvers 
                solver_time_dict: mapping solver to pre-solver time
        '''
        
        counter_removed = 0
        for inst_ in inst_dict.values():
            runtimes = inst_._cost_vec
            for t,s in zip(runtimes,solver_list):
                for solver_time_dict in core_solver_time_dict.values():
                    if solver_time_dict.get(s,0) > 0 and t >= solver_time_dict[s]:
                        inst_._pre_solved_by_schedule = True
                        Printer.print_verbose("%s solved by pre-solving schedule (%s)" %(inst_._name, s))
                        counter_removed += 1
                        break
        Printer.print_nearly_verbose("Number of instances marked as solved by pre-solving schedule: \t %d" %(counter_removed))       
            
        
        
    
