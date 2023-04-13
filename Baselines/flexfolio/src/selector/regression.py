'''
Created on Nov 5, 2012

@author: manju
'''

import os
import operator

from sklearn.externals import joblib

from misc.printer import Printer
from selector import Selector

try: # hack for asp competition 2013
    from binaries.libsvm_weights_312.svmutil import *
except:
    pass

class Regression(Selector):
    '''
      select an algorithm based on regression models and classification of meta classes (e.g. SAT/UNSAT)
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def select_algorithms(self, se_dic, features, pwd=""):
        '''
            select algorithms
            Parameter:
                args: dictionary with attributes
                features: list of float values
                pwd: directory of flexfolio (search path for models)
            Returns:
                ordered list of configurations with their decision valuess
        '''
        
        self._set_base_args(se_dic, features)
        
        self._normalize(self._normalization["approach"], self._normalization["filter"], features)
        
        if self._features is None:    #CVSH original was: if not self._features:
            return None
        
        sorted_scores = self.__select(se_dic, pwd)    
        return sorted_scores
        
    def __select(self,se_dic, pwd):
        '''
            scores each configurations
            and returns a list (conf,score)
        '''
        
        x0 = [self._features]
        y0 = [0] # pseudo label
        
        model_files = se_dic["approach"]["models"]
        
        conf_dic = se_dic["configurations"]
        n_solver = len(conf_dic)
        
        dic_solver_class_scores = dict([x,{}] for x in range(0, n_solver))

        class_model_file = None

        no_load = False
        if isinstance(model_files, dict): # if cv evaluation is used, the models are not saved in the file system 
            no_load = True
            model_dict = model_files
            model_files = model_files.keys()
            
        for model_file in model_files:
            if "class.model" in model_file:
                class_model_file = model_file
                continue
            base_name = os.path.basename(model_file) # format: class_solver_id.model
            class_sid = base_name.split(".")[0].split("_")
            class_ = int(class_sid[0])
            solver_id = int(class_sid[1])

            if isinstance(model_dict[model_file],float) or isinstance(model_dict[model_file],int):
                p_label = model_dict[model_file]
            else:
                if no_load:
                    model = model_dict[model_file]
                else:
                    model = joblib.load(os.path.join(pwd,model_file))
                p_label = model.predict(x0)[0]
                
            #model = svm_load_model(model_file)
            #p_label, p_acc, p_val = svm_predict(y0, x0, model)
            #p_label = float(p_label[0])
            dic_solver_class_scores[solver_id][class_] = p_label
            
        # class probabilities
        # class_model should be an instance of sklearn.svm.SVC
        class_scores = {}
        if no_load:
            class_model = model_dict[class_model_file]
        else:
            
            class_model = joblib.load(os.path.join(pwd,class_model_file))
            
        if class_model: # if only one class was known while training, model is none
            probs = class_model.predict_proba(x0)[0]
            classes_ = class_model.classes_
        else:
            probs = [1.0]
            classes_ = [-1]
        
        index = 0
        for class_ in classes_:
            class_scores[class_] = probs[index]
            index += 1
        
        dic_solver_scores = {}
        for solver_id, dic_class_score in dic_solver_class_scores.items():
            solver_score = 0
            str_list = []
            for class_, score in dic_class_score.items():
                prob_class = class_scores[class_]
                str_list.append("%f * %f" % (prob_class, score))
                solver_score += prob_class * score
            Printer.print_verbose(" + ".join(str_list) + " = " + str(solver_score)) 
            dic_solver_scores[solver_id] = solver_score
            
        dic_solver_scores = self.__map_ids_2_names(dic_solver_scores, se_dic["configurations"])
        
        Printer.print_verbose(str(dic_solver_scores))
        sorted_scores = sorted(dic_solver_scores.iteritems(),key=operator.itemgetter(1))
        
        for (solver,score) in sorted_scores:
            Printer.print_nearly_verbose("[%s]: %f" %(solver,score))
        
        return sorted_scores
        
        
    def __map_ids_2_names(self, dic_scores, conf_dic):
        '''
            map id of solver to its name
        '''
        dic_name_score = {}
        for solver_name, meta_dic in conf_dic.items():
            id = meta_dic["id"]
            dic_name_score[solver_name] = dic_scores[int(id)]
        return dic_name_score
                     
        