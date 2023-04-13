'''
Created on Nov 13, 2012

@author: manju
'''

from tempfile import NamedTemporaryFile
import json
import math

from trainer.parser.reader import Reader
#from trainer.selection.SVM import SVM
#from trainer.selection.SVMMulti import SVMMulti
from trainer.selection.regression import Regression
from trainer.selection.NN import NearestNeighbourTrainer
from trainer.selection.MajorityVoter import MajorityVoter
#from trainer.selection.KMeans import KMeansTrainer

from misc.printer import Printer

class Updater(object):
    '''
        Add new encountered features, runtime and status 
        and retrains models
    '''


    def __init__(self, up_dic, se_dic, ex_dic, ori_config_file):
        '''
        Constructor
        '''
        self.__up_dic = up_dic
        self.__se_dic = se_dic
        self.__ex_dic = ex_dic
        self.__ori_config_file = ori_config_file
        self.__DECAY = 0.99
        
    def update_models(self, runtime, features, status, solver, instance):
        '''
            main method of class
        '''
        Printer.disable_printing = True
        
        added_instances = self.__up_dic["n_new"] + 1
        generic_instance = "new_"+str(added_instances)+"_"+instance.get_name()
        id_solver = int(self.__se_dic["configurations"][str(solver)]["id"])
        n_solver = len(self.__se_dic["configurations"])
        
        Printer.print_c("Retrain!")
        
        # write new data
        Printer.print_nearly_verbose("Write new data")
        self.__add_new_runtime(self.__up_dic["runtime_update"], runtime, id_solver, generic_instance, n_solver)
        self.__add_new_feature(self.__up_dic["feature_update"], features, generic_instance)
        self.__add_new_class(self.__up_dic["class_update"], status, generic_instance)
        
        Printer.print_nearly_verbose("Concat old and new data")
        new_time_file = self.__concatenate_files(self.__up_dic["runtime_file"], self.__up_dic["runtime_update"])
        new_feature_file = self.__concatenate_files(self.__up_dic["feature_file"], self.__up_dic["feature_update"])
        new_class_file = self.__concatenate_files(self.__up_dic["class_file"], self.__up_dic["class_update"])
        new_old_config_file = self.__write_config_file(self.__se_dic)
    
        Printer.print_nearly_verbose("Retrain!")
        instance_dic, solver_list, config_dic = self.__read_in(self.__up_dic["cutoff"], self.__up_dic["n_feats"], new_time_file.name, new_feature_file.name, new_class_file.name, new_old_config_file.name)
        self.__adjust_instance_weights(instance_dic)
        
        selection_dic = self.__retrain(self.__up_dic, instance_dic, solver_list, config_dic, self.__up_dic["n_feats"])
        if self.__ori_config_file:
            self.__write_new_config_file(added_instances, selection_dic)
        
        Printer.disable_printing = False
        
        return selection_dic
        
    def __add_new_runtime(self, time_file, runtime, id_solver, instance, n_solver):
        '''
            adds new line with runtime in time file
            Parameter:
                time_file: name of file with updated runtimes
                runtime: measured runtime
                id_solver: id of solver (alignment in new file)
                instance: name of solved instance
                n_solver: number of solvers in portfolio
        '''
        fp_ = open(time_file,"a")
        times = [-512.0] * n_solver
        times[id_solver] = runtime
        fp_.write("%s,%s\n" % (instance, ",".join(map(str,times))))
        fp_.flush()
        fp_.close()
        Printer.print_nearly_verbose("Added new Runtime Data:")
        Printer.print_nearly_verbose("%s,%s\n" % (instance, ",".join(map(str,times))))

    def __add_new_feature(self, feature_file, features, instance):
        '''
            adds new line with features in feature file
            Parameter:
                feature_file: name of file with updated features
                feature: list of instance features of instance
                instance: name of solved instance
        '''
        fp_ = open(feature_file, "a")
        fp_.write("%s,%s\n" % (instance, ",".join(map(str,features))) )
        fp_.flush() 
        fp_.close()
        Printer.print_nearly_verbose("Added new Feature Data:")
        Printer.print_nearly_verbose("%s,%s\n" % (instance, ",".join(map(str,features))))
    
    def __add_new_class(self, class_file, status, instance):
        '''
            adds new line with status in class file
            Parameter:
                class_file: name of file with updated classes (SAT/UNSAT)
                status: status  of instance
                instance: name of solved instance
        '''
        class_ = None
        if status == "SAT":
            class_ = 1
        if status == "UNSAT":
            class_ = -1
        if status == 1 or status == -1:
            class_ = status
        if not class_:
            Printer.print_e("Could not detect status (SAT/UNSAT) of solved instance; no learning!")
        fp_ = open(class_file, "a")
        fp_.write("%s,%d\n" %(instance,class_))
        fp_.flush()
        fp_.close()
         
    def __adjust_instance_weights(self, instance_dic):
        '''
            reduce the weights of all old instances
        '''
        # get names of all "new" data 
        new_instance_names = self.__get_all_new_instances(self.__up_dic["runtime_update"])
        number_of_new_inst =  len(new_instance_names)
        
        for inst_name, inst in instance_dic.items():
            try:
                age = number_of_new_inst - new_instance_names.index(inst_name) + 1
            except:
                age = number_of_new_inst
            inst.penalize_weight(math.pow(self.__DECAY, age))

    def __get_all_new_instances(self, file_):
        '''
            reads all names of new instances
            Args:
                file_ : file name for a file in csv format
            Return:
                instance_names : name of all instances in the file
        '''    
        instance_names = []
        with open(file_,"r") as fp:
            for line in fp:
                name = line.split(",")[0]
                instance_names.append(name)
        return instance_names        
    
    def __concatenate_files(self, file1, file2):
        '''
            concatenate two files in a temporary file
        '''
        new_file = NamedTemporaryFile(dir=".", suffix=".csv", delete=True)
        fp1_ = open(file1,"r")
        fp2_ = open(file2,"r")
        
        for line in fp1_:
            new_file.write(line)
        for line in fp2_:
            new_file.write(line)
        new_file.flush()
        fp1_.close() 
        fp2_.close()
        
        return new_file
    
    def __write_config_file(self, se_dic):
        '''
            write config_file for reading in (<- strange)
        '''
        config_file_dic = {}
        for algo,c_dic in se_dic["configurations"].items():
            call = c_dic["call"]
            config_file_dic[algo] = call
            
        config_file = NamedTemporaryFile(prefix="UPDATE_Config",dir=".", delete = True)
        
        #print(json.dumps(config_file_dic, indent=2))
        
        json.dump(config_file_dic,config_file)
        
        config_file.flush()
        return config_file
        
    def __read_in(self,cutoff, n_feats, time_file, feats_file, class_file, config_file):
        '''
            read in files for training
            Parameter:
                cutoff: cutoff of measured runtime
                n_feats: number of features
                time_file: file with runtimes per algorithm and instance
                feats_file: file with features per instance
                class_file: sat/unsat class file
                config_file: file with all configuration informations
        '''
        
        
        reader = Reader(cutoff, n_feats, filter_duplicates=True)
        instance_dic, self.__invalid_f_runtime, solver_list, config_dic = reader.get_data(time_file, feats_file, class_file, config_file)
        
        return instance_dic, solver_list, config_dic

    def __retrain(self, up_dic, instance_dic, solver_list, config_dic, n_feats):
        '''
            retrain models
            (copy of trainer.Trainer.train())
            TODO: REWRITE!!!
        '''
        
        
        selection_dic = None
        selection_methods = {"REGRESSION":Regression(), "SVM": SVM(), "SVMMULTI": SVMMulti(), "NN":NearestNeighbourTrainer(), "KMEANS": KMeansTrainer(), "MAJORITY": MajorityVoter()}

        approach = up_dic["approach"].upper()
        norm = up_dic["norm"]
        f_indicator = self.__se_dic["normalization"]["filter"]
        cutoff = up_dic["cutoff"]
        model_dir = up_dic["model_dir"]
        svm_train = up_dic["svm_train"]

        if approach == "SVR":
            selection_dic = selection_methods[approach].train(instance_dic, solver_list, config_dic,
                                                           norm, cutoff, 
                                                           model_dir, f_indicator, n_feats)
        if approach == "SVM":
            selection_dic = selection_methods[approach].train(instance_dic, solver_list, config_dic,
                                                           norm, cutoff, 
                                                           model_dir, f_indicator, n_feats)
        if approach == "SVMMULTI":
            selection_dic = selection_methods[approach].train(instance_dic, solver_list, config_dic,
                                                           norm, cutoff, 
                                                           model_dir, f_indicator, n_feats)
        if approach == "NN":
            selection_dic = selection_methods[approach].train(instance_dic, solver_list, config_dic,
                                                              norm, cutoff, model_dir, f_indicator, n_feats)
  
        if approach == "MAJORITY":
            selection_dic = selection_methods[approach].train(instance_dic, solver_list, config_dic,
                                                              norm, cutoff, model_dir, f_indicator, n_feats)
            
        if approach == "KMEANS":
            selection_dic = selection_methods[approach].train(instance_dic, solver_list, config_dic,
                                                           norm, cutoff, model_dir, 
                                                           f_indicator, n_feats)
            
        return selection_dic

    def __write_new_config_file(self, added_instances, selection_dic):
        '''
            read in old config_file; change nr. of updates; and rewrite it
        '''
        if self.__ori_config_file:
            fp_ = open(self.__ori_config_file,"r")
            config_dic = json.load(fp_)
            fp_.close()
            
            config_dic["update"]["n_new"] = added_instances
            config_dic["selector"]["normalization"].update(selection_dic["normalization"]) 
            fp_ = open(self.__ori_config_file, "w")
            fp_.seek(0)
            json.dump(config_dic, fp_, indent=2)
        