'''
Created on Nov 5, 2012

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
        self._arg_parser.add_argument('-I','--instance', dest='inst', action='store', default=None, required=False, help='path to instance file or \"-\" to read from stdin')

        self._arg_parser.add_argument('-A','--algoselect', dest='values_stop', action='store_true', default = False, help='Stop after algorithm selection')
        self._arg_parser.add_argument('-F','--features', dest='features_stop', action='store_true', default = False, help='Stop after computation of features')
        #self.__arg_parser.add_argument('--update-model', dest='update', action='store_true', default=False, help='update learnt model with new encountered runtime and features')
        self._arg_parser.add_argument('--update-model', dest='update', action='store_true', default=False, help=argparse.SUPPRESS)
        
        self._arg_parser.add_argument('--verbose', dest='verbose', action='store', default=0, type=int, help='verbosity level (0..2)')
        
        special_parser = self._arg_parser.add_argument_group("Special")
        
        special_parser.add_argument('-t','--threads', dest='al_threads', action='store', required=False, type=int, default=1, help='number of parallel executed algorithms')
        special_parser.add_argument('--clause-sharing', dest='clause_sharing', action='store_true', default=False,  help=argparse.SUPPRESS) #help='enable clause sharing of clasp (Attention: configurations have to be valid thread parameters)')
        special_parser.add_argument('--oracle_dir', dest='o_dir', action='store', required=False, default=None, help='oracle best configuration for instances in a directory (recursive lookup)')
        special_parser.add_argument('--env', dest='env', action='store', required=False, choices=["default","zuse","aspcomp"], default="default", help='change some calls for special system environments')
        
    def parse_command_line(self,sys_argv):
        '''
            parse based on self.__parser command line arguments 
            Parameter: 
                sys_argv: command line arguments (sys.argv)
            return args_
        '''
        args_ = self._arg_parser.parse_args(sys_argv)
        
       # if args_.version:
       #     sys.exit(1) # version will be printed anyway
         
        return self.parse(args_)
        
    def parse(self,args_):
        '''
            returns dictionaries based one arguments groups
            Parameter: 
                sys_argv: parsed command line (argparse object)
        '''
        
        self.__check_arguments(args_)
        config_dic = self.__read_config_file(args_.config)
        
        ex_dic = {
                    }
        ex_dic.update(config_dic["extractor"])
        se_dic = {
                  }
        se_dic.update(config_dic["selector"])
        al_dic = {
                  "threads": args_.al_threads,
                  }  
        if args_.update and config_dic.get("update"):
            up_dic = config_dic["update"]
        else:
            up_dic = None
        Printer.print_verbose(str(json.dumps(ex_dic, indent=2)))
        Printer.print_verbose(str(json.dumps(se_dic, indent=2)))
        Printer.print_verbose(str(json.dumps(al_dic, indent=2)))
        
        Printer.verbose = args_.verbose
        
        return args_.inst, ex_dic, se_dic, al_dic, args_.features_stop, args_.values_stop, up_dic, args_.config, args_.o_dir, args_.env, args_.clause_sharing

    def __check_arguments(self,args_):
        '''
            check file paths
            Parameter:
                args_ : argparse object
        '''
        if not args_.inst and not args_.o_dir:
            Printer.print_e("--instance <instance> or --oracle_dir <dir> is required!")
        
        if not os.path.isfile(args_.config):
            Printer.print_e("File not found: " + args_.config)       # print error and exit
        
        if args_.o_dir: # oracle mode
            if not os.path.isdir(args_.o_dir):
                Printer.print_e("Directory not found: " + args_.o_dir)       # print error and exit
        else: # normal mode
            if args_.inst == "-": # read from stdin
                memory_file = StringIO.StringIO()
                memory_file.writelines(sys.stdin.readlines())
                args_.inst = memory_file
            else:
                if not os.path.isfile(args_.inst):
                    Printer.print_e("File not found: " + args_.inst)       # print error and exit
                else:
                    args_.inst = open(args_.inst,"r")
        
        
    def __read_config_file(self,config_file):
        '''
            read config file for algorithm selector; 
            json format
        '''
        config_fp = open(config_file,"r")
        return json.load(config_fp)
        