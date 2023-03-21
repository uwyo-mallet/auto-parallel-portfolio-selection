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
SatSolver
PartitionName
Directory of Test Instances
InstanceName
File Extension
Command Line Arguments for the solver
'''

def SubmitJob(SatSolvers,Partition,Node,TestInstances,Path,Argument,InstanceName):
    '''
    Submits a test set to the cluster given the following inputs:

    SatSolvers - What SatSolvers to use
    Partition - What Partition to use
    Node - Specified nodes #Depricated
    TestInstances - A list of Instances to run tests on
    Path - Path to output folder
    Argument - Arguments to run with the given solver
    '''
    returnString = []

    pool = 0
    StartInstance = 0

    #for k in range(len(SatSolvers)):
        #TestString += "echo {}; ".format(os.getcwd() + "/" + SatSolvers[k])
    #TestString +="} "
    #print("teststring: " + TestString)
    Instance = ""
    for i in range(len(TestInstances)):
        print("TESTINSTANCE:" + TestInstances[i])
        if "2018" in TestInstances[i]:
            print(TestInstances[i])
            Instance = TestInstances[i].replace('.','').replace('*','').split('/')[7][:-3]
        elif "2016" in TestInstances[i]:
            Instance = TestInstances[i].replace('.','').replace('*','').split('/')[7][:-3]
        print("instance:" + Instance)
        for k in range(len(SatSolvers)):
            TestString = ""
            if SatSolvers[k] == "solvers/sparrow2riss/bin/SparrowToRiss.sh":
                solver = "sparrow2riss/bin/SparrowToRiss.sh"
                print("solver:" + solver)
                TestString += " /usr/bin/time -o {}__{}.log {} {} 100 {} | tail -n 200 > {}__{}.output ".format("SparrowToRiss", Instance, os.getcwd() + "/" + SatSolvers[k], TestInstances[i], os.getcwd() + "/" + Path , "SparrowToRiss", Instance)
                with  open (Path + "/jobs/" + "{}_{}.job".format(Instance,"SparrowToRiss"),"w") as file:
                           file.write('#!/bin/bash'+'\n')
                           file.write('#SBATCH --chdir="{}"'.format(os.getcwd() + "/" + Path)+ '\n')
                           file.write('#SBATCH --account=mallet'+'\n')
                           file.write('#SBATCH --time=0-01:23:20'+'\n')
                           file.write('#SBATCH --partition={}'.format(Partition)+'\n')
                           file.write('#SBATCH --job-name={}_{}'.format("SparrowToRiss", Instance)+ '\n')
                           file.write('#SBATCH --output=./{}_{}__J%j.out'.format("SparrowToRiss", Instance) + '\n')
                           file.write('#SBATCH --error=./{}_{}__J%j.error'.format("SparrowToRiss", Instance) + '\n')
                           file.write('module load gcc' + '\n')
                           file.write(" {}".format(TestString + '\n'))
            elif SatSolvers[k] == "solvers/Maple_LCM_Scavel_200":
                solver = SatSolvers[k].split('/')[1]
                print("solver:" + solver)
                TestString += " /usr/bin/time -o {}__{}.log {} {} {} | tail -n 200 > {}__{}.output ".format(solver, Instance, os.getcwd() + "/" + SatSolvers[k], TestInstances[i],' -drup-file=/gscratch/hkashgar/BatchScripts/solvertests/Maple_LCM_Scavel_200_fix2/sources/core/proof.out', solver, Instance)
                with  open (Path + "/jobs/" + "{}_{}.job".format(Instance,solver),"w") as file:
                           file.write('#!/bin/bash'+'\n')
                           file.write('#SBATCH --chdir="{}"'.format(os.getcwd() + "/" + Path)+ '\n')
                           file.write('#SBATCH --account=mallet'+'\n')
                           file.write('#SBATCH --time=0-01:23:20'+'\n')
                           file.write('#SBATCH --partition={}'.format(Partition)+'\n')
                           file.write('#SBATCH --job-name={}_{}'.format(solver, Instance)+ '\n')
                           file.write('#SBATCH --output=./{}_{}__J%j.out'.format(solver, Instance) + '\n')
                           file.write('#SBATCH --error=./{}_{}__J%j.error'.format(solver, Instance) + '\n')
                           file.write('module load gcc' + '\n')
                           file.write(" {}".format(TestString + '\n'))
            elif SatSolvers[k] == "solvers/Maple_LCM_Scavel_fix2":
                solver = SatSolvers[k].split('/')[1]
                print("solver:" + solver)
                TestString += " /usr/bin/time -o {}__{}.log {} {} {} | tail -n 200 > {}__{}.output ".format(solver, Instance, os.getcwd() + "/" + SatSolvers[k], TestInstances[i],' -drup-file=/gscratch/hkashgar/satsolvers/sat2018solvers/Maple_LCM_Scavel_fix2/sources/core/proof.out', solver, Instance)
                with  open (Path + "/jobs/" + "{}_{}.job".format(Instance,solver),"w") as file:
                           file.write('#!/bin/bash'+'\n')
                           file.write('#SBATCH --chdir="{}"'.format(os.getcwd() + "/" + Path)+ '\n')
                           file.write('#SBATCH --account=mallet'+'\n')
                           file.write('#SBATCH --time=0-01:23:20'+'\n')
                           file.write('#SBATCH --partition={}'.format(Partition)+'\n')
                           file.write('#SBATCH --job-name={}_{}'.format(solver, Instance)+ '\n')
                           file.write('#SBATCH --output=./{}_{}__J%j.out'.format(solver, Instance) + '\n')
                           file.write('#SBATCH --error=./{}_{}__J%j.error'.format(solver, Instance) + '\n')
                           file.write('module load gcc' + '\n')
                           file.write(" {}".format(TestString + '\n'))
            else:
                solver = SatSolvers[k].split('/')[1]
                print("solver:" + solver)
                TestString += " /usr/bin/time -o {}__{}.log {} {} | tail -n 200 > {}__{}.output ".format(solver, Instance, os.getcwd() + "/" + SatSolvers[k], TestInstances[i], solver, Instance)
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
                           file.write(" {}".format(TestString + '\n'))
        #print("Running Test {} on {}".format(SatSolver,Test))
        pool = 0

        #subprocess.run(['sbatch', '{}/jobs/{}'.format(Path,Instance)])
        returnString.append("{NumOfSolvers},{Instance},{TestNumber}".format(NumOfSolvers=len(SatSolvers),Instance=TestInstances[i],TestNumber=i))
    return '\n'.join(returnString)

ConfigurationFileName = sys.argv[1]
SatSolver = ""
Partition = ""
Nodes = []

print("Starting up sat solvers based on the following configureation file {}".format(ConfigurationFileName))


#Get Data from the file provided at input
Data = ""
with open(ConfigurationFileName, "r") as file:
    Data = file.read()
    print(Data)

Data = Data.split('\n')

#Save the data into the file
SatSolvers = Data[0].replace(' ','').split(',')
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
Path = '{}-{}-solvers-in-parallel-{}-{}'.format(Partition,len(SatSolvers),jobname,date.strftime("%B-%d-%Y")).replace('.','').replace('/','')
os.mkdir(Path)
os.mkdir(Path + "/jobs")

log.append(SubmitJob(SatSolvers,Partition,1,TestInstances,Path,Arguments,InstanceName))


SatSolver = SatSolver.replace('.','')
SatSolver = SatSolver.replace('/','')
with open('RunLog-{}-{}-solvers-in-parallel-{}-{}.txt'.format(Partition,len(SatSolvers),jobname,date.strftime("%B-%d-%Y")),"w") as file:
    file.write('\n'.join(log))
