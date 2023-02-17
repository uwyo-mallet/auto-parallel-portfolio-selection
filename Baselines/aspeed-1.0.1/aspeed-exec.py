#!/bin/python

# Author: Marius Schneider
# Date: Dec 2011

# script to execute a static solver schedule

import sys
import os
import argparse
import time
import tempfile
import json
import signal
import termios
import threading

from subprocess import Popen, PIPE

class ScheduleExecuter(threading.Thread):

    def __init__(self,id,schedule,inst,runsolver,pErr):
        self.id = id
        self.schedule = schedule
        self.inst = inst
        self.runsolver = runsolver
        self.pErr = pErr
        self.end = False
        self.p = None
        self.status = 0
        self.output = ""
        self.outF = None
        self.errF = None
        threading.Thread.__init__(self)

    def childStatus(self,watcherFp):
        watcherFp.seek(0)
        self.status = 0
        for line in watcherFp:
            #print(line)
            if (line.find("Child status") != -1):
                self.status = int(line.split(":")[1])
                break
            
    def executeSolver(self,bin,cutoff,args):
        watcher = tempfile.NamedTemporaryFile(delete=True)
        cmd = ['taskset', '0xfe',self.runsolver,"-M 10000","-W "+str(cutoff),"-w",str(watcher.name),bin]   
        if (args != ""):
            cmd.extend(args.split(" "))
        cmd.append(self.inst)
        sys.stdout.write("c "+str(self.id)+" "+" ".join(cmd)+"\n")
        self.p = Popen(cmd,stdout = self.outF, stderr = self.errF)  #work with tmpfiles because pipe can reach limit and block procs
        self.p.communicate()
        
      #  if (True):
        try: 
            self.outF.seek(0)
            self.errF.seek(0)
            errors = "".join(self.errF.readlines())
            output = "".join(self.outF.readlines())
       
            if (errors != "" and self.pErr == True):
                sys.stdout.write("c "+str(self.id)+" Errors: \n")
                for line in errors.split("\n"):
                    sys.stdout.write("c "+str(self.id)+" "+line+"\n")
            self.childStatus(watcher)
            sys.stdout.write("c "+str(self.id)+" status: "+str(self.status)+"\n")
            if (self.status == 10 or self.status == 20):  #status 10 SAT or 20 UNSAT
                self.output = output
                #print("c "+str(self.id)+" Output: ")
                #print(output)
            else:
                sys.stdout.write("c "+str(self.id)+" Solver has not found a model.\n")
                sys.stdout.write("c "+str(self.id)+" Try next Solver.\n")
        except:
            sys.stdout.write("c "+str(self.id)+" WARNING: Read of output files is not possible\n")
        #print(output)
    
    def executeSchedule(self):
        cumtime = 0
        for solverdata in self.schedule:
            for solver,meta in solverdata.items():
                sys.stdout.write("c "+str(self.id)+" Solver : "+solver+"\n")
                path = meta["path"]
                cutoff = meta["time"]
                args = meta["args"]
                try:
                    self.outF.close()
                    self.errF.close()
                except:
                    pass
                self.outF = tempfile.NamedTemporaryFile(delete=True)
                self.errF = tempfile.NamedTemporaryFile(delete=True)
                self.executeSolver(path,cutoff,args)
                if (self.status == 10 or self.status == 20 or self.end == True):
                    return
        self.end = True
    def run(self):
        self.executeSchedule()
    #time.sleep(1000)    
    
def readSchedule(sched):
    fp = open(sched,"r")
    schedule = json.load(fp)
    return schedule

def finisher(signal,frame):
    sys.stdout.write("c INTERRUPTED!\n")
    sys.stdout.write("c kill last solver\n")
    stati = 0
    sucSolverInd = 0
    sucSolver = -1
    for exe in executers:
        if (exe.status == 10 or exe.status == 20):
            stati = exe.status
            sucSolver = sucSolverInd
        sucSolverInd += 1
        exe.end = True
        exe.outF.close()
        exe.errF.close()
        try: 
            exe.p.terminate()
        except:
            pass
    time.sleep(0.1) # buffer time to be sure that threads can read outputs
    solverInd = 0
    for exe in executers:
        if (solverInd == sucSolver):
            sys.stdout.write("c OUTPUT: \n")
            sys.stdout.write(str(exe.output))
            sys.stdout.write("c WARNING: displayed time will be probably the runtime of the last solver (not the whole runtime!)\n")
            break
        solverInd += 1
    sys.exit(stati)

if __name__ == '__main__':
    
    description  = "usage: python -O seqexec.py --schedule [file] {options}\n"
    parser = argparse.ArgumentParser(prog="master.py",usage=description)
    req_group = parser.add_argument_group("Options")
    req_group.add_argument('--schedule', dest='schedFile', action='store', default="", required=True,  help='path to json schedule file')
    req_group.add_argument('--inst', dest='inst', action='store', default="", required=False,  help='instance to solve')
    req_group.add_argument('--runsolver', dest='runsolver', action='store', default="/home/wv/bin/linux/64/runsolver", required=False,  help='path to runsolver binary')
    req_group.add_argument('--maxT', dest='maxT', action='store', default=1, required=False, type=int,  help='maximal number of threads')
    req_group.add_argument('--printErr', dest='pErr', action='store_true', default=False, help='print error messages of solver')
    
    (args,params) = parser.parse_known_args()     
    
    
    if (os.path.isfile(args.schedFile) == False):
        sys.stderr.write("ERROR: schedule was not found!\n")
        sys.exit()
    
    if args.inst == "":
        inFile = sys.stdin
        fp = tempfile.NamedTemporaryFile(dir=".",delete=True)
        for line in inFile:
            fp.write(line)
            #line = inFile.readline()
        args.inst = fp.name
        fp.flush()

    #print(fp.name)
    #time.sleep(1000)

    signal.signal(signal.SIGINT,finisher)
    signal.signal(signal.SIGTERM,finisher)

    global executers
    executers = []
    
    schedules = readSchedule(args.schedFile)
    threadindex = 1
    for schedule in schedules:
        if (threadindex > args.maxT):
            break
        exe = ScheduleExecuter(threadindex,schedule,args.inst,args.runsolver,args.pErr)
        exe.start()
        executers.append(exe)
        threadindex += 1
        
    finished = False # one thread has solved instance
    allTerminated = False # all threads finished without result
    while (finished == False and allTerminated == False):
        allTerminated = True
        for exe in executers:
            if exe.status == 10 or exe.status == 20:
                finished = True
                break
            if exe.isAlive() == True:
                allTerminated = False
            time.sleep(0.1)
    finisher(signal.SIGTERM,"")
        