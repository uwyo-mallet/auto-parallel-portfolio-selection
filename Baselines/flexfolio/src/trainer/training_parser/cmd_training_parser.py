'''
Created on Nov 8, 2012

@author: manju
'''
import argparse
from argparse import ArgumentDefaultsHelpFormatter

import os
from pickle import FALSE
import sys

from misc.printer import Printer


class TainerParser(object):
    '''
     parse the input of the flexfolio trainer
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self._arg_parser = argparse.ArgumentParser(
                                            description = "Command line arguments:",
                                            formatter_class=ArgumentDefaultsHelpFormatter
                                            )
        
        self.__init_parser()
        
        
    def __init_parser(self):
        '''
            init argparse object with all command line arguments
        '''
        
        def cv_def(s):
            '''
                parse list of tuples in format: (int;int), ...
            '''
            try:
                s = s.split(",")
                s = map(lambda x: x.strip("()"), s)
                return map(lambda x: map(int,x.split(";")) ,s)
            except:
                raise argparse.ArgumentTypeError("Expected: (int,int),(int,int),...")
        
        __version__ = "1.0"
        __updated__ = "09-03-2015"
        program_version = "v%s" % __version__
        program_build_date = str(__updated__)
        program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
        
        self._arg_parser.add_argument('-V', '--version', action='version', version=program_version_message)
        
        REQ_GROUP = self._arg_parser.add_argument_group("Required Options")
        #=======================================================================
        # REQ_GROUP.add_argument('--runtimes', dest='times', action='store', default=None, help='runtimes in csv (first col with instance names')    
        # REQ_GROUP.add_argument('--features', dest='feats', action='store', default=None, help='instance features in csv (first col with instance names')
        # REQ_GROUP.add_argument('--cutoff', dest='cutoff', action='store', type=int, default=None, help='cutoff time')
        #=======================================================================
        REQ_GROUP.add_argument('--aslib-dir', dest='coseal', action='store', default=None, required=True, help='directory with files in COSEAL format')
        REQ_GROUP.add_argument('--model-dir', dest='model_dir', action='store', default="./models", required=True, help='Path to save trained models')
        #REQ_GROUP.add_argument('--nFeats', dest='n_feats', action='store', default=32, type=int, help="number of parsed features")
        
        TRA_GROUP = self._arg_parser.add_argument_group("Training Options")
        TRA_GROUP.add_argument('--feature-class', dest='feat_class', action='store', default="claspre2", choices=["claspre", "claspre2", "satzilla"], help='Class to extract features')
        TRA_GROUP.add_argument('--feature-extractor', dest='feature_path', action='store', help='Path to feature extractor binary')
        TRA_GROUP.add_argument('--approach', dest='approach', action='store', default="CLASSVOTER", choices=["REGRESSION", "REGRESSIONPAIRS", "CLASSVOTER", "CLASSMULTI", "NN", "kNN", "CLUSTERING", "SNNAP", "SBS", "ENSEMBLE", "ASPEED"], help='selection approach')
        TRA_GROUP.add_argument('--classifier', dest='classifier', action='store', default="RANDOMFOREST", choices=["SVM", "GRADIENTBOOSTING", "RANDOMFOREST"], help='classifier used for approach \"CLASSVOTER\"')
        TRA_GROUP.add_argument('--classifiermulti', dest='classifiermulti', action='store', default="RANDOMFOREST", choices=["SVM", "RANDOMFOREST", "GRADIENTBOOSTING"], help='classifier used for approach \"CLASSVOTER\"')
        TRA_GROUP.add_argument('--regressor', dest='regressor', action='store', default="RANDOMFOREST", choices=["SVR", "RIDGE", "LASSO", "RANDOMFOREST"], help='regressor used for approach \"REGRESSION\" and \"SNNAP\"')
        TRA_GROUP.add_argument('--clusteralgo', dest='cluster_algo', action='store', default="KMEANS", choices=["KMEANS","GMEANS","GM", "SPECTRAL", "CSHC"], help='clustering algorithm')
        TRA_GROUP.add_argument('--update-support', dest='update_sup', action='store_true', default=False, help="Remembers original training files and adds empty update files for new learnt information")
        TRA_GROUP.add_argument('--max-feature-time', dest='feat_time', action='store', default=-1, type=int, help="Maximal runtime of feature extractor (default: cutoff/10)")
        
        PER_GROUP = self._arg_parser.add_argument_group("Performance Preprocessing")
        PER_GROUP.add_argument('--approx-weights', dest='approx_weights', action='store', default="None", choices=["None","max","rmsd","nrmsd"], help="Approximate instance weights by the maximal penalty (max), the root mean squared distance to the minimal runtime (rmsd), normalized nrmsd (nrmsd)")
        PER_GROUP.add_argument('--performance_trans', dest='perf_trans', action='store', default="None", choices=["None","log","zscore"], help="Transform the performance data with log or zscore normalization")
        PER_GROUP.add_argument('--contr-filter', dest='contributor_filter', action='store', type=float, default=-1, help="Filter all algorithms which contribute less than this argument ]0,1[")
        PER_GROUP.add_argument('--algorithms', dest='algorithms', action='store', nargs='+', help="Algorithms that we will be considered during training")
        
        FEA_GROUP = self._arg_parser.add_argument_group("Feature Preprocessing")
        FEA_GROUP.add_argument('--normalize', dest='norm', action='store', default="zscore", choices=["zscore","linear","dec","pca","none"], help='normalization approach')
        FEA_GROUP.add_argument('--impute', dest='impute', action='store', default="mean", choices=["mean","median", "most_frequent", "-512", "none"], help='feature imputation approach')
        FEA_GROUP.add_argument('--pca-dims', dest='pca_dims', action='store', default=7, type=int, help='number of features after dimension pca reduction')
        FEA_GROUP.add_argument('--feature-selection', dest='feat_sel', action='store', default=None, choices=[None,"forward","backward","random"], help="Perform feature selection before training (beginning with forward (empty set) or backward (full feature set)")
        FEA_GROUP.add_argument('--feature-selection-restarts', dest='feat_sel_restarts', action='store', default=1, type=int, help="Number of restarts of feature selection; selection start point should be \"random\"")
        FEA_GROUP.add_argument('--feature-indicator', dest='feature_indicator', action='store', nargs='+', help="list of 1 and 0 for indicating use of feature on position n yes or no (disables feature selection; ensure same length of feature and this indicator)")
        FEA_GROUP.add_argument('--feature-steps', dest='feature_steps', action='store', nargs='+', help="use only feature steps (groups) given in this list")
        FEA_GROUP.add_argument('--features', dest='features', action='store', nargs='+', help="use only features given in this list (disables --feature-steps)")
        
        SVR_GROUP = self._arg_parser.add_argument_group("SVM/R Free Parameters (see sklearn docu); only used if all are specified")
        SVR_GROUP.add_argument('--svm-gamma', dest='svm_gamma', action='store', default=None, type=float, help="Kernel coefficient for rbf kernel")
        SVR_GROUP.add_argument('--svm-C', dest='svm_C', action='store', default=None, type=float, help="Penalty parameter C of the error term.")
        SVR_GROUP.add_argument('--svr-epsilon', dest='svm_epsilon', action='store', default=None, type=float, help="Epsilon in the epsilon-SVR model.")

        RF_GROUP = self._arg_parser.add_argument_group("Random Forest Free Parameters (see sklearn docu); only used if all are specified")
        RF_GROUP.add_argument('--rf-max_features', dest='rf_max_features', action='store', default="sqrt", choices=['sqrt','log2','None'], help="The number of features to consider when looking for the best split")
        RF_GROUP.add_argument('--rf-criterion', dest='rf_criterion', action='store', default="entropy", choices=['gini','entropy'], help="The function to measure the quality of a split. (only for classification)")
        RF_GROUP.add_argument('--rf-min_samples_leaf', dest='rf_min_samples_leaf', action='store', default=10, type=int, help="The minimum number of samples in newly created leaves.")
        
        GB_GROUP = self._arg_parser.add_argument_group("Gradient Boosting Free Parameters (see sklearn docu); only used if all are specified")
        GB_GROUP.add_argument('--gb-max_depth', dest='gb_max_depth', action='store', default=None, type=int, help="Maximum depth of the individual regression estimators.")
        GB_GROUP.add_argument('--gb-min_samples_leaf', dest='gb_min_samples_leaf', action='store', default=None, type=int, help="The minimum number of samples required to be at a leaf node.")
        GB_GROUP.add_argument('--gb-max_features', dest='gb_max_features', action='store', default=None, choices=['sqrt','log2','None'], help="The number of features to consider when looking for the best split.")
        
        RIDGE_GROUP = self._arg_parser.add_argument_group("Ridge Regression Free Parameters (see sklearn docu); only used if all are specified")
        RIDGE_GROUP.add_argument('--ridge-alpha', dest='ridge_alpha', action='store', default=None, type=float, help="Small positive values of alpha improve the conditioning of the problem and reduce the variance of the estimates")
        
        LASSO_GROUP = self._arg_parser.add_argument_group("Lasso Regression Free Parameters (see sklearn docu); only used if all are specified")
        LASSO_GROUP.add_argument('--lasso-alpha', dest='lasso_alpha', action='store', default=None, type=float, help="SConstant that multiplies the L1 term")
        
        CLUST_GROUP = self._arg_parser.add_argument_group("Clustering Options (requires --approach CLUSTERING)")
        CLUST_GROUP.add_argument('--clu-max-clusters', dest='clu_max_cluster', action='store', default='sqrt', choices=['sqrt','log','solvers'], help="maximal number of clusters")
        
        NN_GROUP = self._arg_parser.add_argument_group("kNN Options (requires --approach kNN|SNNAP)")
        NN_GROUP.add_argument('--kNN', dest='knn', action='store', default=1, type=int, help="k of k-NN")
        
        SNNAP_GROUP = self._arg_parser.add_argument_group("kNN Options (requires --approach SNNAP)")
        SNNAP_GROUP.add_argument('--best_n', dest='best_n', action='store', default=1, type=int, help="consider the best n solvers at ranking prediction (should be at most as large as the number of algorithms")
        
        ASPEED_GROUP = self._arg_parser.add_argument_group("ASPEED Options (requires --aspeed-opt)")
        ASPEED_GROUP.add_argument('--aspeed-opt', dest='aspeed_opt', action='store_true', default=False, help="Combine flexfolio with an algorithm schedule computed with aspeed")
        ASPEED_GROUP.add_argument('--concentrate', dest='aspeed_concentrate', action='store_true', default=False, help="concentrate on unsolved instances for selector training (filter solved instances before training)")
        ASPEED_GROUP.add_argument('--max-solver', dest='aspeed_max_solver', action='store', default=3, type=int, help="maximal size of aspeed schedule (excl. flexfolio)")
        ASPEED_GROUP.add_argument('--opt-mode', dest='aspeed_opt_mode', action='store', default=3, type=int, help="third optimization criterion of aspeed (see encoding)")
        ASPEED_GROUP.add_argument('--mem-limit', dest='aspeed_mem_limit', action='store', default=6000, type=int, help="maximal memory used by gringo and clasp")
        ASPEED_GROUP.add_argument('--time-limit', dest='aspeed_time_limit', action='store', default=300, type=int, help="maximal time used by each gringo and clasp")
        ASPEED_GROUP.add_argument('--time-pre-solvers', dest='aspeed_pre_slice', action='store', default=10000, type=int, help="maximal time used by the presolvers in the schedule (all others solvers than flexfolio")
        ASPEED_GROUP.add_argument('--clasp-path', dest='aspeed_clasp', action='store', default=None, help="path to clasp binary")
        ASPEED_GROUP.add_argument('--gringo-path', dest='aspeed_gringo', action='store', default=None, help="path to gringo (3.x) binary")
        ASPEED_GROUP.add_argument('--runsolver-path', dest='aspeed_runsolver', action='store', default=None, help="path to runsolver binary")
        ASPEED_GROUP.add_argument('--enc-path', dest='aspeed_enc', action='store', default=None, help="path to aspeed encoding file")
        ASPEED_GROUP.add_argument('--pre-solver-schedule', dest='pre_schedule', action='store', nargs='+', help=argparse.SUPPRESS) # format: pre-solver,time
        
        
        ENSEMBLE_GROUP = self._arg_parser.add_argument_group("ENSEMBLE Options (requires --approach ENSEMBLE)")
        ENSEMBLE_GROUP.add_argument('--sub-size', dest='ensemble_sub_size', action='store', default=0.7, type=float, help="percentage of subsampled training sets (0<x<1)")
        ENSEMBLE_GROUP.add_argument('--n-models', dest='ensemble_num_models', action='store', default="0,3,0,0,3,3", type=str, help="number of trained models for <REGRESSION>,<CLASSVOTER>,<CLASSMULTI>,<NN>,<kNN>,<KMEANS>")
        ENSEMBLE_GROUP.add_argument('--bootstrapping', dest='ensemble_bootstrapping', action='store_true', default=False, help="use bootstrapping to sample subset of training set")
        ENSEMBLE_GROUP.add_argument('--en-opt-q', dest='ensemble_q', action='store', default=50, type=int, help="percentile q of score distribution for optimization [0,100]")
        ENSEMBLE_GROUP.add_argument('--en-opt-base', dest='ensemble_base', action='store', default="ranks", choices=["ranks","scores"], help="is the portfolio constructed based on predicted scores or algorithm rankings")
        ENSEMBLE_GROUP.add_argument('--en-max-features', dest='ensemble_mfeatures', action='store', type=float, default=0.9,  help="ratio of sampled features per model in ensemble (0<x<1)")
    
        PARALLEL_GROUP = self._arg_parser.add_argument_group("PARALLEL Options")
        PARALLEL_GROUP.add_argument('--correlation', dest='correlation', action='store', default=0.0, type=float, help="consider correlation with <factor> between algorithms in selection of parallel portfolio", metavar="factor")

        TES_GROUP = self._arg_parser.add_argument_group("Test Options")
        TES_GROUP.add_argument('--train', dest='train', action='store_true', default=False, help='ignore all testing and simply train flexfolio')
        TES_GROUP.add_argument('--test-mode', dest='test_mode', action='store', default="normal", choices=["normal","satzilla"], help='normal: 1. features, 2. schedule\n satzilla: 1. schedule, 2. features')
        TES_GROUP.add_argument('--crossfold', dest='crossfold', action='store', default=10, type=int, help='use a x-fold cross validation for evaluation')
        TES_GROUP.add_argument('--cv-repetition', dest='cv_repetition', action='store', default=1, type=int, help='Repetition of CV as specified in cv.arff')
        TES_GROUP.add_argument('--test-set', dest='test_set', action='store', default=None, type=cv_def, help='Pairs of Repetition and Fold: \"(#rep1;#fold1),(#rep2;#fold2)...\" to define test set (disjunction)')
        TES_GROUP.add_argument('--train-set', dest='train_set', action='store', default=None, type=cv_def, help='Pairs of Repetition and Fold: \"(#rep1;#fold1),(#rep2;#fold2)...\" to define training set (disjunction)')
        TES_GROUP.add_argument('--classevaluation', dest='class_evaluation', action='store_true', default=False, help='extract classes based on paths and train on all instances except a class')
        TES_GROUP.add_argument('--seed', dest='seed', action='store', default=12345, type=int, help='random seed for reproducibility')
        TES_GROUP.add_argument('--print-times', dest='print_time', action='store', default=None, help='file for writing csv runtime file with flexfolio performance (with penalized scores)')
        TES_GROUP.add_argument('--sigtest-threads', dest='sigtest_threads', action='store_true', default=False, help='perform sigtest between threads and oracle')
        #=======================================================================
        # TES_GROUP.add_argument('--test-runtimes', dest='test_times', action='store', required=False, default= None, help='test instances: runtimes in csv (first col with instance names')    
        # TES_GROUP.add_argument('--test-features', dest='test_feats', action='store', required=False, default= None, help='test instances: instance features in csv (first col with instance names')
        # TES_GROUP.add_argument('--test-satunsat', dest='test_satunsat', action='store', required=False, default= None, help='test instances: sat (1) / unsat (-1) file')
        # #=======================================================================
        #=======================================================================
        # TES_GROUP.add_argument('--feature-time', dest='feature_time', action='store', required=False, default= None, help='file with times to compute features per instance')
        # TES_GROUP.add_argument('--feature-time-const', dest='feature_time_const', action='store', required=False, type=float, default=3.0, help='assume constant time for feature computation')
        #=======================================================================

        ADD_GROUP = self._arg_parser.add_argument_group("Additional Options")
        #=======================================================================
        # ADD_GROUP.add_argument('--configurations', dest='configs', action='store', required=False, default=None, help='JSON file with dic: confname -> configuration')
        # ADD_GROUP.add_argument('--satunsat', dest='satunsat', action='store', required=False, default=None, help='sat (1) / unsat (-1) file (only used with --approach SVR')
        #=======================================================================
        ADD_GROUP.add_argument('--filter-dups', dest='filter_duplicates', action='store_true', required=False, default=False, help='filter duplicated observations (same feature vector)')
        ADD_GROUP.add_argument('--verbose', dest='verbose', action='store', default=0, type=int, help='verbosity level of stdout')
    
        PRE_GROUP = self._arg_parser.add_argument_group("Pre-Configurations (overwrites other arguments")
        PRE_GROUP.add_argument('--preconf', dest='pre_conf', action='store', required=False, default=None, choices=["satzilla09","satzilla11","isac","3s", "claspfolio", "measp", "sbs", "aspeed", "aspeed1", "aspeed2"], help='use configurations like satzilla, ISAC or 3S')
    
        HIDDEN_GROUP = self._arg_parser.add_argument_group("HIDDEN Options")
        HIDDEN_GROUP.add_argument('--table-format', dest='table_format', action='store_true', default=False, help=argparse.SUPPRESS)
        HIDDEN_GROUP.add_argument('--plot-mt', dest='plot_mt', action='store_true', default=False, help=argparse.SUPPRESS)
        HIDDEN_GROUP.add_argument('--plot-classes', dest='plot_classes', action='store_true', default=False, help=argparse.SUPPRESS)
        HIDDEN_GROUP.add_argument('--plot-clusters', dest='clu_plot_cluster', action='store_true', default=False, help=argparse.SUPPRESS)
        HIDDEN_GROUP.add_argument('--smac', dest='smac', action='store_true', default=False, help=argparse.SUPPRESS)
        HIDDEN_GROUP.add_argument('--metric', dest='metric', action='store', default="PAR10", choices=["PAR10","PAR1","RMSE"], help=argparse.SUPPRESS)
        HIDDEN_GROUP.add_argument('--fold', dest='fold', action='store', default=-1, type=int, help=argparse.SUPPRESS) # [1 : 10] 
        HIDDEN_GROUP.add_argument('--t-aspeed', dest='threads_aspeed', action='store', default=1, type=int, help=argparse.SUPPRESS) # number of threads for pre-solving schedule by aspeed 

    def parse_arguments(self,sys_argv):
        '''
            parse all command line arguments based on previously initialized argparse object
            Parameter:
                sys_argv : sys.argv[1:]
        '''
        args_ = self._arg_parser.parse_args(sys_argv)

        if args_.pre_conf:
            args_ = self.__pre_configurations(args_)
        
        # map approach "ASPEED" to "SBS" with "--aspeed-opt"
        if args_.approach == "ASPEED":
            args_.approach = "SBS"
            args_.aspeed_opt = True
            args_.aspeed_max_solver = 10000 # practically not bounded

        self.__check_pathes(args_)
        self.__check_dependencies(args_)
        
        Printer.verbose = int(args_.verbose)
        
        # if a captime for feature computation is not given, use a tenth of the overall captime
        #=======================================================================
        # if args_.feat_time == -1:
        #     args_.feat_time = int(args_.cutoff / 10) 
        #=======================================================================
        
        if args_.feature_indicator:
            try:
                args_.feature_indicator = map(int,args_.feature_indicator)
            except:
                Printer.print_w("Feature Indicator list is not valid; expected something like: 0 1 0 0 1 1")
                args_.feature_indicator = None
        
        if args_.feature_indicator and not len(args_.feature_indicator) == args_.n_feats:
            Printer.print_e("Feature Indicator list has not the same length as the expected number of features (--nFeats)")
        
        return args_
        
    def __check_pathes(self, args_):
        '''
            check whether pathes of parsed arguments are valid
        '''
        #=======================================================================
        # if args_.times and not os.path.isfile(args_.times):
        #     Printer.print_e("File not found: %s" %(args_.times))
        # if args_.feats and not os.path.isfile(args_.feats):
        #     Printer.print_e("File not found: %s" %(args_.feats))
        # if args_.satunsat and not os.path.isfile(args_.satunsat):
        #     Printer.print_e("File not found: %s" %(args_.satunsat))     
        # if args_.configs and not os.path.isfile(args_.configs):
        #     Printer.print_e("File not found: %s" %(args_.configs))                 
        # if args_.feature_path and not os.path.isfile(args_.feature_path):
        #     Printer.print_e("File not found: %s" %(args_.feature_path))                 
        #     
        #=======================================================================
        if not os.path.isdir(args_.model_dir):
            Printer.print_e("Model Directory not found: %s" %(args_.model_dir)) 
        if args_.coseal and not os.path.isdir(args_.coseal):
            Printer.print_e("Coseal Directory not found: %s" %(args_.coseal))
        
        #=======================================================================
        # if args_.test_times and not os.path.isfile(args_.test_times):
        #     Printer.print_e("File not found: %s" %(args_.test_times)) 
        # if args_.test_feats and not os.path.isfile(args_.test_feats):
        #     Printer.print_e("File not found: %s" %(args_.test_feats)) 
        # if args_.test_satunsat and not os.path.isfile(args_.test_satunsat):
        #     Printer.print_e("File not found: %s" %(args_.test_satunsat))  
        #=======================================================================

        #=======================================================================
        # if args_.feature_time and not os.path.isfile(args_.feature_time):
        #     Printer.print_e("File not found: %s" %(args_.feature_time))      
        #=======================================================================
            
        if args_.gb_max_features == "None":
            args_.gb_max_features = None
        if args_.rf_max_features == "None":
            args_.rf_max_features = None
            
        #=======================================================================
        # if (not args_.times or not args_.feats or not args_.cutoff) and not args_.coseal:
        #     Printer.print_e("Specify single input files (times, cutoff and features) or provide all data in coseal style directory!")  
        #=======================================================================
        
        #aspeed paths
        if args_.aspeed_opt:
            # try to apply default look ups
            main_path = os.path.dirname(sys.argv[0]) # a bit ugly but better than nothing ... really useful comment ....
            if not args_.aspeed_clasp:
                args_.aspeed_clasp = os.path.join(main_path,"..","binaries/clasp")
            if not args_.aspeed_gringo:
                args_.aspeed_gringo = os.path.join(main_path,"..","binaries/gringo")
            if not args_.aspeed_runsolver:
                args_.aspeed_runsolver = os.path.join(main_path,"..","binaries/runsolver")
            if not args_.aspeed_enc:
                args_.aspeed_enc = os.path.join(main_path,"trainer/aspeed/enc/encoding-bounded-paper-Step1.lp")
            
            if not os.path.isfile(args_.aspeed_clasp):
                Printer.print_e("File not found: %s" %(args_.aspeed_clasp))
            if not os.path.isfile(args_.aspeed_gringo):
                Printer.print_e("File not found: %s" %(args_.aspeed_gringo))
            if not os.path.isfile(args_.aspeed_runsolver):
                Printer.print_e("File not found: %s" %(args_.aspeed_runsolver))
            if not os.path.isfile(args_.aspeed_enc):
                Printer.print_e("File not found: %s" %(args_.aspeed_enc))
            
    def __check_dependencies(self, args_):
        '''
            check all dependencies and exit by violation
        '''
        if args_.contributor_filter > 0 and args_.update_sup:
            Printer.print_e("Contribution Filtering and Update Support are not simultaneously supported!")
            
        if args_.aspeed_max_solver < 1:
            Printer.print_e("The schedule size of aspeed has to be at least 1!")

        #=======================================================================
        # if args_.feat_time < 0:
        #     args_.feat_time = args_.cutoff /10
        #=======================================================================

        try:
            args_.ensemble_num_models = map(int,args_.ensemble_num_models.split(","))
        except:
            Printer.print_e("The option --n-models expects a list with 6 elements (comma seperated)")
        if len(args_.ensemble_num_models) != 6:
            Printer.print_e("The option --n-models expects a list with 6 elements (comma seperated)")
        if sum(args_.ensemble_num_models) <= 0:
            Printer.print_e("The option --n-models has to have at least one element with > 0")
            
    def __pre_configurations(self, args_):
        '''
            reconfigure if pre configuration is given
        '''
        
        if args_.pre_conf == "satzilla11":
            args_.approach = "CLASSVOTER"
            args_.classifier = "RANDOMFOREST"
            args_.rf_max_features = "sqrt"
            args_.rf_criterion = "entropy"
            args_.rf_min_samples_leaf = 10
            args_.aspeed_opt = True
            args_.aspeed_max_solver = 3
            args_.aspeed_opt_mode  = 1
            args_.aspeed_pre_slice = 70 
            args_.norm = "zscore"
            
        if args_.pre_conf == "satzilla09":
            args_.approach = "REGRESSION"
            args_.regressor = "RIDGE"
            args_.log_data = True
            #args_.ridge_alpha = 1 
            args_.aspeed_opt = True
            args_.aspeed_max_solver = 2
            args_.aspeed_opt_mode  = 1
            args_.aspeed_pre_slice = 20 
            args_.norm = "zscore"
            
        if args_.pre_conf == "claspfolio":
            args_.approach = "REGRESSION"
            args_.regressor = "SVR"
            args_.log_data = False
            args_.norm = "zscore"
        
        if args_.pre_conf == "measp":
            args_.approach = "NN"
            args_.norm = "none"
        
        if args_.pre_conf == "isac":
            args_.approach = "CLUSTERING"
            args_.cluster_algo = "KMEANS"
            args_.clu_max_clusters = "sqrt"
            args_.norm = "linear"
            
        if args_.pre_conf == "3s":
            args_.approach = "kNN"
            args_.knn = 32
            args_.aspeed_opt = True
            args_.aspeed_max_solver = 100
            args_.aspeed_opt_mode  = 1
            args_.aspeed_pre_slice = -10 # int(args_.cutoff / 10)
            args_.norm = "linear"
        
        if args_.pre_conf == "sbs":
            args_.approach = "SBS"
            
        if args_.pre_conf == "aspeed":
            args_.approach = "ASPEED"          


        return args_
    