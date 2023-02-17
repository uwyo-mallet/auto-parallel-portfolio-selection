#! /usr/bin/env python
# written by Marius Schneider (manju@cs.uni-potsdam.de)
# under GPL 3.0; available under http://www.gnu.org/copyleft/gpl.html
# written for scientific purpose; no warranty of bugs
# tested with python-2.7.1
# available at http://www.cs.uni-potsdam.de/wv/aspeed/

#example call:
# python2.7.1 aspeed.py --csv data.csv --enc ./enc/roland1-MinL2-Cores.lp --maxTime 600 --precision 0 --threads 4 --cutoff 900 --cores 8 --cutoffTest 900 --perm 4 --par 10 --confheader --instheader --testFile testdata.csv --printJSON

import sys
import os 
from subprocess import Popen, PIPE
import argparse
import tempfile
import time
import signal
import random
import itertools
import math
import json

def readInCSV(file,sep,instHeader,confHeader,to,prec,testset):
    ''' read csv file in an 2-dim array and split in training and test set (NOT USED ANYMORE!)
        file        : csv file to read runtimes
        sep         : seperator of csv file
        instHeader  : first column with instances names?
        confHeader  : first row with configuration names?
        to          : cutoff  
        prec        : precision to parse runtimes (10**prec)
        testset     : split in test and training set?
        RETURN
            matrix      : 2d array of runtimes (training)
            matrix2     : 2d array of runtimes (test)
            confs       : number of solvers/configurations
            mindex      : index of best solver
            min         : runtime of best solver
    ''' 
    fh = open(file,"r")
    matrix = []
    matrix2 = []
    first = False
    confs = 0
    timeoutsGlobTrain = []
    timeoutsGlobTest = []
    switch = False
    for line in fh:
        if (first==True and confHeader==True):
            first = False
            continue
        splits = line.split(sep)
        if (instHeader == True):
            splits = splits[1:len(splits)+1]
        splits = strlistToIntlist(splits,prec,True)
        timeoutsLocal = timeouts(splits,to)
        if (testset == True and switch == True):
            matrix2.append(splits)
            timeoutsGlobTest = sumList(timeoutsLocal,timeoutsGlobTest)
        else:
            matrix.append(splits)
            timeoutsGlobTrain = sumList(timeoutsLocal,timeoutsGlobTrain)
        switch = not(switch)
        if (confs != 0 and confs != len(splits)):
            print("WARNING: Not all rows have the same number of data points!")
        if (confs == 0):
            confs = len(splits)#
            

    if (testset == True):
        min = sys.maxint    # min timeouts
        mindex = 0
        print("Test Timeouts: "+str(timeoutsGlobTest))
        for t in timeoutsGlobTest:
            if (t < min):
                min = t
                mindex = timeoutsGlobTest.index(t)
        print("Test set: single best configuration ["+str(mindex+1)+"]: "+str(min))    
    
    min = sys.maxint
    mindex = 0
    for t in timeoutsGlobTrain:
        if (t < min):
            min = t
            mindex = timeoutsGlobTrain.index(t)
    print("Train set: single best configuration ["+str(mindex+1)+"]: "+str(min))
    
    fh.close()
    print("Size Trainingset: "+str(len(matrix)))
    if (testset == True):
        print("Size Testset: "+str(len(matrix2)))
    return [matrix,matrix2,confs,mindex,min]


def readIn(file,sep,instHeader,confHeader,prec,co):
    ''' read in data from file with seperator
        file        : csv file to read runtimes
        sep         : seperator of csv file
        instHeader  : first column with instances names?
        confHeader  : first row with configuration names?
        prec        : precision to parse runtimes (10**prec)
        co          : cutoff
        RETURN
            matrix      : 2d array of runtimes
            confs       : number of solvers/configurations
            configs     : names of configurations (empty if confHeader==False)
    '''
    matrix = []
    fh = open(file,"r")
    first = True        # first line
    confs = 0           # number of configurations
    configs = []
    for line in fh:
        line = line.replace("\n","")
        splits = line.split(sep)
        if (first==True and confHeader==True):  # filter first line if first line is header
            configs = splits[1:len(splits)]
            first = False
            continue
        if (instHeader == True):    # filter instance header (first col)
            splits = splits[1:len(splits)+1]
        try:
            splits = strlistToIntlist(splits,prec,True,co)
        except:
            sys.stderr.write(line+"\n")
            sys.exit(-1)
        matrix.append(splits)
        
        if (confs != 0 and confs != len(splits)):
            print("WARNING: Not all rows have the same number of data points!")
        if (confs == 0):
            confs = len(splits)#
    fh.close()
    return [matrix,confs,configs]

def crossSplit(matrix,folds):
    ''' cross validation split of data matrix in n folds
        matrix    : 2d array of runtimes
        folds     : number of folds of cross validation
        RETURN    
            foldmatrix    : 3d array (first dim: folds)
    '''
    foldmatrix = []
    insts = len(matrix)
    allInsts = insts
    foldSize = int(round(insts/folds))
    random.seed(12345)  # secure reproducibility
    usedInst = 0
    shouldInst = 0
    for fold in range(0,folds-1): # from first fold to folds-1
        foldmatrix.append([])
        foldSize += (shouldInst - usedInst)   # guarantee similar size of folds
        usedInst += foldSize
        shouldInst = int(round((allInsts*(fold+1))/folds)) 
        for i in range(1,foldSize+1):
            rIndex = random.randint(0,insts-1)
            insts += -1
            rInst = matrix.pop(rIndex)
            foldmatrix[fold].append(rInst)
        #print(len(foldmatrix[fold]))
    foldmatrix.append(matrix)  # last fold : left over items of matrix
    #print(len(foldmatrix[fold+1]))

    return foldmatrix

def mergeFolds(foldmatrix,exclude):
    ''' merge folds of splitted matrix, without excluded fold; returns training set
        foldmatrix    : 3d array of runtimes (first dim: folds of cross validation)
        exclude       : fold to exclude for next iteration of cross validation
        RETURN    
            mergedMatrix    : matrix with excluded fold
    '''
    mergedMatrix = []
    folds = len(foldmatrix)
    for f in range(0,folds):
        if (f != exclude):
            for m in foldMatrix[f]:
                mergedMatrix.append(m)
    return mergedMatrix

def singleBestSolver(matrix,co):
    ''' determine best single solver regarding timeouts 
        matrix    : 2d array of runtimes
        co        : cutoff
        RETURN
            sortedTimeouts     : sorted list of timeouts (solver,timeouts)
    '''
    solvers = len(matrix[0])
    timeoutsSolver = getConstDic(solvers,0)
    for inst in matrix:
        for s in range(0,solvers):
            if (inst[s] >= co):
                timeoutsSolver[s] += 1
                
    sortedTimeouts = sorted(timeoutsSolver.iteritems(), key=lambda (k,v): (v,k))
    #print(sortedTimeouts)
    return sortedTimeouts

def sortSolverByUnsolvedInst(matrix,schedule,coreMap):
    ''' sort solvers by the number of their timeouts under a given schedule
        matrix        : 2d array of runtimes
        schedule      : list of time slices
        coreMap       : list -> index of list (id of solver) mapped to value (core)
        RETURN
            heuperm   : permutation [[solver,core],...] sorted by the number of timeouts 
    '''
    solvers = len(matrix[0])
    timeoutsSolver = getConstDic(solvers,0)
    for inst in matrix:
        for s in range(0,solvers):
            if (inst[s] >= schedule[s]):
                timeoutsSolver[s] += 1
    sortedTimeouts = sorted(timeoutsSolver.iteritems(), key=lambda (k,v): (v,k))
    heuperm = []
    for s in sortedTimeouts:
        solver = s[0]
        if (schedule[solver] > 0):
            heuperm.append([solver, coreMap[solver]])
    print("sortedTimeouts : " +str(sortedTimeouts))
    return heuperm  # starts with best solver

def strlistToIntlist(list,prec,zeroElim,co):
    ''' cast a List<String> to List<Double>
        list     : list of strings
        prec     : precision to cast in integers (10**prec)
        zeroElim : eliminate runtimes of 0 to 1
        co       : cutoff 
    '''
    ret = []
    for l in list:
         if (float(l) < 0):
             l = sys.maxint
         time = int(float(l)*(10**int(prec)))
         delta = float(l) - float(time)
         if  delta > 0:  # aufrunden!
            time += 1
         if (time == 0 and zeroElim == True):
             time = 1 
         #print(str(float(time))+" : "+str(float(co)))
         if (float(time) == float(co)):
             time += 1 # secure that timeouts are real timeouts
         ret.append(time)
    return ret
            
def timeouts(list,to):
    ''' transform list of runtimes to a list of timeouts (0/1) 
        list    : list of runtimes
        to      : cutoff
        RETURN    
            ret    : list of timeouts indicators
    '''
    ret = []
    for l in list:
        if (l > to):
            ret.append(1)
        else:
            ret.append(0)
    return ret
            
def sumList(list1, list2):
    ''' sum up to lists
        list1    : first list
        list2    : second list
        RETURN    
            ret    : summed up list
    '''
    ret = []
    i = 0
    if (len(list2) == 0):
        return list1
    for l in list1:
        ret.append(l+list2[i])
        i += 1
    return ret

def writeASPFacts(matrix,to,maxSolver,best):
    ''' write facts in gringo syntax
        matrix    : 2d array of runtimes
        to        : cutoff
        maxSolver : number of maximal number of solvers to use
        best      : get uniform schedule of best complementary solvers
        RETURN
            newF    : filehandle to fact file
    '''
    newF = tempfile.NamedTemporaryFile(prefix="FACTS",dir=".",delete=True)
    #newF = open(outF,"w")
    instIndex = 0
    newF.write("kappa("+str(to)+").\n")
    newF.write("datas("+str(len(matrix))+").\n")
    newF.write("maxSolver("+str(maxSolver)+").\n")
    if(best == True):
        newF.write("best(1).\n")
    for inst in matrix:
        instIndex += 1
        confIndex = 0
        for time in inst:
            confIndex += 1
            newF.write("time(i"+str(instIndex)+", c"+str(confIndex)+","+str(time)+").\n")
    newF.flush()
    return newF

def callGringo(gringo,enc,factsFHList,runsolver,maxMem,cores,secCrit):
    ''' call gringo to ground instance
        gringo        : path to gringo
        enc           : filename of encoding
        factsFHList   : list of filehandles to files with facts
        runsolver     : path to runsolver
        maxMem        : maximal memory for gringo
        cores         : cores for schedule
        secCrit       : name of the secondary optimization criterion  
        RETURN    
            groundFile    : filehandle to grounded instances
    '''
    #print("gringo path")
    #print(gringo)
    groundFile = tempfile.NamedTemporaryFile(prefix="GROUND",delete=True)
    cmd = [runsolver, "-w", "/dev/null", "-M", str(maxMem), gringo, '-c cores='+str(cores),'-c opt='+str(secCrit),enc]
    for file in factsFHList:
        cmd.append(file.name)
    print(" ".join(cmd))
    p = Popen(cmd,stdout=groundFile,stderr = PIPE)
    (stdout, stderr ) = p.communicate()
    if (stderr != ""):
        print("Error Gringo: ")
        print(stderr)
    #factsFH.close()
    return groundFile

def callClasp(clasp,threads,grFile,runsolver,maxMem,maxTime,optStart,hOpt):
    ''' call clasp to solve
        clasp        : path to clasp binary
        threads      : number of threads for clasp
        grFile       : Filepoint to grounded file
        runsolver    : path to runsolver
        maxMem       : maximal memory for clasp
        maxTime      : maximal runtime for clasp
        optStart     : start value of optimization
        hOpt         : parameter value for --opt-hierarch (see clasp -h)
    '''
    cmd = [runsolver, "-w", "/dev/null", "-M", str(maxMem),"-W",str(maxTime), clasp, "--opt-hierarch="+str(hOpt),"--restart-on-model","--solution-recording","--quiet=1,1",grFile.name]
    #cmd = [runsolver, "-w", "/dev/null", "-M", str(maxMem),"-W",str(maxTime), clasp, "--threads",str(threads),"--opt-hierarch="+str(hOpt),"--restart-on-model","--solution-recording","--distribute=short","-p","./portfolio.txt","--quiet=1,1",grFile.name]
#    cmd = [runsolver, "-w", "/dev/null", "-M", str(maxMem),clasp, "--threads",str(threads),"--opt-hierarch="+str(hOpt),"--restart-on-model","--solution-recording","--distribute=short","-p","./portfolio.txt","--quiet=1,1","--dinit=0,20000","--dsched=+,10000,600",grFile.name]
    if (optStart != -1):
#        cmd.extend(["--opt-all",str(0)])
        cmd.extend(["--opt-value",str(optStart)])
    #else:
    #    cmd.extend(["--opt-all",str(29)])
    print(" ".join(cmd))
    p = Popen(cmd,stdout = PIPE, stderr = PIPE)
    (stdo, stderr) = p.communicate()
    if (stderr != ""):
        print("Error Clasp: ")
        print(stderr)   
    grFile.close()
    return stdo
    
def getConstVec(size,Const):
    ''' get a list filled with a constant
        size     : size of list
        Const    : constant 
        RETURN
            nullVec     : list
    '''
    nullVec = []
    for v in range(0,size): #changed 2.12.
        nullVec.append(Const)
    return nullVec

def getConstDic(size,Const):
    ''' get a dictionary filled with a constant
        size     : size of dictionary
        Const    : constant 
        RETURN
            nullVec     : dictionary {0:const, 1:const,...}
    '''
    nullVec = {}
    for v in range(0,confs):
        nullVec[v] = Const
    return nullVec    
    
def parseOutput(output,confs,prec):
    ''' parse output of clasp
        output    : output of clasp (has to include slice/2 and solverOnCore/3)
        confs     : number of configurations
        prec      : precison of used data (10**prec)
    '''
    nextAS = False
    vec = getConstVec(confs,0)
    coreMapping = getConstVec(confs,1)
    print(output)
    output = output.split("\n")
    for line in output:
        #print(line)
        if (nextAS == True):
            preds = line.split(" ")
            for p in preds:
                if (p.find("slice") != -1):
                    [core,id,time]  = p.replace("slice(","").replace(")","").split(",") #slice(core,id,time)
                    id = int(id.replace("c",""))
                    vec[id-1] = int(time)*(10**(-prec))
                    coreMapping[id-1] = int(core)
               # if (p.find("solverOnCore") != -1):
               #     [id,core] = p.replace("solverOnCore(","").replace(")","").split(",")
               #     id = int(id.replace("c",""))
               #     coreMapping[id-1] = int(core)
        if (line.find("Answer:")!=-1):
            nextAS = True
            vec = getConstVec(confs,0)
            coreMapping = getConstVec(confs,1)
        else:
            nextAS = False
    #print("Best Solution: "+str(vec))
    return [vec,coreMapping]
    
def evaluateSolution(vecSol,testset,singleBestC,kappa):
    ''' evaluate a schedule and the single best solver regarding timeouts
        vecSol         : list with solver time slices (index = solverID)
        testset        : 2d array of test data
        singleBestC    : index of single best solver
        kappa          : cutoff in sec.
        RETURN    
             singleBestTO    : timeouts of single best solver
             timeouts        : timeouts of schedule
    '''
    timeouts = 0
    singleBestTO = 0
    for data in testset:
        localtimeOut = True
        if (kappa <= data[singleBestC]):
            singleBestTO += 1
        for index in range(0,len(vecSol)):
            if (vecSol[index] >= data[index] and data[index] < kappa):
                localtimeOut = False
                break
        if (localtimeOut == True):
            timeouts += 1
    return [singleBestTO,timeouts]

def stockupUniform(vec,coreMap,cores,co,prec):
    ''' stock up uniformly solver time slices so that the sum of all time slices is kappa on all cores
        vec         : list with solver time slices (index = solverID)
        coreMap     : list -> index of list (id of solver) mapped to value (core)
        cores       : number of available cores
        co          : cutoff (kappa)
        prec        : precision of data rounding (10**prec)
        RETURN
        implicit: vec will be changed!
    '''
    numSolverOnCore = getConstVec(cores,0)#
    usedTimeOnCore = getConstVec(cores,0)
    #print(coreMap)
    for index in range(0,len(coreMap)):
        #print(coreMap[i]-1)
        usedTimeOnCore[coreMap[index]-1] += vec[index]
        if (vec[index] > 0):
            numSolverOnCore[coreMap[index]-1] += 1
    #print(usedTimeOnCore)
    restTimes = []
    for index in range(0,cores):
        if (numSolverOnCore[index] > 0):
            restTimes.append(float((co - usedTimeOnCore[index]))/numSolverOnCore[index])
        else:
            restTimes.append(0)
    #print(restTimes)
    for index in range(0,len(coreMap)):
        core = coreMap[index]
        addTime = restTimes[core-1]
        if (vec[index] != 0):
            vec[index] += addTime
    #print(vec)
    
def stockup2Uni(vec,coreMap,cores,co,prec):
    ''' stock up solver time slices so that the sum of all time slices is kappa on all cores and the time slices are uniform distributed
        vec         : list with solver time slices (index = solverID)
        coreMap     : list -> index of list (id of solver) mapped to value (core)
        cores       : number of available cores
        co          : cutoff (kappa)
        prec        : precision of data rounding (10**prec)
        RETURN
        implicit: vec will be changed!
    '''
    numSolverOnCore = getConstVec(cores,0)#
    usedTimeOnCore = getConstVec(cores,0)
    #print(coreMap)
    for index in range(0,len(coreMap)):
        #print(coreMap[i]-1)
        usedTimeOnCore[coreMap[index]-1] += vec[index]
        if (vec[index] > 0):
            numSolverOnCore[coreMap[index]-1] += 1
    restTimes = []
    for index in range(0,cores):
        if (numSolverOnCore[index] > 0):
            restTimes.append(float(co)/numSolverOnCore[index])
        else:
            restTimes.append(0)
    for index in range(0,len(coreMap)):
        core = coreMap[index]
        addTime = restTimes[core-1]
        if (vec[index] != 0):
            vec[index] = addTime

def stockup(vecSol,coreMap,cores,kappa,prec):
    ''' stock up solver time slices with highest runtime so that the sum of all time slices is kappa on all cores
        vecSol    : list with solver time slices (index = solverID)
        coreMap   : list -> index of list (id of solver) mapped to value (core)
        cores     : number of available cores
        kappa     : cutoff in sec
        prec      : precision of data rounding (10**prec)
        RETURN
          vecSol  : stocked up list of solver time slices 
    '''
    #print("unscaled: "+str(vecSol))
    notUsedCores = 0
    for c in range(1,cores+1):
        max = -1
        maxIndex = -1
        index = 0
        sum = 0
        for s in vecSol:
            if (coreMap[index] == c):
                vecSol[index] = vecSol[index] * (10**(prec)) # daten sind hochskaliert -> solution darf nicht runterskaliert sein!
                s = s * (10**(prec))
                if (s > max):
                    max = s
                    maxIndex = index
                sum += s
            index += 1
        delta = kappa - sum
        #print("core : "+str(c)+ "delta : "+str(delta) + " kappa: "+str(kappa) + "sum : "+str(sum) + " maxValue : "+str(vecSol[maxIndex])+" MaxIndex: "+str(maxIndex))
        if (maxIndex > -1):
            if (delta > 0):
                vecSol[maxIndex] += delta #increase solver with the biggest runtime
        else: 
            print("WARNING: Core "+str(c)+" is not used.")
            notUsedCores +=1
    if (notUsedCores > 1):
        print("# Used Cores: "+str(cores - notUsedCores))
        #print(str(vecSol))
    return vecSol

def intListToStrList (list):
    ''' float list to string list
        list    : list of float list
        RETURN
            ret    : list of doubles (rounded with 2 decimals)
    '''
    ret = []
    for l in list:
        ret.append(str(round(l,2)))
    return ret

def calcASPSchedule(train,test,args,confs,optStart,best=False):
    ''' calculate schedule with ASP
        train    : 2d array of training data
        test     : 2d array of test data
        args     : command line arguments
        confs    : start point of optimization process (e.g., timeouts of best solver)
        best     : True -> get uniform schedule with a limited number of solvers
        RETURN
            vecSol     : list of time slices (index = solverID)
            coreMap    : list of mappings to cores (index = solverID)
            factsFH    : file pointer to facts file in gringo syntax
    '''
    print("Writing!")
    if (best == False):
        factsFH = writeASPFacts(train,args.co,confs,best)
    else:
        factsFH = writeASPFacts(train,args.co,args.best,best)
    print(factsFH.name)
    #time.sleep(100)
    #print("Ground!")
    grFile = callGringo(args.gringo,args.enc,[factsFH],args.runsolver,args.maxMem,args.cores,args.secCrit)
    print("Solve!")
    output = callClasp(args.clasp,args.threads,grFile,args.runsolver,args.maxMem,args.maxTime,optStart,args.hOpt)
    print("Parse!")
    [vecSol,coreMap] = parseOutput(output,confs,int(args.prec))
    return [vecSol,coreMap,factsFH]

def calcBestN(sortedSinglePairs,n,cutoff,cores):
    ''' calculate schedule for the best n solvers 
        sortedSinglePairs : [[solverID,#TO],...]
        n                 : number of solvers to select
        cutoff            : cutoff in sec
        cores             : number of available cores
        RETURNS           : schedule list (Index = solverID)  
    '''
    solvers = len(sortedSinglePairs)
    timeLimitperSolver = round(float((cutoff * cores)) / n,2)
    schedule = getConstVec(solvers,0)
    for i in range(0,n):
        schedule[sortedSinglePairs[i][0]] = timeLimitperSolver
    #print(sortedSinglePairs)
    #print(schedule)
    return schedule
    
def printStats(unif,bestnSchedule,combiNSchedule,coreMap,vecSol,f,singleBestC,singleBestTO,unifTimeouts,bestNTimeouts,combiNTimeouts,timeouts):
    ''' print some stats for each fold of the cross validation
        unif              : uniform schedule
        bestnSchedule     : schedule of best N Solvers
        combiNSchedule    : best complementary solvers (ppfolio-like)
        coreMap           : list -> index of list (id of solver) mapped to value (core)
        vecSol            : list of time slices (normally "schedule" named)
        f                 : id of fold in cross validation
        singleBestC       : id of best solver
        singleBestTO      : timeouts of single best solver
        uniffTimeouts     : timeouts of uniform schedule
        bestNTimeouts     : timeouts of best solvers
        combiNTimoutes    : timeouts of best complementary solvers (ppfolio-like)
        timeouts          : timeouts of asp schedule
    '''
    print("Uniform  Schedule : \t"+"\t".join(intListToStrList(unif)))
    print("Best N Schedule :   \t"+"\t".join(intListToStrList(bestnSchedule)))
    print("ppfolio-like Schedule :   \t"+"\t".join(intListToStrList(combiNSchedule)))
    print("core mapping: \t\t"+"\t".join(intListToStrList(coreMap)))
    print("ASP Schedule:       \t"+"\t".join(intListToStrList(vecSol)))
    print("Single Best: Timeouts in "+str(f)+"-th fold ["+str(singleBestC+1)+"]: \t"+str(singleBestTO))    
    print("Uniform: Timeouts in "+str(f)+"-th fold: \t\t"+str(unifTimeouts))
    print("Best N: Timeouts in "+str(f)+"-th fold: \t\t\t"+str(bestNTimeouts))
    print("ppfolio-like: Timeouts in "+str(f)+"-th fold: \t\t\t"+str(combiNTimeouts))
    print("Schedule: Timeouts in "+str(f)+"-th fold: \t\t"+str(timeouts))
    
def getBestPermutations(matrix,schedule,cores,coreMap,permutate,co):
    ''' bruteforce search for best permutation
        matrix    : 2d list of runtimes
        schedule  : list of time slices
        cores     : number of cores
        coreMap   : list -> index of list (id of solver) mapped to value (core)
        permutate : true: do search, false: give performance of first permutation back
        co        : cutoff
        RETURN
             minPerm    : best permutation
             minTime    : corresponding runtime
             parTime    : corresponding par10 runtime
             sumTime/math.factorial(len(permutstart)) : performance of average permutation
    '''
    index = 0
    permutstart = []
    for s in schedule:
        if (s != 0):
            permutstart.append([index,coreMap[index]])
        index += 1
    if (permutate == True):
        allPerm = itertools.permutations(permutstart)
        print("Number of Permutations: "+str(math.factorial(len(permutstart))))
        minTime = sys.maxint
        minParTime = sys.maxint
        minPerm = []
        sumTime = 0
        for p in allPerm:
            [pTime,parTime,unsolved,t] = evaluatePermutation(matrix,p,schedule,args.cores,args.par,co)
            sumTime += pTime
            if (pTime < minTime):
                minTime = pTime
                minPerm = list(p)
                minParTime = parTime
        print("Best Permutation: "+str(minTime))
        print("AVG Permutation: "+str(sumTime/math.factorial(len(permutstart))))
    else:
        minPerm = permutstart
        minTime = 0
        parTime = 0
        sumTime = 0
    return [minPerm,minTime,parTime,sumTime/math.factorial(len(permutstart))]
    
def evaluatePermutation(matrix,permut,schedule,cores,par,co):
    ''' evaluate a permutation on runtimes 
        matrix    : 2d list of runtimes
        permut    : permutation of solvers (list) ([solver,core]) - ordering important!
        schedule  : list of time slices
        cores     : number of cores
        par       : factor of PAR score
        co        : cutoff
        RETURN
            sumtime     : sum of runtimes
            sumParTime  : sum of PAR-scores
            unsolved    : number of unsolved instances
            times       : runtime of each instance
    '''
    
    #print("Schedule: "+str(schedule))
    #print(permut)
    instanceCoreTime = []
    instanceCoreParTime = []
    iIndex = 0
    unsolved = 0
    times = []  # list of minimal runtimes
    for inst in matrix:
        instanceCoreTime.append([])
        instanceCoreParTime.append([])
        solved = False
        for c in range(1,cores+1):
            time = 0
            solvedOnCore = False
            for p in permut:
                solver = int(p[0])
               # print(str(solver) + " "+str(schedule[solver]))
                core = int(p[1])
                if (core == c):
                    #print(str(inst[solver])+" : "+str(schedule[solver]))
                    time += min([schedule[solver],inst[solver]])
                    #print(str(schedule[solver]) +" : "+str(inst[solver]) + " : "+str(min([schedule[solver],inst[solver]])))
                    if(inst[solver] <= schedule[solver]):
                        solved = True
                        solvedOnCore = True
                        break
            if (solvedOnCore == False):
                partime = time * par    # PAR10      
            else:
                partime = time
            #print(time)
            if (time != 0):
                instanceCoreTime[iIndex].append(time)
                instanceCoreParTime[iIndex].append(partime)
        if(solved == False):
            unsolved += 1
        iIndex += 1
    #print(instanceCoreTime)
    sumtime = 0
    sumParTime = 0
    for i in instanceCoreTime:
        if len(i) > 0:
            mini = min(i)
            if (mini > co):
                mini = co
            sumtime += mini
            times.append(str(mini))
    for i in instanceCoreParTime:
        if len(i) > 0:
            #print(str(i)+" : "+str(min(i)))
            sumParTime += min(i)
   # print(str(permut)+ " : "+str(sumtime))
    return [sumtime,sumParTime,unsolved,times]

def calcMinPermutation(schedule,coreMap,train,test,args,permutate):
    ''' sort solvers regarding their time slices in the schedule 
        schedule    : list of time slices per solver
        coreMap     : list -> index of list (id of solver) mapped to value (core)
        train       : 2d list of training runtimes
        test        : 2d list of test runtimes
        args        : all command line parsed arguments
        permutate   : bool flag; at uniform only a pseudo permutation is necessary
        RETURNS      
          timeMinP  : PAR1 on test runtimes
          parMinP   : PAR10 on test runtimes
          unsolved  : number of timeouts on test runtimes
          0 : average performance of permutations on test runtimes (cannot be calculated here, but same interface as other permutation function nec.)
          times     : runtime of each instance
          minPerm   : min permutation    
    '''
    sindex = 0
    dicSchedule = dict(zip(xrange(len(schedule)),schedule))
    sortedSchedule = sorted(dicSchedule.iteritems(), key=lambda (k,v): (v,k))
    minPerm = []
    for s in sortedSchedule:
        solver = s[0]
        time = s[1]
        if (time > 0):
            minPerm.append([solver,coreMap[solver]])
    print("MinPerm: "+str(minPerm))
    [timeMinP,parMinP,unsolved,times] = evaluatePermutation(train,minPerm,schedule,args.cores,args.par,args.co)   
    print("Train TO: "+str(unsolved))
    [timeMinP,parMinP,unsolved,times] = evaluatePermutation(test,minPerm,schedule,args.cores,args.par,args.coTest)     
    return [timeMinP,parMinP,unsolved,0,times,minPerm] 
    
def calcHeuPermutation(schedule,coreMap,train,test,args,permutate):
    ''' sort solvers regarding the number of instances solved with their time slices 
        schedule    : list of time slices per solver
        coreMap     : list -> index of list (id of solver) mapped to value (core)
        train       : 2d list of training runtimes
        test        : 2d list of test runtimes
        args        : all command line parsed arguments
        permutate   : bool flag; at uniform only a pseudo permutation is necessary
        RETURNS      
          timeHeu  : PAR1 on test runtimes
          parHeu   : PAR10 on test runtimes
          unsolved  : number of timeouts on test runtimes
          0 : average performance of permutations on test runtimes (cannot be calculated here, but same interface as other permutation function nec.)
          times     : runtime of each instance
          heuperm   : heuristic permutation
    '''
    heuperm = sortSolverByUnsolvedInst(train,schedule,coreMap)
    print("Heurstic Permutation: "+str(heuperm))
    [timeHeu,parHeu,unsolved,times] = evaluatePermutation(test,heuperm,schedule,args.cores,args.par,args.coTest)     
    return [timeHeu,parHeu,unsolved,0,times,heuperm] 

def calcPermutation(schedule,coreMap,train,test,args,permutate):
    ''' try to find best permutation of the schedule (bruteforce)
        schedule    : list of time slices per solver
        coreMap     : list -> index of list (id of solver) mapped to value (core)
        train       : 2d list of training runtimes
        test        : 2d list of test runtimes
        args        : all command line parsed arguments
        permutate   : bool flag; at uniform only a pseudo permutation is necessary
        RETURNS      
          testtime  : PAR1 on test runtimes
          testPar   : PAR10 on test runtimes
          unsolved  : number of timeouts on test runtimes
          avgTestTime : average performance of permutations on test runtimes
          times     : runtime of each instance
          minPerm   : best permutation
          heuPermPerformance[0] : performance of heuristic permutation (see calcHeuPermutation)
          minPermPerformance[0] : performance of min permutation (see calcMinPermutation)
    '''
    nschedule = []
    for s in schedule:
        nschedule.append(int(s))
    schedule = nschedule
    #print(nschedule)
    [minPerm,minTime,minParTime,avgTime] = getBestPermutations(train,schedule,args.cores,coreMap,permutate,args.co)
    print("MinPerm : "+str(minPerm))
    #print("Test : "+str(test))
    [minTestPerm,minTestTime,minTestParTime,avgTestTime] = getBestPermutations(test,schedule,args.cores,coreMap,permutate,args.coTest)
    [testTime,testPar,unsolved,times] = evaluatePermutation(test,minPerm,schedule,args.cores,args.par,args.coTest)
    
    # to compute values for comparision - not needed for the actual schedule
    heuPermPerformance = calcHeuPermutation(schedule,coreMap,train,test,args,permutate)
    minPermPerformance = calcMinPermutation(schedule,coreMap,train,test,args,permutate)
    
    return [testTime,testPar,unsolved,avgTestTime,times,minPerm,heuPermPerformance[0],minPermPerformance[0]]

def getCoreMapBest(sortedSinglePairs,nBestSolver,nSolver,cores,co):
    ''' find best mapping of a solver to a core
        sortedSinglePairs    : sorted number of timeouts per Solver
        nBestSolver          : number of solvers to use
        nSolver              : number of solvers
        cores                : number of cores
        co                   : cutoff
        RETURN               
            schedule         : list -> index of list (id of solver) mapped to value (time slice)
            CoreMap          : list -> index of list (id of solver) mapped to value (core)
    '''
    coreMap = getConstVec(nSolver,0)
    schedule = getConstVec(nSolver,0)
    bestSolver = []
    index = 1
    for s in sortedSinglePairs:
        if (index > nBestSolver):
            break
        bestSolver.append(s[0])
        index +=1 
    #print(bestSolver)
    if (nBestSolver <= cores):   # ideal mapping possible
        usedCore = 0
        for b in bestSolver:
            coreMap[b] = usedCore+1
            schedule[b] = co
            usedCore += 1
    else:        
        #perCore = round(nBestSolver / cores)
        perCore = max([int(nBestSolver / cores), 1])
        lastPerCore = nBestSolver - (cores-1)*perCore
        #print("Last per Core: "+str(lastPerCore))
        #print("perCore : "+str(perCore))
        #print("co : "+str(co))
        #print("bestN :"+str(nBestSolver))
        usedSolvers = 0
        coreIndex = 1
        for b in bestSolver:
            usedSolvers += 1
            coreMap[b] = coreIndex
            if (coreIndex != cores):
                schedule[b] = round(float(co) / perCore,2)
            else:
                schedule[b] = round(float(co) / lastPerCore,2)
            #coreIndex += 1
            if ((cores-1)*perCore > usedSolvers):   #first n 
                coreIndex = (coreIndex % (cores-1)) + 1
                #print(cores)
                #print(coreIndex)
            else:
                coreIndex = cores
    #print(sortedSinglePairs)
    print("Schedule : "+str(schedule))
    #print(coreMap)
    return [schedule,coreMap]
         
def parallelRun(matrix,schedule,coreMap,co,cores,parF):
    ''' simulate parallel execution on a single core 
        each solver has the same amount of time used at every time point (if not time slice is exceeded)
        matrix    : 2d list of runtimes
        schedule    : list of time slices per solver
        coreMap   : list -> index of list (id of solver) mapped to value (core)
        co        : cutoff
        cores     : number of cores
        parF      : factor of PAR score
        RETURN    : PAR1,PAR10,#TO,0
    '''
    sumOfRuntime = 0
    sumOfParRuntime = 0
    sumOfTimeouts = 0
    for inst in matrix:
        coreTime = []
        coreParTime = []
        coreTimeout = []
        for c in range(1,cores+1):
            minimalTime = co
            sIndex = 0
            for s in schedule:
                if (c == coreMap[sIndex] and s >= inst[sIndex] and inst[sIndex] < minimalTime):
                    minimalTime = inst[sIndex]
                sIndex += 1
            sumInstTime = 0
            sIndex = 0
            for s in schedule:
                if (c == coreMap[sIndex]):
                    if (s < minimalTime):
                        sumInstTime += s
                    else:
                        sumInstTime += minimalTime
                sIndex += 1
            if (minimalTime == co):
                coreParTime.append(sumInstTime*parF)
                coreTimeout.append(1)
            else:
                coreParTime.append(sumInstTime)
                coreTimeout.append(0)
            coreTime.append(sumInstTime)
        sumOfRuntime += min(coreTime)
        sumOfParRuntime += min(coreParTime)
        sumOfTimeouts += min(coreTimeout)
    return [sumOfRuntime,sumOfParRuntime,sumOfTimeouts,0]

def addLists(L1,L2):
    ''' add entries of two lists 
    L1     : first List
    L2     : second List
    RETURN : summed up list
    '''
    index = 0
    res = []
    for l in L1:
        res.append(l+L2[index])
        index += 1
    return res

def printResults(single,uni,bestn,combin,asp,oracle,numberInst):
    ''' formated print performances of all approaches 
        single    : performance list of single best solver (0:3)
        uni       : performance list of uniform schedule (0:3)
        combin    : performance list of combined N uniform schedule (0:3)
        asp       : performance list of asp-based schedule (0:3)
        oracle    : performance list of oracle
        numberInst: number of instances
    '''
    print("Runtime (PAR"+str(args.par)+") SBS: \t\t\t"+str(round(single[0],2))+"("+str(round(single[1],2))+")"+"["+str(single[2])+"]")
    print("Runtime (PAR"+str(args.par)+") Uniform: \t\t"+str(round(uni[0],2))+"("+str(round(uni[1],2))+")"+"["+str(uni[2])+"]")
    print("Runtime (PAR"+str(args.par)+") BestN: \t\t\t"+str(round(bestn[0],2))+"("+str(round(bestn[1],2))+")"+"["+str(bestn[2])+"]")
    #print("Runtime (PAR"+str(args.par)+") CombiN: \t\t"+str(round(combin[0],2))+"("+str(round(combin[1],2))+")"+"["+str(combin[2])+"]")
    print("Runtime (PAR"+str(args.par)+") ASPEED: \t\t"+str(round(asp[0],2))+"("+str(round(asp[1],2))+")"+"["+str(asp[2])+"]")
    print("#Instances: "+str(numberInst))
    if (asp[3] != 0):
        print("AVG AVG Permutation (BestN):\t\t"+str(round(bestn[3]/numberInst,2)))
        print("AVG AVG Permutation (CombiN):\t\t"+str(round(combin[3]/numberInst,2)))
        print("AVG AVG Permutation (ASP):\t\t"+str(round(asp[3]/numberInst,2)))
        print("Speedup Permutation (BestN):\t\t"+str(round(bestn[3]/bestn[0],2)) )
        #print("Speedup Permutation (CombiN):\t\t"+str(round(combin[3]/combin[0],2)) )
        print("Speedup Permutation (ASP):\t\t"+str(round(asp[3]/asp[0],2)) )
    print("AVG Runtime (PAR"+str(args.par)+") SBS: \t\t"+str(round(single[0]/numberInst,2))+"("+str(round(single[1]/numberInst,2))+")"+"["+str(single[2])+"]")
    print("AVG Runtime (PAR"+str(args.par)+") Uniform: \t\t"+str(round(uni[0]/numberInst,2))+"("+str(round(uni[1]/numberInst,2))+")"+"["+str(uni[2])+"]")
    print("AVG Runtime (PAR"+str(args.par)+") BestN: \t\t"+str(round(bestn[0]/numberInst,2))+"("+str(round(bestn[1]/numberInst,2))+")"+"["+str(bestn[2])+"]")
    #print("AVG Runtime (PAR"+str(args.par)+") CombiN: \t\t"+str(round(combin[0]/numberInst,2))+"("+str(round(combin[1]/numberInst,2))+")"+"["+str(combin[2])+"]")
    print("AVG Runtime (PAR"+str(args.par)+") ASPEED: \t\t"+str(round(asp[0]/numberInst,2))+"("+str(round(asp[1]/numberInst,2))+")"+"["+str(asp[2])+"]")
    print("AVG Runtime (PAR"+str(args.par)+") ORACLE: \t\t"+str(round(oracle[0],2))+"("+str(round(oracle[1],2))+")"+"["+str(oracle[2])+"]")
    
def raiseSchedule(schedule,raiseFactor):
    ''' raise the time slices of a schedule by a factor 
        schedule    : list of time slices
        raiseFactor : factor for muliplication
        RETURN      : a raised schedule
    '''
    raisedSched = []
    for s in schedule:
        s = s*raiseFactor
        raisedSched.append(s)
    return raisedSched
    
def extendInternal(ulist,list,init=False):
    ''' add a new column on a 2d list 
        ulist    : 2d list
        list     : new column
        init     : add to an empty 2d list
    '''
    if (init == False):
        for index in range(0,len(ulist)):
            ulist[index].append(list[index])
    else:
        for l in list:
            ulist.append([l])
            
def printtimes(times):
    ''' print runtimes of each instance in csv-format
        times    : 2d list (each sub list is one instance)
    '''
    #print(times)
    sys.stderr.write("ASP,BestN,CombiN,Uniform,SBS\n")
    for t in times:
        sys.stderr.write(",".join(t)+"\n")
    #print(len(times[0]))
    #print(len(times))
    
def oraclePerform(data,par,co):
    ''' calculates the performance of the oracle (minimal runtime per instance)
        data    : 2d-matrix with runtimes
        par     : factor for PAR score (penalized average score)
        co      : cutoff (/captime)
        RETURN  : PAR1,PAR10,#TO of oracle
    '''
    oPerfPAR1 = 0
    oPerfPAR10 = 0
    oPerfTO = 0
    l = len(data)
    for d in data:
        mini = min(d)
        if (mini >= co):
            oPerfPAR1 += co
            oPerfTO += 1
            oPerfPAR10 += co*par
        else:
            oPerfPAR1 += mini
            oPerfPAR10 += mini
    return [oPerfPAR1/l,oPerfPAR10/l,oPerfTO]

def printJSONSched(configs,sched,perm,cores):
    ''' prints the calculated Schedule in JSON-Format 
        configs    : list of solver/configuration names 
        sched      : schedule list 
        perm       : permutation of solvers (list) ([solver,core]) - ordering important!
    '''
    print(configs)
    print(sched)
    print(perm)
    jsonList = []
    
    coreID = 0
    new = True
    while (coreID < cores):
        coreList = []
        coreID +=1
        new = False
        for p in perm:  # format [solverID,coreID]
            if (p[1] == coreID):
                new = True
                execDic = {}
                settingDiC = {}
                settingDiC["path"] = ""
                settingDiC["time"] = sched[p[0]]
                settingDiC["args"] = ""
                execDic[configs[p[0]]] = settingDiC
                coreList.append(execDic)
        if (len(coreList) != 0):
            jsonList.append(coreList)
   # print(jsonList)
    print json.dumps(jsonList, sort_keys=True, indent=4)
    
def getASPPermutation(schedule,coreMap,train,test,args,permutate):
    ''' calculate best permutation of solvers with ASP
    schedule    : list of time slices per solver
    coreMap     : list -> index of list (id of solver) mapped to value (core)
    train       : 2d array of training data 
    test        : 2d array of test data
    args        : command line arguments
    permutate   : (if False: only evaluate one permutation)
    RETURN      : [PAR1, PAR10, TO, 0, runtimes,permutation]
    '''
    print(">>> ASP Permutation <<<")
    
    if (permutate == True):
        # write time table
        trainFH = writeASPFacts(train,args.co,args.co,False)
        
        #write schedule as facts
        scheduleFacts = ""
        nschedule = []
        for index in range(0,len(schedule)):
            if (int(schedule[index]) != 0):
                scheduleFacts+= " solverTimeCore(c"+str(index+1)+","+str(int(schedule[index]))+","+str(coreMap[index])+")."
            nschedule.append(int(schedule[index]))
        #print(scheduleFacts)
        schedule = nschedule
        factsFH = tempfile.NamedTemporaryFile(prefix="Slices",delete=True)
        factsFH.write(scheduleFacts+"\n")
        factsFH.flush()
        #print(factsFH.name)
        #time.sleep(1000)
        grFH = callGringo(args.gringo,args.pEnc,[trainFH,factsFH],args.runsolver,args.maxMem,-1,-1)
        output = callClasp(args.clasp,args.threads,grFH,args.runsolver,args.maxMem,args.maxTime,-1,args.hOpt)
        print(output)
        perm = parsePermatutation(output)
    else:
        [perm,minTime,minParTime,avgTime] = getBestPermutations(train,schedule,args.cores,coreMap,permutate,args.co)
    [testTime,testPar,unsolved,times] = evaluatePermutation(test,perm,schedule,args.cores,args.par,args.coTest)
    return [testTime,testPar,unsolved,0,times,perm]

def parsePermatutation(output):
    ''' 
    output     : format order(Core,Solve(cX),Order) 
    RETURN     : [ [Solver,Core], ...]
    '''
    answer = ""
    for line in output.split("\n"):
    	if not line.strip():
            if (line.find("order(") != -1):
                answer = line.split(" ")
                break
    idDic = {}
    for order in answer:
        order = order.replace("order(","").replace(")","").split(",")
        core = int(order[0])
        solver = int(order[1].replace("c","")) -1
        orderID = int(order[2]) + 10**core
        idDic[orderID] = [solver,core]
    perm = []
    for key in sorted(idDic.iterkeys()):
        perm.append(idDic[key])
    print("Permutation w.h.o. ASP : "+str(perm))
    return perm

if __name__ == '__main__':
    
    description  = "usage: python -O aspeed.py --csv=[file] [options]\n"
    description  += "Note: The script is made for a scientific publication and not optimized for practical usage."
    parser = argparse.ArgumentParser(prog="aspeed.py",usage=description)
    req_group = parser.add_argument_group("Required Options")
    req_group.add_argument('--csv', dest='csv', action='store', default="", required=True,  help='csv file with instance in rows and configurations as columns')    
    
    path_group = parser.add_argument_group("Path Options")
    path_group.add_argument('--clasp', dest='clasp', action='store', default="clasp", help='path to clasp mt binary')
    path_group.add_argument('--gringo', dest='gringo', action='store', default="gringo", help='path to gringo binary')
    path_group.add_argument('--runsolver', dest='runsolver', action='store', default="runsolver", help='path to runsolver binary')
    path_group.add_argument('--enc', dest='enc', action='store', default="./enc/encoding-paper-Step1.lp", help='path to encoding')
    path_group.add_argument('--permenc', dest='pEnc', action='store', default= "./enc/encoding-paper-Step2.lp", help='encoding for permutation computation')
    
    opt_group = parser.add_argument_group("Misc Options")
    opt_group.add_argument('--cutoff', dest='co', action='store', default=600.0, type=float, help='cutoff of runtime')
    opt_group.add_argument('--instheader', dest='ih', action='store_true', default=False, help='first columns are instance names (filter)')
    opt_group.add_argument('--confheader', dest='ch', action='store_true', default=False, help='first row are configuration names (filter)')
    opt_group.add_argument('--seperator', dest='sep', action='store', default=",", help='seperator of datas')
    opt_group.add_argument('--precision', dest='prec', action='store', default=1, type=int, help='precision of floats - n decimals (needs more time for grounding)')
    opt_group.add_argument('--threads', dest='threads', action='store', default=1, type=int, help=argparse.SUPPRESS) # not used right now
    opt_group.add_argument('--maxMem', dest='maxMem', action='store', default=6000, help='maximum RAM for solving and grounding (in MB)')
    opt_group.add_argument('--maxTime', dest='maxTime', action='store', default=120, help='maximum seconds to solve opt problem')
    opt_group.add_argument('--hOpt', dest='hOpt', action='store', default=0, help='hierarchical optimization option of clasp')
    opt_group.add_argument('--testFile', dest='testFile', action='store', default= None, help='test file as csv (same number of solvers as main csv file)')
   # opt_group.add_argument('--alternative', dest='alt', action='store', default= None, help='alternative solution to evaluate (comma separated string')
    opt_group.add_argument('--cores', dest='cores', action='store', default= 1, type=int, help='schedule on n cores')
    opt_group.add_argument('--folds', dest='folds', action='store', default= 2, type=int, help='number of folds for cross validation')
    opt_group.add_argument('--best', dest='best', action='store', default= 3, type=int, help='uniform schedule of best n solver')
    opt_group.add_argument('--par', dest='par', action='store', default= 10, type=int, help='PAR-X score of runtime')
    opt_group.add_argument('--perm', dest='perm', action='store', default=4, type=int, help='compute optimal permutation (0: None, 1:Brutefore, 2:HeuOpt, 3:HeuMin, 4:ASP-Optimization')
    opt_group.add_argument('--parallel', dest='parallel', action='store_true', default=False, help='idealized parallel run of schedule')
    opt_group.add_argument('--cutoffTest', dest='coTest', action='store', default=None, type=float, help='idealized parallel run of schedule')
    opt_group.add_argument('--secCrit', dest='secCrit', action='store', default=1, type=int, help='secondary optimization criteria (0:None, 1:MinL2, 2:MaxL2, 3:MinL1, 4:MaxL1, 5: MinL0, 6:MaxL0')
    opt_group.add_argument('--printTimes', dest='printT', action='store_true', default=False,  help='print runtimes in csv')
    opt_group.add_argument('--printJSON', dest='printJ', action='store_true', default=False,  help='print schedule in JSON Format')
    opt_group.add_argument('--printJSONB', dest='printJBest', action='store_true', default=False,  help='print schedule of bestN in JSON Format')

    permutationFuns = {1 : calcPermutation, 2:calcHeuPermutation, 3:calcMinPermutation, 4:getASPPermutation}
    
    #(args,misc) = parser.parse_known_args() 
    args = parser.parse_args() 
    
    
    if (os.path.isfile(args.csv) == False):
        sys.stderr.write("ERROR: CSV File was not found!\n")
        sys.exit()
    if (os.path.isfile(args.enc) == False):
        sys.stderr.write("ERROR: enc File was not found!\n")
        sys.exit()
    if (args.testFile != None and os.path.isfile(args.testFile) == False):
        sys.stderr.write("ERROR: testSet File was not found!\n")
        sys.exit()
    if (args.perm == 4):
        if (args.pEnc != None):
            if (os.path.isfile(args.pEnc) == False):
                sys.stderr.write("ERROR: Permutation Encoding File is missing (use --permenc)!\n")
                sys.exit()
        else:
            sys.stderr.write("ERROR: Permutation Encoding File is missing (use --permenc)!\n")
            sys.exit()

    if(args.printJ == True):
        if not(args.testFile != None and args.ch == True and args.perm != 0):
            sys.stderr.write("ERROR: --printJSON requires --confheader, --perm != 0 and --testFile [file]\n")
            sys.exit()
            
    args.raiseFactor = 1
    if (args.coTest == None):
        args.coTest = args.co
    else:
        #print(args.coTest)
        #print(args.co)
        args.raiseFactor = args.coTest / args.co
        
    args.co = args.co * (10**args.prec)
    args.co = int(args.co)  # abrunden
    print("Reading!")
    
    [matrix,confs, configs] = readIn(args.csv,args.sep,args.ih,args.ch,args.prec,args.coTest)
    numberInst = len(matrix)
    
    # trivial case: uniform time slices
    allSolver = []
    for i in range(0,confs):
        allSolver.append([i,0])
    [unifSchedule,uniCoreMapping] = getCoreMapBest(allSolver,confs,confs,args.cores,args.co)

    # test file
    if (args.testFile != None):
        print(">>>TEST FILE EVALUATION<<<")
        train = matrix
        [test, confs, configs] = readIn(args.testFile,args.sep,args.ih,args.ch,args.prec,args.co)
        
        sortedSinglePairs = singleBestSolver(train,args.co)
        singleBestSolver(test,args.co)
        singleBestSolver(test,args.coTest)
        singleBestC = sortedSinglePairs[0][0]
        [aspSchedule,coreMap,FactsFH] = calcASPSchedule(train,test,args,confs,sortedSinglePairs[0][1])
        print("ppfolio-like ASP...")
        #[combiNSchedule,combiNCoreMapping,bFactsFH] = calcASPSchedule(train,test,args,confs,sortedSinglePairs[0][1],True)
        #stockup2Uni(combiNSchedule,combiNCoreMapping,args.cores,args.coTest,args.prec)
        combiNTimeouts = 0
        combiNSchedule = [0]

        stockupUniform(aspSchedule,coreMap,args.cores,args.co,args.prec)
            
        [bestSchedule,bestCoreMapping] = getCoreMapBest(sortedSinglePairs,args.best,confs,args.cores,args.co)
            
        [uniSchedule,uniCoreMapping] = getCoreMapBest(sortedSinglePairs,confs,confs,args.cores,args.co)
            
        bestSchedule = raiseSchedule(bestSchedule,args.raiseFactor)
        uniSchedule = raiseSchedule(uniSchedule,args.raiseFactor)
        aspSchedule = raiseSchedule(aspSchedule,args.raiseFactor)
            
        [singleBestTO,timeouts] = evaluateSolution(aspSchedule,test,singleBestC,args.coTest)
        [singleBestTO,unifTimeouts] = evaluateSolution(uniSchedule,test,singleBestC,args.coTest)
        [singleBestTO,bestNTimeouts] = evaluateSolution(bestSchedule,test,singleBestC,args.coTest)     
        [singleBestTO,combiNTimeouts] = evaluateSolution(combiNSchedule,test,singleBestC,args.coTest)
        
        printStats(uniSchedule,bestSchedule,combiNSchedule,coreMap,aspSchedule,-1,singleBestC,singleBestTO,unifTimeouts,bestNTimeouts,combiNTimeouts,timeouts)
        if (args.perm != 0):
            
            times = []    
            print(">>>Permutation<<<")
            print("Permutation format: [[Solver_1,Core]...[Solver_N,Core]]")
            print("Permutation Schedule...")
            res = permutationFuns[args.perm](aspSchedule,coreMap,train,test,args,True)
            stockupUniform(aspSchedule,coreMap,args.cores,args.co,args.prec)
            aspPerm = res[0:4]
            extendInternal(times,res[4],True)
            aspPermutation = res[5]
            print("INSTANCES in TEST: "+str(len(res[4])))
            
            #print("Manuel")
            #manualSlices = [606,2,2364,33,1,9,1918,51,4] #random
            #manualSlices = [1,2,8,2,2,145,423,14] # folio-g
            #manualSlices = [1,225,18,0,2120,1,1,0,0,0,0,0,4,0,0,1,23,2606] #indu
            #manualSlices = [349,46,174,6,0,0,3963,0,0,0,0,2,0,374,86] # sathand
            #res = permutationFuns[args.perm](manualSlices,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],train,test,args,True)
            #manualPerm = res[0:4]
            #print(manualSlices)
            #print(aspSchedule)
            #print(manualPerm)
            #print(aspPerm)
                
            print("Permutation BestN...")
            res = permutationFuns[args.perm](bestSchedule,bestCoreMapping,train,test,args,True)
            bestnPerm = res[0:4]
            extendInternal(times,res[4])
                
            print("Permutation ppfolio-like...")
            #res = permutationFuns[args.perm](combiNSchedule,combiNCoreMapping,train,test,args,True)
            #combinPerm = res[0:4]
            #combiPermutation = res[5]
            combinPerm = [1,1,1,1]
                
            print("Pseudo Permutate Uniform...")
            res = permutationFuns[args.perm](uniSchedule,uniCoreMapping,train,test,args,False)
            uniPerm = res[0:4]
            extendInternal(times,res[4])
               
            print("Pseudo Permutate Single Best...")
            [singleSchedule,singleCoreMapping] = getCoreMapBest(sortedSinglePairs,1,confs,args.cores,args.co)
            singleSchedule = raiseSchedule(singleSchedule,args.raiseFactor)
            res = permutationFuns[args.perm](singleSchedule,singleCoreMapping,train,test,args,False)
            singlePerm = res[0:4]
            extendInternal(times,res[4])
            
            print("Number of Timeouts on test set")
#            print("single best solver: \t"+str(sumSingle)+" ("+str(round(float(sumSingle)/numberInst*100,2))+"%)")
#            print("uniform schedule: \t"+str(sumUniform)+" ("+str(round(float(sumUniform)/numberInst*100,2))+"%)")
#            print("best n schedule: \t"+str(sumBestN)+" ("+str(round(float(sumBestN)/numberInst*100,2))+"%)")
#            print("combi n schedule: \t"+str(sumCombiN)+" ("+str(round(float(sumCombiN)/numberInst*100,2))+"%)")
#            print("asp schedule: \t\t"+str(sumSchedule)+" ("+str(round(float(sumSchedule)/numberInst*100,2))+"%)")
            testOPerf = oraclePerform(test,args.par,args.coTest)
            printResults(singlePerm,uniPerm,bestnPerm,combinPerm,aspPerm,testOPerf,len(res[4]))
            
            #print(str(configs))
            if (len(configs) != 0 and args.printJ == True):
                printJSONSched(configs,aspSchedule,aspPermutation,args.cores)
            if (len(configs) != 0 and args.printJBest == True):
                printJSONSched(configs,combiNSchedule,combiPermutation,args.cores)
                
            if (args.printT == True):
                printtimes(times)
    # cross validation
    if (args.folds > 1 and args.testFile == None):
        print(">>>CROSS VALIDATION<<<")
        trainOPerf = oraclePerform(matrix,args.par,args.coTest)
        foldMatrix = crossSplit(matrix,args.folds)
        sumSingle = 0
        sumUniform = 0
        sumSchedule = 0
        sumBestN = 0    
        sumCombiN = 0
        
        singlePerm = [0,0,0,0]
        bestnPerm = [0,0,0,0]
        combinPerm = [0,0,0,0]
        uniPerm = [0,0,0,0]
        aspPerm = [0,0,0,0]
        times = []
        
        singlePar = [0,0,0,0]
        bestnPar = [0,0,0,0]
        uniPar = [0,0,0,0]
        aspPar = [0,0,0,0]
        combiPar = [0,0,0,0]
        
        if (args.perm == 1): # compare average permutation against best and heuristic approaches
            compareASP = [[],[],[],[]]
            compareCombi = [[],[],[],[]]
            compareBest = [[],[],[],[]]

        for f in range(0,args.folds):
            train = mergeFolds(foldMatrix,f)
            test = foldMatrix[f]
            sortedSinglePairs = singleBestSolver(train,args.co)
            singleBestSolver(test,args.co)
            singleBestSolver(test,args.coTest)
            singleBestC = sortedSinglePairs[0][0]
            [aspSchedule,coreMap,FactsFH] = calcASPSchedule(train,test,args,confs,sortedSinglePairs[0][1])
            print("ppfolio-like ASP...")
            [combiNSchedule,combiNCoreMapping,bFactsFH] = calcASPSchedule(train,test,args,confs,sortedSinglePairs[0][1],True)
            stockup2Uni(combiNSchedule,combiNCoreMapping,args.cores,args.coTest,args.prec)
            #print("Best 3 Schedule :"+str(combiNSchedule))
            #aspSchedule = stockup(aspSchedule,coreMap,args.cores,args.co,args.prec)
            stockupUniform(aspSchedule,coreMap,args.cores,args.co,args.prec)
            
            #print("scaled solution: \t"+"\t".join(intListToStrList(vecSol)))
            #bestnSchedule = calcBestN(sortedSinglePairs,args.best,args.co,args.cores)
            [bestSchedule,bestCoreMapping] = getCoreMapBest(sortedSinglePairs,args.best,confs,args.cores,args.co)
            
            [uniSchedule,uniCoreMapping] = getCoreMapBest(sortedSinglePairs,confs,confs,args.cores,args.co)
            
            bestSchedule = raiseSchedule(bestSchedule,args.raiseFactor)
            uniSchedule = raiseSchedule(uniSchedule,args.raiseFactor)
            aspSchedule = raiseSchedule(aspSchedule,args.raiseFactor)
            
            [singleBestTO,timeouts] = evaluateSolution(aspSchedule,test,singleBestC,args.coTest)
            [singleBestTO,unifTimeouts] = evaluateSolution(uniSchedule,test,singleBestC,args.coTest)
            [singleBestTO,bestNTimeouts] = evaluateSolution(bestSchedule,test,singleBestC,args.coTest)     
            [singleBestTO,combiNTimeouts] = evaluateSolution(combiNSchedule,test,singleBestC,args.coTest)         
           
            printStats(uniSchedule,bestSchedule,combiNSchedule,coreMap,aspSchedule,f,singleBestC,singleBestTO,unifTimeouts,bestNTimeouts,combiNTimeouts,timeouts)
            sumSingle += singleBestTO
            sumUniform += unifTimeouts
            sumSchedule += timeouts
            sumBestN += bestNTimeouts
            sumCombiN += combiNTimeouts
                            
            if (args.perm != 0):
                
                print(">>>Permutation<<<")
                print("Permutation format: [[Solver_1,Core]...[Solver_N,Core]]")
                print("Permutation Schedule...")
                #permutationFuns
                res = permutationFuns[args.perm](aspSchedule,coreMap,train,test,args,True)
                aspPerm = addLists(aspPerm,res[0:4])
                timesFold = []
                extendInternal(timesFold,res[4],True)
                print("INSTANCES in TEST: "+str(len(res[4])))

                if (args.perm == 1):
                    compareASP[0].append(res[3]) # avg
                    compareASP[1].append(res[0]) # best
                    compareASP[2].append(res[6]) # heu
                    compareASP[3].append(res[7]) # min
                
                print("Permutation BestN...")
                res = permutationFuns[args.perm](bestSchedule,bestCoreMapping,train,test,args,True)
                bestnPerm = addLists(bestnPerm,res[0:4])
                extendInternal(timesFold,res[4])
                
                print("Permutation ppfolio-like...")
                res = permutationFuns[args.perm](combiNSchedule,combiNCoreMapping,train,test,args,True)
                combinPerm = addLists(combinPerm,res[0:4])#
                extendInternal(timesFold,res[4])

                if (args.perm == 1):
                    compareCombi[0].append(res[3]) # avg
                    compareCombi[1].append(res[0]) # best
                    compareCombi[2].append(res[6]) # heu
                    compareCombi[3].append(res[7]) # min
                
                print("Pseudo Permutate Uniform...")
                res = permutationFuns[args.perm](uniSchedule,uniCoreMapping,train,test,args,False)
                uniPerm = addLists(uniPerm,res[0:4])
                extendInternal(timesFold,res[4])
                
                print("Pseudo Permutate Single Best...")
                [singleSchedule,singleCoreMapping] = getCoreMapBest(sortedSinglePairs,1,confs,args.cores,args.co)
                singleSchedule = raiseSchedule(singleSchedule,args.raiseFactor)
                res = permutationFuns[args.perm](singleSchedule,singleCoreMapping,train,test,args,False)
                singlePerm = addLists(singlePerm,res[0:4])
                extendInternal(timesFold,res[4])
                
                #add it to list over all files
                times.extend(timesFold)                           
                
            if (args.parallel == True):
                # ASP Schedule
                res = parallelRun(test,aspSchedule,coreMap,args.coTest,args.cores,args.par)
                aspPar = addLists(aspPar,res[0:4])
                # Combi Schedule
                res = parallelRun(test,combiNSchedule,combiNCoreMapping,args.coTest,args.cores,args.par)
                combiPar = addLists(combiPar,res[0:4])
                # Best N Schedule
                [bestSchedule,bestCoreMapping] = getCoreMapBest(sortedSinglePairs,args.best,confs,args.cores,args.co) #bestn
                res = parallelRun(test,bestSchedule,bestCoreMapping,args.coTest,args.cores,args.par)
                bestnPar = addLists(bestnPar,res[0:4])
                # Uni Schedule
                [uniSchedule,uniCoreMapping] = getCoreMapBest(sortedSinglePairs,confs,confs,args.cores,args.co) #uniform
                res = parallelRun(test,uniSchedule,uniCoreMapping,args.coTest,args.cores,args.par)
                uniPar = addLists(uniPar,res[0:4])
                # Single Schedule
                [singleSchedule,singleCoreMapping] = getCoreMapBest(sortedSinglePairs,1,confs,args.cores,args.co) #single
                res = parallelRun(test,singleSchedule,singleCoreMapping,args.coTest,args.cores,args.par)
                singlePar = addLists(singlePar,res[0:4])
                
        print("Number of Timeouts over "+str(args.folds)+" fold cross validation")
        print("single best solver: \t"+str(sumSingle)+" ("+str(round(float(sumSingle)/numberInst*100,2))+"%)")
        print("uniform schedule: \t"+str(sumUniform)+" ("+str(round(float(sumUniform)/numberInst*100,2))+"%)")
        print("best n schedule: \t"+str(sumBestN)+" ("+str(round(float(sumBestN)/numberInst*100,2))+"%)")
        print("combi n schedule: \t"+str(sumCombiN)+" ("+str(round(float(sumCombiN)/numberInst*100,2))+"%)")
        print("asp schedule: \t\t"+str(sumSchedule)+" ("+str(round(float(sumSchedule)/numberInst*100,2))+"%)")
        
        if (args.parallel == True):
            print("")
            print(">>>Parallel Execution<<<")
            printResults(singlePar,uniPar,bestnPar,combiPar,aspPar,trainOPerf,numberInst)
            print("Unsolved Parallel: "+str(aspPar[2]))
        if (args.perm != 0):
            print("")
            print(">>>Ordered Excecution<<<")
            printResults(singlePerm,uniPerm,bestnPerm,combinPerm,aspPerm,trainOPerf,numberInst)
            
            if (args.perm == 1):
                print("Schedule")
                print("AVG/Best : "+str((sum(compareASP[0])/args.folds) / ((sum(compareASP[1])/args.folds))))
                print("AVG/Heu : "+str((sum(compareASP[0])/args.folds) / ((sum(compareASP[2])/args.folds))))
                print("AVG/Min : "+str((sum(compareASP[0])/args.folds) / ((sum(compareASP[3])/args.folds))))
                print("Combi")
                print("AVG/Best : "+str((sum(compareCombi[0])/args.folds) / ((sum(compareCombi[1])/args.folds))))
                print("AVG/Heu : "+str((sum(compareCombi[0])/args.folds) / ((sum(compareCombi[2])/args.folds))))
                print("AVG/Min : "+str((sum(compareCombi[0])/args.folds) / ((sum(compareCombi[3])/args.folds))))

            outputTime = [str(args.cores),str(round(singlePerm[0]/numberInst,2)),str(round(uniPerm[0]/numberInst,2)),str(round(bestnPerm[0]/numberInst,2)),str(round(aspPerm[0]/numberInst,2)),str(round(combinPerm[0]/numberInst,2)),str(args.co),str(args.secCrit),str(round(trainOPerf[0],2)),str(args.best)]
            print(",".join(outputTime))    
            outputParTime = [str(args.cores),str(round(singlePerm[1]/numberInst,2)),str(round(uniPerm[1]/numberInst,2)),str(round(bestnPerm[1]/numberInst,2)),str(round(aspPerm[1]/numberInst,2)),str(round(combinPerm[1]/numberInst,2)),str(args.co),str(args.secCrit),str(round(trainOPerf[1],2)),str(args.best)]
            print(",".join(outputParTime))    
        
        
        
        outputTO = [str(args.cores),str(singlePerm[2]),str(uniPerm[2]),str(bestnPerm[2]),str(aspPerm[2]),str(combinPerm[2]),str(args.co),str(args.secCrit),str(args.best)]
        #print(",".join(outputTO))
        
        if (args.printT == True):
            printtimes(times)
        
        
