'''
Created on Nov 8, 2012

@author: manju
'''

from misc.printer import Printer
from subprocess import Popen, PIPE
from tempfile import NamedTemporaryFile

from featureExtractor import FeatureExtractor
import threading

class Claspre(FeatureExtractor):
    '''
        DEPRECATED: Extract Feature from claspre(1.0)
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.__pattern = "Features"
        
    def run_extractor(self, args_dic, instance):
        '''
            run extractor and look for instance features
            Parameter:
                args_dic : dictionary with options
                instance : instance to solve
        '''
        
        Printer.print_c("\nExtracted Features:")
        self._set_args(args_dic,instance)
        
        cmd = [self._path, "--features"]
        Printer.print_c(" ".join(cmd))
        
        stdout_file = NamedTemporaryFile(prefix="OUT-FEATURES",dir=".",delete=True)
        try:
            popen_ = Popen(cmd, stdin=PIPE, stdout = stdout_file)
            t = threading.Timer(self._maxTime, self._timeout, [popen_])
            t.start()
            instance.seek(0)
            popen_.communicate(input=instance.read())
        except OSError:
            Printer.print_e("Feature extractor was not found: %s" % (self._path))
        
        stdout_file.seek(0)
        features = None
        
        for line in stdout_file.readlines():
            Printer.print_verbose(line)
            if line.startswith(self.__pattern):
                line = line.lstrip(self.__pattern).strip(": ")
                features = map(float,line.split(","))
                Printer.print_c("Features: "+",".join(map(str,features)))
                break
        stdout_file.close()
        
        try:
            t.cancel()
        except:
            pass
        
        return features
