if(Sys.info()['sysname']=="Linux"){
  if(file.exists("/home/haniye/Documents/OrganizedScripts/SequentialPerformance.R")){
    source("/home/haniye/Documents/OrganizedScripts/SequentialPerformance.R") 
  }
  else{ 
    source("/gscratch/hkashgar/OrganizedScripts/SequentialPerformance.R") 
  }
} else{
  source("C:/Users/hnyk9/OneDrive - University of Wyoming/OrganizedScripts/SequentialPerformance.R")
}


PredictionResults = R6Class(
  classname = "PredictionResults",
  public = list(
    sequentialData = NULL,
    benchmarks_name = NULL,
    predictionPath = NULL,
    modelPath = NULL,
    selectionPath = NULL,
    cluster = FALSE,
    cpus = detectCores(),
    initialize = function(benchmarks_name="SAT2018", cluster = FALSE){
      self$benchmarks_name = benchmarks_name
      self$sequentialData = SequentialPerformance$new(benchmarks_name, cluster)
      self$cluster = cluster
      if(Sys.info()['sysname']=="Linux"){
        self$predictionPath = paste("/home/haniye/Documents/OrganizedScripts/",self$benchmarks_name,"/preds/",sep = "")
        self$modelPath =  paste("/home/haniye/Documents/mlr-scripts/",self$benchmarks_name,"/Prediction/StandardError/",sep="")
        self$selectionPath = paste("/home/haniye/Documents/OrganizedScripts/",self$benchmarks_name,"/selection/",sep = "")
        if(cluster){
          self$predictionPath = paste("/gscratch/hkashgar/OrganizedScripts/",self$benchmarks_name,"/preds/",sep = "")
          self$modelPath =  paste("/gscratch/hkashgar/mlr-scripts/",self$benchmarks_name,"/Prediction/StandardError/",sep="")
          self$selectionPath = paste("/gscratch/hkashgar/OrganizedScripts/",self$benchmarks_name,"/selection/",sep = "")
          
        }
      } else{
        self$predictionPath = paste("C:/Users/hnyk9/OneDrive - University of Wyoming/OrganizedScripts/",self$benchmarks_name,"/preds/",sep = "")
        self$modelPath =  paste("C:/Users/hnyk9/OneDrive - University of Wyoming/mlr-scripts/",self$benchmarks_name,"/Prediction/StandardError/",sep="")
        self$selectionPath = paste("C:/Users/hnyk9/OneDrive - University of Wyoming/OrganizedScripts/",self$benchmarks_name,"/selection/",sep = "")
      }
      if(is.null(self$sequentialData$scenario)) self$sequentialData$get_scenario()
    },  
    
    #get the models' prediction for test set
    get_models_prediction = function(modelPath = self$modelPath,savePath = self$predictionPath,train_by_par10=FALSE){
      modelPath = paste(modelPath,"randomForest_predictions.RDS",sep="")
      print(modelPath)
      predictions = readRDS(modelPath)$predictions
      instances = self$sequentialData$llamaData$data$instance_id
      #instance ids are ordered as 
      parallelStartSocket(cpus = self$cpus)
      for(i in 1:length(instances)){
        if(startsWith(self$benchmarks_name,"SAT")){
          if(!file.exists(paste(savePath,"/",str_split(instances[i],"sat/")[[1]][2],".csv",sep=""))){
            data = predictions[which(predictions$instance_id==instances[i]),]
            data = data[-5]
            rowTruth = self$sequentialData$get_actual_result_csv()
            rowTruth = rowTruth[which(rowTruth$InstanceName==instances[i]),]
            Truth <- melt(rowTruth, id.vars = c("InstanceName"), variable_name = "Solver")
            colnames(Truth)[2] = "Solver"
            Truth = Truth[order(Truth$Solver),]
            data = data[order(data$algorithm),]
            #print(data$algorithm == Truth$Solver)
            data = add_column(data,Truth$value,.after = "algorithm")
            #check if data is par10
            if(train_by_par10) {colnames(data)<-c("InstanceName","Solver","ActualPar10","PredictedPar10","Prediction_StandardError")}
            else {colnames(data)<-c("InstanceName","Solver","ActualRuntime","PredictedRuntime","Prediction_StandardError")}
            write.csv(data,paste(savePath,"/",str_split(instances[i],"sat/")[[1]][2],".csv",sep=""), row.names = FALSE)
          }
          else{
            print(paste("File ",paste(savePath,"/",str_split(instances[i],"sat/")[[1]][2],".csv",sep=""), " exist!",sep = ""))
          }
        } else {
          if(!file.exists(paste(savePath,"/",instances[i],".csv",sep=""))){
            data = predictions[which(predictions$instance_id==instances[i]),]
            data = data[-5]
            rowTruth = self$sequentialData$get_actual_result_csv()
            rowTruth = rowTruth[which(rowTruth$InstanceName==instances[i]),]
            Truth <- melt(rowTruth, id.vars = c("InstanceName"), variable_name = "Solver")
            colnames(Truth)[2]<-"Solver"
            Truth = Truth[order(Truth$Solver),]
            data = data[order(data$algorithm),]
            #print(data$algorithm == Truth$Solver)
            data = add_column(data,Truth$value,.after = "algorithm")
            #check if data is par10
            if(train_by_par10) {colnames(data)<-c("InstanceName","Solver","ActualPar10","PredictedPar10","Prediction_StandardError")}
            else {colnames(data)<-c("InstanceName","Solver","ActualRuntime","PredictedRuntime","Prediction_StandardError")}
            write.csv(data,paste(savePath,"/",instances[i],".csv",sep=""), row.names = FALSE)
          }
          else{
            print(paste("File ",paste(savePath,"/",str_split(instances[i],"sat/")[[1]][2],".csv",sep=""), " exist!",sep = ""))
          }
        }
      }
      parallelStop()
      invisible(self)
    },
    
    #get the models' prediction for test set
    get_models_prediction_test = function(modelPath,savePath,train_by_par10=FALSE){
      instances = self$sequentialData$llamaData$data$instance_id
      solvers = self$sequentialData$solvers
      #instance ids are ordered as 
      parallelStartSocket(cpus = self$cpus)
      for(i in 1:length(instances)){
        if(!file.exists(paste(savePath,"/",str_split(instances[i],"sat/")[[1]][2],".csv",sep=""))){
          data = data.frame(matrix(nrow = 0,ncol=5))
          for(solver in solvers){
            rds = readRDS(paste(modelPath,"/",solver,".rds",sep = ""))
            id_instance = i
            predictions_solver = rds$pred$data[which(rds$pred$data$id == i),]
            predictions_solver = predictions_solver[which(predictions_solver$set == "test"),]
            row = c(instances[i],solver,as.numeric(predictions_solver$truth), as.numeric(predictions_solver$response),as.numeric(predictions_solver$se))
            data = rbind(data,row)
          }
          #check if data is par10
          if(train_by_par10) {colnames(data)<-c("InstanceName","Solver","ActualPar10","PredictedPar10","Prediction_StandardError")}
          else {colnames(data)<-c("InstanceName","Solver","ActualRuntime","PredictedRuntime","Prediction_StandardError")}
          write.csv(data,paste(savePath,"/",str_split(instances[i],"sat/")[[1]][2],".csv",sep=""), row.names = FALSE)
        }
        else{
          print(paste("File ",paste(savePath,"/",str_split(instances[i],"sat/")[[1]][2],".csv",sep=""), " exist!",sep = ""))
        }
      }
      parallelStop()
      invisible(self)
    },
    
    #get the models' prediction for test and train sets
    get_models_prediction_train_test = function(modelPath,CVsetsPath,train_by_par10=FALSE){
      self$sequentialData$ignore_instances()
      instances = self$sequentialData$llamaData$data$instance_id
      solvers = self$sequentialData$solvers
      #instance ids are ordered as 
      parallelStartSocket(cpus = self$cpus)
      for(i in 1:length(instances)){
        if(!file.exists(paste(CVsetsPath,"/",
                              str_split(instances[i],"sat/")[[1]][2],".csv",sep=""))){
          data = data.frame(matrix(nrow = 0,ncol=5))
          for(solver in solvers){
            rds = readRDS(paste(modelPath,"/",solver,".rds",sep = ""))
            id_instance = i
            predictions_solver = rds$pred$data[which(rds$pred$data$id == i),]
            for(row in 1:nrow(predictions_solver)){
              row = c(instances[i],solver,as.numeric(predictions_solver[row,]$truth), 
                      as.numeric(predictions_solver[row,]$response),
                      as.numeric(predictions_solver[row,]$se),
                      as.numeric(predictions_solver[row,]$iter),
                      predictions_solver[row,]$set)
              data = rbind(data,row) 
            }
          }
          #check if data is par10
          if(train_by_par10) {colnames(data)<-c("InstanceName","Solver",
                                                "ActualPar10","PredictedPar10",
                                                "Prediction_StandardError",
                                                "Iteration","Validation_set")}
          else {colnames(data)<-c("InstanceName","Solver","ActualRuntime",
                                  "PredictedRuntime","Prediction_StandardError",
                                  "Iteration","Validation_set")}
          final = data.frame(matrix(nrow = 0,ncol=8))
          for(iter in 1:10){
            set = data[which(data$Iteration==iter),]
            set$PredictedRuntime = as.numeric(set$PredictedRuntime)
            set = set[order(set$PredictedRuntime),]
            solver_prediction_rank = c(1:39)
            set = cbind(set,solver_prediction_rank)
            final = rbind(final,set)
          }
          final = final[order(final$Solver),]
          write.csv(final,paste(CVsetsPath,"/",
                                str_split(instances[i],"sat/")[[1]][2],".csv",sep=""), 
                    row.names = FALSE)
        }
        else{
          print(paste("File ",paste(CVsetsPath,"/",
                                    str_split(instances[i],"sat/")[[1]][2],".csv",sep=""), 
                      " exist!",sep = ""))
        }
      }
      parallelStop()
      invisible(self)
    },
    
    #get the models' prediction for all sets
    get_models_prediction_train_test_validation = function(modelPath,CVsetsPath,train_by_par10=FALSE, CV = FALSE){
      self$sequentialData$ignore_instances()
      instances = self$sequentialData$llamaData$data$instance_id
      solvers = self$sequentialData$solvers
      if(CV == TRUE){
        valid_instances = readRDS(paste(modelPath,"/",solvers[1],"_validation_preds.rds",sep = ""))[[1]]$data$InstanceName
      } else{
        valid_instances = readRDS(paste(modelPath,"/",solvers[1],"_validation_preds.rds",sep = ""))$data$InstanceName
      }
      test_train_instances = subset(instances, !(instances %in% valid_instances))
      
      #instance ids are ordered as 
      parallelStartSocket(cpus = self$cpus)
      for(i in 1:length(valid_instances)){
        if(!file.exists(paste(CVsetsPath,"/validation/",
                              str_split(valid_instances[i],"sat/")[[1]][2],".csv",sep=""))){
          data = data.frame(matrix(nrow = 0,ncol=5))
          for(solver in solvers){
            rds = readRDS(paste(modelPath,"/",solver,"_validation_preds.rds",sep = ""))
            if(CV == TRUE){
              for(iter in 1:length(rds)){
                predictions_solver = rds[[iter]]$data[which(rds[[iter]]$data$InstanceName == valid_instances[i]),]
                row = c(predictions_solver$InstanceName,solver,as.numeric(predictions_solver$truth), 
                        as.numeric(predictions_solver$response),
                        as.numeric(predictions_solver$se),
                        as.numeric(predictions_solver$iter),
                        predictions_solver$set)
                data = rbind(data,row)
              }
            }
            else{
              predictions_solver = rds$data[which(rds$data$InstanceName == valid_instances[i]),]
              row = c(predictions_solver$InstanceName,solver,as.numeric(predictions_solver$truth), 
                      as.numeric(predictions_solver$response),
                      as.numeric(predictions_solver$se),
                      1,
                      predictions_solver$set)
              data = rbind(data,row)
            }
          }
          #check if data is par10
          if(train_by_par10) {colnames(data)<-c("InstanceName","Solver",
                                                "ActualPar10","PredictedPar10",
                                                "Prediction_StandardError",
                                                "Iteration","Validation_set")}
          else {colnames(data)<-c("InstanceName","Solver","ActualRuntime",
                                  "PredictedRuntime","Prediction_StandardError",
                                  "Iteration","Validation_set")}
          final = data.frame(matrix(nrow = 0,ncol=8))
          if(CV == TRUE){
            for(iter in 1:10){
              set = data[which(data$Iteration==iter),]
              set$PredictedRuntime = as.numeric(set$PredictedRuntime)
              set = set[order(set$PredictedRuntime),]
              solver_prediction_rank = c(1:39)
              set = cbind(set,solver_prediction_rank)
              final = rbind(final,set)
            }
          } else{
            set = data[which(data$Iteration==1),]
            set$PredictedRuntime = as.numeric(set$PredictedRuntime)
            set = set[order(set$PredictedRuntime),]
            solver_prediction_rank = c(1:39)
            set = cbind(set,solver_prediction_rank)
            final = rbind(final,set)
          }
          final = final[order(final$Solver),]
          write.csv(final,paste(CVsetsPath,"/validation/",
                                str_split(valid_instances[i],"sat/")[[1]][2],".csv",sep=""), 
                    row.names = FALSE)
        }
        else{
          print(paste("File ",paste(CVsetsPath,"/",
                                    str_split(valid_instances[i],"sat/")[[1]][2],".csv",sep=""), 
                      " exist!",sep = ""))
        }
      }
      parallelStop()
      
      #instance ids are ordered as 
      parallelStartSocket(cpus = self$cpus)
      for(i in 1:length(test_train_instances)){
        if(!file.exists(paste(CVsetsPath,"/",
                              str_split(test_train_instances[i],"sat/")[[1]][2],".csv",sep=""))){
          data = data.frame(matrix(nrow = 0,ncol=5))
          for(solver in solvers){
            rds = readRDS(paste(modelPath,"/",solver,".rds",sep = ""))
            if(CV==TRUE){
              predictions_solver = rds$pred$data[which(rds$pred$data$InstanceName == test_train_instances[i]),]
            } else{
              predictions_solver = rds$data[which(rds$data$InstanceName == test_train_instances[i]),]
            }
            for(row in 1:nrow(predictions_solver)){
              row = c(test_train_instances[i],solver,as.numeric(predictions_solver[row,]$truth), 
                      as.numeric(predictions_solver[row,]$response),
                      as.numeric(predictions_solver[row,]$se),
                      as.numeric(predictions_solver[row,]$iter),
                      predictions_solver[row,]$set)
              data = rbind(data,row) 
            }
          }
          #check if data is par10
          if(train_by_par10) {colnames(data)<-c("InstanceName","Solver",
                                                "ActualPar10","PredictedPar10",
                                                "Prediction_StandardError",
                                                "Iteration","Validation_set")}
          else {colnames(data)<-c("InstanceName","Solver","ActualRuntime",
                                  "PredictedRuntime","Prediction_StandardError",
                                  "Iteration","Validation_set")}
          final = data.frame(matrix(nrow = 0,ncol=8))
          if(CV==TRUE){
            for(iter in 1:10){
              set = data[which(data$Iteration==iter),]
              set$PredictedRuntime = as.numeric(set$PredictedRuntime)
              set = set[order(set$PredictedRuntime),]
              solver_prediction_rank = c(1:39)
              set = cbind(set,solver_prediction_rank)
              final = rbind(final,set)
            }
          } else{
            set = data[which(data$Iteration==1),]
            set$PredictedRuntime = as.numeric(set$PredictedRuntime)
            set = set[order(set$PredictedRuntime),]
            solver_prediction_rank = c(1:39)
            set = cbind(set,solver_prediction_rank)
            final = rbind(final,set)
          }
          final = final[order(final$Solver),]
          write.csv(final,paste(CVsetsPath,"/",
                                str_split(test_train_instances[i],"sat/")[[1]][2],".csv",sep=""), 
                    row.names = FALSE)
        }
        else{
          print(paste("File ",paste(CVsetsPath,"/",
                                    str_split(predictions_solver[i],"sat/")[[1]][2],".csv",sep=""), 
                      " exist!",sep = ""))
        }
      }
      parallelStop()
      invisible(self)
    },
    
    #probability of having vbs selected in the folds 
    get_VBS_probability_folds = function(CVsetsPath,saveTo){
      self$sequentialData$ignore_instances()
      instances = self$sequentialData$solvedInstances
      solvers = self$sequentialData$solvers
      vbs = self$sequentialData$get_VBS()
      #instance ids are ordered as 
      parallelStartSocket(cpus = self$cpus)
      count_vbs = data.frame(matrix(nrow=0,ncol=40))
      for(i in 1:length(instances)){
        if(file.exists(paste(CVsetsPath,"/",
                             str_split(instances[i],"sat/")[[1]][2],".csv",sep=""))){
          data = read.csv(paste(CVsetsPath,"/",
                                str_split(instances[i],"sat/")[[1]][2],".csv",sep=""))
          instance_preds = data[which(data$InstanceName == instances[i]),]
          vbs_ins = vbs[which(vbs$InstanceName==instances[i]),]
          counts = rep(0,40)
          counts[1] = instances[i]
          for(iter in 1:10){
            set = data[which(data$Iteration==iter),]
            set = set[order(set$PredictedRuntime),]
            for(j in 1:39){
              if(set[j,]$Solver == vbs_ins$VBS_Solvers){
                counts[j+1] = as.numeric(counts[j+1])+1
              }
            }
          }
          count_vbs = rbind(count_vbs,counts)
        }
      }
      colnames(count_vbs) <- c("InstanceName",c(1:39))
      count_vbs_cumulative = data.frame(matrix(nrow=nrow(count_vbs),ncol=40))
      count_vbs_cumulative[1] = count_vbs$InstanceName
      count_vbs_cumulative[2] = count_vbs[,2]
      for(col in 3:ncol(count_vbs)){
        count_vbs_cumulative[col] = as.numeric(count_vbs[,col])+
          as.numeric(count_vbs_cumulative[,col-1])
      }
      count_vbs_cumulative[2:40] = sapply(count_vbs_cumulative[2:40] ,as.numeric)
      count_vbs_cumulative[2:40] = count_vbs_cumulative[2:40] /10
      colnames(count_vbs_cumulative) <- c("InstanceName",c(1:39))
      write.csv(count_vbs_cumulative,paste(saveTo,"/VBS_occurance_cumulative.csv",sep = ""),row.names = FALSE)
      parallelStop()
      return(count_vbs_cumulative)
    },
    
    #probability of having vbs selected in all instances prediction
    get_VBS_probability_all_instances = function(predictionPath = self$predictionPath,saveTo=""){
      self$sequentialData$ignore_instances()
      instances = self$sequentialData$solvedInstances
      solvers = self$sequentialData$solvers
      vbs = self$sequentialData$get_VBS()
      count_vbs = data.frame(matrix(nrow=0,ncol=length(solvers)+1))
      parallelStartSocket(cpus = self$cpus)
      for(instance in vbs$InstanceName){
        preds = read.csv(paste(predictionPath,"/",
                               str_split(instance,"sat/")[[1]][2],".csv",sep=""))
        preds = preds[order(preds$PredictedRuntime),]
        solver_order = preds$Solver
        vbs_solver = vbs[which(vbs$InstanceName ==instance),"VBS_Solvers"]
        counts = rep(0,length(solvers)+1)
        counts[1] = instance
        for(j in 1:length(solvers)){
          if(solver_order[j] == vbs_solver){
            counts[j+1] = as.numeric(counts[j+1])+1
          }
        }
        count_vbs = rbind(count_vbs,counts)
      }
      colnames(count_vbs) <- c("InstanceName",c(1:length(solvers)))
      count_vbs_cumulative = data.frame(matrix(nrow=nrow(count_vbs),ncol=length(solvers)+1))
      count_vbs_cumulative[1] = count_vbs$InstanceName
      count_vbs_cumulative[2] = count_vbs[,2]
      for(col in 3:ncol(count_vbs)){
        count_vbs_cumulative[col] = as.numeric(count_vbs[,col])+
          as.numeric(count_vbs_cumulative[,col-1])
      }
      count_vbs_cumulative[2:length(solvers)+1] = sapply(count_vbs_cumulative[2:length(solvers)+1] ,as.numeric)
      colnames(count_vbs_cumulative) <- c("InstanceName",c(1:length(solvers)))
      if(saveTo!=""){
        write.csv(count_vbs_cumulative,paste(saveTo,"/VBS_occurance_test.csv",sep=""),
                  row.names = FALSE)
      }
      parallelStop()
      return(count_vbs_cumulative)
    },
    
    #the expected values for prediction, SE, lower and upperbound (mean values across all folds)
    #use only when you have CV
    get_expected_values_validation = function(preds_path_valid){
      csvs_validation = list.files(preds_path_valid,".csv",full.names = TRUE)
      for(csv in csvs_validation)
      {
        data = read.csv(csv)
        solvers = unique(data$Solver)
        expected_value = data.frame(matrix(ncol=9,nrow = 0))
        probs = c(rep(1,max(unique(data$Iteration))))
        for(solver in solvers){
          data_solver = data[which(data$Solver == solver),]
          expected_pred = sum(data_solver$PredictedRuntime*probs)
          expected_se = sum(data_solver$Prediction_StandardError*probs)
          expected_lowerbound = sum((data_solver$PredictedRuntime - data_solver$Prediction_StandardError)*probs)
          expected_upperbound = sum((data_solver$PredictedRuntime + data_solver$Prediction_StandardError)*probs)
          expected_prediction_rank = sum(data_solver$solver_prediction_rank*probs)
          row = c(unique(data_solver$InstanceName),
                  solver,
                  unique(data_solver$ActualRuntime),
                  expected_pred,
                  expected_se,
                  expected_lowerbound,
                  expected_upperbound,
                  unique(data_solver$Validation_set),
                  expected_prediction_rank)
          expected_value = rbind(expected_value,row)
        }
        colnames(expected_value) = c("InstanceName","Solver","ActualRuntime","ExpectedPrediction","ExpectedSE","ExpectedLowebound","ExpectedUpperbound","Validation_set","ExpectedPredictionRank")
        write.csv(expected_value,paste(preds_path_valid,"/expectedValues/",tail(str_split(csv,"/")[[1]],1),sep =""),row.names = FALSE)
      }
    },
    
    #the expected values for prediction, SE, lower and upperbound for each fold seperatedly 
    #(10 csv file for each instance will be created)
    #use only when you have CV
    get_expected_values_validation_per_fold = function(preds_path_valid){
      csvs_validation = list.files(preds_path_valid,".csv",full.names = TRUE)
      for(csv in csvs_validation)
      {
        data = read.csv(csv)
        for(i in unique(data$Iteration)){
          dt = data[which(data$Iteration == i),]
          solvers = unique(dt$Solver)
          expected_value = data.frame(matrix(ncol=9,nrow = 0))
          probs = c(rep(1,max(unique(dt$Iteration))))
          for(solver in solvers){
            data_solver = dt[which(dt$Solver == solver),]
            expected_pred = sum(data_solver$PredictedRuntime*probs)
            expected_se = sum(data_solver$Prediction_StandardError*probs)
            expected_lowerbound = sum((data_solver$PredictedRuntime - data_solver$Prediction_StandardError)*probs)
            expected_upperbound = sum((data_solver$PredictedRuntime + data_solver$Prediction_StandardError)*probs)
            expected_prediction_rank = sum(data_solver$solver_prediction_rank*probs)
            row = c(unique(data_solver$InstanceName),
                    solver,
                    unique(data_solver$ActualRuntime),
                    expected_pred,
                    expected_se,
                    expected_lowerbound,
                    expected_upperbound,
                    unique(data_solver$Validation_set),
                    expected_prediction_rank)
            expected_value = rbind(expected_value,row)
          }
          colnames(expected_value) = c("InstanceName","Solver","ActualRuntime","ExpectedPrediction","ExpectedSE","ExpectedLowebound","ExpectedUpperbound","Validation_set","ExpectedPredictionRank")
          write.csv(expected_value,paste(preds_path_valid,"/expectedValues/",i,"_",tail(str_split(csv,"/")[[1]],1),sep =""),row.names = FALSE)
        }
      }
    },
    
    #merge all preds into a dataframe
    get_all_preds = function(ignoreInstances = TRUE){
      instances = list.files(self$predictionPath,".csv",full.names = TRUE)
      all = do.call(rbind,lapply(instances, read.csv))
      all = all[order(all$Solver),]
      all = all[c(1,2,4)] %>% spread(Solver,PredictedRuntime)
      all = all[order(all$InstanceName),]
      if(ignoreInstances){
        sequential = SequentialPerformance$new()
        sequential$ignore_instances()
        unsolved = sequential$unsolvedInstances
        all = all[which(!all$InstanceName %in%unsolved),]
      }
      return(all)
    },
    
    #plot instances predictions 
    plot_instances_predictions = function(predictionPath = self$predictionPath, savePath = ""){
      instanceCSVs = list.files(predictionPath,pattern = ".csv",full.names = TRUE)
      if(length(instanceCSVs)==0) return("No file was found!")
      parallelStartSocket(cpus = self$cpus)
      for(instanceCSV in instanceCSVs){
        data = read.csv(instanceCSV)
        data$ActualRuntime <- as.numeric(data$ActualRuntime)
        data$PredictedRuntime <- as.numeric(data$PredictedRuntime)
        data$Prediction_StandardError <- as.numeric(data$Prediction_StandardError)
        p<-ggplot(data, aes(x=Solver, y=PredictedRuntime,colour="PredictedRuntime")) +
          geom_point()+
          geom_point(aes(y=ActualRuntime,colour="ActualRuntime"))+
          geom_errorbar(aes(ymin=PredictedRuntime-Prediction_StandardError, 
                            ymax=PredictedRuntime+Prediction_StandardError), width=.2,
                        position=position_dodge(0.05))+
          ggtitle(unique(data$InstanceName))+
          scale_y_continuous(
            name = "Runtime"
            #sec.axis = sec_axis( trans=~./self$Cutoff , name="probability of solving instance RegRF prediction")
          )+
          theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))
        if(savePath!=""){
          ggsave(paste(savePath,"/",str_split(str_split(unique(data$InstanceName),".cnf")[[1]][1],
                                              "sat/")[[1]][2],".PNG",sep = "")
                 ,width = 10,height = 7,dpi = 200)
        }
      }
      
      parallelStop()
      invisible(self)
      return(p)
    },
    
    #single algorithm selection - the mean predicted solver across all folds
    Single_Algorithm_Selection = function(predictionPath= self$predictionPath,savePath="",ignoreTimeoutsOnVBS=FALSE){
      instanceCSVs = list.files(predictionPath,pattern = ".csv",full.names = TRUE)
      if(length(instanceCSVs)==0) return("No file was found!")
      result = data.frame(matrix(nrow = 0,ncol = 8))
      parallelStartSocket(cpus = self$cpus)
      for(instanceCSV in instanceCSVs){
        data = read.csv(instanceCSV)
        #get min prediction row 
        if("ExpectedPrediction" %in% colnames(data)){
          minpred = data[order(data$ExpectedPrediction),][1,]
        }
        else{
          minpred = data[order(data$PredictedRuntime),][1,]
        }
        #get vbs value for the instance
        VBSRuntime = data[order(data$ActualRuntime),][1,"ActualRuntime"]
        #par10 value based on actual value of min predicted solver
        Par10 = if(minpred$ActualRuntime>=self$sequentialData$Cutoff) 
          (self$sequentialData$Cutoff * 10) else minpred$ActualRuntime
        #compute mcp based on actual value of min predicted solver
        MCP = if(minpred$ActualRuntime-VBSRuntime <0) 0 else (minpred$ActualRuntime-VBSRuntime)
        row = cbind(minpred,VBSRuntime,Par10,MCP)
        result = rbind(result,row)
      }
      parallelStop()
      if(ignoreTimeoutsOnVBS){
        result = result[which(result$VBSRuntime<self$sequentialData$Cutoff ),]
      }
      if(savePath!=""){
        write.csv(paste(savePath,"/SingleAlgorithmSelection.csv",sep = ""))
      }
      return(result)
    },
    
    #top_selection should be 0 if no preference
    #should be changed based on selection method
    #method = -1 >> no selection just order based on predicted runtime
    #method = 0 >> select top solvers based on mean predicted solver accross all folds
    #method = 1 >> select top solvers based on mean predicted solver accross all folds
    #method = 0 >> select top solvers based on mean predicted solver accross all folds
    #method = 0 >> select top solvers based on mean predicted solver accross all folds
    #method = 0 >> select top solvers based on mean predicted solver accross all folds
    
    #add options for par10 prediction
    selection_based_on_SE = function(predictionPath = self$predictionPath, saveTo = self$selectionPath, method_number = 1, 
                                     top_selection = 0,ignoreTimeoutsOnVBS=FALSE, orderBy = "pred", delta = 0, 
                                     delta_prime = 0, alpha = 0, JP_limit = 0.1){
      print(predictionPath)
      ds.files = list.files(predictionPath,pattern = ".csv")
      solvers = self$sequentialData$solvers
      solvers = solvers[order(solvers)]
      instances = unlist(lapply(ds.files,function(x){
        str_split(x,".csv")[[1]][1]
      }))
      instances = as.vector(unlist(instances))
      if(ignoreTimeoutsOnVBS) {
        if(is.null(self$sequentialData$solvedInstances)) self$sequentialData$get_VBS()
        instances = instances[which(paste("sat/",instances,sep="") %in% self$sequentialData$solvedInstances)]
      }
      #ids are  ordered
      
      
      coresSelection = data.frame(matrix(ncol = 2, nrow = 0))
      parallelStartSocket(cpus = self$cpus)
      for(instance in instances){
        instanceName = instance
        csv = read.csv(paste(predictionPath,"/",instanceName[],".csv",sep=""))
        if(nrow(csv)<1){
          print("predictions are empty!")
        }
        minrow = csv[which(csv$PredictedRuntime == min(csv$PredictedRuntime)),]
        min = minrow$PredictedRuntime
        #don't do selection
        if(method_number==-1){
          if(orderBy == "pred-se"){
            print("We cannot consider uncertainty in this method! So, ordering is by prediction value!")
            return()
          }
          if(top_selection != 0){
            print("This method is to run all solvers in parallel, keep the default value for top_selection!")
            return()
          }
          otherRows = csv
          otherRows = otherRows[order(otherRows$PredictedRuntime),]
          data = otherRows
        }
        
        #top selections
        else if(method_number==0){
          if(orderBy == "pred-se"){
            print("We cannot consider uncertainty in this method! So, ordering is by prediction value!")
            return()
          }
          otherRows = csv
          otherRows = otherRows[order(otherRows$PredictedRuntime),]
          if(top_selection != 0 && nrow(otherRows)>top_selection){
            otherRows = otherRows[1:top_selection,]
          }
          data = otherRows
        }
        
        #minpred <= pred <= [minpred + delta_prime*SE]
        else if(method_number==1){
          upperbound = min + (delta_prime*minrow$Prediction_StandardError)
          lowerbound = min
          otherRows = csv[which(csv$PredictedRuntime<= upperbound),]
          otherRows = otherRows[which(otherRows$PredictedRuntime>=lowerbound),]
          #top 5 
          if(orderBy == 'pred'){
            otherRows = otherRows[order(otherRows$PredictedRuntime),]
            if(top_selection != 0 && nrow(otherRows)>top_selection){
              otherRows = otherRows[1:top_selection,]
            }
          } else if(orderBy == 'pred-se'){ 
            otherRows = otherRows[order(otherRows$PredictedRuntime- (alpha*otherRows$Prediction_StandardError)),]
            if(top_selection != 0 && nrow(otherRows)>top_selection){
              otherRows = otherRows[1:top_selection,]
              otherRows = na.omit(otherRows)
              if(!minrow$Solver %in% otherRows$Solver){
                otherRows = rbind(minrow, otherRows)
                if(nrow(otherRows)>top_selection){
                  otherRows = otherRows[1:(nrow(otherRows)-1),]  
                }
              }
            }
          }
          data = otherRows
        }
        
        #lowebound as good as min pred, [pred-delta*SE]<=minpred
        else if(method_number==2){
          upperbound = min
          otherRows = csv[which((csv$PredictedRuntime - (delta*csv$Prediction_StandardError))<= upperbound),]
          if(orderBy == 'pred'){
            otherRows = otherRows[order(otherRows$PredictedRuntime),]
            #top 5 
            if(top_selection!=0){
              if(nrow(otherRows)>top_selection){
                otherRows = otherRows[1:top_selection,]
              }
            }
          } else if(orderBy == 'pred-se'){
            otherRows = otherRows[order(otherRows$PredictedRuntime - (alpha*otherRows$Prediction_StandardError)),]
            if(top_selection!=0){
              if(nrow(otherRows)>top_selection){
                otherRows = otherRows[1:top_selection,]
                otherRows = na.omit(otherRows)
                if(!minrow$Solver %in% otherRows$Solver){
                  otherRows = rbind(minrow, otherRows)
                  if(nrow(otherRows)>top_selection){
                    otherRows = otherRows[1:(nrow(otherRows)-1),]  
                  }
                }
              }
            }  
          }
          data = otherRows
        }
        #generalized 2 and 1
        #p-delta*se <= minP + deltaPrime*SE_min
        else if(method_number==3){
          #p-delta*se <= minP + deltaPrime*SE_min
          upperbound = min + (delta_prime*minrow$Prediction_StandardError)
          otherRows = csv[which((csv$PredictedRuntime - (delta*csv$Prediction_StandardError))<= upperbound),]
          #top 5 
          if(orderBy == 'pred'){
            otherRows = otherRows[order(otherRows$PredictedRuntime),]
            if(top_selection != 0 && nrow(otherRows)>top_selection){
              otherRows = otherRows[1:top_selection,]
            }
          } else if(orderBy == 'pred-se'){ 
            otherRows = otherRows[order(otherRows$PredictedRuntime- (alpha*otherRows$Prediction_StandardError)),]
            if(top_selection != 0 && nrow(otherRows)>top_selection){
              otherRows = otherRows[1:top_selection,]
              otherRows = na.omit(otherRows)
              if(!minrow$Solver %in% otherRows$Solver){
                otherRows = rbind(minrow, otherRows)
                if(nrow(otherRows)>top_selection){
                  otherRows = otherRows[1:(nrow(otherRows)-1),]  
                }
              }
            }
          }
          data = otherRows
        }
        
        #lower as good as min, but nor lower than [minpred-delta_prime*SE], 
        #[minpred-delta_prime*SE]<=[pred-delta*SE]<=minpred
        else if(method_number==4){
          upperbound = min
          lowerbound = min - delta_prime*minrow$Prediction_StandardError
          otherRows = csv[which((csv$PredictedRuntime-delta*csv$Prediction_StandardError)<= upperbound),]
          otherRows = otherRows[which((otherRows$PredictedRuntime-delta*otherRows$Prediction_StandardError)>=lowerbound),]
          if(orderBy == 'pred'){
            otherRows = otherRows[order(otherRows$PredictedRuntime),]
            if(top_selection!=0){
              if(nrow(otherRows)>top_selection){
                otherRows = otherRows[1:top_selection,]
                otherRows = na.omit(otherRows)
                if(!minrow$Solver %in% otherRows$Solver){
                  otherRows = rbind(minrow, otherRows)
                  if(nrow(otherRows)>top_selection){
                    otherRows = otherRows[1:(nrow(otherRows)-1),]  
                  }
                }
              }
            }
          } else if(orderBy == 'pred-se'){
            otherRows = otherRows[order((otherRows$PredictedRuntime-alpha*otherRows$Prediction_StandardError)),]
            if(top_selection!=0){
              if(nrow(otherRows)>top_selection){
                otherRows = otherRows[1:top_selection,]
                otherRows = na.omit(otherRows)
                if(!minrow$Solver %in% otherRows$Solver){
                  otherRows = rbind(minrow, otherRows)
                  if(nrow(otherRows)>top_selection){
                    otherRows = otherRows[1:(nrow(otherRows)-1),]  
                  }
                  
                }
              }
            }
          }
          data = otherRows
        }
        #selection based on Joint probability
        #p_min = 1-pnorm(mean_A-3*sd_A,mean = mean_min,sd = sd_min)
        #p_A = pnorm(mean_min+3*sd_min,mean = mean_A,sd = sd_A)
        #jointprobability = p_min*p_A
        else if(method_number==5){
          mean_min = minrow$PredictedRuntime
          sd_min = minrow$Prediction_StandardError
          otherRows = minrow
          for(row in 1:nrow(csv)){
            mean_A = csv[row,]$PredictedRuntime
            sd_A = csv[row,]$Prediction_StandardError
            c = ((mean_A*(sd_min^2))-(sd_A*((mean_min*sd_A)+sd_min* sqrt((mean_min-mean_A)^2+(2*(sd_min^2-sd_A^2)*log(sd_min/sd_A))))))/(sd_min^2 - sd_A^2)
            ovelapping_area = 1-pnorm(c,mean = mean_min,sd = sd_min)+pnorm(c,mean = mean_A,sd = sd_A)
            # p_min = 1-pnorm(mean_A-3*sd_A,mean = mean_min,sd = sd_min)
            # p_A = pnorm(mean_min+3*sd_min,mean = mean_A,sd = sd_A)
            # jointprobability = p_min*p_A
            if(ovelapping_area >= JP_limit || is.na(ovelapping_area)){
              if(csv[row,]$Solver != minrow$Solver){
                otherRows = rbind(otherRows, csv[row,]) 
              }
            }
          }
          if(orderBy == 'pred'){
            otherRows = otherRows[order(otherRows$PredictedRuntime),]
            if(top_selection!=0){
              if(nrow(otherRows)>top_selection){
                otherRows = otherRows[1:top_selection,]
                otherRows = na.omit(otherRows)
                if(!minrow$Solver %in% otherRows$Solver){
                  otherRows = rbind(minrow, otherRows)
                  if(nrow(otherRows)>top_selection){
                    otherRows = otherRows[1:(nrow(otherRows)-1),]  
                  }
                }
              }
            }
          } else if(orderBy == 'pred-se'){
            otherRows = otherRows[order((otherRows$PredictedRuntime-alpha*otherRows$Prediction_StandardError)),]
            if(top_selection!=0){
              if(nrow(otherRows)>top_selection){
                otherRows = otherRows[1:top_selection,]
                otherRows = na.omit(otherRows)
                if(!minrow$Solver %in% otherRows$Solver){
                  otherRows = rbind(minrow, otherRows)
                  if(nrow(otherRows)>top_selection){
                    otherRows = otherRows[1:(nrow(otherRows)-1),]  
                  }
                  
                }
              }
            }
          }
          data = otherRows
        }
        #--------------
        # 
        # #the following ones are statistical selection - they may be wrong
        # else if(method_number==7){
        #   tvalues = vector()
        #   for(i in 1:nrow(csv)){
        #     s1 = csv$Prediction_StandardError[i]
        #     s2 = minrow$Prediction_StandardError
        #     n = 500
        #     m1 = csv$PredictedRuntime[i]
        #     m2 = minrow$PredictedRuntime
        #     tvalues = append(tvalues,abs(m1-m2)/sqrt(((s1^2)/n)+((s2^2)/n)))
        #     #df = ((s1^2/n+s2^2/n)^2)/(((((s1^2)/n)^2)/(n-1))+((((s2^2)/n)^2)/(n-1)))
        #   }
        #   
        #   values = tvalues>1.96
        #   
        #   solvers = which(values==1)
        #   data = csv[solvers,]
        #   if(!(minrow$Solver %in% data$Solver)){
        #     data = rbind(data,minrow)
        #   }
        #   data = data[order(data$PredictedRuntime),]
        #   if(top_selection!=0){
        #     if(nrow(data)>top_selection){
        #       data = data[1:top_selection,]
        #     }
        #   }
        # }
        # else if(method_number==8){
        #   #pred in SE
        #   upperbound = min + minrow$Prediction_StandardError
        #   lowerbound = min - minrow$Prediction_StandardError
        #   otherRows = csv[which(csv$PredictedRuntime<= upperbound),]
        #   otherRows = otherRows[which(otherRows$PredictedRuntime>=lowerbound),]
        #   #top 5 
        #   otherRows = otherRows[order(otherRows$PredictedRuntime),]
        #   tvalues = vector()
        #   for(i in 1:nrow(otherRows)){
        #     s1 = otherRows$Prediction_StandardError[i]
        #     s2 = minrow$Prediction_StandardError
        #     n = 500
        #     m1 = otherRows$PredictedRuntime[i]
        #     m2 = minrow$PredictedRuntime
        #     tvalues = append(tvalues,abs(m1-m2)/sqrt(((s1^2)/n)+((s2^2)/n)))
        #     #df = ((s1^2/n+s2^2/n)^2)/(((((s1^2)/n)^2)/(n-1))+((((s2^2)/n)^2)/(n-1)))
        #   }
        #   
        #   values = tvalues>1.96
        #   
        #   solvers = which(values==1)
        #   data = otherRows[solvers,]
        #   if(!(minrow$Solver %in% data$Solver)){
        #     data = rbind(data,minrow)
        #   }
        #   data = data[order(data$PredictedRuntime),]
        #   if(top_selection!=0){
        #     if(nrow(data)>top_selection){
        #       data = data[1:top_selection,]
        #     }
        #   }
        # }
        # else if(method_number==9){
        #   #lowebound as good as min pred
        #   upperbound = min
        #   otherRows = csv[which((csv$PrdictedRuntime-csv$Prediction_StandardError)<= upperbound),]
        #   otherRows = otherRows[order(otherRows$PredictedRuntime - otherRows$Prediction_StandardError),]
        #   otherRows = otherRows[order(otherRows$PredictedRuntime - otherRows$Prediction_StandardError),]
        #   #top 5 
        #   otherRows = otherRows[order(otherRows$PredictedRuntime),]
        #   tvalues = vector()
        #   for(i in 1:nrow(otherRows)){
        #     s1 = otherRows$Prediction_StandardError[i]
        #     s2 = minrow$Prediction_StandardError
        #     n = 500
        #     m1 = otherRows$PredictedRuntime[i]
        #     m2 = minrow$PredictedRuntime
        #     tvalues = append(tvalues,abs(m1-m2)/sqrt(((s1^2)/n)+((s2^2)/n)))
        #     #df = ((s1^2/n+s2^2/n)^2)/(((((s1^2)/n)^2)/(n-1))+((((s2^2)/n)^2)/(n-1)))
        #   }
        #   
        #   values = tvalues>1.96
        #   
        #   solvers = which(values==1)
        #   data = otherRows[solvers,]
        #   if(!(minrow$Solver %in% data$Solver)){
        #     data = rbind(data,minrow)
        #   }
        #   data = data[order(data$PredictedRuntime),]
        #   if(top_selection!=0){
        #     if(nrow(data)>top_selection){
        #       data = data[1:top_selection,]
        #     }
        #   }
        # }
        # else if(method_number==10){
        #   #top 5 
        #   otherRows = csv[order(csv$PredictedRuntime),]
        #   tvalues = vector()
        #   solo = self$sequentialData$actual_CSV
        #   minsolver = minrow$Solver
        #   B = sum(solo[minsolver]>=5000)
        #   
        #   for(solver in solvers){
        #     C = sum(solo[solver]>=5000)
        #     x_2 = ((abs(C-B)-1)^2)/(B+C)
        #     tvalues = append(tvalues,x_2)
        #   }
        #   
        #   values = tvalues>3.841
        #   
        #   solvers = which(values==1)
        #   data = otherRows[solvers,]
        #   if(!(minrow$Solver %in% data$Solver)){
        #     data = rbind(data,minrow)
        #   }
        #   data = data[order(data$PredictedRuntime),]
        #   if(top_selection!=0){
        #     if(nrow(data)>top_selection){
        #       data = data[1:top_selection,]
        #     }
        #   }
        # }
        # else if(method_number==11){
        #   #top 5 
        #   otherRows = csv[order(csv$PredictedRuntime),]
        #   tvalues = vector()
        #   solo = read.csv("../prediction_simple_reg.csv")
        #   minsolver = minrow$Solver
        #   B = sum(solo[minsolver]>=5000)
        #   
        #   for(solver in solvers_all){
        #     C = sum(solo[solver]>=5000)
        #     x_2 = ((abs(C-B)-1)^2)/(B+C)
        #     tvalues = append(tvalues,x_2)
        #   }
        #   
        #   values = tvalues>3.841
        #   
        #   solvers = which(values==1)
        #   data = otherRows[solvers,]
        #   if(!(minrow$Solver %in% data$Solver)){
        #     data = rbind(data,minrow)
        #   }
        #   data = data[order(data$PredictedRuntime),]
        #   if(top_selection!=0){
        #     if(nrow(data)>top_selection){
        #       data = data[1:top_selection,]
        #     }
        #   }
        # }
        # else if(method_number==12){
        #   #pred in SE
        #   upperbound = min + minrow$Prediction_StandardError
        #   lowerbound = min - minrow$Prediction_StandardError
        #   otherRows = csv[which(csv$prediction<= upperbound),]
        #   otherRows = otherRows[which(otherRows$PredictedRuntime>=lowerbound),]
        #   #top 5 
        #   otherRows = otherRows[order(otherRows$PredictedRuntime),]
        #   tvalues = vector()
        #   solo = read.csv("../prediction_simple_reg.csv")
        #   minsolver = minrow$Solver
        #   B = sum(solo[minsolver]>=5000)
        #   
        #   for(solver in otherRows$Solver){
        #     C = sum(solo[solver]>=5000)
        #     x_2 = ((abs(C-B)-1)^2)/(B+C)
        #     tvalues = append(tvalues,x_2)
        #   }
        #   
        #   values = tvalues>3.841
        #   
        #   solvers = which(values==1)
        #   data = otherRows[solvers,]
        #   if(!(minrow$Solver %in% data$Solver)){
        #     data = rbind(data,minrow)
        #   }
        #   data = data[order(data$PredictedRuntime),]
        #   if(top_selection!=0){
        #     if(nrow(data)>top_selection){
        #       data = data[1:top_selection,]
        #     }
        #   }
        # }
        # else if(method_number==13){
        #   #pred in SE
        #   upperbound = min
        #   otherRows = csv[which((csv$PredictedRuntime-csv$Prediction_StandardError)<= upperbound),]
        #   otherRows = otherRows[order(otherRows$PredictedRuntime - otherRows$Prediction_StandardError),]
        #   #top 5 
        #   otherRows = otherRows[order(otherRows$PredictedRuntime),]
        #   tvalues = vector()
        #   solo = read.csv("../prediction_simple_reg.csv")
        #   minsolver = minrow$Solver
        #   B = sum(solo[minsolver]>=5000)
        #   
        #   for(solver in otherRows$Solver){
        #     C = sum(solo[solver]>=5000)
        #     x_2 = ((abs(C-B)-1)^2)/(B+C)
        #     tvalues = append(tvalues,x_2)
        #   }
        #   
        #   values = tvalues>3.841
        #   
        #   solvers = which(values==1)
        #   data = otherRows[solvers,]
        #   if(!(minrow$Solver %in% data$Solver)){
        #     data = rbind(data,minrow)
        #   }
        #   data = data[order(data$PredictedRuntime),]
        #   if(top_selection!=0){
        #     if(nrow(data)>top_selection){
        #       data = data[1:top_selection,]
        #     }
        #   }
        # }
        # else if(method_number==14){
        #   #top 5 
        #   otherRows = csv[order(csv$PredictedRuntime),]
        #   tvalues = vector()
        #   solo = read.csv("../lowerbound_prediction_simple_reg.csv")
        #   minsolver = minrow$Solver
        #   B = sum(solo[minsolver]>=5000)
        #   
        #   for(solver in solvers_all){
        #     C = sum(solo[solver]>=5000)
        #     x_2 = ((abs(C-B)-1)^2)/(B+C)
        #     tvalues = append(tvalues,x_2)
        #   }
        #   
        #   values = tvalues>3.841
        #   
        #   solvers = which(values==1)
        #   data = otherRows[solvers,]
        #   if(!(minrow$Solver %in% data$Solver)){
        #     data = rbind(data,minrow)
        #   }
        #   data = data[order(data$PredictedRuntime),]
        #   if(top_selection!=0){
        #     if(nrow(data)>top_selection){
        #       data = data[1:top_selection,]
        #     }
        #   }
        # }
        # else if(method_number==15){
        #   #pred in SE
        #   upperbound = min + minrow$Prediction_StandardError
        #   lowerbound = min - minrow$Prediction_StandardError
        #   otherRows = csv[which(csv$prediction<= upperbound),]
        #   otherRows = otherRows[which(otherRows$PredictedRuntime>=lowerbound),]
        #   #top 5 
        #   otherRows = otherRows[order(otherRows$PredictedRuntime),]
        #   tvalues = vector()
        #   solo = read.csv("../lowerbound_prediction_simple_reg.csv")
        #   minsolver = minrow$Solver
        #   B = sum(solo[minsolver]>=5000)
        #   
        #   for(solver in otherRows$Solver){
        #     C = sum(solo[solver]>=5000)
        #     x_2 = ((abs(C-B)-1)^2)/(B+C)
        #     tvalues = append(tvalues,x_2)
        #   }
        #   
        #   values = tvalues>3.841
        #   
        #   solvers = which(values==1)
        #   data = otherRows[solvers,]
        #   if(!(minrow$Solver %in% data$Solver)){
        #     data = rbind(data,minrow)
        #   }
        #   data = data[order(data$PredictedRuntime),]
        #   if(top_selection!=0){
        #     if(nrow(data)>top_selection){
        #       data = data[1:top_selection,]
        #     }
        #   }
        # }
        # else if(method_number==16){
        #   #pred in SE
        #   upperbound = min
        #   otherRows = csv[which((csv$PredictedRuntime-csv$Prediction_StandardError)<= upperbound),]
        #   otherRows = otherRows[order(otherRows$PredictedRuntime - otherRows$Prediction_StandardError),]
        #   #top 5 
        #   otherRows = otherRows[order(otherRows$PredictedRuntime),]
        #   tvalues = vector()
        #   solo = read.csv("../lowerbound_prediction_simple_reg.csv")
        #   minsolver = minrow$Solver
        #   B = sum(solo[minsolver]>=5000)
        #   
        #   for(solver in otherRows$Solver){
        #     C = sum(solo[solver]>=5000)
        #     x_2 = ((abs(C-B)-1)^2)/(B+C)
        #     tvalues = append(tvalues,x_2)
        #   }
        #   
        #   values = tvalues>3.841
        #   
        #   solvers = which(values==1)
        #   data = otherRows[solvers,]
        #   if(!(minrow$Solver %in% data$Solver)){
        #     data = rbind(data,minrow)
        #   }
        #   data = data[order(data$PredictedRuntime),]
        #   if(top_selection!=0){
        #     if(nrow(data)>top_selection){
        #       data = data[1:top_selection,]
        #     }
        #   }
        # }
        
        
        #--------------
        
        
        
        data = data[1:5]
        colnames(data)<-c("InstanceName","Solver","ActualRuntime","PredictedRuntime","Prediction_StandardError")
        number_of_solvers = nrow(data)
        actual_parallel_runtime = data.frame()
        path = self$sequentialData$actual_CSV_path
        path = str_split(path,"/")[[1]]
        path = path[-length(path)]
        path = paste(path, collapse = '/') 
        #this can be improved by a reg model 
        if(number_of_solvers==1){
          filename = paste(path,"/teton-",self$benchmarks_name,"-",length(self$sequentialData$solvers),"-solvers-solo.csv",sep = "")
          actual_parallel_runtime = read.csv(filename)
        } else if (number_of_solvers<10){
          filename = paste(path,"/teton-",self$benchmarks_name,"-",length(self$sequentialData$solvers),"-solvers-",number_of_solvers,"-parallel.csv",sep = "")
          actual_parallel_runtime = read.csv(filename)
        } else if(number_of_solvers>31){
          filename = paste(path,"/teton-",self$benchmarks_name,"-",length(self$sequentialData$solvers),"-solvers-32-parallel.csv",sep = "")
          actual_parallel_runtime = read.csv(filename)    
        } else if(number_of_solvers>=10 ){
          core = round(number_of_solvers,-1)
          filename = paste(path,"/teton-",self$benchmarks_name,"-",length(self$sequentialData$solvers),"-solvers-",core,"-parallel.csv",sep = "")
          actual_parallel_runtime = read.csv(filename)
        } 
        parallel_runtimes <- vector()
        csvrow = actual_parallel_runtime[which(actual_parallel_runtime$InstanceName == data[1,]$InstanceName),]
        for(m in 0:nrow(data)){
          parallel_runtimes <- append(parallel_runtimes,csvrow[data[m,]$Solver])
          parallel_runtimes = unname(unlist(parallel_runtimes))
        }
        vbs_runtime = self$sequentialData$get_VBS()[which(self$sequentialData$get_VBS()$InstanceName == data[1,]$InstanceName),]$VBS_Runtime
        #parallel_runtimes[which(parallel_runtimes==5000)]<-50000
        #vbs_runtime[which(vbs_runtime==5000)]<-50000
        data <- cbind(data,parallel_runtimes)
        data <- cbind(data,c(rep(vbs_runtime,number_of_solvers)))
        #colnames(data) = c("instance","solver","sequential_par10","prediction","standardError","parallel_par10","vbs_par10")
        colnames(data) = c("InstanceName","Solver","SequentialRuntime","PredictedRuntime",
                           "Prediction_StandardError","ParallelRuntime","VBSRuntime")
        data$delta = rep(x = delta, times = nrow(data))
        data$delta_prime = rep(x = delta_prime, times = nrow(data))
        data$alpha = rep(x = alpha, times = nrow(data))
        data$method_number = method_number
        data$orderBy = orderBy
        coresSelection = rbind(coresSelection,c(instance,nrow(data)))
        colnames(coresSelection) <- c("instances","selectedCores")
        
        if(saveTo!="")
          write.csv(data,paste(saveTo,"/",instanceName,".csv",sep=""),row.names = FALSE)
      }
      parallelStop()
      return(coresSelection)
    },
    #ned to have csvs from (selection-based_on_SE)
    time_splitting_scheduling = function(predictionPath = self$predictionPath, saveTo = self$selectionPath, method_number = 1, 
                                         top_selection = 0,ignoreTimeoutsOnVBS=FALSE, orderBy = "pred", delta = 0, 
                                         delta_prime = 0, alpha = 0, JP_limit = 0.1, getCores = TRUE){
      
    },
    selection_based_on_SE_thetaForAlg = function(predictionPath = self$predictionPath, saveTo = self$selectionPath, 
                                                 top_selection = 0,ignoreTimeoutsOnVBS=FALSE, orderBy = "pred", thetas){
      print(predictionPath)
      ds.files = list.files(predictionPath,pattern = ".csv")
      solvers = self$sequentialData$solvers
      solvers = solvers[order(solvers)]
      instances = unlist(lapply(ds.files,function(x){
        str_split(x,".csv")[[1]][1]
      }))
      instances = as.vector(unlist(instances))
      if(ignoreTimeoutsOnVBS) {
        if(is.null(self$sequentialData$solvedInstances)) self$sequentialData$get_VBS()
        instances = instances[which(paste("sat/",instances,sep="") %in% self$sequentialData$solvedInstances)]
      }
      #ids are  ordered
      
      parallelStartSocket(cpus = self$cpus)
      for(instance in instances){
        instanceName = instance
        csv = read.csv(paste(predictionPath,"/",instanceName[],".csv",sep=""))
        if(nrow(csv)<1){
          print("predictions are empty!")
        }
        csv$theta = thetas
        minrow = csv[which(csv$PredictedRuntime == min(csv$PredictedRuntime)),]
        
        min = minrow$PredictedRuntime
        
        #p-delta*se <= minP + deltaPrime*SE_min
        upperbound = min + (minrow$theta*minrow$Prediction_StandardError)
        otherRows = csv[which((csv$PredictedRuntime - (csv$theta*csv$Prediction_StandardError))<= upperbound),]
        #top 5 
        if(orderBy == 'pred'){
          otherRows = otherRows[order(otherRows$PredictedRuntime),]
          if(top_selection != 0 && nrow(otherRows)>top_selection){
            otherRows = otherRows[1:top_selection,]
          }
        } else if(orderBy == 'pred-se'){ 
          otherRows = otherRows[order(otherRows$PredictedRuntime- (otherRows$theta*otherRows$Prediction_StandardError)),]
          if(top_selection != 0 && nrow(otherRows)>top_selection){
            otherRows = otherRows[1:top_selection,]
            otherRows = na.omit(otherRows)
            if(!minrow$Solver %in% otherRows$Solver){
              otherRows = rbind(minrow, otherRows)
              if(nrow(otherRows)>top_selection){
                otherRows = otherRows[1:(nrow(otherRows)-1),]  
              }
            }
          }
        }
        data = otherRows
        data = data[1:5]
        colnames(data)<-c("InstanceName","Solver","ActualRuntime","PredictedRuntime","Prediction_StandardError")
        number_of_solvers = nrow(data)
        actual_parallel_runtime = data.frame()
        path = self$sequentialData$actual_CSV_path
        path = str_split(path,"/")[[1]]
        path = path[-length(path)]
        path = paste(path, collapse = '/') 
        #this can be improved by a reg model 
        if(number_of_solvers==1){
          filename = paste(path,"/teton-",self$benchmarks_name,"-",length(self$sequentialData$solvers),"-solvers-solo-replacement.csv",sep = "")
          actual_parallel_runtime = read.csv(filename)
        } else if (number_of_solvers<10){
          filename = paste(path,"/teton-",self$benchmarks_name,"-",length(self$sequentialData$solvers),"-solvers-",number_of_solvers,
                           "-parallel-replacement.csv",sep = "")
          actual_parallel_runtime = read.csv(filename)
        } else if(number_of_solvers>31){
          filename = paste(path,"/teton-",self$benchmarks_name,"-",length(self$sequentialData$solvers),"-solvers-32-parallel-replacement.csv",sep = "")
          actual_parallel_runtime = read.csv(filename)    
        } else if(number_of_solvers>=10 ){
          core = round(number_of_solvers,-1)
          filename = paste(path,"/teton-",self$benchmarks_name,"-",length(self$sequentialData$solvers),"-solvers-",core,"-parallel-replacement.csv",sep = "")
          actual_parallel_runtime = read.csv(filename)
        } 
        parallel_runtimes <- vector()
        csvrow = actual_parallel_runtime[which(actual_parallel_runtime$InstanceName == data[1,]$InstanceName),]
        for(m in 0:nrow(data)){
          parallel_runtimes <- append(parallel_runtimes,csvrow[data[m,]$Solver])
          parallel_runtimes = unname(unlist(parallel_runtimes))
        }
        vbs_runtime = self$sequentialData$get_VBS()[which(self$sequentialData$get_VBS()$InstanceName == data[1,]$InstanceName),]$VBS_Runtime
        #parallel_runtimes[which(parallel_runtimes==5000)]<-50000
        #vbs_runtime[which(vbs_runtime==5000)]<-50000
        data <- cbind(data,parallel_runtimes)
        data <- cbind(data,c(rep(vbs_runtime,number_of_solvers)))
        #colnames(data) = c("instance","solver","sequential_par10","prediction","standardError","parallel_par10","vbs_par10")
        colnames(data) = c("InstanceName","Solver","SequentialRuntime","PredictedRuntime",
                           "Prediction_StandardError","ParallelRuntime","VBSRuntime")
        for(solver in solvers){
          data[paste(solver,"_theta",sep="")] <- rep(x=csv[which(csv$Solver == solver),]$theta,times = nrow(data))
        }
        data$orderBy = orderBy
        if(saveTo!="")
          write.csv(data,paste(saveTo,"/",instanceName,".csv",sep=""),row.names = FALSE)
      }
      parallelStop()
    },
    #nemidonam ina chian 
    selection_based_on_SE_validation = function(predictionPath, saveTo, method_number = 1, 
                                                top_selection = 0,ignoreTimeoutsOnVBS=TRUE){
      ds.files = list.files(predictionPath,pattern = ".csv")
      solvers = self$sequentialData$solvers
      solvers = solvers[order(solvers)]
      instances = unlist(lapply(ds.files,function(x){
        str_split(x,".csv")[[1]][1]
      }))
      instances = as.vector(unlist(instances))
      if(ignoreTimeoutsOnVBS) {
        if(is.null(self$sequentialData$solvedInstances)) self$sequentialData$get_VBS()
        instances = instances[which(paste("sat/",instances,sep="") %in% self$sequentialData$solvedInstances)] 
      }
      #ids are  ordered
      
      parallelStartSocket(cpus = self$cpus)
      for(instance in instances){
        instanceName = instance
        csv = read.csv(paste(predictionPath,"/",instanceName[],".csv",sep=""))
        for(iter in c(1:max(csv$Iteration))){
          csv_iter = csv[which(csv$Iteration == iter),]
          minrow = csv_iter[which(csv_iter$PredictedRuntime == min(csv_iter$PredictedRuntime)),]
          min = minrow$PredictedRuntime
          #don't do selection
          if(method_number==-1){
            otherRows = csv_iter
            otherRows = otherRows[order(otherRows$PredictedRuntime),]
            data = otherRows
          }
          
          #top selections
          else if(method_number==0){
            otherRows = csv_iter
            otherRows = otherRows[order(otherRows$PredictedRuntime),]
            if(top_selection != 0 && nrow(otherRows)>top_selection){
              otherRows = otherRows[1:top_selection,]
              otherRows = na.omit(otherRows)
              if(!minrow$Solver %in% otherRows$Solver){
                otherRows = rbind(minrow, otherRows)
                if(nrow(otherRows)>top_selection){
                  otherRows = otherRows[1:(nrow(otherRows)-1),]  
                }
                
              }
            }
            data = otherRows
          }
          
          #pred >= [minpred + SE], then order by pred value
          else if(method_number==1){
            upperbound = min + minrow$Prediction_StandardError
            lowerbound = min
            otherRows = csv_iter[which(csv_iter$PredictedRuntime<= upperbound),]
            otherRows = otherRows[which(otherRows$PredictedRuntime>=lowerbound),]
            #top 5 
            otherRows = otherRows[order(otherRows$PredictedRuntime),]
            if(top_selection != 0 && nrow(otherRows)>top_selection){
              otherRows = otherRows[1:top_selection,]
              otherRows = na.omit(otherRows)
              if(!minrow$Solver %in% otherRows$Solver){
                otherRows = rbind(minrow, otherRows)
                if(nrow(otherRows)>top_selection){
                  otherRows = otherRows[1:(nrow(otherRows)-1),]  
                }
                
              }
            }
            data = otherRows
          }
          
          #pred >= [minpred + SE], then order by (pred-SE)
          else if(method_number==2){
            upperbound = min + minrow$Prediction_StandardError
            lowerbound = min
            otherRows = csv_iter[which(csv_iter$PredictedRuntime<= upperbound),]
            otherRows = otherRows[which(otherRows$PredictedRuntime>=lowerbound),]
            #top 5 
            otherRows = otherRows[order(otherRows$PredictedRuntime- otherRows$Prediction_StandardError),]
            if(top_selection != 0 && nrow(otherRows)>top_selection){
              otherRows = otherRows[1:top_selection,]
              otherRows = na.omit(otherRows)
              if(!minrow$Solver %in% otherRows$Solver){
                otherRows = rbind(minrow, otherRows)
                if(nrow(otherRows)>top_selection){
                  otherRows = otherRows[1:(nrow(otherRows)-1),]  
                }
                
              }
            }
            data = otherRows
          }
          
          #lowebound as good as min pred, [pred-SE]<=minpred, then order by pred value
          else if(method_number==3){
            upperbound = min
            otherRows = csv_iter[which((csv_iter$PredictedRuntime-csv_iter$Prediction_StandardError)<= upperbound),]
            otherRows = otherRows[order(otherRows$PredictedRuntime),]
            #top 5 
            if(top_selection!=0){
              if(nrow(otherRows)>top_selection){
                otherRows = otherRows[1:top_selection,]
                otherRows = na.omit(otherRows)
                if(!minrow$Solver %in% otherRows$Solver){
                  otherRows = rbind(minrow, otherRows)
                  if(nrow(otherRows)>top_selection){
                    otherRows = otherRows[1:(nrow(otherRows)-1),]  
                  }
                  
                }
              }
            }
            data = otherRows
          }
          
          #lowebound as good as min pred, [pred-SE]<=minpred, then order by (pred-SE)
          else if(method_number==4){
            upperbound = min
            otherRows = csv_iter[which((csv_iter$PredictedRuntime-csv_iter$Prediction_StandardError)<= upperbound),]
            otherRows = otherRows[order(otherRows$PredictedRuntime - otherRows$Prediction_StandardError),]
            #top 5 
            if(top_selection!=0){
              if(nrow(otherRows)>top_selection){
                otherRows = otherRows[1:top_selection,]
                otherRows = na.omit(otherRows)
                if(!minrow$Solver %in% otherRows$Solver){
                  otherRows = rbind(minrow, otherRows)
                  if(nrow(otherRows)>top_selection){
                    otherRows = otherRows[1:(nrow(otherRows)-1),]  
                  }
                  
                }
              }
            }
            data = otherRows
          }
          
          #lower as good as min, but nor lower than [minpred-SE], [minpred-SE]<=[pred-SE]<=minpred, then order by pred value
          else if(method_number==5){
            upperbound = min
            lowerbound = min - minrow$Prediction_StandardError
            otherRows = csv_iter[which((csv_iter$PredictedRuntime-csv_iter$Prediction_StandardError)<= upperbound),]
            otherRows = otherRows[which((otherRows$PredictedRuntime-otherRows$Prediction_StandardError)>=lowerbound),]
            otherRows = otherRows[order(otherRows$PredictedRuntime),]
            if(top_selection!=0){
              if(nrow(otherRows)>top_selection){
                otherRows = otherRows[1:top_selection,]
                otherRows = na.omit(otherRows)
                if(!minrow$Solver %in% otherRows$Solver){
                  otherRows = rbind(minrow, otherRows)
                  if(nrow(otherRows)>top_selection){
                    otherRows = otherRows[1:(nrow(otherRows)-1),]  
                  }
                  
                }
              }
            }
            data = otherRows
          }
          
          #lower as good as min, but nor lower than [minpred-SE], [minpred-SE]<=[pred-SE]<=minpred, then order by (pred-SE)
          else if(method_number==6){
            upperbound = min
            lowerbound = min - minrow$Prediction_StandardError
            otherRows = csv_iter[which((csv_iter$PredictedRuntime-csv_iter$Prediction_StandardError)<= upperbound),]
            otherRows = otherRows[which((otherRows$PredictedRuntime-otherRows$Prediction_StandardError)>=lowerbound),]
            otherRows = otherRows[order((otherRows$PredictedRuntime-otherRows$Prediction_StandardError)),]
            if(top_selection!=0){
              if(nrow(otherRows)>top_selection){
                otherRows = otherRows[1:top_selection,]
                otherRows = na.omit(otherRows)
                if(!minrow$Solver %in% otherRows$Solver){
                  otherRows = rbind(minrow, otherRows)
                  if(nrow(otherRows)>top_selection){
                    otherRows = otherRows[1:(nrow(otherRows)-1),]  
                  }
                  
                }
              }
            }
            data = otherRows
          }
          
          #the following ones are statistical selection - they may be wrong
          colnames(data)<-c("InstanceName","Solver","SequentialRuntime","PredictedRuntime","Prediction_StandardError","Iteration","Validation_set","solver_prediction_rank")
          number_of_solvers = nrow(data)
          actual_parallel_runtime = data.frame()
          path = self$sequentialData$actual_CSV_path
          path = str_split(path,"/")[[1]]
          path = path[-length(path)]
          path = paste(path, collapse = '/') 
          #this can be improved by a reg model 
          if(number_of_solvers==1){
            filename = paste(path,"/teton-SAT2018-39-solvers-solo-replacement.csv",sep = "")
            actual_parallel_runtime = read.csv(filename)
          } else if (number_of_solvers<10){
            filename = paste(path,"/teton-SAT2018-39-solvers-",number_of_solvers,
                             "-parallel-replacement.csv",sep = "")
            actual_parallel_runtime = read.csv(filename)
          } else if(number_of_solvers>31){
            filename = paste(path,"/teton-SAT2018-39-solvers-32-parallel-replacement.csv",sep = "")
            actual_parallel_runtime = read.csv(filename)    
          } else if(number_of_solvers>=10 ){
            core = round(number_of_solvers,-1)
            filename = paste(path,"/teton-SAT2018-39-solvers-",core,"-parallel-replacement.csv",sep = "")
            actual_parallel_runtime = read.csv(filename)
          } 
          parallel_runtimes <- vector()
          csvrow = actual_parallel_runtime[which(actual_parallel_runtime$InstanceName == data[1,]$InstanceName),]
          for(m in 0:nrow(data)){
            parallel_runtimes <- append(parallel_runtimes,csvrow[data[m,]$Solver])
            parallel_runtimes = unname(unlist(parallel_runtimes))
          }
          vbs_runtime = self$sequentialData$get_VBS()[which(self$sequentialData$get_VBS()$InstanceName == data[1,]$InstanceName),]$VBS_Runtime
          #parallel_runtimes[which(parallel_runtimes==5000)]<-50000
          #vbs_runtime[which(vbs_runtime==5000)]<-50000
          data <- cbind(data,parallel_runtimes)
          data <- cbind(data,c(rep(vbs_runtime,number_of_solvers)))
          #colnames(data) = c("instance","solver","sequential_par10","prediction","standardError","parallel_par10","vbs_par10")
          colnames(data) = c("InstanceName","Solver","SequentialRuntime","PredictedRuntime",
                             "Prediction_StandardError","Iteration","Validation_set","solver_prediction_rank","ParallelRuntime","VBSRuntime")
          write.csv(data,paste(saveTo,"/",instanceName,"_",iter,"_fold.csv",sep=""),row.names = FALSE)
        }
      }
      parallelStop()
    },
    
    selection_based_on_SE_iterations = function(selectionpath, saveTo, method_number = 2, 
                                                top_selection = 0,ignoreTimeoutsOnVBS=TRUE){
      ds.files = list.files(predictionPath,pattern = ".csv")
      solvers = self$sequentialData$solvers
      solvers = solvers[order(solvers)]
      instances = unlist(lapply(ds.files,function(x){
        str_split(x,".csv")[[1]][1]
      }))
      instances = as.vector(unlist(instances))
      if(ignoreTimeoutsOnVBS) {
        if(is.null(self$sequentialData$solvedInstances)) self$sequentialData$get_VBS()
        instances = instances[which(paste("sat/",instances,sep="") %in% self$sequentialData$solvedInstances)]
      }
      #ids are  ordered
      
      parallelStartSocket(cpus = self$cpus)
      for(instance in instances){
        instanceName = instance
        csv = read.csv(paste(predictionPath,"/",instanceName[],".csv",sep=""))
        minrow = csv[which(csv$PredictedRuntime == min(csv$PredictedRuntime)),]
        min = minrow$PredictedRuntime
        #don't do selection
        if(method_number==-1){
          otherRows = csv
          otherRows = otherRows[order(otherRows$PredictedRuntime),]
          data = otherRows
        }
        #lowebound as good as min pred
        else if(method_number==2){
          upperbound = min
          otherRows = csv[which((csv$PredictedRuntime-csv$Prediction_StandardError)<= upperbound),]
          otherRows = otherRows[order(otherRows$PredictedRuntime - otherRows$Prediction_StandardError),]
          #top 5 
          if(top_selection!=0){
            if(nrow(otherRows)>top_selection){
              otherRows = otherRows[1:top_selection,]
            }
          }
          data = otherRows
        }
        colnames(data)<-c("InstanceName","Solver","ActualRuntime","PredictedRuntime","Prediction_StandardError")
        number_of_solvers = nrow(data)
        actual_parallel_runtime = data.frame()
        path = self$sequentialData$actual_CSV_path
        path = str_split(path,"/")[[1]]
        path = path[-length(path)]
        path = paste(path, collapse = '/') 
        #this can be improved by a reg model 
        if(number_of_solvers==1){
          filename = paste(path,"/teton-SAT2018-39-solvers-solo-replacement.csv",sep = "")
          actual_parallel_runtime = read.csv(filename)
        } else if (number_of_solvers<10){
          filename = paste(path,"/teton-SAT2018-39-solvers-",number_of_solvers,
                           "-parallel-replacement.csv",sep = "")
          actual_parallel_runtime = read.csv(filename)
        } else if(number_of_solvers>31){
          filename = paste(path,"/teton-SAT2018-39-solvers-32-parallel-replacement.csv",sep = "")
          actual_parallel_runtime = read.csv(filename)    
        } else if(number_of_solvers>=10 ){
          core = round(number_of_solvers,-1)
          filename = paste(path,"/teton-SAT2018-39-solvers-",core,"-parallel-replacement.csv",sep = "")
          actual_parallel_runtime = read.csv(filename)
        } 
        parallel_runtimes <- vector()
        csvrow = actual_parallel_runtime[which(actual_parallel_runtime$InstanceName == data[1,]$InstanceName),]
        for(m in 0:nrow(data)){
          parallel_runtimes <- append(parallel_runtimes,csvrow[data[m,]$Solver])
          parallel_runtimes = unname(unlist(parallel_runtimes))
        }
        vbs_runtime = self$sequentialData$get_VBS()[which(self$sequentialData$get_VBS()$InstanceName == data[1,]$InstanceName),]$VBS_Runtime
        #parallel_runtimes[which(parallel_runtimes==5000)]<-50000
        #vbs_runtime[which(vbs_runtime==5000)]<-50000
        data <- cbind(data,parallel_runtimes)
        data <- cbind(data,c(rep(vbs_runtime,number_of_solvers)))
        #colnames(data) = c("instance","solver","sequential_par10","prediction","standardError","parallel_par10","vbs_par10")
        colnames(data) = c("InstanceName","Solver","SequentialRuntime","PredictedRuntime",
                           "Prediction_StandardError","ParallelRuntime","VBSRuntime")
        write.csv(data,paste(saveTo,"/",instanceName,".csv",sep=""),row.names = FALSE)
      }
      parallelStop()
    },
    
    selection_based_on_SE_expectedValues = function(predictionPath, saveTo, method_number = 1, 
                                                    top_selection = 0,ignoreTimeoutsOnVBS=TRUE){
      ds.files = list.files(predictionPath,pattern = ".csv")
      solvers = self$sequentialData$solvers
      solvers = solvers[order(solvers)]
      instances = unlist(lapply(ds.files,function(x){
        str_split(x,".csv")[[1]][1]
      }))
      instances = as.vector(unlist(instances))
      if(ignoreTimeoutsOnVBS) {
        if(is.null(self$sequentialData$solvedInstances)) self$sequentialData$get_VBS()
        instances = instances[which(paste("sat/",instances,sep="") %in% self$sequentialData$solvedInstances)] 
      }
      #ids are  ordered
      
      parallelStartSocket(cpus = self$cpus)
      for(instance in instances){
        instanceName = instance
        csv = read.csv(paste(predictionPath,"/",instanceName[],".csv",sep=""))
        minrow = csv[which(csv$ExpectedPrediction == min(csv$ExpectedPrediction)),]
        min = minrow$ExpectedPrediction
        #don't do selection
        if(method_number==-1){
          otherRows = csv
          otherRows = otherRows[order(otherRows$ExpectedPrediction),]
          data = otherRows
        }
        #top selections
        else if(method_number==0){
          otherRows = csv
          otherRows = otherRows[order(otherRows$ExpectedPrediction),]
          if(top_selection != 0 && nrow(otherRows)>top_selection){
            otherRows = otherRows[1:top_selection,]
          }
          data = otherRows
        }
        #pred in min SE
        else if(method_number==1){
          upperbound = min + minrow$ExpectedSE
          lowerbound = min - minrow$ExpectedSE
          otherRows = csv[which(csv$ExpectedPrediction<= upperbound),]
          otherRows = otherRows[which(otherRows$ExpectedPrediction>=lowerbound),]
          #top 5 
          otherRows = otherRows[order(otherRows$ExpectedPrediction),]
          if(top_selection != 0 && nrow(otherRows)>top_selection){
            otherRows = otherRows[1:top_selection,]
          }
          data = otherRows
        }
        #lowebound as good as min pred
        else if(method_number==2){
          upperbound = min
          otherRows = csv[which((csv$ExpectedPrediction-csv$ExpectedSE)<= upperbound),]
          otherRows = otherRows[order(otherRows$ExpectedPrediction - otherRows$ExpectedSE),]
          #top 5 
          if(top_selection!=0){
            if(nrow(otherRows)>top_selection){
              otherRows = otherRows[1:top_selection,]
            }
          }
          data = otherRows
        }
        #pred in SE and lower as good as min
        else if(method_number==3){
          upperbound = min + minrow$ExpectedSE
          lowerbound = min - minrow$ExpectedSE
          otherRows = csv[which(csv$ExpectedPrediction<= upperbound),]
          otherRows = otherRows[which(otherRows$ExpectedPrediction>=lowerbound),]
          otherRows = otherRows[which((otherRows$ExpectedPrediction-otherRows$ExpectedSE) <= min),]
          otherRows = otherRows[order(otherRows$ExpectedPrediction),]
          if(top_selection!=0){
            if(nrow(otherRows)>top_selection){
              otherRows = otherRows[1:top_selection,]
            }
          }
          data = otherRows
        }
        
        colnames(data)<-c("InstanceName","Solver","SequentialRuntime","ExpectedPrediction","ExpectedSE","ExpectedLowebound","ExpectedUpperbound","Validation_set","ExpectedPredictionRank")
        number_of_solvers = nrow(data)
        actual_parallel_runtime = data.frame()
        path = self$sequentialData$actual_CSV_path
        path = str_split(path,"/")[[1]]
        path = path[-length(path)]
        path = paste(path, collapse = '/') 
        #this can be improved by a reg model 
        if(number_of_solvers==1){
          filename = paste(path,"/teton-SAT2018-39-solvers-solo-replacement.csv",sep = "")
          actual_parallel_runtime = read.csv(filename)
        } else if (number_of_solvers<10){
          filename = paste(path,"/teton-SAT2018-39-solvers-",number_of_solvers,
                           "-parallel-replacement.csv",sep = "")
          actual_parallel_runtime = read.csv(filename)
        } else if(number_of_solvers>31){
          filename = paste(path,"/teton-SAT2018-39-solvers-32-parallel-replacement.csv",sep = "")
          actual_parallel_runtime = read.csv(filename)    
        } else if(number_of_solvers>=10 ){
          core = round(number_of_solvers,-1)
          filename = paste(path,"/teton-SAT2018-39-solvers-",core,"-parallel-replacement.csv",sep = "")
          actual_parallel_runtime = read.csv(filename)
        } 
        parallel_runtimes <- vector()
        csvrow = actual_parallel_runtime[which(actual_parallel_runtime$InstanceName == data[1,]$InstanceName),]
        for(m in 0:nrow(data)){
          parallel_runtimes <- append(parallel_runtimes,csvrow[data[m,]$Solver])
          parallel_runtimes = unname(unlist(parallel_runtimes))
        }
        vbs_runtime = self$sequentialData$get_VBS()[which(self$sequentialData$get_VBS()$InstanceName == data[1,]$InstanceName),]$VBS_Runtime
        #parallel_runtimes[which(parallel_runtimes==5000)]<-50000
        #vbs_runtime[which(vbs_runtime==5000)]<-50000
        data <- cbind(data,parallel_runtimes)
        data <- cbind(data,c(rep(vbs_runtime,number_of_solvers)))
        #colnames(data) = c("instance","solver","sequential_par10","prediction","standardError","parallel_par10","vbs_par10")
        colnames(data) = c(head(colnames(data),-2),"ParallelRuntime","VBSRuntime")
        write.csv(data,paste(saveTo,"/",instanceName,".csv",sep=""),row.names = FALSE)
      }
      parallelStop()
    },
    
    plot_selection_increasing_core_folds = function(selection_valid_path){
      #library(plotly)
      all_instances = list.files(selection_valid_path,".csv")
      for(ins in 1:length(all_instances)){
        sample_instance = all_instances[ins:(ins+10)]
        ins = ins+10
        csv = read.csv(paste(selection_valid_path,sample_instance[1],sep = ""))
        fig = plot_ly()
        fig = fig%>%add_trace(x=c(1:nrow(csv)),y= csv$VBSRuntime,mode='lines',name="VBS",line = list(width = 4, dash = "dot"))
        for(j in 1:length(sample_instance)){
          csv = read.csv(paste(selection_valid_path,sample_instance[j],sep = ""))
          csv$increasing_cores_runtime = c(rep(0,nrow(csv)))
          for(i in 1:nrow(csv)){
            core =0
            if(i ==1){
              core = "solo"
            } else if(i<=10){
              core = i
            } else if(i<=14){
              core = 10
            } else if(i <= 24){
              core = 20
            } else if(i<=31){
              core = 30
            } else if(i>=32){
              core =32
            }
            if(core == "solo"){
              runtimes = read.csv(paste("~/Documents/Portfolio-Scheduling/originalCSVs-Teton_SAT18/without_twoinstances/teton-SAT2018-39-solvers-",core,"-replacement.csv",sep=""))
            } else{
              runtimes = read.csv(paste("~/Documents/Portfolio-Scheduling/originalCSVs-Teton_SAT18/without_twoinstances/teton-SAT2018-39-solvers-",core,"-parallel-replacement.csv",sep=""))
            }
            instanceName = str_split(sample_instance,".csv")[[1]][1]
            instanceName = paste0(head(str_split(instanceName,"_")[[1]],-2),collapse="_")
            
            related_row = runtimes[which(runtimes$InstanceName==paste("sat/",instanceName,sep="")),]
            solvers = csv[1:i,]$Solver
            csv$increasing_cores_runtime[i] = min(unlist(unname(related_row[solvers])))
          }
          fig = fig%>%add_trace(x=c(1:nrow(csv)),y= csv$increasing_cores_runtime,mode='lines+markers',name=paste("Fold ",j))
        }
        htmlwidgets::saveWidget(fig,paste("~/Documents/OrganizedScripts/preds_valid/validation/plot/",instanceName,".html",sep=""))
      }
      
    },
    
    plot_selection_increasing_core_expected = function(selection_valid_exptected_path){
      #library(plotly)
      all_instances = list.files(selection_valid_exptected_path,".csv")
      for(ins in 1:length(all_instances)){
        sample_instance = all_instances[ins]
        csv = read.csv(paste(selection_valid_exptected_path,sample_instance,sep = ""))
        fig = plot_ly()
        fig = fig%>%add_trace(x=c(1:nrow(csv)),y= csv$VBSRuntime,mode='lines',name="VBS",line = list(width = 4, dash = "dot"))
        csv$increasing_cores_runtime = c(rep(0,nrow(csv)))
        for(i in 1:nrow(csv)){
          core =0
          if(i ==1){
            core = "solo"
          } else if(i<=10){
            core = i
          } else if(i<=14){
            core = 10
          } else if(i <= 24){
            core = 20
          } else if(i<=31){
            core = 30
          } else if(i>=32){
            core =32
          }
          if(core == "solo"){
            runtimes = read.csv(paste("~/Documents/Portfolio-Scheduling/originalCSVs-Teton_SAT18/without_twoinstances/teton-SAT2018-39-solvers-",core,"-replacement.csv",sep=""))
          } else{
            runtimes = read.csv(paste("~/Documents/Portfolio-Scheduling/originalCSVs-Teton_SAT18/without_twoinstances/teton-SAT2018-39-solvers-",core,"-parallel-replacement.csv",sep=""))
          }
          instanceName = str_split(sample_instance,".csv")[[1]][1]
          related_row = runtimes[which(runtimes$InstanceName==paste("sat/",instanceName,sep="")),]
          solvers = csv[1:i,]$Solver
          csv$increasing_cores_runtime[i] = min(unlist(unname(related_row[solvers])))
          csv$increasing_cores_prediction[i] = min(csv$ExpectedPrediction[1:i])  
          csv$increasing_cores_prediction_lowerbound[i] = min(csv$ExpectedLowebound[1:i])
          
        }
        fig = fig%>%add_trace(x=c(1:nrow(csv)),y= csv$increasing_cores_runtime,mode='lines+markers',name="Actual Parallel")
        fig = fig%>%add_trace(x=c(1:nrow(csv)),y= csv$increasing_cores_prediction,mode='lines+markers',name="Expected Prediction")
        fig = fig%>%add_trace(x=c(1:nrow(csv)),y= csv$increasing_cores_prediction_lowerbound,mode='lines+markers',name="Expected Lowerbound")
        
        htmlwidgets::saveWidget(fig,paste("~/Documents/OrganizedScripts/preds_valid/validation/plot/",instanceName,".html",sep=""))
      }
      
    },
    
    #get mcp, par10, runtime and success rate of selection
    get_summary_selection_result = function(selectionPath,ignoreTimeouts=TRUE, method_number = 0, median = FALSE){
      tablePar10 <- data.frame(matrix(nrow = 0, ncol = 13))
      tableMCP <- data.frame(matrix(nrow = 0, ncol = 13))
      tableSuccess <- data.frame(matrix(nrow = 0, ncol = 13))
      tableRuntime <- data.frame(matrix(nrow = 0, ncol = 13))
      instance_files = list.files(selectionPath,pattern =".csv")
      if(ignoreTimeouts){
        unsolved = lapply(self$sequentialData$unsolvedInstances, function(x) str_split(x,"sat/")[[1]][2])
        unsolved = unlist(unsolved)
        unsolved = paste(unsolved,".csv",sep = "")
        instance_files = instance_files[!instance_files %in% unsolved]
      }
      #min parallel runtime of selected schedule
      parallel_runtimes = vector()
      
      sequential_runtimes = vector()
      vbs_runtime = vector()
      nrows = vector()
      data = data.frame(matrix(nrow=0,ncol=11))
      for(instance in instance_files){
        #if(".csv" %in% instance){
        csv = read.csv(paste(selectionPath,"/",instance,sep = ""))
        #}
        #else{
        #  csv = read.csv(paste(selectionPath,"/",instance,".csv",sep = ""))
        #}
        min_parallel_min = min(csv$ParallelRuntime)
        min_sequential_runtimes = min(csv$SequentialRuntime)
        vbs_runtime = csv$VBSRuntime[1]
        n_selected_solvers = nrow(csv)
        row = c(instance,vbs_runtime,min_sequential_runtimes,min_parallel_min,n_selected_solvers, csv$delta[1], csv$delta_prime[1], csv$alpha[1], csv$orderBy[1])
        data = rbind(row,data)
      }
      colnames(data)= c("InstanceName","VBSRuntime","min_sequential_runtimes",
                        "min_parallel_runtime","n_selected_solvers", "delta", "delta_prime", "alpha", "orderBy")
      #vbs_not_selected= data[which(data$vbs_runtime!=data$min_sequential_runtimes),]
      vbs = as.numeric(data$VBSRuntime)
      selec_seq = as.numeric(data$min_sequential_runtimes)
      mcp_seq = selec_seq - vbs
      mcp_seq[which(mcp_seq<0)]<-0
      selec_par = as.numeric(data$min_parallel_runtime)
      mcp_par = selec_par - vbs
      mcp_par[which(mcp_par<0)]<-0
      delta = data$delta[1]
      delta_prime = data$delta_prime[1]
      alpha = data$alpha[1]
      orderBy = data$orderBy[1]
      #success
      if(median == TRUE){
        rowRuntime <- c("Runtime",method_number,median(vbs),median(selec_seq),median(selec_par),
                        median(as.numeric(data$n_selected_solvers)),mean(selec_seq == vbs), delta, delta_prime, alpha, ignoreTimeouts, median, orderBy)
        #success
        #should be mean since will be true false otherwise
        rowSuccess <- c("Success",method_number,mean(vbs<self$sequentialData$Cutoff),mean(selec_seq<self$sequentialData$Cutoff),mean(selec_par<self$sequentialData$Cutoff),
                        median(as.numeric(data$n_selected_solvers)),mean(selec_seq == vbs), delta, delta_prime, alpha, ignoreTimeouts, median, orderBy)
        
        rowMCP <- c("MCP",method_number,0,median(mcp_seq),median(mcp_par),
                    median(as.numeric(data$n_selected_solvers)),mean(selec_seq == vbs), delta, delta_prime, alpha, ignoreTimeouts, median, orderBy)
        
        vbs[which(vbs>=self$sequentialData$Cutoff)]<-self$sequentialData$Cutoff*10
        selec_seq[which(selec_seq>=self$sequentialData$Cutoff)]<-self$sequentialData$Cutoff*10
        selec_par[which(selec_par>=self$sequentialData$Cutoff)]<-self$sequentialData$Cutoff*10
        
        rowPar10 <- c("Par10",method_number,median(vbs),median(selec_seq),median(selec_par),
                      median(as.numeric(data$n_selected_solvers)),mean(selec_seq == vbs), delta, delta_prime, alpha, ignoreTimeouts, median, orderBy)
      } else{
        rowRuntime <- c("Runtime",method_number,mean(vbs),mean(selec_seq),mean(selec_par),
                        mean(as.numeric(data$n_selected_solvers)),mean(selec_seq == vbs), delta, delta_prime, alpha, ignoreTimeouts, median, orderBy)
        #success
        rowSuccess <- c("Success",method_number,mean(vbs<self$sequentialData$Cutoff*10),mean(selec_seq<self$sequentialData$Cutoff*10),mean(selec_par<self$sequentialData$Cutoff*10),
                        mean(as.numeric(data$n_selected_solvers)),mean(selec_seq == vbs), delta, delta_prime, alpha, ignoreTimeouts, median, orderBy)
        
        rowMCP <- c("MCP",method_number,0,mean(mcp_seq),mean(mcp_par),
                    mean(as.numeric(data$n_selected_solvers)),mean(selec_seq == vbs), delta, delta_prime, alpha, ignoreTimeouts, median, orderBy)
        
        vbs[which(vbs>=self$sequentialData$Cutoff)]<-self$sequentialData$Cutoff*10
        selec_seq[which(selec_seq>=self$sequentialData$Cutoff)]<-self$sequentialData$Cutoff*10
        selec_par[which(selec_par>=self$sequentialData$Cutoff)]<-self$sequentialData$Cutoff*10
        
        rowPar10 <- c("Par10",method_number,mean(vbs),mean(selec_seq),mean(selec_par),
                      mean(as.numeric(data$n_selected_solvers)),mean(selec_seq == vbs), delta, delta_prime, alpha, ignoreTimeouts, median, orderBy)
      }
      
      tableRuntime <- rbind(rowRuntime,tableRuntime)
      tableMCP <- rbind(rowMCP,tableMCP)
      tableSuccess <- rbind(rowSuccess,tableSuccess)
      tablePar10 <- rbind(rowPar10,tablePar10)
      colnames(tableRuntime)<- c("metric","method","VBS","Sequential_time","Parallel_time",
                                 "#selected_solvers","vbs_selection", "delta", "delta_prime", "alpha", "ignoreTimeouts", "median", "orderBy")
      colnames(tableMCP)<- c("metric","method","VBS","Sequential_time","Parallel_time",
                             "#selected_solvers","vbs_selection", "delta", "delta_prime", "alpha", "ignoreTimeouts", "median", "orderBy")
      colnames(tableSuccess)<- c("metric","method","VBS","Sequential_time","Parallel_time",
                                 "#selected_solvers","vbs_selection", "delta", "delta_prime", "alpha", "ignoreTimeouts", "median", "orderBy")
      colnames(tablePar10)<- c("metric","method","VBS","Sequential_time","Parallel_time",
                               "#selected_solvers","vbs_selection", "delta", "delta_prime", "alpha", "ignoreTimeouts", "median", "orderBy")
      return(list(tableRuntime, tableMCP,tablePar10,tableSuccess))
    },
    
    #get mcp, par10, runtime and success rate of selection
    get_summary_selection_result_differentThetasEachAlg = function(selectionPath,ignoreTimeouts=TRUE, method_number = 0, median = FALSE){
      tablePar10 <- data.frame(matrix(nrow = 0, ncol = 8+self$sequentialData$n_solvers))
      tableMCP <- data.frame(matrix(nrow = 0, ncol = 8+self$sequentialData$n_solvers))
      tableSuccess <- data.frame(matrix(nrow = 0, ncol = 8+self$sequentialData$n_solvers))
      tableRuntime <- data.frame(matrix(nrow = 0, ncol = 8+self$sequentialData$n_solvers))
      instance_files = list.files(selectionPath,pattern =".csv")
      if(ignoreTimeouts){
        unsolved = lapply(self$sequentialData$unsolvedInstances, function(x) str_split(x,"sat/")[[1]][2])
        unsolved = unlist(unsolved)
        unsolved = paste(unsolved,".csv",sep = "")
        instance_files = instance_files[!instance_files %in% unsolved]
      }
      #min parallel runtime of selected schedule
      parallel_runtimes = vector()
      
      sequential_runtimes = vector()
      vbs_runtime = vector()
      nrows = vector()
      data = data.frame(matrix(nrow=0,ncol=8+self$sequentialData$n_solvers))
      for(instance in instance_files){
        #if(".csv" %in% instance){
        csv = read.csv(paste(selectionPath,"/",instance,sep = ""))
        #}
        #else{
        #  csv = read.csv(paste(selectionPath,"/",instance,".csv",sep = ""))
        #}
        min_parallel_min = min(csv$ParallelRuntime)
        min_sequential_runtimes = min(csv$SequentialRuntime)
        vbs_runtime = csv$VBSRuntime[1]
        n_selected_solvers = nrow(csv)
        row = c(instance,vbs_runtime,min_sequential_runtimes,min_parallel_min,n_selected_solvers, unlist(unname(csv[1,8:length(colnames(csv))])))
        data = rbind(row,data)
      }
      colnames(data)= c("InstanceName","VBSRuntime","min_sequential_runtimes",
                        "min_parallel_runtime","n_selected_solvers", colnames(csv)[9:length(colnames(csv))-1],"orderBy")
      #vbs_not_selected= data[which(data$vbs_runtime!=data$min_sequential_runtimes),]
      vbs = as.numeric(data$VBSRuntime)
      selec_seq = as.numeric(data$min_sequential_runtimes)
      mcp_seq = selec_seq - vbs
      mcp_seq[which(mcp_seq<0)]<-0
      selec_par = as.numeric(data$min_parallel_runtime)
      mcp_par = selec_par - vbs
      mcp_par[which(mcp_par<0)]<-0
      theta = unlist(unname(data[1,7:length(colnames(data))-1]))
      orderBy = data$orderBy[1]
      #success
      if(median == TRUE){
        rowRuntime <- c("Runtime",method_number,median(vbs),median(selec_seq),median(selec_par),
                        median(as.numeric(data$n_selected_solvers)),mean(selec_seq == vbs), theta, ignoreTimeouts, median, orderBy)
        #success
        #should be mean since will be true false otherwise
        rowSuccess <- c("Success",method_number,mean(vbs<self$sequentialData$Cutoff),mean(selec_seq<self$sequentialData$Cutoff),mean(selec_par<self$sequentialData$Cutoff),
                        median(as.numeric(data$n_selected_solvers)),mean(selec_seq == vbs), theta, ignoreTimeouts, median, orderBy)
        
        rowMCP <- c("MCP",method_number,0,median(mcp_seq),median(mcp_par),
                    median(as.numeric(data$n_selected_solvers)),mean(selec_seq == vbs), theta, ignoreTimeouts, median, orderBy)
        
        vbs[which(vbs>=self$sequentialData$Cutoff)]<-self$sequentialData$Cutoff*10
        selec_seq[which(selec_seq>=self$sequentialData$Cutoff)]<-self$sequentialData$Cutoff*10
        selec_par[which(selec_par>=self$sequentialData$Cutoff)]<-self$sequentialData$Cutoff*10
        
        rowPar10 <- c("Par10",method_number,median(vbs),median(selec_seq),median(selec_par),
                      median(as.numeric(data$n_selected_solvers)),mean(selec_seq == vbs), theta, ignoreTimeouts, median, orderBy)
      } else{
        rowRuntime <- c("Runtime",method_number,mean(vbs),mean(selec_seq),mean(selec_par),
                        mean(as.numeric(data$n_selected_solvers)),mean(selec_seq == vbs), theta , ignoreTimeouts, median, orderBy)
        #success
        rowSuccess <- c("Success",method_number,mean(vbs<self$sequentialData$Cutoff),mean(selec_seq<self$sequentialData$Cutoff),mean(selec_par<self$sequentialData$Cutoff),
                        mean(as.numeric(data$n_selected_solvers)),mean(selec_seq == vbs), theta, ignoreTimeouts, median, orderBy)
        
        rowMCP <- c("MCP",method_number,0,mean(mcp_seq),mean(mcp_par),
                    mean(as.numeric(data$n_selected_solvers)),mean(selec_seq == vbs), theta, ignoreTimeouts, median, orderBy)
        
        vbs[which(vbs>=self$sequentialData$Cutoff)]<-self$sequentialData$Cutoff*10
        selec_seq[which(selec_seq>=self$sequentialData$Cutoff)]<-self$sequentialData$Cutoff*10
        selec_par[which(selec_par>=self$sequentialData$Cutoff)]<-self$sequentialData$Cutoff*10
        
        rowPar10 <- c("Par10",method_number,mean(vbs),mean(selec_seq),mean(selec_par),
                      mean(as.numeric(data$n_selected_solvers)),mean(selec_seq == vbs), theta, ignoreTimeouts, median, orderBy)
      }
      
      tableRuntime <- rbind(rowRuntime,tableRuntime)
      tableMCP <- rbind(rowMCP,tableMCP)
      tableSuccess <- rbind(rowSuccess,tableSuccess)
      tablePar10 <- rbind(rowPar10,tablePar10)
      colnames(tableRuntime)<- c("metric","method","VBS","Sequential_time","Parallel_time",
                                 "#selected_solvers","vbs_selection", colnames(data)[7:length(data)-1], "ignoreTimeouts", "median", "orderBy")
      colnames(tableMCP)<- c("metric","method","VBS","Sequential_time","Parallel_time",
                             "#selected_solvers","vbs_selection", colnames(data)[7:length(data)-1], "ignoreTimeouts", "median", "orderBy")
      colnames(tableSuccess)<- c("metric","method","VBS","Sequential_time","Parallel_time",
                                 "#selected_solvers","vbs_selection", colnames(data)[7:length(data)-1], "ignoreTimeouts", "median", "orderBy")
      colnames(tablePar10)<- c("metric","method","VBS","Sequential_time","Parallel_time",
                               "#selected_solvers","vbs_selection", colnames(data)[7:length(data)-1], "ignoreTimeouts", "median", "orderBy")
      return(list(tableRuntime, tableMCP,tablePar10,tableSuccess))
    },
    
    get_summary_all = function(predictionPath = self$predictionPath, 
                               selectionPath = self$selectionPath,
                               ignoreTimeoutsOnVBS=FALSE, 
                               method_numbers,
                               top_selections, 
                               median = FALSE,
                               delta = 0 , alpha = 0 , delta_prime= 0){
      runtime = data.frame(matrix(nrow = 0, ncol = 7))
      mcp = data.frame(matrix(nrow = 0, ncol = 7))
      par10 = data.frame(matrix(nrow = 0, ncol = 7))
      success = data.frame(matrix(nrow = 0, ncol = 7))
      for(method_number in method_numbers){
        for(top_selection in top_selections){
          if(method_number == 0){
            self$selection_based_on_SE(predictionPath = predictionPath, 
                                       saveTo = selectionPath, 
                                       method_number = method_number, 
                                       top_selection = top_selection,
                                       ignoreTimeoutsOnVBS = ignoreTimeoutsOnVBS)
            
          } else{
            self$selection_based_on_SE(predictionPath = predictionPath, 
                                       saveTo = selectionPath, 
                                       method_number = method_number, 
                                       top_selection = top_selection,
                                       ignoreTimeoutsOnVBS = ignoreTimeoutsOnVBS, 
                                       orderBy = "pred-se",
                                       delta = delta,
                                       delta_prime = delta_prime,
                                       alpha = alpha)
          }
          summary = self$get_summary_selection_result(selectionPath = selectionPath, ignoreTimeouts = ignoreTimeoutsOnVBS, 
                                                      method_number = method_number, median = median)
          runtime = rbind(runtime, summary[[1]])
          mcp = rbind(mcp, summary[[2]])
          par10 = rbind(par10, summary[[3]])
          success = rbind(success, summary[[4]])
          print(success)
        }
      }
      retval = list(runtime,mcp,par10,success)
      return(retval)
    },
    
    randomSearch_delta_prime = function(randomNumbers, method_number, top_selection, selectionPath, orderBy, 
                                        predictionPath, ignoreTimeoutsOnVBS = FALSE, alpha = 0, delta = 0, median = FALSE){
      runtime = data.frame(matrix(nrow = 0, ncol = 10))
      mcp = data.frame(matrix(nrow = 0, ncol = 10))
      par10 = data.frame(matrix(nrow = 0, ncol = 10))
      success = data.frame(matrix(nrow = 0, ncol = 10))
      parallelStartSocket(cpus = self$cpus)
      i = 1
      for (d_p in randomNumbers){
        self$selection_based_on_SE(method_number = method_number, top_selection = top_selection, delta_prime = d_p , 
                                   saveTo = selectionPath, orderBy = orderBy, predictionPath = predictionPath, 
                                   ignoreTimeoutsOnVBS = ignoreTimeoutsOnVBS, alpha = alpha, delta = delta)
        summary = self$get_summary_selection_result(selectionPath = selectionPath, ignoreTimeouts = ignoreTimeoutsOnVBS, 
                                                    method_number = method_number, median = median)
        runtime = rbind(runtime, summary[[1]])
        mcp = rbind(mcp, summary[[2]])
        par10 = rbind(par10, summary[[3]])
        success = rbind(success, summary[[4]])
        print(paste("Iteration:", i))
        i = i+1
        print(paste("delta_prime:",d_p))
        print(paste("runtime:",runtime$Parallel_time[length(runtime$Parallel_time)]))
        print(paste("mcp:",mcp$Parallel_time[length(mcp$Parallel_time)]))
        print(paste("par10:",par10$Parallel_time[length(par10$Parallel_time)]))
        print(paste("success:",success$Parallel_time[length(success$Parallel_time)]))
      }
      retval = list(runtime,mcp,par10,success)
      retval = do.call(rbind, retval)
      return(retval)
    },
    
    randomSearch_delta = function(randomNumbers, method_number, top_selection, selectionPath, orderBy, 
                                  predictionPath, ignoreTimeoutsOnVBS = FALSE, alpha = 0, delta_prime = 0, median = FALSE){
      runtime = data.frame(matrix(nrow = 0, ncol = 10))
      mcp = data.frame(matrix(nrow = 0, ncol = 10))
      par10 = data.frame(matrix(nrow = 0, ncol = 10))
      success = data.frame(matrix(nrow = 0, ncol = 10))
      parallelStartSocket(cpus = self$cpus)
      i = 1
      for (d in randomNumbers){
        self$selection_based_on_SE(method_number = method_number, top_selection = top_selection, delta = d , 
                                   saveTo = selectionPath, orderBy = orderBy, predictionPath = predictionPath, 
                                   ignoreTimeoutsOnVBS = ignoreTimeoutsOnVBS, alpha = alpha, delta_prime = delta_prime)
        summary = self$get_summary_selection_result(selectionPath = selectionPath, ignoreTimeouts = ignoreTimeoutsOnVBS, 
                                                    method_number = method_number, median = median)
        runtime = rbind(runtime, summary[[1]])
        mcp = rbind(mcp, summary[[2]])
        par10 = rbind(par10, summary[[3]])
        success = rbind(success, summary[[4]])
        print(paste("Iteration:", i))
        i = i+1
        print(paste("delta:",d))
        print(paste("runtime:",runtime$Parallel_time[length(runtime$Parallel_time)]))
        print(paste("mcp:",mcp$Parallel_time[length(mcp$Parallel_time)]))
        print(paste("par10:",par10$Parallel_time[length(par10$Parallel_time)]))
        print(paste("success:",success$Parallel_time[length(success$Parallel_time)]))
      }
      retval = list(runtime,mcp,par10,success)
      retval = do.call(rbind, retval)
      return(retval)
    },
    
    #alpha is equal to delta, so we don't need to do randomsearch for alpha
    # randomSearch_alpha = function(randomNumbers, method_number, top_selection, selectionPath, orderBy, 
    #                               predictionPath, ignoreTimeoutsOnVBS = FALSE, delta = 0, delta_prime = 0, median = FALSE){
    #   runtime = data.frame(matrix(nrow = 0, ncol = 10))
    #   mcp = data.frame(matrix(nrow = 0, ncol = 10))
    #   par10 = data.frame(matrix(nrow = 0, ncol = 10))
    #   success = data.frame(matrix(nrow = 0, ncol = 10))
    #   parallelStartSocket(cpus = self$cpus)
    #   i = 1
    #   for (a in randomNumbers){
    #     self$selection_based_on_SE(method_number = method_number, top_selection = top_selection, alpha = a , 
    #                                saveTo = selectionPath, orderBy = orderBy, predictionPath = predictionPath, 
    #                                ignoreTimeoutsOnVBS = ignoreTimeoutsOnVBS, delta = a, delta_prime = delta_prime)
    #     summary = self$get_summary_selection_result(selectionPath = selectionPath, ignoreTimeouts = ignoreTimeoutsOnVBS, 
    #                                                 method_number = method_number, median = median)
    #     runtime = rbind(runtime, summary[[1]])
    #     mcp = rbind(mcp, summary[[2]])
    #     par10 = rbind(par10, summary[[3]])
    #     success = rbind(success, summary[[4]])
    #     print(paste("Iteration:", i))
    #     i = i+1
    #     print(paste("alpha:",a))
    #     print(paste("runtime:",runtime$Parallel_time[length(runtime$Parallel_time)]))
    #     print(paste("mcp:",mcp$Parallel_time[length(mcp$Parallel_time)]))
    #     print(paste("par10:",par10$Parallel_time[length(par10$Parallel_time)]))
    #     print(paste("success:",success$Parallel_time[length(success$Parallel_time)]))
    #   }
    #   retval = list(runtime,mcp,par10,success)
    #   retval = do.call(rbind, retval)
    #   return(retval)
    # },
    
    randomSearch_combination = function(randomNumbers_delta, randomNumbers_delta_prime, 
                                        #randomNumbers_alpha,
                                        method_number, top_selection, selectionPath, orderBy = c('pred','pred-se'), predictionPath, 
                                        ignoreTimeoutsOnVBS = FALSE, median = c('mean','median')){
      runtime = data.frame(matrix(nrow = 0, ncol = 13))
      mcp = data.frame(matrix(nrow = 0, ncol = 13))
      par10 = data.frame(matrix(nrow = 0, ncol = 13))
      success = data.frame(matrix(nrow = 0, ncol = 13))
      parallelStartSocket(cpus = self$cpus)
      i = 1
      for(d_p in randomNumbers_delta_prime){
        for(d in randomNumbers_delta){
          for(order in orderBy){
            if(order == 'pred'){
              a = 0
              self$selection_based_on_SE(method_number = method_number, top_selection = top_selection, alpha = a, 
                                         saveTo = selectionPath, orderBy = order, predictionPath = predictionPath, 
                                         ignoreTimeoutsOnVBS = ignoreTimeoutsOnVBS, delta = d, delta_prime = d_p)
              for(m in median){
                mFlag = (m=='median')
                summary = self$get_summary_selection_result(selectionPath = selectionPath, ignoreTimeouts = ignoreTimeoutsOnVBS, 
                                                            method_number = method_number, median = mFlag)
                runtime = rbind(runtime, summary[[1]])
                mcp = rbind(mcp, summary[[2]])
                par10 = rbind(par10, summary[[3]])
                success = rbind(success, summary[[4]])
                print(paste("Iteration:", i))
                print(paste("delta:",d))
                print(paste("delta_prime:",d_p))
                print(paste("alpha:",a))
                print(paste("runtime:",runtime$Parallel_time[length(runtime$Parallel_time)]))
                print(paste("mcp:",mcp$Parallel_time[length(mcp$Parallel_time)]))
                print(paste("par10:",par10$Parallel_time[length(par10$Parallel_time)]))
                print(paste("success:",success$Parallel_time[length(success$Parallel_time)]))
              }
              i = i+1
            } 
            else if(order == 'pred-se'){
              a = d
              self$selection_based_on_SE(method_number = method_number, top_selection = top_selection, alpha = a, 
                                         saveTo = selectionPath, orderBy = order, predictionPath = predictionPath, 
                                         ignoreTimeoutsOnVBS = ignoreTimeoutsOnVBS, delta = d, delta_prime = d_p)
              for(m in median){
                mFlag = (m=='median')
                summary = self$get_summary_selection_result(selectionPath = selectionPath, ignoreTimeouts = ignoreTimeoutsOnVBS, 
                                                            method_number = method_number, median = mFlag)
                runtime = rbind(runtime, summary[[1]])
                mcp = rbind(mcp, summary[[2]])
                par10 = rbind(par10, summary[[3]])
                success = rbind(success, summary[[4]])
                print(paste("Iteration:", i))
                print(paste("delta:",d))
                print(paste("delta_prime:",d_p))
                print(paste("alpha:",a))
                print(paste("runtime:",runtime$Parallel_time[length(runtime$Parallel_time)]))
                print(paste("mcp:",mcp$Parallel_time[length(mcp$Parallel_time)]))
                print(paste("par10:",par10$Parallel_time[length(par10$Parallel_time)]))
                print(paste("success:",success$Parallel_time[length(success$Parallel_time)]))
              }
              i = i+1
            }
          }
        }
      }
      retval = list(runtime,mcp,par10,success)
      retval = do.call(rbind, retval)
      return(retval)
    },
    
    randomSearch_allEqual = function(randomNumbers, method_number, top_selection, 
                                     selectionPath, orderBy = c('pred','pred-se'), predictionPath, 
                                     ignoreTimeoutsOnVBS = FALSE, median = c('mean','median')){
      runtime = data.frame(matrix(nrow = 0, ncol = 13))
      mcp = data.frame(matrix(nrow = 0, ncol = 13))
      par10 = data.frame(matrix(nrow = 0, ncol = 13))
      success = data.frame(matrix(nrow = 0, ncol = 13))
      parallelStartSocket(cpus = self$cpus)
      i = 1
      for(d in randomNumbers){
        for(order in orderBy){
          if(order == 'pred'){
            self$selection_based_on_SE(method_number = method_number, top_selection = top_selection, alpha = 0, 
                                       saveTo = selectionPath, orderBy = order, predictionPath = predictionPath, 
                                       ignoreTimeoutsOnVBS = ignoreTimeoutsOnVBS, delta = d, delta_prime = d)
            for(m in median){
              mFlag = (m=='median')
              summary = self$get_summary_selection_result(selectionPath = selectionPath, ignoreTimeouts = ignoreTimeoutsOnVBS, 
                                                          method_number = method_number, median = mFlag)
              runtime = rbind(runtime, summary[[1]])
              mcp = rbind(mcp, summary[[2]])
              par10 = rbind(par10, summary[[3]])
              success = rbind(success, summary[[4]])
              print(paste("Iteration:", i))
              print(paste("delta:",d))
              print(paste("delta_prime:",d))
              print(paste("alpha:",d))
              print(paste("runtime:",runtime$Parallel_time[length(runtime$Parallel_time)]))
              print(paste("mcp:",mcp$Parallel_time[length(mcp$Parallel_time)]))
              print(paste("par10:",par10$Parallel_time[length(par10$Parallel_time)]))
              print(paste("success:",success$Parallel_time[length(success$Parallel_time)]))
            }
            i = i+1
          } 
          else if(order == 'pred-se'){
            self$selection_based_on_SE(method_number = method_number, top_selection = top_selection, alpha = d, 
                                       saveTo = selectionPath, orderBy = order, predictionPath = predictionPath, 
                                       ignoreTimeoutsOnVBS = ignoreTimeoutsOnVBS, delta = d, delta_prime = d)
            for(m in median){
              mFlag = (m=='median')
              summary = self$get_summary_selection_result(selectionPath = selectionPath, ignoreTimeouts = ignoreTimeoutsOnVBS, 
                                                          method_number = method_number, median = mFlag)
              runtime = rbind(runtime, summary[[1]])
              mcp = rbind(mcp, summary[[2]])
              par10 = rbind(par10, summary[[3]])
              success = rbind(success, summary[[4]])
              print(paste("Iteration:", i))
              print(paste("delta:",d))
              print(paste("delta_prime:",d))
              print(paste("alpha:",d))
              print(paste("runtime:",runtime$Parallel_time[length(runtime$Parallel_time)]))
              print(paste("mcp:",mcp$Parallel_time[length(mcp$Parallel_time)]))
              print(paste("par10:",par10$Parallel_time[length(par10$Parallel_time)]))
              print(paste("success:",success$Parallel_time[length(success$Parallel_time)]))
            }
            i = i+1
          }
        }
      }
      retval = list(runtime,mcp,par10,success)
      retval = do.call(rbind, retval)
      return(retval)
    },
    
    randomSearch_eachAlgTheta = function(iterations= 100, top_selection=0, 
                                         selectionPath=self$selectionPath, orderBy = c('pred','pred-se'), predictionPath = self$predictionPath, 
                                         ignoreTimeoutsOnVBS = FALSE, median = c('mean','median')){
      set.seed(1234)
      #I hope this is fine
      randomNumbers = 2^rnorm(iterations*self$sequentialData$n_solvers)
      runtime = data.frame(matrix(nrow = 0, ncol = 13+self$sequentialData$n_solvers))
      mcp = data.frame(matrix(nrow = 0, ncol = 13+self$sequentialData$n_solvers))
      par10 = data.frame(matrix(nrow = 0, ncol = 13+self$sequentialData$n_solvers))
      success = data.frame(matrix(nrow = 0, ncol = 13+self$sequentialData$n_solvers))
      parallelStartSocket(cpus = self$cpus)
      i = 1
      for(iter in 1:iterations){
        for(order in orderBy){
          theta = randomNumbers[c(((iter-1)*self$sequentialData$n_solvers+1): (iter*self$sequentialData$n_solvers))]
          self$selection_based_on_SE_thetaForAlg(top_selection = top_selection, saveTo = selectionPath, orderBy = order, 
                                                 predictionPath = predictionPath, ignoreTimeoutsOnVBS = ignoreTimeoutsOnVBS, thetas = theta)
          for(m in median){
            mFlag = (m=='median')
            summary = self$get_summary_selection_result_differentThetasEachAlg(selectionPath = selectionPath, ignoreTimeouts = ignoreTimeoutsOnVBS, 
                                                                               method_number = "DifferenctThetaForEachAlg", median = mFlag)
            runtime = rbind(runtime, summary[[1]])
            mcp = rbind(mcp, summary[[2]])
            par10 = rbind(par10, summary[[3]])
            success = rbind(success, summary[[4]])
            print(paste("Iteration:", i))
            print(paste(colnames(summary[[1]])[11:ncol(summary[[1]])-3],": ", summary[[1]][1,11:ncol(summary[[1]])-3]))
            print(paste("runtime:",runtime$Parallel_time[length(runtime$Parallel_time)]))
            print(paste("mcp:",mcp$Parallel_time[length(mcp$Parallel_time)]))
            print(paste("par10:",par10$Parallel_time[length(par10$Parallel_time)]))
            print(paste("success:",success$Parallel_time[length(success$Parallel_time)]))
            print(paste("orderby: ",order))
            print(paste("median: ", mFlag))
          }
        }
        i = i+1
      }
      retval = list(runtime,mcp,par10,success)
      retval = do.call(rbind, retval)
      return(retval)
    },
    
    #split by solver preds, should be completed
    split_pred_by_solver = function(predictionPath){
    }
  )
)
