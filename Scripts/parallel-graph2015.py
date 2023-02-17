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

def SubmitJob(GraphSolvers,Partition,Node,TestInstances,Path,Argument,InstanceName):
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

    pool = 0
    StartInstance = 0

    #for k in range(len(GraphSolvers)):
        #TestString += "echo {}; ".format(os.getcwd() + "/" + GraphSolvers[k])
    #TestString +="} "
    #print("teststring: " + TestString)
    solver_path = "/gscratch/hkashgar/BatchScripts/GRAPHS2015/Solvers/"
    solver_post_path = "starexec_run_default"
    Instance = ""
    for i in range(len(TestInstances)):
        print("TESTINSTANCE:" + TestInstances[i])
        Instance = TestInstances[i].replace('.','').replace('*','').split('/')[6][:-3]
        print("instance:" + Instance)
        for k in range(len(GraphSolvers)):
            TestString = ""
            print(GraphSolvers[k])
            solver = GraphSolvers[k]
            print("solver:" + solver)
            if GraphSolvers[k] == "lad":
                TestString += " /usr/bin/time -o {}__{}.log {} {} | tail -n 200 > {}__{}.output ".format(solver, Instance, solver_path + "/" + GraphSolvers[k] + "/main", TestInstances[i], solver, Instance)
            elif GraphSolvers[k] == "supplementallad":
                TestString += " /usr/bin/time -o {}__{}.log {} {} | tail -n 200 > {}__{}.output ".format(solver, Instance, solver_path + "/" + GraphSolvers[k] + "/main", TestInstances[i], solver, Instance)
            elif GraphSolvers[k] in ["glasgow1","glasgow2","glasgow3","glasgow4"]:
                TestString += " /usr/bin/time -o {}__{}.log {} {} {} | tail -n 200 > {}__{}.output ".format(solver, Instance, solver_path + "/glasgow/solve_subgraph_isomorphism", GraphSolvers[k], TestInstances[i], solver, Instance)
            elif GraphSolvers[k] == "vflib":
                TestString += " /usr/bin/time -o {}__{}.log {} {} | tail -n 200 > {}__{}.output ".format(solver, Instance, solver_path + "/" + GraphSolvers[k] + "/solve_vf", TestInstances[i], solver, Instance)

            with  open (Path + "/jobs/" + "{}_{}.job".format(Instance,solver),"w") as file:
                       file.write('#!/bin/bash'+'\n')
                       file.write('#SBATCH --chdir="{}"'.format(os.getcwd() + "/" + Path)+ '\n')
                       file.write('#SBATCH --account=mallet'+'\n')
                       file.write('#SBATCH --time=0-01:23:20'+'\n')
                       file.write('#SBATCH --partition={}'.format(Partition)+'\n')
                       file.write('#SBATCH --job-name={}_{}'.format(solver,Instance)+ '\n')
                       file.write('#SBATCH --output=./{}_{}__J%j.out'.format(solver,Instance) + '\n')
                       file.write('#SBATCH --error=./{}_{}__J%j.error'.format(solver,Instance) + '\n')
                       file.write('module load gcc' + '\n')
                       file.write('module load parallel' + '\n')
                       file.write('module load boost/1.72.0' + '\n')
                       file.write(" {}".format(TestString + '\n'))
        #print("Running Test {} on {}".format(GraphSolver,Test))
        pool = 0

        #subprocess.run(['sbatch', '{}/jobs/{}'.format(Path,Instance)])
        returnString.append("{NumOfSolvers},{Instance},{TestNumber}".format(NumOfSolvers=len(GraphSolvers),Instance=TestInstances[i],TestNumber=i))
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
InstancesDirectory = Data[2]
InstanceName = Data[3]
jobname = Data[4]
FileExtensions = Data[5].split(',')
Arguments = Data[6]
print(InstancesDirectory)
print("Nodes :", Nodes)
print("CWD = ",os.getcwd())
#this gets the files with the fileextension in the directory
for i in FileExtensions:
    TestInstances = glob.glob(InstancesDirectory+ "*" + i)


date = datetime.datetime.now()

log = []
Path = '{}-{}-solvers-in-parallel-{}-{}'.format(Partition,len(GraphSolvers),jobname,date.strftime("%B-%d-%Y")).replace('.','').replace('/','')
os.mkdir(Path)
os.mkdir(Path + "/jobs")

log.append(SubmitJob(GraphSolvers,Partition,1,TestInstances,Path,Arguments,InstanceName))


GraphSolver = GraphSolver.replace('.','')
GraphSolver = GraphSolver.replace('/','')
with open('RunLog-{}-{}-solvers-in-parallel-{}-{}.txt'.format(Partition,len(GraphSolvers),jobname,date.strftime("%B-%d-%Y")),"w") as file:
    file.write('\n'.join(log))
