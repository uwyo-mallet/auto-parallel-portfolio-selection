# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 18:06:58 2020

@author: hnyk9
"""


#imports
import glob
import subprocess
import sys
import datetime
import os

#Haniye Kashgarani
#Version 2.0
#parallel solvers 1 instance
'''
This program runs a sets of parallel processes and reports the time they took to finish.
This program requires the following input file in order to work!

FILE FORMAT::
GraphSolver
PartitionName
Directory of Test Instances
InstanceName
File Extension
Command Line Arguments for the solver
'''

def SubmitJob(GraphSolvers,Partition,Node,Instancefile,Path,Argument,InstanceName):
    '''
    Submits a test set to the cluster given the following inputs:

    GraphSolvers - What GraphSolvers to use
    Partition - What Partition to use
    Node - Specified nodes #Depricated
    TestInstances - A list of Instances to run tests on
    Path - Path to output folder
    Argument - Arguments to run with the given solver
    '''
    returnString = []
    print(GraphSolvers)
    pool = 0
    StartInstance = 0

    #for k in range(len(GraphSolvers)):
        #TestString += "echo {}; ".format(os.getcwd() + "/" + GraphSolvers[k])
    #TestString +="} "
    #print("teststring: " + TestString)
    solver_path = "/gscratch/hkashgar/BatchScripts/IPC2020/solvers/"
    Instance = ""
    for i in range(len(Instancefile)):
        Instance = Instancefile[i].split(" ")
        currentInstance = Instance[0].split(".hddl")[0]
        domainInstance = Instance[1]
        problemInstance = Instance[2]
        print("TESTINSTANCE:" + currentInstance)
        for k in range(len(GraphSolvers)):
            TestString = ""
            print(GraphSolvers[k])
            solver = GraphSolvers[k].split("/")[0]
            print("solver:" + solver)
            if solver in ["HyperTensioN","Lilotane"]:
                TestString += "/usr/bin/time -o {}__{}.log singularity run {} {} {} {}__{}.plan {} {} {} | tail -n 200 > {}__{}.output ".format(solver, currentInstance, solver_path + "/" + GraphSolvers[k], domainInstance, problemInstance, solver, currentInstance, runtime, memory, randomSeed, solver, currentInstance)
            elif solver in ["PDDL4J-PO", "PDDL4J-TO"]:
                TestString += "/usr/bin/time -o {}__{}.log singularity run {} {} {} {}__{}.plan {} {} | tail -n 200 > {}__{}.output ".format(solver, currentInstance, solver_path + "/" + GraphSolvers[k], domainInstance, problemInstance, solver, currentInstance, runtime, memory, solver, currentInstance)
            elif solver in ["pyHiPOP", "SIADEX"]:
                TestString += "/usr/bin/time -o {}__{}.log singularity run {} {} {} {}__{}.plan | tail -n 200 > {}__{}.output ".format(solver, currentInstance, solver_path + "/" + GraphSolvers[k], domainInstance, problemInstance, solver, currentInstance, solver, currentInstance)
    
            with  open (Path + "/jobs/" + "{}_{}.job".format(currentInstance,solver),"w") as file:
                file.write('#!/bin/bash'+'\n')
                file.write('#SBATCH --chdir="{}"'.format(os.getcwd() + "/" + Path)+ '\n')
                file.write('#SBATCH --account=mallet'+'\n')
                file.write('#SBATCH --time=0-00:30:00'+'\n')
                file.write('#SBATCH --partition={}'.format(Partition)+'\n')
                file.write('#SBATCH --job-name={}_{}'.format(solver,currentInstance)+ '\n')
                file.write('#SBATCH --output=./{}_{}__J%j.out'.format(solver,currentInstance) + '\n')
                file.write('#SBATCH --error=./{}_{}__J%j.error'.format(solver,currentInstance) + '\n')
                file.write('module load gcc' + '\n')
                file.write('module load parallel' + '\n')
                file.write('module load singularity' + '\n')
                file.write(" {}".format(TestString + '\n'))
        #print("Running Test {} on {}".format(GraphSolver,Test))
        pool = 0

        #subprocess.run(['sbatch', '{}/jobs/{}'.format(Path,Instance)])
        returnString.append("{NumOfSolvers},{Instance},{TestNumber}".format(NumOfSolvers=len(GraphSolvers),Instance=currentInstance,TestNumber=i))
    return '\n'.join(returnString)

ConfigurationFileName = sys.argv[1]
GraphSolver = ""
Partition = ""
Nodes = []

print("Starting up Graph solvers based on the following configureation file {}".format(ConfigurationFileName))


#Get Data from the file provided at input
Data = ""
with open(ConfigurationFileName, "r") as file:
    Data = file.read()
    print(Data)

Data = Data.split('\n')

#Save the data into the file
GraphSolvers = Data[0].replace(' ','').split(',')
Partition = Data[1]
Instancefile = Data[2]
with open(Instancefile, "r") as file:
    Instancefile = file.read()
Instancefile = Instancefile.split("\n")
InstanceName = Data[3]
jobname = Data[4]
runtime = Data[5]
memory = Data[6]
randomSeed = Data[7]
FileExtensions = Data[8].split(',')
Arguments = Data[9]
#print(InstancesDirectory)
print("Nodes :", Nodes)
print("CWD = ",os.getcwd())
#this gets the files with the fileextension in the directory
#for i in FileExtensions:
#    TestInstances = glob.glob(InstancesDirectory+ "*" + i)

print(len(GraphSolvers))
date = datetime.datetime.now()

log = []
Path = '{}-{}-solvers-in-parallel-{}-{}'.format(Partition,len(GraphSolvers),jobname,date.strftime("%B-%d-%Y")).replace('.','').replace('/','')
os.mkdir(Path)
os.mkdir(Path + "/jobs")

log.append(SubmitJob(GraphSolvers,Partition,1,Instancefile,Path,Arguments,InstanceName))


GraphSolver = GraphSolver.replace('.','')
GraphSolver = GraphSolver.replace('/','')
with open('RunLog-{}-{}-solvers-in-parallel-{}-{}.txt'.format(Partition,len(GraphSolvers),jobname,date.strftime("%B-%d-%Y")),"w") as file:
    file.write('\n'.join(log))
