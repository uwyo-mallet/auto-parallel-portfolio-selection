'''
Created on Jun 18, 2013

@author: manju

python transform_satzilla12.py --file SATzilla2012_data/SATALL12S.csv --fgroup satzilla11_data/f_group_dict.json --cutoff 1200 --dir sat12-all/ --fcutoff 1200 --name SAT12-ALL
python transform_satzilla12.py --file SATzilla2012_data/SATHAND12S.csv --fgroup satzilla11_data/f_group_dict.json --cutoff 1200 --dir sat12-hand/ --fcutoff 1200 --name SAT12-HAND
python transform_satzilla12.py --file SATzilla2012_data/SATINDU12S.csv --fgroup satzilla11_data/f_group_dict.json --cutoff 1200 --dir sat12-indu/ --fcutoff 1200 --name SAT12-INDU
python transform_satzilla12.py --file SATzilla2012_data/SATRAND12S.csv --fgroup satzilla11_data/f_group_dict.json --cutoff 1200 --dir sat12-rand/ --fcutoff 1200 --name SAT12-RAND'''
import sys
import argparse
import os
import re
import json

class Transformer(object):
    '''
        transform satzilla 2011 data to arff format
        
    '''
    
    def __init__(self):
        self.__FIRST_FEATURE = "nvarsOrig"
        
        self._status_dic = {0:"?",1:"SAT",2:"UNSAT"}
    
    def parse_command_line(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--file', dest='file_', action='store', required=True, help='input csv file in satzilla format')
        parser.add_argument('--listfile', dest='list_file_', action='store', required=True, help='file with one instance per list to match IDs')
        parser.add_argument('--fgroup', dest='fgroup_file_', action='store', required=True, help='file in json with feature group mapping')
        parser.add_argument('--dir', dest='dir_', action='store', required=True, help='output director for arff files')
        parser.add_argument('--cutoff', dest='cutoff', action='store', default=5000, type=int, help='runtime cutoff')
        parser.add_argument('--fcutoff', dest='f_cutoff', action='store', default="500", help='feature computation runtime cutoff')
        parser.add_argument('--memlimit', dest='memlimit', action='store', default="?", help='memory cutoff')
        parser.add_argument('--name', dest='name', action='store', required=True, help='project / relation name')
        
        args = parser.parse_args(sys.argv[1:])

        if not os.path.isdir(args.dir_):
            sys.stderr.write("WARNING: Directory does not exist. I generate it.\n")
            os.mkdir(args.dir_)
        
        return args
        
    def read_in(self, file_, list_file_, fgroup_file, cutoff):
        
        #read list file to find instance id mapping
        fp = open(list_file_,"r")
        id_inst_list = []
        for line in fp:
            splits = line.rstrip("\n").split(",")
            inst_name = splits[5]
            path = splits[6].replace("/home/jastyles/SATBench/","")
            inst_ = os.path.join(path,inst_name)
            id_inst_list.append(inst_)  
        fp.close()
        
        #read json file for mapping from feature_group name to feature list
        #read json file for mapping from feature_group name to feature list
        fp = open(fgroup_file,"r")
        json_dict = json.load(fp)
        fgroup_dict = json_dict["groups"]
        fgroup_order = json_dict["order"]
        fgroup_dep = json_dict["deps"]
        fp.close()
        
        # read big csv file
        fp = open(file_,"r")
        header = fp.readline()
        h_elems = map(lambda x: x.strip(" "), header.replace(" ","").replace("\r","").replace("\n","").split(","))
        first_feature_index = h_elems.index(self.__FIRST_FEATURE) # find first feature
        
        solver_names = []
        # extract solver names
        for index in range(0,first_feature_index-1, 5):
            name_ = re.sub('[:,]',"",h_elems[index+1].replace("_Time",""))
            solver_names.append(name_)
            
        # extract feature names
        feature_names = h_elems[first_feature_index:]
        feature_time_indexes = []
        feature_time_names = []
        for f_name,index in zip(feature_names,range(0,len(feature_names))):
            if "featuretime" in f_name:
                feature_names.remove(f_name)
                feature_time_names.append(f_name)
                feature_time_indexes.append(index)
        feature_time_indexes.reverse()
        feature_time_names.reverse()
        defined_fgroups = list(fgroup_dict.keys())
        
        times = {} # id -> list of times
        features = {} # id -> list of features
        feature_times = {} # id -> feature computation time
        sat_unsat = {} # id -> class
        stati = {} # id_ -> list of stati
        presolved = {} # id_ -> True/False
        for line in fp:
            elems = line.replace(" ","").replace("\n","").split(",")
            #extract runtimes and classes
            for index in range(0,first_feature_index-1,5):
                id_ = int(elems[index])
                id_ = id_inst_list[id_-1] # override id with instance name
                status = int(elems[index+2])
                if status > 0:
                    runtime = float(elems[index+1])
                else:
                    runtime = "?"

                stati[id_] = stati.get(id_,[])
                stati[id_].append(status)

                times[id_] = times.get(id_,[])
                times[id_].append(runtime)

            
            features[id_] = elems[first_feature_index:]
            features[id_] = map(float,features[id_])
            features[id_] = map(lambda x: round(x,4) if x >= 0 else "?", features[id_])

            total_time = 0
            fgroup_times = {}
            ps = False
            for index,fgroup in zip(feature_time_indexes, feature_time_names):
                if fgroup in defined_fgroups:
                    fgroup_times[fgroup] = features[id_][index]
                if not (features[id_][index] == "?"):
                    total_time += float(features[id_][index])
                else:
                    ps = True # if any presolving time is -512, instance was solved during preprocessing
                features[id_].pop(index)
            feature_times[id_] = {"total": total_time,
                                  "fgroup": fgroup_times
                                  }
            presolved[id_] = ps
        fp.close()
        
        #aggregate ground truth
        for id_,stati_list in stati.items():
            if 1 in stati_list and 2 in stati_list:
                sys.stderr.write("Conflicting stati at %s" %(id_) )
            sat_unsat[id_] = max(stati_list)
        
        return times, stati, features, sat_unsat, solver_names, feature_names, feature_times, fgroup_dict, fgroup_order, presolved, fgroup_dep
    
    def write_out(self, runtimes, stati, features, sat_unsat, solver_names, feature_names, feature_times, fgroup_dict, fgroup_order, presolved, fgroup_dep, dir_, relation_name, cutoff, f_cutoff, memlimit):
        
        ##################################################        
        # write readme
        ##################################################        
        fp = open(os.path.join(dir_,"readme.txt"),"w")
        fp.write("source: http://www.cs.ubc.ca/labs/beta/Projects/SATzilla/\n")
        fp.write("authors: L. Xu, F. Hutter, H. Hoos, K. Leyton-Brown\n")
        fp.write("translator in coseal format: M. Lindauer with the help of Alexandre Frechette\n")
        fp.write("the data do not distinguish between timeout, memout or crashes!\n")
        fp.write("the status file will only have ok or timeout!\n")
        fp.write("If features are \"?\", the instance was solved during feature computation.\n")
        fp.write("\n")
        fp.write("Although there is no necessary alignment and dependencies between the feature processing steps,\n")
        fp.write("the steps were executed in a fixed alignment.\n")
        fp.write("Therefore, all feature steps depend on the previous executed ones.")
        fp.flush()
        fp.close()
        
        ##################################################        
        # write descrition
        ##################################################        
        fp = open(os.path.join(dir_,"description.txt"),"w")
        fp.write("task_id: %s\n"  % (relation_name))
        fp.write("performance_measures: runtime\n")
        fp.write("maximize: false\n")
        fp.write("performance_type: runtime\n")
        fp.write("algorithm_cutoff_time: %d\n" %(cutoff))
        fp.write("algorithm_cutoff_memory: %s\n" %(memlimit))
        fp.write("features_cutoff_time: %s\n" %(f_cutoff))
        fp.write("features_cutoff_memory: %s\n" %(memlimit))
        fp.write("features_deterministic: %s\n" %(",".join(feature_names)))
        fp.write("features_stochastic: \n")
        fp.write("algorithms_deterministic: %s \n" %(",".join(solver_names)))
        fp.write("algorithms_stochastic: \n")
        fp.write("number_of_feature_steps: %d\n" %(len(fgroup_dict)))
        fgroup_order.reverse()
        str_list = []
        for group_name in fgroup_order:
            collected_features = []
            collected_features.extend(fgroup_dict[str(group_name)])
            for sname, deps in fgroup_dep.items():
                if group_name in deps:
                    collected_features.extend(fgroup_dict[str(sname)])
            str_list.append("feature_step %s: %s" %(group_name,",".join(collected_features)))
        str_list.reverse()
        fp.write("\n".join(str_list))
        fp.flush()
        fp.close()
        
        ##################################################        
        # write runtimes
        ##################################################        
        fp = open(os.path.join(dir_,"algorithm_runs.arff"),"w")
        
        fp.write("@RELATION ALGORITHM_RUNS_%s\n\n" %(relation_name))
        
        fp.write("@ATTRIBUTE instance_id STRING\n")
        fp.write("@ATTRIBUTE repetition NUMERIC\n")
        fp.write("@ATTRIBUTE algorithm STRING\n")
        fp.write("@ATTRIBUTE runtime NUMERIC\n")
        fp.write("@ATTRIBUTE runstatus {ok , timeout , memout , not_applicable , crash , other}\n")
        fp.write("\n")
            
        fp.write("@DATA\n")
        for id_, times in runtimes.items():
            status_list = stati[id_]
            for t, algo, status in zip(times, solver_names, status_list):
                if status > 0 and t != "?" and t < cutoff:
                    status = "ok"
                else:
                    status = "timeout"
                fp.write("%s,1,%s,%s,%s\n" %(id_, algo, t, status))
        fp.flush()
        fp.close()
        
        ##################################################        
        # write status
        ##################################################        
        fp = open(os.path.join(dir_,"feature_runstatus.arff"),"w")
        
        fp.write("@RELATION FEATURE_RUNSTATUS%s\n\n" %(relation_name))
        
        fp.write("@ATTRIBUTE instance_id STRING\n")
        fp.write("@ATTRIBUTE repetition NUMERIC\n")
        f_groups = fgroup_dict.keys()
        for group_name in f_groups:
            fp.write("@ATTRIBUTE %s {ok, timeout, memout, presolved, crash, other}\n" %(group_name))
        
        fp.write("\n")
        fp.write("@DATA\n")
        for id_, feat_vector in features.items():
            error_status = "presolved" if presolved[id_] else "crash"
            status_step_vector = []
            for group in f_groups:
                feats = fgroup_dict[group]
                feats_index = []
                for f in feats:
                    feats_index.append(feature_names.index(f))
                feat_vec = [feat_vector[indx] for indx in feats_index]
                status = error_status if "?" in feat_vec else "ok"
                if status != "ok":
                    for indx in feats_index:
                        feat_vector[indx] = "?"
                status_step_vector.append(status)
            fp.write("%s,1,%s\n" %(id_, ",".join(status_step_vector)))
        fp.flush()
        fp.close()
        
        ##################################################        
        #write features    
        ##################################################        
        fp = open(os.path.join(dir_,"feature_values.arff"),"w")
        
        fp.write("@RELATION FEATURE_VALUES-%s\n\n" %(relation_name))
        
        fp.write("@ATTRIBUTE instance_id STRING\n")
        fp.write("@ATTRIBUTE repetition NUMERIC\n")
        for feat in feature_names:
            fp.write("@ATTRIBUTE %s NUMERIC\n" %(feat))
        fp.write("\n")
            
        fp.write("@DATA\n")
        for id_, f in features.items():
            fp.write("%s,1,%s\n" %(id_, ",".join(map(str,f))))
        fp.flush()
        fp.close()

        ##################################################    
        #write satunsat
        ##################################################        
        fp = open(os.path.join(dir_,"ground_truth.arff"),"w")
        
        fp.write("@RELATION %s-Ground-Truth\n\n" %(relation_name))
        
        fp.write("@ATTRIBUTE instance_id STRING\n")
        fp.write("@ATTRIBUTE satunsat {SAT,UNSAT}\n")
        fp.write("\n")
            
        fp.write("@DATA\n")
        for id_, status in sat_unsat.items():
            fp.write("%s,%s\n" %(id_,self._status_dic[int(status)]))
        fp.flush()
        fp.close()  
        
        ##################################################
        #write feature times
        ##################################################
        fp = open(os.path.join(dir_,"feature_costs.arff"),"w")
        
        fp.write("@RELATION %s-FeatureRuntime\n\n" %(relation_name))
        
        fp.write("@ATTRIBUTE instance_id STRING\n")
        fp.write("@ATTRIBUTE repetition NUMERIC\n")
        f_groups = fgroup_dict.keys()
        for group_name in f_groups:
            fp.write("@ATTRIBUTE %s NUMERIC\n" %(group_name))
        fp.write("\n")
            
        fp.write("@DATA\n")
        for id_, ftime_dict in feature_times.items():
            ft_vector = map(str,[ftime_dict["fgroup"][fg] for fg in f_groups])
            fp.write("%s,1,%s\n" %(id_, ",".join(ft_vector)))
        fp.flush()
        fp.close() 

    def main(self):
        args = self.parse_command_line()
        times, stati, features, sat_unsat, solver_names, feature_names, feature_times, fgroup_dict, fgroup_order, presolved, fgroup_dep = self.read_in(args.file_,args.list_file_, args.fgroup_file_, args.cutoff)
        self.write_out(times, stati, features, sat_unsat, solver_names, feature_names, feature_times, fgroup_dict, fgroup_order, presolved, fgroup_dep, args.dir_, args.name, args.cutoff, args.f_cutoff, args.memlimit)

if __name__ == '__main__':
    Transformer().main()