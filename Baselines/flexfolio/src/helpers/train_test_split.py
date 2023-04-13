'''
Created on Jun 12, 2013

@author: manju
'''

import sys
import argparse
import random
import os

class Splitter(object):
    
    def __init__(self):
        '''
        '''
        self._runtime_file = ""
        self._remaining_files = []
        self._fraction_test = 0.5
    
    def parse_cmd(self):
        '''
            parse command line arguments with argparse
        '''
        
        arg_parser = argparse.ArgumentParser(
                                            description = "That's my command line arguments:",
                                            epilog = "Example call"+
                                                "python2.7 -O train_test_split.py ..."
                                            )
        
        arg_parser.add_argument('--runtimes', dest='time_file', action='store', required=True, help='runtime file in arff')
        arg_parser.add_argument('--files', dest='files', action='store', nargs='+', type=str, required=False,help='remaining files (features etc.)')
        arg_parser.add_argument('--fraction-test', dest='fraction_test', action='store', type=float, required=True, help='fraction of test instances 0<x<1')
        
        args = arg_parser.parse_args(sys.argv[1:])
        self._runtime_file = args.time_file
        self._remaining_files = args.files
        self._fraction_test = args.fraction_test
    
    def read_instances(self):
        '''
            read instances from runtime file
            Implicit use of self._runtime_file
        '''
        instances = []
        with open(self._runtime_file,"r") as fp:
            for line in fp:
                line = line.replace("\n","")
                if line == "" or "@" in line or "%" in line:
                    # @: meta in information in arff
                    # %: comment in line; shouldn't be used in data
                    continue
                parts = line.split(",")
                instances.append(parts[0]) # instance name is always the first coloumn
        return instances
    
    def sample_test_instances(self, instances):
        '''
            sample test instances and return training and test set
            Args:
                list of instance names
        '''
        n_inst = len(instances)
        print("Number of instances: %d" %(n_inst))
        
        test_set = []
        n_test = int(n_inst * self._fraction_test)
        print("Training instances: %d" %(n_inst - n_test))
        print("Test instances: %d" %(n_test))
        
        for i in range(1,n_test+1):
            rand_index = random.randint(0,n_inst-i)
            rand_instance = instances.pop(rand_index)
            test_set.append(rand_instance)
            
        return test_set, instances
    
    def write_new_files (self, test_set, train_set):

        self._remaining_files.append(self._runtime_file)
        for file_ in self._remaining_files:
            fp_in = open(file_,"r")
            file_name = os.path.basename(file_)
            fp_test = open("test-"+file_name,"w")
            fp_train = open("train-"+file_name,"w")
            for line in fp_in:
                line = line.replace("\n","")
                instance = line.split(",")[0]
                in_test = True if instance in test_set else False
                in_train = True if instance in train_set else False
                #in_test = reduce(lambda y,x: True if y or line[0:len(x)]==str(x) else False, test_set, False)
                #in_train = reduce(lambda y,x: True if y or line[0:len(x)]==str(x) else False, train_set, False)
                if line == "" or "@" in line or "%" in line:
                    # @: meta in information in arff
                    # %: comment in line; shouldn't be used in data
                    fp_test.write(line+"\n")
                    fp_train.write(line+"\n")
                elif in_test:
                    fp_test.write(line+"\n")
                elif in_train:
                    fp_train.write(line+"\n")
                else:
                    print("Don't understand line:\n %s" %(line))
                    fp_test.write(line+"\n")
                    fp_train.write(line+"\n")
            fp_test.flush()
            fp_train.flush()
            fp_test.close()
            fp_train.close()
                    
    def main(self):
        '''
            main method
        '''
        self.parse_cmd()
        instances = self.read_instances()
        test_set, train_set = self.sample_test_instances(instances)
        self.write_new_files(test_set, train_set)

if __name__ == '__main__':
    
    splitter = Splitter()
    splitter.main()