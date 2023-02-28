# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 16:39:54 2022

@author: Haniye Kashgarani
"""

#imports
import glob
import subprocess
import sys
import datetime
import os

#Version 3
#Haniye Kashgarani
'''
#sequential Test/ One Solver One Instance at a time
This program runs a sets of processes and reports the time they took to finish.
This program requires the following input file in order to work!

FILE FORMAT::
GraphsSolver
PartitionName
Directory of Test Instances
Name of instances
File Extension
Command Line Arguments for the solver
'''

def SubmitJob(GraphsSolver,Partition,Node,Instancefile,Path,Argument,InstanceName):
    '''
    Submits a test set to the cluster given the following inputs:
    GraphsSolver - What GraphsSolver to use
    Partition - What Partition to use
    Instancefile txt file- A list of Instances to run tests on
    Path - Path to output folder
    Argument - Arguments to run with the given solver
    InstanceName - Graphs2015-instances
    '''
    returnString = []

    pool = 0
    TestString = ""
    StartInstance = 0
    #print(TestInstances)
    for i in range(len(Instancefile)):
        Instance = Instancefile[i].split(" ")
        currentInstance = Instance[0]
        patternInstance = Instance[1]
        targetInstance = Instance[2]
        #TestString = Instancefile[i] 
        print("GraphsSolver:"+GraphsSolver)
        print("CurrentInstance:"+currentInstance)
        with  open (Path + "/jobs/" + "{}__{}".format(GraphsSolver,currentInstance),"w") as file:
                  file.write('#!/bin/bash'+'\n')
                  file.write('#SBATCH --chdir="{}"'.format(os.getcwd() + '/' + Path)+ '\n')
                  file.write('#SBATCH --account=mallet'+'\n')
                  file.write('#SBATCH --time=0-01:23:20'+'\n')
                  file.write('#SBATCH --partition={}'.format(Partition)+'\n')
                  file.write('#SBATCH --job-name={}__{}'.format(GraphsSolver,currentInstance)+ '\n')
                  file.write('#SBATCH --output=./{}__{}.output'.format(GraphsSolver,currentInstance) + '\n')
                  file.write('#SBATCH --error=./{}__{}.error'.format(GraphsSolver,currentInstance) + '\n')
                  file.write('#SBATCH --exclusive' + '\n')
                  file.write('module load gcc' + '\n')
                  file.write('module load parallel' + '\n')
                  file.write('module load boost/1.72.0' + '\n')
                  if GraphsSolver == "lad":
                      file.write('time {} -p {} -t {} | tail -n 200'.format('/gscratch/hkashgar/BatchScripts/GRAPHS2015/solvers/' + GraphsSolver + "/main", patternInstance, targetInstance))
                  elif GraphsSolver == "supplementallad":
                      file.write('time {} -p {} -t {} | tail -n 200'.format('/gscratch/hkashgar/BatchScripts/GRAPHS2015/solvers/' + GraphsSolver + "/main", patternInstance, targetInstance))
                  elif GraphsSolver in ["glasgow1","glasgow2","glasgow3","glasgow4"]:
                      file.write('time {} {} {} {} | tail -n 200'.format('/gscratch/hkashgar/BatchScripts/GRAPHS2015/solvers/glasgow/solve_subgraph_isomorphism', GraphsSolver, patternInstance, targetInstance))
                  elif GraphsSolver == "vflib":
                      file.write('time {} {} {} 100000 | tail -n 200'.format('/gscratch/hkashgar/BatchScripts/GRAPHS2015/solvers/' + GraphsSolver + "/solve_vf", patternInstance, targetInstance))
        pool = 0
        TestString = "{ "

        subprocess.run(['sbatch', '{}/jobs/{}__{}'.format(Path,GraphsSolver,currentInstance)])
        returnString.append("{NumOfNodes},{Instance},{TestNumber}".format(NumOfNodes=1,Instance=currentInstance,TestNumber=i))
        #print(returnString)
    return '\n'.join(returnString)

ConfigurationFileName = sys.argv[1]
GraphsSolver = ""
Partition = ""
Nodes = []

print("Starting up Graphs solvers based on the following configureation file {}".format(ConfigurationFileName))


#Get Data from the file provided at input
Data = ""
with open(ConfigurationFileName, "r") as file:
    Data = file.read()
    print(Data)

Data = Data.split('\n')

#Save the data into the file
GraphsSolver = Data[0]
Partition = Data[1]
Instancefile = Data[2]
with open(Instancefile, "r") as file:
    Instancefile = file.read()
Instancefile = Instancefile.split("\n")
#print(Instancefile)
#InstancesDirectory = Data[2]
InstanceName = Data[3]
FileExtensions = Data[4].split(',')
Arguments = ""
print("Graphs Solver:", GraphsSolver)
print("Partition:", Partition)
#print("Instance Directory:", InstancesDirectory)
print("FileExtensions:", FileExtensions)
print("Nodes :", Nodes)
print("CWD: ",os.getcwd())
#for i in FileExtensions:
#    TestInstances = glob.glob(InstancesDirectory+ "*" + i)
#print(TestInstances)
date = datetime.datetime.now()

log = []
Path = '{}-Partition-{}-Solver-{}-{}-NormalTest'.format(Partition,GraphsSolver,InstanceName,date.strftime("%B-%d-%Y")).replace('.','').replace('/','')
os.mkdir(Path)
os.mkdir(Path + "/jobs")

log.append(SubmitJob(GraphsSolver,Partition,1,Instancefile,Path,Arguments,InstanceName))


GraphsSolver = GraphsSolver.replace('.','')
GraphsSolver = GraphsSolver.replace('/','')

with open('RunLog-{}-Partition-{}-Solver-{}-{}-NormalTests.txt'.format(Partition,GraphsSolver,InstanceName,date.strftime("%B-%d-%Y")),"w") as file:
    file.write('\n'.join(log))
