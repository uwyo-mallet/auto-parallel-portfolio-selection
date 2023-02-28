# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 17:06:24 2020

@author: hnyk9
"""


#!usr/bin/env python
#File Version 1.0 10/11/19 12 PM
import plotly.express as px
import plotly
import glob
import sys
import statistics
import pandas as pd
import os
from os import path
Version_Number = 3.0



#-------------------------What this script does-----------------------------------------
#This script takes a directory of output files from slurm.error and scrapes the runtime.
#Runtime must be gathered using the linux Time command. Other formats may not be supported.
#This data is then processed into pandas dataframes and saved as CSV files in the following
#format:

#InstanceName,SolverTime,Partition,ErrorTime,ErrorMemory,ErrorUndefined
#Some notes:
#Data will be NA for all numerical categories if the data has an error


#Command to run this script:
#python DataScraper.py Directory_To_Scrape/ Runlog.txt AppendCSV

#Where Directory_To_Scrape/ is a directory that containes .error files with runtimes in them.
#Runlog.txt is the runlog associated with the directory being graphed.
#AppendCSV is the file to append the data to. If left blank the program will create a new file.
#This new CSV File will be called DefaultCSVOut.csv

#Additional Options


#Simple function to return wether or not the data is numeric
def isNumeric(S):
    try:
        float(S)
        return True
    except ValueError:
        return False



#Returns a list of tuples from a string with runtimes.
# Format:
# [[minute,second],[minute,second],...]
def scrapeData(toScrapeData):
    toScrapeData = toScrapeData.split()
    mark = 0
    currentTuple = []
    listOfTuples = []
    #input(toScrapeData)
    for i in toScrapeData:

        #Find the runtimes in the file
        if mark == 1:
            currentTuple.append(float(i))
            listOfTuples.append(currentTuple)
            currentTuple = []
            mark = 0
        if mark == 2:
            currentTuple.append(float(i))
            mark = 1
        if i == "user":
            mark = 2
    return listOfTuples

def MakeDataElement(InstanceName,Solver,Partition,Time,ErrorTime,ErrorMemory,ErrorUndefined):
  if(Time is 0):
    return [InstanceName,Solver,Partition,"NA",ErrorTime,ErrorMemory,ErrorUndefined]
  else:
    return [InstanceName,Solver,Partition,Time,ErrorTime,ErrorMemory,ErrorUndefined]

#-----------------------------------PROGRAM START-----------------------------------
#Dir is the directory we are getting data from
Dir =  sys.argv[1]
#Dir = "C:/Users/hnyk9/OneDrive/Documents/teton-Partition-Maple_LCM_Scavel_200-Solver-HourLongTests-June-02-2020-NormalTest"
#Runlog data is associated with
#RunLog = sys.argv[2]
#RunLog = "C:/Users/hnyk9/OneDrive/Documents/RunLog-teton-Partition-Maple_LCM_Scavel_200-Solver-HourLongTests-June-02-2020-NormalTests.txt"
#Find if the user specified a CSV file or not, and set it
CSV = "DefaultCSVOut.csv"
if(len(sys.argv) > 2):
  CSV = sys.argv[2]


DirData = Dir.replace("/"," ").split()[-1].replace("-Partition-"," ").replace("-Solver-"," ").replace(Dir," ").split()
Solver  = DirData[1]
Partition = DirData[0]
#print(DirData)


#RunlogDataFrame = pd.read_csv(RunLog,header = None)

#print("Scraping the Directory ", Dir," With Script Version ", Version_Number)

Times = []

FullData = [["InstanceName","Solver","Partition","Time","TimeError","MemoryError","UndefinedError"]]

#print(Solver + Partition)

#For every file in the given directory that ends in .error
for file in glob.glob("./{}/*.error".format(Dir)):
    #print(file)
    fileText = ""
    Runtime = 0
    RunSum = 0
    Out_Of_Memory_Error =  False
    Time_Out_Error = False
    Undefined_Error = False
    with open(file, "r") as data:
        print(file)
        data = data.read()
        #Error Checking, make sure there is no timeouts
        if not (data.find("oom-kill") == -1):
            Out_Of_Memory_Error = True
        if not (data.find("memory") == -1):
            Out_Of_Memory_Error = True
        if not (data.find("TIME") == -1):
            Time_Out_Error = True
        if not (data.find("segmentation") == -1):
            Undefined_Error = True
        if not (data.find("DIMACS") == -1):
            Undefined_Error = True
        data = data.replace("m"," ")
        data = data.replace("s\n"," ")
        fileText = data.replace('\n',' ')
        
    output_file = file.replace(".error",".output")
    #print(output_file)
    words = []
    if not Out_Of_Memory_Error:
        if not Time_Out_Error:
            if path.exists(output_file):         
                with open(output_file,"r") as output_f:
                    for line in output_f:
                        words = line.replace("\n","").split(" ")
                    if len(words)>0:
                        if words[-1] != "UNSATISFIABLE" and words[-1] != "SATISFIABLE" and words[-1] != "0":
                            print("last word = " + words[-1])
                            Undefined_Error = True
                


    #Get the Test ID and how many Parallel solvers
    #filename = file.replace("TestNum",' Mark ').replace("-",' ').replace(".",' ').replace(Dir," ").split()
    #print(filename)
    #TestNumber, and Core count [File 1 File 2]
    #TestID = 0

    #Get the TestID and Parallel Solvers from the filename
    #for i in range(len(filename)):
        #if filename[i] == "Mark":
            #TestID = filename[i+2]
            #break

        #TestID = int(TestID)
    #If nothing was found then flag it

    instName = file.replace(".error","").split("__")[1] + ".cnf"
    print(instName)
    if not fileText:
        print("not fileText")
        if Time_Out_Error == False and Out_Of_Memory_Error == False:
            Undefined_Error = True
        FullData.append(MakeDataElement(instName,Solver,Partition,0,Time_Out_Error,Out_Of_Memory_Error,Undefined_Error))
        #print(RunlogDataFrame[RunlogDataFrame[2] == TestID][1][TestID])
        continue


    fileText = scrapeData(fileText)
    print(fileText)
    #If the file has no runtmes flag it
    if len(fileText) == 0:
        print("len(fileText) == 0")
        if Time_Out_Error == False and Out_Of_Memory_Error == False:
            Undefined_Error = True
        FullData.append(MakeDataElement(instName,Solver,Partition,0,Time_Out_Error,Out_Of_Memory_Error,Undefined_Error))
        #print(RunlogDataFrame[RunlogDataFrame[2] == TestID][1][TestID])
        continue

    #Median of the runs
    Mean = statistics.mean([x[0]*60 + x[1] for x in fileText])
    Medians = statistics.median([x[0]*60 + x[1] for x in fileText])
    Mode = 0
    try:
        Mode = statistics.mode([x[0]*60 + x[1] for x in fileText])
    except statistics.StatisticsError:
        Mode = Medians

    StdDev = 0
    try:
        StdDev = statistics.stdev([x[0]*60 + x[1] for x in fileText])
    except statistics.StatisticsError:
        StdDev = 0
    #print(Mean)
    #print(Medians)
    #print(StdDev)
    #Just find the testNum in the file list and use that to index the file names! no need for regexp
    #Push Test with average runtime on the Times list
    #Times.append([ParallelSolvers,TestID,Runtime])
    #Push Test with median of runtimes on the Times list
    for i in fileText: 
        print(i[0]*60 + i[1])
        FullData.append(MakeDataElement(instName,Solver,Partition,i[0]*60 + i[1],Time_Out_Error,Out_Of_Memory_Error,Undefined_Error))
        #print(RunlogDataFrame[RunlogDataFrame[2] == TestID][1][TestID])
#Prepare the dataframe for appending to a CSV file.
FullData = pd.DataFrame(FullData[1:],columns = FullData[0])

#If the file already exists, deal with it by appending data
if (os.path.isfile(r'./{}'.format(CSV))):
    OldData = pd.read_csv(r'./{}'.format(CSV))
    FullData = pd.concat([FullData,OldData],ignore_index=True)
print(FullData)
FullData.to_csv(r'./{}'.format(CSV))

