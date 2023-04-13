'''
Created on Nov 8, 2012

@author: manju
'''

from misc.printer import Printer
from featureExtractor import FeatureExtractor

from subprocess import Popen, PIPE
import signal
import threading
import json
import sys

class Claspre2(FeatureExtractor):
    '''
        Extract Feature from claspre2
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self._timer = None
        self._popen_ = None
        
    def run_extractor(self, args_dic, instance):
        '''
            run extractor and look for instance features
            Parameter:
                args_dic : dictionary with options
                instance : instance to solve
        '''
        
        Printer.print_c("\nFeature Extraction:")
        self._set_args(args_dic,instance)
        
        cmd = self._cmd
        Printer.print_c(" ".join(cmd))
        
        signal.signal(signal.SIGINT, self.__clean_up_with_signal)
        signal.signal(signal.SIGHUP, self.__clean_up_with_signal)
        signal.signal(signal.SIGQUIT, self.__clean_up_with_signal)
        signal.signal(signal.SIGSEGV, self.__clean_up_with_signal)
        signal.signal(signal.SIGTERM, self.__clean_up_with_signal)
        signal.signal(signal.SIGXCPU, self.__clean_up_with_signal)
        signal.signal(signal.SIGXFSZ, self.__clean_up_with_signal)
        
        #stdout_file = NamedTemporaryFile(prefix="OUT-FEATURES",dir=".",delete=True)
        try:
            self._popen_ = Popen(cmd, stdin = PIPE, stdout = PIPE, stderr = PIPE)
            self._timer = threading.Timer(self._maxTime, self._timeout, [self._popen_])
            self._timer.start()
            self._instance.seek(0)
            if isinstance(self._instance, file) and self._instance.name.endswith(".gz"):
                zcat_popen = Popen(["zcat", self._instance.name], stdout=PIPE )
                input_ = zcat_popen.stdout.read()
            else:
                input_ = self._instance.read()
            (out_, err_) = self._popen_.communicate(input=input_)
        except OSError:
            Printer.print_w("Feature extractor was unable to compute features (path correct?): %s" % (cmd))
        
        #stdout_file.seek(0)
        features = None
        try:
            feature_dict = json.loads(out_)
        except:
            try:
                Printer.print_w("Could not parse features. %s!" %(self._instance.name))
            except AttributeError:
                Printer.print_w("Could not parse features from stdin!")
            try:
                self._timer.cancel()
            except:
                pass
            return features
        
        preprocessing_feats = feature_dict["Static"]
        
        dynamic_feats = []
        index = 1
        while True:
            restart_feats = feature_dict.get("Dynamic-%d" % (index))
            if restart_feats:
                dynamic_feats.extend(restart_feats)
            else:
                break
            index += 1
        
        opt_feats = feature_dict.get("Optimization")
         
        flat_feats = []
        flat_feats.extend([y for (x,y) in preprocessing_feats])
        flat_feats.extend([y for (x,y) in dynamic_feats])
        if opt_feats:
            flat_feats.extend([y for (x,y) in opt_feats])
        
        features = flat_feats
        
        try:
            self._timer.cancel()
        except:
            Printer.print_w("Could not cancel threading timer (should not happen)")
            pass
        
        return features

    def __clean_up_with_signal(self, signal, frame):
        try:
            self._timer.cancel()
            self._popen_.kill()
        except:
            pass
        sys.exit(1)