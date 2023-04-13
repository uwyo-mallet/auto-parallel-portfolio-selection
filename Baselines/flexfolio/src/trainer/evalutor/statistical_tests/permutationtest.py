#!/bin/python

'''
permutation test (one sided p-value)
following the description of: Ensemble-based Prediction of RNA Secondary Structures (Nima Aghaeepour and Holger H. Hoos)

Created on Dez 1, 2011

@author: Marius Schneider

Input: csv file
'''

import sys
import os 
import math
import csv
import argparse
import random
import functools
from misc.printer import Printer

class PermutationTest(object):

    def randomSwap(self, col1,col2):
        n = len(col1)
        sc1 = []
        sc2 = []
        for i in range(0,n):
            if (random.random() > 0.5):
                sc1.append(col2[i])
                sc2.append(col1[i])
            else:
                sc1.append(col1[i])
                sc2.append(col2[i])
        avg1 = self.avg(sc1)
        avg2 = self.avg(sc2)
        return avg1-avg2    # betrag?
    
    def getPValue(self, col1,col2,p,avgS):
        avgs = [avgS]
        for i in range(0,p-1):
            avgs.append(self.randomSwap(col1,col2))
        Printer.print_verbose("AVG Start : " +str(avgS))
        Printer.print_verbose("min AVG : "+str(min(avgs)))
        Printer.print_verbose("max AVG : "+str(max(avgs)))
        v = self.percentile(avgs,avgS)
        Printer.print_verbose("Percentile : "+str(v))
        pValue = v / 100
        return pValue
    
    def percentile(self, N, value):
        ''' returns percentile of value on list N '''
        N.sort()
        #print(N)
        first = N.index(value)
        count = N.count(value)
        #return float(first+count-1)*100/len(N)
        return float(first)*100/len(N)
    
    def avg(self, N):
        return (float(sum(N)) / len(N))
    
    def filter(self, col1,col2,noise):
        for i in range(0,len(col1)):
            delta = math.sqrt(noise/2) * math.sqrt((col1[i]+col2[i])/2)  
            avgI = (col1[i]+col2[i])/2
            #print("Delta : "+str(delta))
            #print("AVG : "+str(avgI))
            #print("cols :"+str(col1[i]) + " : "+str(col2[i]))
            if ((col1[i] < col2[i] and col1[i] >= (avgI-delta)) or (col2[i] <= col1[i] and col2[i] >= (avgI-delta))):
                col1[i] = col2[i]
                #print("Set equal")
        return [col1,col2]
    
    def doTest(self, col1, col2, alpha, permutations, name1, name2, noise):
        '''
            perform permutation test
            Args:
                col1: list of performance data
                col2: list of performance data
                alpha: significance alpha
                permutations: number of permutations
                name1: name of algorithms of col1
                name2: name of algorithms of col2
                noise: eliminate noise (paper of Olivier Roussel SAT2012) 
            Returns:
                rejected[bool], switched[bool], pvalues(float)
        ''' 
        
        if(noise != None):
            [col1,col2] = filter(col1,col2,float(noise))
        oriAVG = self.avg(col1) - self.avg(col2)
        switched = False   
        if (oriAVG > 0):
            Printer.print_verbose("Alternative Hypothesis: Coloumn "+str(name2) + " is better than Coloumn "+str(name1))
            tmp = col1
            col1 = col2
            col2 = tmp
            oriAVG *= -1
            switched = True
        else:
            Printer.print_verbose("Alternative Hypothesis: Coloumn "+str(name1) + " is better than Coloumn "+str(name2))
        random.seed(1234)
        pValue = self.getPValue(col1,col2,permutations,oriAVG)
        if (pValue < alpha):
            return [True,switched,pValue]
        else:
            return [False,switched,pValue]
            
    
