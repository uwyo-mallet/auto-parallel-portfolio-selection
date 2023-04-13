'''
Created on Nov 5, 2012

@author: manju
'''

import os
from subprocess import Popen,PIPE
import threading
from thread import start_new_thread
from tempfile import NamedTemporaryFile
import time
import sys
import signal
from StringIO import StringIO
import operator

from misc.printer import Printer

class Executor(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.__lock_start      = threading.Condition(threading.Lock())
        self.__lock_finished   = threading.Condition(threading.Lock())
        self.__lock_waiting    = threading.Condition(threading.Lock())
        self.__processes = []
        self.__logfiles = []
        self.__running_threads = []
        self.__unfinished = 0
        self.__n_running = 0
        
        self.__time = -1
        self.__solver = ""
        self.__status = 1
        
        self.__KILL_DELAY = 1
        
    def __set_args(self, threads, configurations, confs_scores, env_):
        '''
            set internal attributes according to command line options
        '''
        self._threads = threads
        self._configurations = configurations
        self._confs_scores = confs_scores
        self._env = env_
    
    def execute(self, threads, configurations, confs_scores, instance, env_, quit_ = True):
        '''
            exectues best n configurations in scores
            Parameter:
                threads: number of solvers to execute in parallel
                configurations: possible configurations
                confs_scores: sorted list of (confs,scores)
                instance: name of instance to solver
                env_: environment
                quit_ : quit of solving?
        '''
        
        self.__set_args(threads, configurations, confs_scores, env_)
        
        signal.signal(signal.SIGINT, self.__clean_up_with_signal)
        if self._env == "aspcomp":
            signal.signal(signal.SIGHUP, self.__clean_up_with_signal)
            signal.signal(signal.SIGQUIT, self.__clean_up_with_signal)
            signal.signal(signal.SIGSEGV, self.__clean_up_with_signal)
            signal.signal(signal.SIGTERM, self.__clean_up_with_signal)
            signal.signal(signal.SIGXCPU, self.__clean_up_with_signal)
            signal.signal(signal.SIGXFSZ, self.__clean_up_with_signal)
        
        # handling of instances? stdin or file input?
        
        if not self._env == "aspcomp": # no writing of file for asp comp, reading with stdin
            if isinstance(instance,StringIO):
                input_file = NamedTemporaryFile(prefix="Instance", dir=".", delete=True)
                instance.seek(0)
                input_file.writelines(instance.readlines())
                input_file.flush()
                instance = input_file.name
            else:
                instance = instance.name
        
        Printer.print_c("\nExecute:")
        
        pre_solving_schedule = {} # solver name -> presolving time
        for conf_name, conf_dict in self._configurations.items():
            if conf_dict.get("presolving_time"):
                pre_solving_schedule[conf_name] = conf_dict.get("presolving_time")
        
        cmd_list, pre_solving_schedule = self._build_cmd_list(threads, pre_solving_schedule)
        
        if pre_solving_schedule and threads < 2: # do not presolve in mt mode
            
            # sort schedule be execution time (first small time slices)
            sorted_pre_solving = sorted(pre_solving_schedule.iteritems(), key=operator.itemgetter(1))
            
            Printer.print_c("Pre Solving Schedule: %s" % (" -> ".join(map(str,sorted_pre_solving))))
            for pre_solver, pre_solve_time_core in sorted_pre_solving:
                if pre_solve_time_core.get("1"): #TODO: run also other pre-solving schedules
                    pre_solve_time = pre_solve_time_core["1"]
                else:
                    continue
                call_pre_solver = self._configurations[pre_solver]["call"]
                
                call_pre_solver = call_pre_solver.split(" ")
                cmd_pre_solving_list = [(pre_solver, -1.0, call_pre_solver)]
                Printer.print_c("")
                self.__start(cmd_pre_solving_list, instance, max_time = pre_solve_time)
                Printer.print_c("Waiting for Pre-Solver Notification (at most %d seconds)" %(pre_solve_time))
                self.__lock_waiting.wait()
                if self.__is_successful(self.__status, True):
                    Printer.print_c("Solved by Pre-Solver")
                    self.__clean_up(quit_)
                Printer.print_c("")
                
                Printer.print_verbose("Release Waiting Lock")
                self.__lock_waiting.release()
            
        Printer.print_c("Run selected solver(s)!")
        self.__start(cmd_list, instance)
        
        Printer.print_c("")        
        Printer.print_verbose("[0] Waiting for Notification")
        self.__lock_waiting.wait()
        Printer.print_verbose("[0] Notified - performing clean up")
        self.__clean_up(quit_)
        return self.__time, self.__solver, self.__status
    
    def _build_cmd_list(self, threads, pre_solving_schedule):
        '''
            build list of command line calls to execute in parallel
            Args:
                threads: number of threads to use
                pre_solving_schedule: name of pre solver -> pre solving time
            Return:
                list of command line calls
                updated pre solving schedule (running configuration are removed)
        '''
        cmd_list = []
        for t in range(0, min(len(self._confs_scores), threads)): # we cannot run more solvers than available in our models
            conf_2_exec = self._confs_scores[t][0]
            score = self._confs_scores[t][1]
            call = self._configurations[conf_2_exec]["call"]

            cmd = call.split(" ")
            cmd_list.append((conf_2_exec, score, cmd))
            #Printer.print_c("[%s]: %s" %(conf_2_exec,call))
            
            if pre_solving_schedule.get(conf_2_exec,None):
                pre_solving_schedule.pop(conf_2_exec) # remove executed configuration from presolving
        return cmd_list, pre_solving_schedule
        
    def __start(self, cmd_list, instance, max_time = -1):
        '''
            start solver
            Parameter:
                cmd_list: list of command line calls
                max_time: maximal running time
        '''
        self.__lock_waiting.acquire()
        
        for cmd in cmd_list:
            name = cmd[0]
            score = cmd[1]
            cmd = cmd[2]
            
            solver_log = NamedTemporaryFile(prefix="SolverLog", delete=True)
            self.__logfiles.append(solver_log)
            #watcher_log = NamedTemporaryFile(prefix="WatcherLog", delete=True)
            
            if self._env == "zuse" and len(cmd_list) < 8:
                cmd_prefix = ['taskset', '0xfe']
            else:
                cmd_prefix = []
                
            cmd_prefix.extend(map(str,cmd))
            cmd = cmd_prefix
            
            if self._env == "zuse":
                cmd.extend(["-q"])
            if self._env == "aspcomp":
                cmd.extend(["--outf=1","--quiet=1,1"])
            
            Printer.print_c("[%s (%f)]: %s" %(name, score, " ".join(cmd)))
            
            #execute
            self.__n_running += 1
            self.__running_threads.append(start_new_thread(self.__sole_solver, (cmd, instance, name, max_time, self.__n_running)))
        
    def __sole_solver(self, command_line, instance, name, max_time, id_):
        '''
            run a solver with command_line 
            Args:
                command_line: array with command_line call to start a solver
                instance: File() or StringIO()
                name: name of solver
                max_time: maximal running time
                id_: of thread to start
        '''        
        if not command_line:
            return 
        
        stdin_flag = False
        
        start_time = time.time()
        Printer.print_verbose("[%d] Try to acquire Start Lock" %(id_))
        self.__lock_start.acquire()
        Printer.print_verbose("[%d] Acquired Start Lock" %(id_))
        error_due_running = False
        if not os.path.isfile(command_line[0]):
            extended = os.path.join(sys.path[-1],command_line[0]) #TODO: Hack to get path to flexfolio installation
            if os.path.isfile(extended):
                command_line[0] = extended
            else:
                Printer.print_e("Have not found solver: %s" %(command_line[0]), exit_code=22)
        
        if self._env == "aspcomp": # no writing of file for asp comp, reading with stdin
            Printer.print_verbose("[%d] Solver has to read from stdin" %(id_))
            stdin_flag = True
            instance.seek(0)
            try:
                popen_ = Popen(command_line, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            except OSError:
                Printer.print_w("Could not execute: %s" %(" ".join(command_line)))
                Printer.print_verbose("[%d] Release Start Lock" %(id_))
                self.__lock_start.release()  
                error_due_running = True
        else:
            Printer.print_verbose("Solver has to read from file")
            if "$instance" in command_line:
                inst_index =  command_line.index("$instance")
                command_line[inst_index] = instance
            elif not instance.endswith(".gz"):
                command_line.append(instance)
            else:
                stdin_flag = True
                zcat_popen = Popen(["zcat", instance], stdout=PIPE)
                instance = zcat_popen.stdout
            try:
                popen_ = Popen(command_line, stdout=PIPE, stderr=PIPE, stdin=PIPE)
            except OSError:
                Printer.print_w("Could not execute: %s" %(" ".join(command_line)))
                Printer.print_verbose("[%d] Release Start Lock" %(id_))
                self.__lock_start.release()  
                error_due_running = True

        self.__unfinished += 1
        
        if not error_due_running:

            if max_time > 0:
                t = threading.Timer(max_time, self._timeout, [popen_])
                t.start()
            
            self.__processes.append(popen_)
        
            # if reading from stdin use stdin of popen object (not nice solution, but communicate(input) cannot be used here)
            reading_failed = False
            if stdin_flag:
                try:
                    popen_.stdin.write(instance.read())
                except IOError:
                    Printer.print_w("Interrupt while solver was reading from stdin")
                    reading_failed = True
            
            # allow other solvers to start
            Printer.print_verbose("[%d] Release Start Lock" %(id_))
            self.__lock_start.release()        
            
            # wait for solver to finish
            if not reading_failed:
                (out_,err_) = popen_.communicate()
        
            # ensure to cancel timer thread
            try:
                t.cancel()
            except:
                pass
            self.__processes.remove(popen_)
            
        Printer.print_verbose("[%d] Acquire Finish Lock" %(id_))
        self.__lock_finished.acquire()      # do not release lock to ensure no other solver overwrites the results
        self.__unfinished -= 1
        if error_due_running:
            self.__status = 1
        else:
            self.__status = popen_.returncode
        
        if self.__is_successful(self.__status):
            self.__time = time.time() - start_time
            self.__solver = name
            
            Printer.print_c("Solved by: "+" ".join(command_line))
            Printer.print_n(out_, False)
            self._notify_boss()
            
        else:
            if self.__unfinished == 0: #all solvers failed!
                Printer.print_w("(Pre)Solver was not successful!")
                self._notify_boss()
                
            self.__lock_finished.release()
            Printer.print_verbose("Released Finish Lock")
        Printer.print_verbose("[%d] Finished!" %(id_))
   
    def _notify_boss(self):
        '''
            notify main thread to terminate and clean up all other threads
        '''
        Printer.print_verbose("Thread: Acquire lock")
        self.__lock_waiting.acquire()
        Printer.print_verbose("Thread: Notify")
        self.__lock_waiting.notifyAll()
        Printer.print_verbose("Thread: Release")
        self.__lock_waiting.release()         

    def __is_successful(self, returncode, pre_solver=False):
        '''
            check returncode of solver
            and decides whether solving process was successful or not
            Args:
                returncode: of solver (integer)
                pre-solver: return code of presolver? (bool)
        '''
        if self._env == "aspcomp" and not pre_solver:
            if returncode in [10, 11, 20, 30, 31]: #see: https://www.mat.unical.it/aspcomp2013/files/aspoutput.txt
                return True
            else:
                return False
        else:
            if returncode in [10, 20, 30]: # standard returncodes of SAT community (10,20) + ASP specific
                return True
            else:
                return False
             
    def __clean_up_with_signal(self,signal,frame):
        self.__clean_up(True)
       
    def __clean_up(self, quit_):
        '''
            terminate all runnning solvers
            ensure beforehand only one threads calls this method!
            Args:
                quit_: whether to terminate flexfolio of execution or not (bool)
        '''
        # terminate all running threads
        self.__lock_start.acquire() # be sure that no one else is right now starting things
        for t_ in self.__running_threads:
            try:
                t_.exit()
            except:
                Printer.print_verbose("Kill thread: %d" %(t_))
        
        solver_id = 1
        for popen_ in self.__processes:
            try:
                #manual kill of process group
                p = Popen(["pkill","-TERM", "-P",str(popen_.pid)])
                p.communicate()
                Printer.print_verbose("SIGTERM send to %d" % (solver_id))
                #python kill of process
                #popen_.terminate()
                #Printer.print_verbose("SIGTERM send to %d" % (solver_id))
            except OSError:
                Printer.print_c("SIGTERM failed on %d" % (solver_id))
                pass    # already terminated
            solver_id += 1 
                
        time.sleep(self.__KILL_DELAY) # wait 1 second and than ensure killing with SIGKILL
        solver_id = 1
        for popen_ in self.__processes:
            try:
                popen_.kill()
                Printer.print_verbose("SIGKILL send to %d" % (solver_id))
            except OSError:
                Printer.print_verbose("SIGKILL failed on %d" % (solver_id))
                pass    # already terminated
            solver_id += 1 
            
        for log_ in self.__logfiles: # ensure closing of files
            try:
                log_.close()
            except:
                pass # in case it is already closed    
           
        if quit_:  
            if self._env == "aspcomp" and not self.__is_successful(self.__status):
                print("UNKNOWN")
            sys.exit(self.__status)
            
    def _timeout(self, p):
        '''
            terminate/kill process p (after a timeout)
            Args:
                p: instance of Popen()
        '''
        if p.poll() is None:
            Printer.print_w("Timeout of Presolver!")
            p.terminate()
            time.sleep(0.1)
            
        if p.poll() is None:
            time.sleep(self.__KILL_DELAY)
            Printer.print_verbose("Send KILL after timeout")
            try:
                p.kill()
            except:
                pass
        