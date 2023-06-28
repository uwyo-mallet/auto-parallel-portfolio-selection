if(Sys.info()['sysname']=="Linux"){
  if(file.exists("/home/haniye/Documents/OrganizedScripts/ParallelLevel.R")){
    source("/home/haniye/Documents/OrganizedScripts/ParallelLevel.R") 
  }
  else{ 
    source("/gscratch/hkashgar/OrganizedScripts/ParallelLevel.R") 
  }
} else{
  source("C:/Users/hnyk9/Thesis/OrganizedScripts/ParallelLevel.R")
}

library(ggplot2)

SequentialPerformance <- R6Class(
  classname = "SequentialPerformance",
  inherit = ParallelLevel,
  public = list(
    features_path = NULL,
    features = NULL, 
    scenario_path = NULL,
    scenario = NULL,
    llamaData = NULL,
    vbsData = NULL,
    sbsSolver = NULL,
    unsolvedInstances = NULL,
    solvedInstances = NULL,
    cluster = FALSE,
    benchmarks_name = NULL,
    #constructor
    initialize = function(benchmarks_name="SAT2018", cluster = FALSE){
      self$cluster = cluster
      self = super$initialize(cores = 1, benchmarks_name = benchmarks_name, cluster = cluster)
      #set scenario path 
      if(benchmarks_name == "SAT2018"){
        if(Sys.info()['sysname']!="Linux"){
          self$scenario_path = paste("C:/Users/hnyk9/Thesis/PortfolioScheduling/ExperimentResults/aslib_scenarios/SAT18/SAT18_EXP/")
          self$features_path = "C:/Users/hnyk9/Thesis/PortfolioScheduling/ExperimentResults/csvs/SAT18/SAT2018_features.csv"
        } else{
          self$scenario_path = paste("/home/haniye/Documents/PortfolioScheduling/ExperimentResults/aslib_scenarios/SAT18/SAT18_EXP/")
          self$features_path = "/home/haniye/Documents/PortfolioScheduling/ExperimentResults/csvs/SAT18/SAT2018_features.csv"
          if(cluster){
            self$scenario_path = paste("/gscratch/hkashgar/PortfolioScheduling/ExperimentResults/aslib_scenarios/SAT18/SAT18_EXP/")
            self$features_path = "/gscratch/hkashgar/PortfolioScheduling/ExperimentResults/csvs/SAT18/SAT2018_features.csv"
          }
        }
      } else if(benchmarks_name == "SAT2016"){
        if(Sys.info()['sysname']!="Linux"){
          self$scenario_path = paste("C:/Users/hnyk9/Thesis/PortfolioScheduling/ExperimentResults/aslib_scenarios/SAT16/SAT16-MAIN/")
          self$features_path = "C:/Users/hnyk9/Thesis/PortfolioScheduling/ExperimentResults/csvs/SAT16/SAT2016_features.csv"
        } else{
          self$scenario_path = paste("/home/haniye/Documents/PortfolioScheduling/ExperimentResults/aslib_scenarios/SAT16/SAT16-MAIN/")
          self$features_path = "/home/haniye/Documents/PortfolioScheduling/ExperimentResults/csvs/SAT16/SAT2016_features.csv"
          if(cluster){
            self$scenario_path = paste("/gscratch/hkashgar/PortfolioScheduling/ExperimentResults/aslib_scenarios/SAT16/SAT16-MAIN/")
            self$features_path = "/gscratch/hkashgar/PortfolioScheduling/ExperimentResults/csvs/SAT16/SAT2016_features.csv"        
          }
        }
      } else if(benchmarks_name == "GRAPHS2015"){
        if(Sys.info()['sysname']!="Linux"){
          self$scenario_path = paste("C:/Users/hnyk9/Thesis/Portfolio-Scheduling/originalCSVs-Teton_GRAPHS15/GRAPHS-2015/")
          self$features_path = "C:/Users/hnyk9/Thesis/Portfolio-Scheduling/originalCSVs-Teton_GRAPHS15/GRAPHS2015_features.csv"
        } else{
          self$scenario_path = paste("/home/haniye/Documents/Portfolio-Scheduling/originalCSVs-Teton_GRAPHS15/GRAPHS-2015/")
          self$features_path = "/home/haniye/Documents/Portfolio-Scheduling/originalCSVs-Teton_GRAPHS15/GRAPHS2015_features.csv"
          if(cluster){
            self$scenario_path = paste("/gscratch/hkashgar/Portfolio-Scheduling/originalCSVs-Teton_GRAPHS15/GRAPHS-2015/")
            self$features_path = "/gscratch/hkashgar/Portfolio-Scheduling/originalCSVs-Teton_GRAPHS15/GRAPHS2015_features.csv"            
          }
        }
      } else if(benchmarks_name == "MAXSAT2019"){
        if(Sys.info()['sysname']!="Linux"){
          self$scenario_path = paste("C:/Users/hnyk9/Thesis/PortfolioScheduling/ExperimentResults/aslib_scenarios/MAXSAT19/MAXSAT-2019/")
          self$features_path = "C:/Users/hnyk9/Thesis/PortfolioScheduling/ExperimentResults/csvs/MAXSAT19/MAXSAT2019_features.csv"
        } else{
          self$scenario_path = paste("/home/haniye/Documents/PortfolioScheduling/ExperimentResults/aslib_scenarios/MAXSAT19/MAXSAT-2019/")
          self$features_path = "/home/haniye/Documents/PortfolioScheduling/ExperimentResults/csvs/MAXSAT19/MAXSAT2019_features.csv"
          if(cluster){
            self$scenario_path = paste("/gscratch/hkashgar/PortfolioScheduling/ExperimentResults/aslib_scenarios/MAXSAT19/MAXSAT-2019/")
            self$features_path = "/gscratch/hkashgar/PortfolioScheduling/ExperimentResults/csvs/MAXSAT19/MAXSAT2019_features.csv"            
          }
        }
      } else if(benchmarks_name == "IPC2018"){
        if(Sys.info()['sysname']!="Linux"){
          self$scenario_path = paste("C:/Users/hnyk9/Thesis/PortfolioScheduling/ExperimentResults/aslib_scenarios/IPC2018/IPC2018/")
          self$features_path = "C:/Users/hnyk9/Thesis/PortfolioScheduling/ExperimentResults/csvs/IPC2018/IPC2018_features.csv"
        } else{
          self$scenario_path = paste("/home/haniye/Documents/PortfolioScheduling/ExperimentResults/aslib_scenarios/IPC2018/IPC2018/")
          self$features_path = "/home/haniye/Documents/PortfolioScheduling/ExperimentResults/csvs/IPC2018/IPC2018_features.csv"
          if(cluster){
            self$scenario_path = paste("/gscratch/hkashgar/PortfolioScheduling/ExperimentResults/aslib_scenarios/IPC2018/IPC2018/")
            self$features_path = "/gscratch/hkashgar/PortfolioScheduling/ExperimentResults/csvs/IPC2018/IPC2018_features.csv"            
          }
        }
      } else if(benchmarks_name == "SAT11-INDU"){
        if(Sys.info()['sysname']!="Linux"){
          self$scenario_path = paste("C:/Users/hnyk9/Thesis/PortfolioScheduling/ExperimentResults/aslib_scenarios/SAT11-INDU/SAT11-INDU/")
          self$features_path = "C:/Users/hnyk9/Thesis/PortfolioScheduling/ExperimentResults/csvs/SAT11-INDU/SAT11-INDU_features.csv"
        } else{
          self$scenario_path = paste("/home/haniye/Documents/PortfolioScheduling/ExperimentResults/aslib_scenarios/SAT11-INDU/SAT11-INDU/")
          self$features_path = "/home/haniye/Documents/PortfolioScheduling/ExperimentResults/csvs/SAT11-INDU/SAT11-INDU_features.csv"
          if(cluster){
            self$scenario_path = paste("/gscratch/hkashgar/PortfolioScheduling/ExperimentResults/aslib_scenarios/SAT11-INDU/SAT11-INDU/")
            self$features_path = "/gscratch/hkashgar/PortfolioScheduling/ExperimentResults/csvs/SAT11-INDU/SAT11-INDU_features.csv"            
          }
        }
      }
      invisible(self)
    },
    
    #get scenario, scenario path is predefined 
    get_scenario = function(){
      if(is.null(self$scenario)){
        self$scenario = parseASScenario(self$scenario_path)
        #convert scenario to llama data format
        self$llamaData = convertToLlamaCVFolds(self$scenario)
      }
      return(self$scenario)
    },
    
    #get instance features, path of the csv is predefined
    get_features = function(){
      if(is.null(self$features) || nrow(self$features) == 0){
        self$features = read.csv(self$features_path)
        if(!is.null(self$features$benchmark))
          self$features = self$features[order(self$features$benchmark),]
        if(!is.null(self$features$InstanceName))
          self$features = self$features[order(self$features$InstanceName),]
      }
      return(self$features)
    },
    
    #get vbs solvers and runtime per instance    
    get_VBS = function(){
      #get min runtimes
      VBS_Runtime = rowMins(as.matrix(self$actual_CSV[,2:(self$n_solvers+1)]),na.rm = FALSE)
      #get solvers which gives minimum runtimes
      VBS_Solvers = colnames(self$actual_CSV)[apply(self$actual_CSV,1,which.min)]
      #combine both to csv
      vbs = data.frame(self$actual_CSV$InstanceName, VBS_Solvers,VBS_Runtime)
      colnames(vbs)[1] <- "InstanceName"
      #set the props in the class
      self$vbsData = vbs
      self$solvedInstances = subset(vbs,vbs$VBS_Runtime<self$Cutoff )$InstanceName
      if(is.null(self$unsolvedInstances)) self$unsolvedInstances = subset(vbs,vbs$VBS_Runtime>=self$Cutoff )$InstanceName
      return(self$vbsData)
    },
    
    #get vbs's par10
    get_VBS_par10 = function(){
      vbs = self$get_VBS()
      vbs$VBS_Runtime[which(vbs$VBS_Runtime>=self$Cutoff )]<- (self$Cutoff * 10)
      print(summary(vbs$VBS_Runtime))
      return(vbs)
    },
    
    #get vbs's mcp
    get_VBS_mcp = function(){
      return("MCP for VBS is always zero!")
    },
    
    #get instances solved by vbs
    get_solved_instances = function(){
      self$get_VBS()
      return(self$solvedInstances)
    },
    
    #get instances not solved by vbs
    get_unsolved_instances = function(){
      self$get_VBS()
      return(self$unsolvedInstances)
    },
    
    #get SBS for all instances
    get_SBS = function(){
      self$get_scenario()
      self$sbsSolver = as.vector(unique(singleBest(self$llamaData)$algorithm))
      return(self$sbsSolver)
    },
    
    #input = solver name, output = runtimes for solved cases
    get_solvers_solved_runtime = function(solver){
      runtimes = self$actual_CSV[solver]
      return(runtimes[runtimes<self$Cutoff])
    },
    
    #method to use when we want to ignore the instances solved by vbs, overrided from top
    ignore_instances = function(unsolvedinstances=NULL){
      self$get_mcp_dataframe(self)
      #get unsolved instances if not provided
      if(is.null(unsolvedinstances)) {
        self$unsolvedInstances = self$get_unsolved_instances()
        unsolvedinstances = self$unsolvedInstances
      }
      #run parent's method
      super$ignore_instances(unsolvedinstances)
      #get features and ignore unsolved instance features
      if(is.null(self$features) || nrow(self$features) == 0) self$get_features()
      self$features = subset(self$features, !(self$features$benchmark %in% unsolvedinstances))
      #get scenario and ignore instances in scenario
      if(is.null(self$scenario)) self$get_scenario()
      self$scenario$algo.runs = subset(self$scenario$algo.runs,!(self$scenario$algo.runs$instance_id %in% unsolvedinstances))
      self$scenario$algo.runstatus = subset(self$scenario$algo.runstatus,!(self$scenario$algo.runstatus$instance_id %in% unsolvedinstances))
      self$scenario$cv.splits = subset(self$scenario$cv.splits,!(self$scenario$cv.splits$instance_id %in% unsolvedinstances))
      self$scenario$feature.values = subset(self$scenario$feature.values,!(self$scenario$feature.values$instance_id %in% unsolvedinstances))
      self$scenario$feature.costs = subset(self$scenario$feature.costs,!(self$scenario$feature.costs$instance_id %in% unsolvedinstances))
      self$scenario$cv.splits = subset(self$scenario$cv.splits,!(self$scenario$cv.splits$instance_id %in% unsolvedinstances))
      self$scenario$feature.runstatus = subset(self$scenario$feature.runstatus,!(self$scenario$feature.runstatus$instance_id %in% unsolvedinstances))
      self$llamaData = aslib::convertToLlamaCVFolds(self$scenario)
      #get vbs, get sbs
      self$get_VBS()
      self$get_SBS()
      self$n_instances = nrow(self$actual_CSV)
      invisible(self)
    },
    
    #get the second, third vbs solvers and runtime per instance    
    get_nd_VBS = function(nd = 1){
      #get min runtimes
      Runtime = apply(self$actual_CSV[2:ncol(self$actual_CSV)],1, FUN = function(x) sort(x)[nd])
      #get solvers which gives minimum runtimes
      Solvers = colnames(self$actual_CSV)[sapply(1:nrow(self$actual_CSV),FUN = function(x) which(self$actual_CSV[x,1:ncol(self$actual_CSV)] == Runtime[x])[[1]])]
      #combine both to csv
      res = data.frame(self$actual_CSV$InstanceName, Solvers,Runtime)
      colnames(res)[1] <- "InstanceName"
      return(res)
    },
    
    #train simple random forest method 
    #parameter tunning is not implemented (future work)
    train_randomForest = function(savepath, ignoreTimeouts, train_by_par10=FALSE){
      self$get_scenario()
      if(ignoreTimeouts) {self$ignore_instances()}
      # check if instances are not removed already!
      else{if(self$n_instances == length(self$solvedInstances) && (!(is.null(self$unsolvedInstances)) || length(self$unsolvedInstances)!=0)) return("You have already removed the unsolved instances!")}
      data = self$llamaData
      #imputed features 
      features = data$data[data$features]
      #run in parallel
      parallelStartSocket(cpus = detectCores())
      for(solver in self$solvers){
        print(solver)
        solverdata = features
        print(nrow(solverdata))
        performance = data$data[solver]
        if(train_by_par10) performance[which(performance>=self$Cutoff ),] <- (self$Cutoff * 10)
        solverdata = cbind(solverdata,performance)
        solverTask <- makeRegrTask(data = solverdata, target = solver)
        Learner = makeLearner("regr.randomForest",predict.type = "se")
        CV = makeResampleDesc("CV",iters=10 ,predict = "both")
        res = resample(Learner,solverTask,resampling = CV ,models = TRUE)
        saveRDS(res,paste(savepath,"/",solver,".rds",sep = ""))
      }
      parallelStop() 
      invisible(self)
    },
    
    #train simple random forest method 
    #parameter tunning is not implemented (future work)
    train_randomForest_validation_set = function(train_randomForest_validation_setPath, validationInstances = NULL, ignoreTimeouts=TRUE, train_by_par10=FALSE, CrossValidation = FALSE){
      self$get_scenario()
      if(ignoreTimeouts) {self$ignore_instances()}
      # check if instances are not removed already!
      else{if(self$n_instances == length(self$solvedInstances) && (!(is.null(self$unsolvedInstances)) || length(self$unsolvedInstances)!=0)) return("You have already removed the unsolved instances!")}
      llama = self$llamaData
      data = llama$data
      
      if(is_null(validationInstances)){
        set.seed(101) # Set Seed so that same sample can be reproduced in future also
        # Now Selecting 50% of data as sample from total 'n' rows of the data
        sample <- sample.int(n = nrow(data), size = floor(.80*nrow(data)), replace = FALSE)
        train_test <- data[sample, ]
        train_test = train_test[order(train_test$instance_id),]
        validation  <- data[-sample, ]
        validation = validation[order(validation$instance_id),]
      } else{
        train_test <- data[which(! data$instance_id %in% validationInstances), ]
        train_test = train_test[order(train_test$instance_id),]
        validation  <- data[which(data$instance_id %in% validationInstances), ]
        validation = validation[order(validation$instance_id),]
      }
      rownames(train_test) <- c(1:nrow(train_test))
      
      #imputed features 
      features = train_test[c("instance_id",llama$features)]
      valid_features = validation[c("instance_id",llama$features)]
      #run in parallel
      parallelStartSocket(cpus = detectCores())
      i = rownames(train_test)
      for(solver in self$solvers){
        print(solver)
        solverdata = features
        print(nrow(solverdata))
        performance = train_test[solver]
        performance_valid = validation[solver]
        if(train_by_par10){
          performance[which(performance>=self$Cutoff),] <- (self$Cutoff * 10)
          performance_valid[which(performance_valid>=self$Cutoff ),] <- (self$Cutoff * 10)
        }
        solverdata = cbind(solverdata,performance)
        test_train_instances = solverdata[1]
        validation_data = cbind(validation,performance_valid)
        validation_instance = validation[1]
        solverTask <- makeRegrTask(data = solverdata[-1], target = solver)
        Learner = makeLearner("regr.randomForest",predict.type = "se")
        if(CrossValidation == TRUE){
          CV = makeResampleDesc("CV",iters=10 ,predict = "both")
          res = resample(Learner,solverTask,resampling = CV ,models = TRUE)
          ins_rep = c(rep(solverdata$instance_id,10))
          ins_rep = ins_rep[order(ins_rep)]
          res$pred$data$id = as.numeric(res$pred$data$id)
          res$pred$data = res$pred$data[order(res$pred$data$id),]
          res$pred$data$InstanceName = ins_rep
          saveRDS(res,paste(train_randomForest_validation_setPath,"/",solver,".rds",sep = ""))
          validation_predict=list()
          for(i in 1:10){
            pred = predict(res$models[[i]],newdata = validation_data[-1])
            pred$data$InstanceName = validation_data$instance_id
            pred$data$iter = c(rep(i,nrow(validation_data)))
            pred$data$set = c(rep("validation",nrow(validation_data)))
            pred$data = pred$data[,c(4,1,2,3,5,6)]
            validation_predict[[i]] = pred
          }
          saveRDS(validation_predict,paste(train_randomForest_validation_setPath,"/",solver,"_validation_preds.rds",sep = ""))
        } else{
          # Get the number of observations
          n = getTaskSize(solverTask)
          #set seed to always create the sample subset
          set.seed(101)
          # Use 1/3 of the observations for training
          train.set = sample(n, size = 9*n/10)
          test.set = c(1:getTaskSize(solverTask))
          test.set = test.set[which(!test.set%in%train.set)]
          model = train(Learner, solverTask, subset = train.set)
          res = predict(model, task=solverTask)
          res$data = cbind(res$data,rep( 1,n))
          colnames(res$data)[5]<-"iter"
          set = rep("train",n)
          set[test.set]<- "test"
          res$data = cbind(res$data, set)
          res$data = cbind(res$data,test_train_instances)
          colnames(res$data)[ncol(res$data)]<-"InstanceName"
          saveRDS(res,paste(train_randomForest_validation_setPath,"/",solver,".rds",sep = ""))
          
          validation_predict = predict(model, task=makeRegrTask(data = cbind(valid_features,validation_data[solver])[-1], target = solver))
          validation_predict$data = cbind(validation_predict$data,rep(1,nrow(valid_features)))
          colnames(validation_predict$data)[5]<-"iter"
          set = rep("validation",nrow(validation_predict$data))
          validation_predict$data = cbind(validation_predict$data, set)
          validation_predict$data = cbind(validation_predict$data,validation_instance)
          colnames(validation_predict$data)[ncol(validation_predict$data)]<-"InstanceName"
          saveRDS(validation_predict,paste(train_randomForest_validation_setPath,"/",solver,"_validation_preds.rds",sep = ""))
        }
      }
      parallelStop() 
      invisible(self)
    },
    
    #train simple random forest method 
    #parameter tunning is not implemented (future work)
    train_randomForest_except_instance = function(train_randomForest_validation_setPath, ignoreTimeouts=TRUE, train_by_par10=FALSE, instance, CrossValidation = FALSE){
      self$get_scenario()
      if(ignoreTimeouts) {self$ignore_instances()}
      # check if instances are not removed already!
      else{if(self$n_instances == length(self$solvedInstances) && (!(is.null(self$unsolvedInstances)) || length(self$unsolvedInstances)!=0)) return("You have already removed the unsolved instances!")}
      llama = self$llamaData
      data = llama$data
      train_test <- data[which(data$instance_id!=instance),]
      train_test = train_test[order(train_test$instance_id),]
      validation  <- data[which(data$instance_id == instance),]
      validation = validation[order(validation$instance_id),]
      rownames(train_test) <- c(1:nrow(train_test))
      #imputed features 
      features = train_test[c("instance_id",llama$features)]
      valid_features = validation[c("instance_id",llama$features)]
      #run in parallel
      parallelStartSocket(cpus = detectCores())
      i = rownames(train_test)
      for(solver in self$solvers){
        print(solver)
        solverdata = features
        print(nrow(solverdata))
        performance = train_test[solver]
        performance_valid = validation[solver]
        if(train_by_par10){
          performance[which(performance>=self$Cutoff),] <- (self$Cutoff * 10)
          performance_valid[which(performance_valid>=self$Cutoff ),] <- (self$Cutoff * 10)
        }
        solverdata = cbind(solverdata,performance)
        test_train_instances = solverdata[1]
        validation_data = cbind(validation,performance_valid)
        validation_instance = validation[1]
        solverTask <- makeRegrTask(data = solverdata[-1], target = solver)
        Learner = makeLearner("regr.randomForest",predict.type = "se")
        if(CrossValidation == TRUE){
          CV = makeResampleDesc("CV",iters=10 ,predict = "both")
          res = resample(Learner,solverTask,resampling = CV ,models = TRUE)
          ins_rep = c(rep(solverdata$instance_id,10))
          ins_rep = ins_rep[order(ins_rep)]
          res$pred$data$id = as.numeric(res$pred$data$id)
          res$pred$data = res$pred$data[order(res$pred$data$id),]
          res$pred$data$InstanceName = ins_rep
          saveRDS(res,paste(train_randomForest_validation_setPath,"/",solver,".rds",sep = ""))
          validation_predict=list()
          for(i in 1:10){
            pred = predict(res$models[[i]],newdata = validation_data[-1])
            pred$data$InstanceName = validation_data$instance_id
            pred$data$iter = c(rep(i,nrow(validation_data)))
            pred$data$set = c(rep("validation",nrow(validation_data)))
            pred$data = pred$data[,c(4,1,2,3,5,6)]
            validation_predict[[i]] = pred
          }
          saveRDS(validation_predict,paste(train_randomForest_validation_setPath,"/",solver,"_validation_preds.rds",sep = ""))
        }
        else{
          # Get the number of observations
          n = getTaskSize(solverTask)
          #set seed to always create the sample subset
          set.seed(101)
          # Use 1/3 of the observations for training
          train.set = sample(n, size = 9*n/10)
          test.set = c(1:getTaskSize(solverTask))
          test.set = test.set[which(!test.set%in%train.set)]
          model = train(Learner, solverTask, subset = train.set)
          res = predict(model, task=solverTask)
          
          res$data = cbind(res$data,rep( 1,n))
          colnames(res$data)[5]<-"iter"
          set = rep("train",n)
          set[test.set]<- "test"
          res$data = cbind(res$data, set)
          res$data = cbind(res$data,test_train_instances)
          colnames(res$data)[ncol(res$data)]<-"InstanceName"
          saveRDS(res,paste(train_randomForest_validation_setPath,"/",solver,".rds",sep = ""))
          
          validation_predict = predict(model, task=makeRegrTask(data = cbind(valid_features,validation_data[solver])[-1], target = solver))
          validation_predict$data = cbind(validation_predict$data,rep(1,nrow(valid_features)))
          colnames(validation_predict$data)[5]<-"iter"
          set = rep("validation",nrow(validation_predict$data))
          validation_predict$data = cbind(validation_predict$data, set)
          validation_predict$data = cbind(validation_predict$data,validation_instance)
          colnames(validation_predict$data)[ncol(validation_predict$data)]<-"InstanceName"
          saveRDS(validation_predict,paste(train_randomForest_validation_setPath,"/",solver,"_validation_preds.rds",sep = ""))
        }
      }
      parallelStop() 
      invisible(self)
    },
    
    #train random forest, tuned and cv10
    #doesn't work on local machine because of batchtools
    #maybe can be fixed in future
    train_randomForest_aslibLike = function(savepath, ignoreTimeouts, train_by_par10=FALSE){
      asscenario = self$get_scenario()
      learner = makeLearner("regr.randomForest",predict.type = "se")
      learner = makeImputeWrapper(learner = learner,
                                          classes = list(numeric = imputeMean(), integer = imputeMean(), logical = imputeMode(),
                                                         factor = imputeConstant("NA"), character = imputeConstant("NA")))
      learner = makeImputeWrapper(learner = learner,
                                          classes = list(numeric = imputeMean(), integer = imputeMean(), logical = imputeMode(),
                                                         factor = imputeConstant("?"), character = imputeConstant("?")))
      par.set = makeParamSet(
        makeIntegerParam("ntree", lower = 10, upper = 200),
        makeIntegerParam("mtry", lower = 1, upper = 30)
      )
      wd = getwd()
      setwd(savepath)
      rs.iters = asInt(250L, lower = 1L)
      n.inner.folds = asInt(3L, lower = 2L)
      llama.scenario = convertToLlama(asscenario = asscenario, feature.steps = 'ALL')
      llama.cv = self$llamaData
      desc = asscenario$desc
      cutoff = desc$algorithm_cutoff_time
      timeout = if (desc$performance_type[[1L]] == "runtime" && !is.na(cutoff)) {
        cutoff
      } else {
        NULL
      }
      n.algos = length(getAlgorithmNames(asscenario))
      pre = function(x, y = NULL) {
        list(features = x)
      }
      n.outer.folds = length(llama.cv$test)
      outer.preds = vector("list", n.outer.folds)
      ldf = llama.cv
      
      for (i in 1:n.outer.folds) {
        ldf2 = ldf
        ldf2$data = ldf$data[ldf$train[[i]],]
        ldf2$train = NULL
        ldf2$test = NULL
        ldf3 = cvFolds(ldf2, nfolds = n.inner.folds, stratify = FALSE)
        
        des = ParamHelpers::generateRandomDesign(rs.iters, par.set, trafo = TRUE)
        des.list = ParamHelpers::dfRowsToList(des, par.set)
        parallelStartMulticore()
        ys = parallelMap(function(x) {
          par10 = try({
            learner = setHyperPars(learner, par.vals = x)
            p = regression(regressor = learner, data = ldf3, pre = pre)
            ldf4 = fixFeckingPresolve(asscenario, ldf3)
            par10 = mean(parscores(ldf4, p, timeout = timeout))
            messagef("[Tune]: %s : par10 = %g", ParamHelpers::paramValueToString(par.set, x), par10)
            return(par10)
          })
          if(inherits(par10, "try-error")) {
            par10 = NA
          }
          return(par10)
        }, des.list, simplify = TRUE)
        parallelStop()
        best.i = getMinIndex(ys)
        best.parvals = des.list[[best.i]]
        print(best.parvals)
        messagef("[Best]: %s : par10 = %g", ParamHelpers::paramValueToString(par.set, best.parvals), ys[best.i])
        parvals= best.parvals
        
        learner2 = setHyperPars(learner, par.vals = parvals)
        outer.split.ldf = ldf
        outer.split.ldf$train = list(ldf$train[[i]])
        outer.split.ldf$test = list(ldf$test[[i]])
        outer.preds[[i]] = regression(learner2, data = outer.split.ldf, pre = pre)
        outer.preds[[i]]$train = outer.split.ldf$train 
        outer.preds[[i]]$test = outer.split.ldf$test 
      }
      
      retval = outer.preds[[1]]
      retval$predictions = do.call(rbind, lapply(outer.preds, function(x) { x$predictions }))
      saveRDS(retval, file = paste(savepath,"/randomForest_predictions.RDS",sep=""))
      saveRDS(outer.preds, file = paste(savepath,"/randomForest_all.RDS",sep=""))
      return(retval) 
    },
    
    #split by solver all actual
    split_dataframe_by_solver = function(saveto){
      path = self$actual_CSV_path
      path = str_split(path,"/")[[1]]
      path = path[-length(path)]
      path = paste(path, collapse = '/')
      if(self$benchmarks_name == "SAT2018"){
        csvs = list.files(path,"replacement.csv",full.names = TRUE)
      } else if(self$benchmarks_name == "SAT2016"){
        csvs = list.files(path,".csv",full.names = TRUE)
      }
      cores = c(1:10,20,30,32)
      solvercsv = data.frame()
      for(i in 2:self$n_solvers){
        colnames = vector()
        colnames = append(colnames,"InstanceName")
        solver = colnames(self$actual_CSV[i])
        solvercsv = self$actual_CSV[1]
        for(core in cores){
          if(core == 1){ 
            csv = csvs[which(grepl(csvs,pattern = "-solo-"))]
            core = "1-parallel"
          } else {
            csv = csvs[which(grepl(csvs,pattern = paste("-",core,"-parallel",sep = "")))]
            core = paste(core,"-parallel",sep = )
          }
          readcsv = read.csv(csv)
          readcsv = readcsv[order(readcsv$InstanceName),]
          colnames = append(colnames,core)
          solvercsv = cbind(solvercsv,readcsv[solver])
        }
        colnames(solvercsv) <- colnames
        write.csv(solvercsv,paste(saveto,solver,".csv",sep=""),row.names = FALSE)
      }
    }
  )
)
