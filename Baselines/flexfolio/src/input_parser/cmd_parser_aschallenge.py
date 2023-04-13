'''
Created on Jul 1, 2015

@author: manju
'''
import argparse
import os
import json
import sys
import StringIO

from misc.printer import Printer

class Parser(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self._arg_parser = argparse.ArgumentParser(
                                            description = '''
                                            ATTENTION: xfolio in the current version only selects algorithms wrt optimization of runtime on decision problems
                                            '''
                                            )
        
        self.__init_parser()
        
        
    def __init_parser(self):
        '''
            init argparse object with all command line arguments
        '''
        
        __version__ = "1.0"
        __updated__ = "09-03-2015"
        program_version = "v%s" % __version__
        program_build_date = str(__updated__)
        program_version_message = 'xfolio %s (%s)' % (program_version, program_build_date)
    
        self._arg_parser.add_argument('-V', '--version', action='version', version=program_version_message)
        
        self._arg_parser.add_argument('-C','--configfile', dest='config', action='store', required=True, help='path to config file (contains pathes to models, normalization constants, etc. pp.); json format expected')
        self._arg_parser.add_argument('-A','--aslib_dir', dest='aslib_dir', action='store', required=True, help='path to aslib test scenario')
        self._arg_parser.add_argument('--feature-steps', dest='feature_steps', action='store', nargs='+', help="use only feature steps (groups) given in this list")
        self._arg_parser.add_argument('-o','--output', dest='output', action='store', required=True, help='path to output csv file')
        self._arg_parser.add_argument('--pre-solver-schedule', dest='pre_schedule', action='store', nargs='+', help=argparse.SUPPRESS) # format: pre-solver,time
        
        # hidden options for AS Challenge which should be set during training and not here!
        self._arg_parser.add_argument('--features', dest='features', action='store', nargs='+', help=argparse.SUPPRESS)
        self._arg_parser.add_argument('--impute', dest='impute', action='store', default="mean", choices=["mean","median", "most_frequent", "-512", "none"], help=argparse.SUPPRESS)
        self._arg_parser.add_argument('--max-feature-time', dest='feat_time', action='store', default=-1, type=int, help=argparse.SUPPRESS)
        
        
        self._arg_parser.add_argument('--verbose', dest='verbose', action='store', default=0, type=int, help='verbosity level (0..2)')
        
    def parse_command_line(self,sys_argv):
        '''
            parse based on self.__parser command line arguments 
            Parameter: 
                sys_argv: command line arguments (sys.argv)
            return args_
        '''
        args_ = self._arg_parser.parse_args(sys_argv)
        
        return self.parse(args_)
        
    def parse(self,args_):
        '''
            returns dictionaries based one arguments groups
            Parameter: 
                sys_argv: parsed command line (argparse object)
        '''
        
        config_dic = self.__read_config_file(args_.config)
        
        ex_dic = {
                    }
        ex_dic.update(config_dic["extractor"])
        se_dic = {
                  }
        se_dic.update(config_dic["selector"])
        al_dic = {
                  }  
        Printer.print_verbose(str(json.dumps(ex_dic, indent=2)))
        Printer.print_verbose(str(json.dumps(se_dic, indent=2)))
        Printer.print_verbose(str(json.dumps(al_dic, indent=2)))
        
        Printer.verbose = args_.verbose
        
        return args_,  ex_dic, se_dic, al_dic

    def __read_config_file(self,config_file):
        '''
            read config file for algorithm selector; 
            json format
        '''
        config_fp = open(config_file,"r")
        return json.load(config_fp)
        