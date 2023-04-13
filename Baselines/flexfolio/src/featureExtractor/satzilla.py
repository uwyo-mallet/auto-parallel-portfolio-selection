'''
Created on Nov 13, 2012

@author: manju
'''

from misc.printer import Printer
from subprocess import Popen
from tempfile import NamedTemporaryFile
from featureExtractor import FeatureExtractor
import threading
import StringIO

class SatZilla(FeatureExtractor):
    '''
        Extract Feature from satzilla
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.__pattern = "Features"
        
    def run_extractor(self,args_dic,instance):
        '''
            run extractor and look for instance features
            Parameter:
                args_dic : dictionary with options
                instance : instance to solve
        '''
        
        Printer.print_c("\nExtracted Features:")
        self._set_args(args_dic, instance)

        stdout_file = NamedTemporaryFile(prefix="OUT-FEATURES",dir=".",delete=True)
        output_file = NamedTemporaryFile(prefix="OUT-ZILLA-FEATURES",dir=".",delete=True)
        
        if isinstance(instance,StringIO):
            instance_file = NamedTemporaryFile(prefix= "Input", dir=".", delete=True)
            instance.seek(0)
            instance_file.writelines(instance.readlines())
            self._instance = instance_file.name
        else: # else it has to be a real File()
            self._instance = self._instance.name
                
        cmd = self._cmd.extend([ self._instance, output_file.name])
        Printer.print_c(" ".join(cmd))

        try:
            popen_ = Popen(cmd,stdout = stdout_file)
            t = threading.Timer(self._maxTime, self._timeout, [popen_])
            t.start()
            popen_.communicate()
        except OSError:
            Printer.print_e("Feature extractor was not found: %s" % (self._path))
            
        output_file.seek(0)

        try:        
            lines = output_file.readlines()
            line = lines[1]
            Printer.print_verbose(line)
            features = map(float,line.split(","))
        except:
            features = None
        
        stdout_file.close()
        output_file.close()
        
        try:
            t.cancel()
        except:
            pass
                    
        return features