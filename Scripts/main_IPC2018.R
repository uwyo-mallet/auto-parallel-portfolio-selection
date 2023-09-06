set_paths = function(){
  library(emojifont)
  library(reshape2)
  if(Sys.info()['sysname'][[1]]=="Linux"){
    if(file.exists("~/Documents/auto-parallel-portfolio-selection/Scripts/OverheadResults.R")){
      source("~/Documents/auto-parallel-portfolio-selection/Scripts/OverheadResults.R")
      predictionPath = "~/Documents/OrganizedScripts/IPC2018/preds/"
      selectionPath = "~/Documents/OrganizedScripts/IPC2018/selection/"
      finalSelectionPath = "~/Documents/OrganizedScripts/IPC2018/final/"
      modelPath = "~/Documents/mlr-scripts/IPC2018/Prediction/StandardError/"
    } else{
      source("/gscratch/hkashgar/auto-parallel-portfolio-selection/Scripts/OverheadResults.R")
      predictionPath = "/gscratch/hkashgar/OrganizedScripts/IPC2018/preds/"
      selectionPath = "/gscratch/hkashgar/OrganizedScripts/IPC2018/selection/"
      finalSelectionPath = "/gscratch/hkashgar/OrganizedScripts/IPC2018/final/"
      modelPath = "/gscratch/hkashgar/mlr-scripts/IPC2018/Prediction/StandardError/"
    }
    
  } else{
    source("C:/Users/hnyk9/Thesis/auto-parallel-portfolio-selection/Scripts/OverheadResults.R")
    predictionPath = "C:/Users/hnyk9/Thesis/OrganizedScripts/IPC2018/preds/"
    selectionPath = "C:/Users/hnyk9/Thesis/OrganizedScripts/IPC2018/selection/"
    finalSelectionPath = "C:/Users/hnyk9/Thesis/OrganizedScripts/IPC2018/final/"
    modelPath = "C:/Users/hnyk9/Thesis/mlr-scripts/Prediction/IPC2018/StandardError/"
  }
}

check_codes = function(){
  # checking the code
  # ---------------
  self = SequentialPerformance$new(benchmarks_name = "IPC2018")
  self$benchmarks_name
  self$cores
  self$cores_str
  self$Cutoff
  self$actual_CSV_path
  self$features_path
  self$n_solvers
  self$n_instances
  self$solvers
  self$actual_CSV
  self$get_scenario()
  self$get_actual_result_csv()
  self$get_par10_dataframe()
  self$par10_CSV
  self$get_mcp_dataframe(sequentialData = SequentialPerformance$new(benchmarks_name = "IPC2018"))
  self$mcp_CSV
  self$get_optimal_runtime()
  self$get_solved_instances()
  self$get_unsolved_instances()
  self$unsolvedInstances
  self$solvedInstances
  self$ignore_instances()
  self$get_VBS()
  self$get_VBS_par10()
  self$get_VBS_mcp()
  self$get_solved_instances()
  self$get_unsolved_instances()
  self$get_SBS()
  self$get_solvers_solved_runtime(self$get_SBS())
  self$get_actual_result_csv()
  #
  self$get_mcp_dataframe(sequentialData = self)
  self$ignore_instances()
  self$get_features()
  self$features
  self$get_nd_vbs_runtime(nd=2)
  # self$get_nd_VBS(nd = 4)
  # nrow(self$get_nd_VBS(nd = 4))
  # split_dataframe_by_solver should be fixed
}

training = function(){
  #---------------
  #training 
  #---------------
  
  self = SequentialPerformance$new(benchmarks_name = "IPC2018")
  self$train_randomForest_aslibLike(savepath = modelPath, ignoreTimeouts = FALSE, train_by_par10 = FALSE)
  predictions = readRDS(paste(modelPath,"./randomForest_predictions.RDS",sep=""))
  predictions$predictions
  self = PredictionResults$new("IPC2018")
  self$get_models_prediction()
}

get_top_vbs = function(saved = TRUE){
  # # top vbs 
  if(!saved){
    self = SequentialPerformance$new(benchmarks_name = "IPC2018")
    vbs = self$get_VBS()
    range = c(1:10)
    top_vbs = data.frame(matrix(nrow = nrow(vbs), ncol = 0))
    top_vbs = cbind(top_vbs, vbs$InstanceName)
    for(i in range){
      par = ParallelLevel$new(benchmarks_name = "IPC2018", cores = i)
      top_n_vbs = vector()
      for(j in 1:i){
        nd_vbs = par$get_nd_vbs_runtime(instanceset = vbs$InstanceName, ignore_instances = FALSE, nd = j)
        top_n_vbs = cbind(top_n_vbs, nd_vbs$VBS_Runtime)
      }
      nd_vbs = rowMins(top_n_vbs)
      top_vbs = cbind(top_vbs,nd_vbs)
    }
    colnames(top_vbs) = c("InstanceName", str_c(rep("cores_",10), c(1:10)))
    write.csv(top_vbs, "~/Documents/OrganizedScripts/results/IPC2018/top_vbs.csv", row.names = FALSE)
  } else{
    top_vbs = read.csv("~/Documents/OrganizedScripts/results/IPC2018/top_vbs.csv")
  }
  return(top_vbs)
}

get_top_sbs = function(saved = TRUE){
  if(!saved){
    self = SequentialPerformance$new(benchmarks_name = "IPC2018")
    vbs = self$get_VBS()
    range = c(1:10)
    top_sbs = data.frame(matrix(nrow = nrow(vbs), ncol = 0))
    top_sbs = cbind(top_sbs, vbs$InstanceName)
    for(i in range){
      solvers = colnames(self$actual_CSV[2:ncol(self$actual_CSV)])
      means = colMeans(self$actual_CSV[2:ncol(self$actual_CSV)])
      top_n_sbs = vector()
      for(j in 1:i){
        idx = which(means==min(means))
        top_n_sbs = append(top_n_sbs,solvers[idx])
        solvers = solvers[-idx]
        means = means[-idx]
      }
      top_n_sbs
      par = ParallelLevel$new(benchmarks_name = "IPC2018",i)
      nd_sbs = par$get_actual_result_csv()[top_n_sbs]
      nd_sbs = rowMins(as.matrix(nd_sbs))
      print(par$get_actual_result_csv()$InstanceName == vbs$InstanceName)
      top_sbs = cbind(top_sbs,nd_sbs)
    }
    colnames(top_sbs) = c("InstanceName", str_c(rep("cores_",10), c(1:10)))
    write.csv(top_sbs, "~/Documents/OrganizedScripts/results/IPC2018/top_sbs.csv", row.names = FALSE)
  } else{
    top_sbs = read.csv("~/Documents/OrganizedScripts/results/IPC2018/top_sbs.csv")
  }
  return(top_sbs)
}

get_top_AS_noUncertainty_noSplitting = function(saved = TRUE){
  #top AS, no uncertainty just top selected 
  #method number help:
  # -1 : running all in parallel, no selection just ordering based on prediction, (top_selection, orderBy doesn't work here)
  # 0 : algorithm selection, selection besed on predicted runtime, top_selection will choose top algorithms from data frame based on prediction
  # 1 : minpred <= pred <= [minpred + delta_prime*SE]
  # 2 : lowebound as good as min pred, [pred-delta*SE]<=minpred
  # 3 : generalized 2 and 1; p-delta*se <= minP + deltaPrime*SE_min
  # 4 : [minpred-delta_prime*SE]<=[pred-delta*SE]<=minpred
  self = PredictionResults$new("IPC2018")
  range = c(1:10)
  resR = data.frame(matrix(ncol= 13,nrow=0))
  resMCP = data.frame(matrix(ncol= 13,nrow=0))
  resPar10 = data.frame(matrix(ncol= 13,nrow=0))
  resR_m = data.frame(matrix(ncol= 13,nrow=0))
  resMCP_m = data.frame(matrix(ncol= 13,nrow=0))
  resPar10_m = data.frame(matrix(ncol= 13,nrow=0))
  if(!saved){
    for(i in range){
      selectionPath = paste("/home/haniye//Documents/OrganizedScripts/results/IPC2018/selections_algorithmSelection_noUncertainty/",i,"_cores/",sep="")
      self$selection_based_on_SE(predictionPath = self$predictionPath, 
                                 saveTo = selectionPath, 
                                 method_number = 0, 
                                 top_selection = i, 
                                 ignoreTimeoutsOnVBS = FALSE, 
                                 orderBy = "pred")
      summary = self$get_summary_selection_result(ignoreTimeouts = FALSE,
                                                  selectionPath = selectionPath,
                                                  median = FALSE, 
                                                  method_number = 0
      )
      summary_med = self$get_summary_selection_result(ignoreTimeouts = FALSE,
                                                      selectionPath = selectionPath,
                                                      median = TRUE,
                                                      method_number = 0
      )
      resR = rbind(resR,summary[[1]])
      resMCP = rbind(resMCP,summary[[2]])
      resPar10 = rbind(resPar10,summary[[3]])
      resR_m = rbind(resR_m,summary_med[[1]])
      resMCP_m = rbind(resMCP_m,summary_med[[2]])
      resPar10_m = rbind(resPar10_m,summary_med[[3]])
    }
    summary = list(resR, resMCP, resPar10, resR_m, resMCP_m, resPar10_m)
    write.arff(summary,"~/Documents/OrganizedScripts/results/IPC2018/top_as_noUncertainty.arff")
  } else{
    for(i in range){
      selectionPath = paste("/home/haniye//Documents/OrganizedScripts/results/IPC2018/selections_algorithmSelection_noUncertainty/",i,"_cores/",sep="")
      summary = self$get_summary_selection_result(ignoreTimeouts = FALSE,
                                                  selectionPath = selectionPath,
                                                  median = FALSE, 
                                                  method_number = 0
      )
      summary_med = self$get_summary_selection_result(ignoreTimeouts = FALSE,
                                                      selectionPath = selectionPath,
                                                      median = TRUE,
                                                      method_number = 0
      )
      resR = rbind(resR,summary[[1]])
      resMCP = rbind(resMCP,summary[[2]])
      resPar10 = rbind(resPar10,summary[[3]])
      resR_m = rbind(resR_m,summary_med[[1]])
      resMCP_m = rbind(resMCP_m,summary_med[[2]])
      resPar10_m = rbind(resPar10_m,summary_med[[3]])
    }
    summary = list(resR, resMCP, resPar10, resR_m, resMCP_m, resPar10_m)
  }
  return(summary)
}

get_time_splitting_prediction = function(saved = TRUE){
  # AS sequential time spliting 
  self = PredictionResults$new("IPC2018")
  range = c(1:10)
  resR = data.frame(matrix(ncol= 11,nrow=0))
  resMCP = data.frame(matrix(ncol= 11,nrow=0))
  resPar10 = data.frame(matrix(ncol= 11,nrow=0))
  resR_m = data.frame(matrix(ncol= 11,nrow=0))
  resMCP_m = data.frame(matrix(ncol= 11,nrow=0))
  resPar10_m = data.frame(matrix(ncol= 11,nrow=0))
  if(!saved){
    for(c in range){
      path_to_schedule = paste("/home/haniye/Documents/OrganizedScripts/results/IPC2018/time_splitting/",c,"_cores/",sep="")
      self$time_splitting_scheduling(predictionPath = self$predictionPath, 
                                     selectionPath = path_to_schedule, 
                                     cores = c,
                                     ignoreTimeoutsOnVBS = FALSE, 
                                     orderBy = "pred")
      summary = self$time_splitting_scheduling_scraper(selectionPath = path_to_schedule,
                                                       ignoreTimeouts = FALSE,
                                                       median = FALSE,
                                                       orderBy = "pred")
      summary_med = self$time_splitting_scheduling_scraper(selectionPath = path_to_schedule,
                                                           ignoreTimeouts = FALSE,
                                                           median = TRUE,
                                                           orderBy = "pred")
      resR = rbind(resR, summary[[1]])
      resMCP = rbind(resMCP, summary[[2]])
      resPar10 = rbind(resPar10, summary[[3]])
      resR_m = rbind(resR_m,summary_med[[1]])
      resMCP_m = rbind(resMCP_m,summary_med[[2]])
      resPar10_m = rbind(resPar10_m,summary_med[[3]])
    }
    summary = list(resR, resMCP, resPar10, resR_m, resMCP_m, resPar10_m)
  } else { 
    for(c in range){
      path_to_schedule = paste("/home/haniye/Documents/OrganizedScripts/results/IPC2018/time_splitting/",c,"_cores/",sep="")
      summary = self$time_splitting_scheduling_scraper(selectionPath = path_to_schedule,
                                                       ignoreTimeouts = FALSE,
                                                       median = FALSE,
                                                       orderBy = "pred")
      summary_med = self$time_splitting_scheduling_scraper(selectionPath = path_to_schedule,
                                                           ignoreTimeouts = FALSE,
                                                           median = TRUE,
                                                           orderBy = "pred")
      resR = rbind(resR, summary[[1]])
      resMCP = rbind(resMCP, summary[[2]])
      resPar10 = rbind(resPar10, summary[[3]])
      resR_m = rbind(resR_m,summary_med[[1]])
      resMCP_m = rbind(resMCP_m,summary_med[[2]])
      resPar10_m = rbind(resPar10_m,summary_med[[3]])
    }
    summary = list(resR, resMCP, resPar10, resR_m, resMCP_m, resPar10_m)
  }
  return(summary)
}

get_time_splitting_prediction_SE = function(saved = TRUE){
  # AS sequential time spliting 
  self = PredictionResults$new("IPC2018")
  range = c(1:10)
  resR = data.frame(matrix(ncol= 11,nrow=0))
  resMCP = data.frame(matrix(ncol= 11,nrow=0))
  resPar10 = data.frame(matrix(ncol= 11,nrow=0))
  resR_m = data.frame(matrix(ncol= 11,nrow=0))
  resMCP_m = data.frame(matrix(ncol= 11,nrow=0))
  resPar10_m = data.frame(matrix(ncol= 11,nrow=0))
  if(!saved){
    for(c in range){
      path_to_schedule = paste("/home/haniye/Documents/OrganizedScripts/results/IPC2018/time_splitting/pred+SE/",c,"_cores/",sep="")
      self$time_splitting_scheduling(predictionPath = self$predictionPath, 
                                     selectionPath = path_to_schedule, 
                                     cores = c,
                                     ignoreTimeoutsOnVBS = FALSE, 
                                     orderBy = "pred+SE")
      summary = self$time_splitting_scheduling_scraper(selectionPath = path_to_schedule,
                                                       ignoreTimeouts = FALSE,
                                                       median = FALSE,
                                                       orderBy = "pred+SE")
      summary_med = self$time_splitting_scheduling_scraper(selectionPath = path_to_schedule,
                                                           ignoreTimeouts = FALSE,
                                                           median = TRUE,
                                                           orderBy = "pred+SE")
      resR = rbind(resR, summary[[1]])
      resMCP = rbind(resMCP, summary[[2]])
      resPar10 = rbind(resPar10, summary[[3]])
      resR_m = rbind(resR_m,summary_med[[1]])
      resMCP_m = rbind(resMCP_m,summary_med[[2]])
      resPar10_m = rbind(resPar10_m,summary_med[[3]])
    }
    summary = list(resR, resMCP, resPar10, resR_m, resMCP_m, resPar10_m)
  } else { 
    for(c in range){
      path_to_schedule = paste("/home/haniye/Documents/OrganizedScripts/results/IPC2018/time_splitting/pred+SE/",c,"_cores/",sep="")
      summary = self$time_splitting_scheduling_scraper(selectionPath = path_to_schedule,
                                                       ignoreTimeouts = FALSE,
                                                       median = FALSE,
                                                       orderBy = "pred+SE")
      summary_med = self$time_splitting_scheduling_scraper(selectionPath = path_to_schedule,
                                                           ignoreTimeouts = FALSE,
                                                           median = TRUE,
                                                           orderBy = "pred+SE")
      resR = rbind(resR, summary[[1]])
      resMCP = rbind(resMCP, summary[[2]])
      resPar10 = rbind(resPar10, summary[[3]])
      resR_m = rbind(resR_m,summary_med[[1]])
      resMCP_m = rbind(resMCP_m,summary_med[[2]])
      resPar10_m = rbind(resPar10_m,summary_med[[3]])
    }
    summary = list(resR, resMCP, resPar10, resR_m, resMCP_m, resPar10_m)
  }
  return(summary)
}

get_flexfolio_3s_results = function(){
  self = PredictionResults$new("IPC2018")
  range = c(1:10)
  resR = data.frame(matrix(ncol= 6,nrow=0))
  resR_m = data.frame(matrix(ncol= 6,nrow=0))
  
  for(c in range){
    path_to_results = paste("/home/haniye/Documents/auto-parallel-portfolio-selection/Baselines/flexfolio/IPC2018/ipc2018_results/IPC2018-",
                            c,"core-3s.csv",sep="")
    csv = read.csv(path_to_results)
    csv$par10 = csv$claspfolio
    csv$claspfolio[which(csv$claspfolio == 18000)] <- 1800
    csv= csv[order(csv$Instance),]
    vbs = get_top_vbs()[1:2]
    csv$vbs = vbs$cores_1
    csv$mcp = csv$claspfolio - csv$vbs
    
    resR = rbind(resR, c(mean(csv$vbs), mean(csv$claspfolio), mean(csv$mcp), mean(csv$par10),c, "FALSE"))
    colnames(resR) <- c("vbs", "runtime", "mcp", "par10","cores", "median")    
    resR_m = rbind(resR_m, c(median(csv$vbs), median(csv$claspfolio), median(csv$mcp), median(csv$par10),c, "TRUE"))
    colnames(resR_m) <- c("vbs", "runtime", "mcp", "par10","cores", "median")
  }
  summary = list(resR, resR_m)
  return(summary)
}

get_joint_probability_optimum = function(){
  self = PredictionResults$new("IPC2018")
  range = seq(0,1,by=0.01)
  min = Inf
  optimum = Inf
  range = range[1:101]
  for(r in range){
    dir.create(paste("~/Documents/OrganizedScripts/results/IPC2018/JointProbability/tau_",r,sep = ""))
    self$selection_based_on_SE(predictionPath = self$predictionPath,
                               saveTo = paste("~/Documents/OrganizedScripts/results/IPC2018/JointProbability/tau_",r,sep=""),
                               method_number = 5,
                               top_selection = 10,
                               ignoreTimeoutsOnVBS = FALSE,
                               orderBy = "pred",
                               delta = 0,
                               delta_prime = 0,
                               alpha = 0,
                               JP_limit = r)
    summary = self$get_summary_selection_result( paste("~/Documents/OrganizedScripts/results/IPC2018/JointProbability/tau_",r,sep=""),
                                                 ignoreTimeouts = FALSE,
                                                 method_number = 5,
                                                 median = FALSE)
    print(r)
    print(summary)
    if(as.numeric(summary[[1]]$Parallel_time)<=min){
      min = as.numeric(summary[[1]]$Parallel_time)
      optimum = r
    }
  }
  return(optimum)
}

get_joint_probability_results = function(saved = TRUE, optimum = 0.59){
  self = PredictionResults$new("IPC2018")
  range = c(1:10)
  resR = data.frame(matrix(ncol= 11,nrow=0))
  resMCP = data.frame(matrix(ncol= 11,nrow=0))
  resPar10 = data.frame(matrix(ncol= 11,nrow=0))
  resR_m = data.frame(matrix(ncol= 11,nrow=0))
  resMCP_m = data.frame(matrix(ncol= 11,nrow=0))
  resPar10_m = data.frame(matrix(ncol= 11,nrow=0))
  if(!saved){
    for(i in range){
      self$selection_based_on_SE(predictionPath = self$predictionPath,
                                 saveTo = paste("~/Documents/OrganizedScripts/results/IPC2018/joint_optimal/",i, "-core",sep=""),
                                 method_number = 5,
                                 top_selection = i,
                                 ignoreTimeoutsOnVBS = FALSE,
                                 orderBy = "pred",
                                 delta = 0,
                                 delta_prime = 0,
                                 alpha = 0,
                                 JP_limit = optimum)
      summary = self$get_summary_selection_result(paste("~/Documents/OrganizedScripts/results/IPC2018/joint_optimal/",i,"-core",sep=""),
                                                  ignoreTimeouts = FALSE,
                                                  method_number = 5,
                                                  median = FALSE)
      summary_med = self$get_summary_selection_result(paste("~/Documents/OrganizedScripts/results/IPC2018/joint_optimal/",i,"-core",sep=""),
                                                      ignoreTimeouts = FALSE,
                                                      method_number = 5,
                                                      median = TRUE)
      resR = rbind(resR, summary[[1]])
      resMCP = rbind(resMCP, summary[[2]])
      resPar10 = rbind(resPar10, summary[[3]])
      resR_m = rbind(resR_m,summary_med[[1]])
      resMCP_m = rbind(resMCP_m,summary_med[[2]])
      resPar10_m = rbind(resPar10_m,summary_med[[3]])
    }
  } else{ 
    for(i in range){
      summary = self$get_summary_selection_result(paste("~/Documents/OrganizedScripts/results/IPC2018/joint_optimal/",i,"-core",sep=""),
                                                  ignoreTimeouts = FALSE,
                                                  method_number = 5,
                                                  median = FALSE)
      summary_med = self$get_summary_selection_result(paste("~/Documents/OrganizedScripts/results/IPC2018/joint_optimal/",i,"-core",sep=""),
                                                      ignoreTimeouts = FALSE,
                                                      method_number = 5,
                                                      median = TRUE)
      resR = rbind(resR, summary[[1]])
      resMCP = rbind(resMCP, summary[[2]])
      resPar10 = rbind(resPar10, summary[[3]])
      resR_m = rbind(resR_m,summary_med[[1]])
      resMCP_m = rbind(resMCP_m,summary_med[[2]])
      resPar10_m = rbind(resPar10_m,summary_med[[3]])
    }
  }
  summary = list(resR, resMCP, resPar10, resR_m, resMCP_m, resPar10_m)
  return(summary)
}

get_joint_probability_results_averageOpt = function(saved = TRUE, optimum = 0.82){
  self = PredictionResults$new("IPC2018")
  range = c(1:10)
  resR = data.frame(matrix(ncol= 11,nrow=0))
  resMCP = data.frame(matrix(ncol= 11,nrow=0))
  resPar10 = data.frame(matrix(ncol= 11,nrow=0))
  resR_m = data.frame(matrix(ncol= 11,nrow=0))
  resMCP_m = data.frame(matrix(ncol= 11,nrow=0))
  resPar10_m = data.frame(matrix(ncol= 11,nrow=0))
  if(!saved){
    for(i in range){
      self$selection_based_on_SE(predictionPath = self$predictionPath,
                                 saveTo = paste("~/Documents/OrganizedScripts/results/IPC2018/joint_optimal_avg/",i, "-core",sep=""),
                                 method_number = 5,
                                 top_selection = i,
                                 ignoreTimeoutsOnVBS = FALSE,
                                 orderBy = "pred",
                                 delta = 0,
                                 delta_prime = 0,
                                 alpha = 0,
                                 JP_limit = optimum)
      summary = self$get_summary_selection_result(paste("~/Documents/OrganizedScripts/results/IPC2018/joint_optimal_avg/",i,"-core",sep=""),
                                                  ignoreTimeouts = FALSE,
                                                  method_number = 5,
                                                  median = FALSE)
      summary_med = self$get_summary_selection_result(paste("~/Documents/OrganizedScripts/results/IPC2018/joint_optimal_avg/",i,"-core",sep=""),
                                                      ignoreTimeouts = FALSE,
                                                      method_number = 5,
                                                      median = TRUE)
      resR = rbind(resR, summary[[1]])
      resMCP = rbind(resMCP, summary[[2]])
      resPar10 = rbind(resPar10, summary[[3]])
      resR_m = rbind(resR_m,summary_med[[1]])
      resMCP_m = rbind(resMCP_m,summary_med[[2]])
      resPar10_m = rbind(resPar10_m,summary_med[[3]])
    }
  } else{ 
    for(i in range){
      summary = self$get_summary_selection_result(paste("~/Documents/OrganizedScripts/results/IPC2018/joint_optimal_avg/",i,"-core",sep=""),
                                                  ignoreTimeouts = FALSE,
                                                  method_number = 5,
                                                  median = FALSE)
      summary_med = self$get_summary_selection_result(paste("~/Documents/OrganizedScripts/results/IPC2018/joint_optimal_avg/",i,"-core",sep=""),
                                                      ignoreTimeouts = FALSE,
                                                      method_number = 5,
                                                      median = TRUE)
      resR = rbind(resR, summary[[1]])
      resMCP = rbind(resMCP, summary[[2]])
      resPar10 = rbind(resPar10, summary[[3]])
      resR_m = rbind(resR_m,summary_med[[1]])
      resMCP_m = rbind(resMCP_m,summary_med[[2]])
      resPar10_m = rbind(resPar10_m,summary_med[[3]])
    }
  }
  summary = list(resR, resMCP, resPar10, resR_m, resMCP_m, resPar10_m)
  return(summary)
}

get_optimum_tau = function(){
  
  # theta = read.csv("~/Documents/OrganizedScripts/results/IPC2018//RandomSearch_IPC2018_combined_allEqual_NOTignoreTO_300.csv")
  # theta = theta[which(theta$metric=="Runtime"),]
  # theta = theta[which(theta$median==FALSE),]
  # plot(x = theta$delta, y = theta$Parallel_time)
  # #best =  0.1116461, runtime = 110.3998 
  # theta = theta[which(theta$Parallel_time == min(theta$Parallel_time)),]
  # theta = theta$delta[1]
  # range =c(1:10)
  # theta = 0.0625
  # selectionPath = "~/Documents/OrganizedScripts/results/IPC2018/selections_optimal_theta_0.0625/selection_optimal_theta_7_cores/"
  # self = PredictionResults$new("IPC2018")
  # summary = self$get_summary_all(method_numbers = 3,top_selections = 7, predictionPath = self$predictionPath,
  # selectionPath = selectionPath, ignoreTimeoutsOnVBS = FALSE, median = FALSE,
  # delta = theta, alpha = theta, delta_prime = theta)
  # 
  # write.arff(summary,"~/Documents/OrganizedScripts/results/IPC2018/top_Uncertainty_Theta_0.1098642_limitingSolvers.arff")
  
}

plot_vbs_stats = function(save=FALSE){
  top_vbs = get_top_vbs()
  top_vbs[2:11] = apply(top_vbs[2:11],2,as.numeric)
  
  sd = apply(top_vbs[2:11],2,sd)
  mean = apply(top_vbs[2:11],2,mean)
  median = apply(top_vbs[2:11],2,median)
  sum_top_vbs = data.frame(mean = mean, median = median, sd = sd)
  sum_top_vbs$cores = c(1:10)
  sum_top_vbs = sum_top_vbs[which(!(sum_top_vbs$cores%in% c(11:19,20:29,31, 33:38))),]
  
  p<-ggplot(sum_top_vbs, aes(x=cores, y=mean,colour="Mean VBS Runtime")) +
    geom_point()+
    geom_point(aes(y=median,colour="Median VBS Runtime"))+
    geom_errorbar(aes(ymin=mean-sd,
                      ymax=mean+sd), width=.2,
                  position=position_dodge(0.05))+
    scale_y_continuous(
      name = "Runtime"
      #sec.axis = sec_axis( trans=~./self$Cutoff , name="probability of solving instance RegRF prediction")
    )
  if(save){
    ggsave(dpi = 500, width = 7, height = 5, filename = "VBS_behavior_different_cores_runtime.pdf")
  }
  return(p)
}

plot_sbs_stats = function(save=FALSE){
  top_sbs = get_top_sbs()
  top_sbs[2:11] = apply(top_sbs[2:11],2,as.numeric)
  
  sd = apply(top_sbs[2:11],2,sd)
  mean = apply(top_sbs[2:11],2,mean)
  median = apply(top_sbs[2:11],2,median)
  sum_top_sbs = data.frame(mean = mean, median = median, sd = sd)
  sum_top_sbs$cores = c(1:10)
  sum_top_sbs = sum_top_sbs[which(!(sum_top_sbs$cores%in% c(11:19,20:29,31, 33:38))),]
  
  p<-ggplot(sum_top_sbs, aes(x=cores, y=mean,colour="Mean SBS Runtime")) +
    geom_point()+
    geom_point(aes(y=median,colour="Median SBS Runtime"))+
    geom_errorbar(aes(ymin=mean-sd,
                      ymax=mean+sd), width=.2,
                  position=position_dodge(0.05))+
    scale_y_continuous(
      name = "Runtime"
      #sec.axis = sec_axis( trans=~./self$Cutoff , name="probability of solving instance RegRF prediction")
    )
  if(save){
    ggsave(filename = "SBS_behavior_different_cores_runtime.pdf",dpi = 500, width = 7, height = 5)
  }
  return(p)
}

plot_all_results = function(save = FALSE, optimum = 0.59, metric = "Runtime"){
  results = scrape_all_results()
  results[2:11] <- lapply(results[2:11],as.numeric)
  optimum = 0.852
  if(metric == "Runtime"){
    p <- ggplot(results, aes(x=cores, y=Runtime, colour = Approach, shape = Approach)) +
      geom_point(size = 3)+
      geom_line(size = 1)+
      # geom_line(aes(linetype="Mean"), size = 1)+
      # geom_point(aes(y=Median),size = 3)+
      # geom_line(aes(y = Median, linetype = "Median"), size = 1)+
      guides(linetype=guide_legend(title="",keywidth = 3, keyheight = 1.5),
             colour = guide_legend(keywidth = 3, keyheight = 1.5))+
      expand_limits(x = 1, y = 0)+ theme(text=element_text(size=22,  family="Times"))+
      labs(x = "Cores", y = "Runtime (s)", title = "IPC2018-MAIN")+theme(plot.title = element_text(hjust = 0.5))+
      scale_x_continuous(breaks=c(1:10))+
      scale_color_discrete(labels=c(bquote(AS[1]), 'Single Best Solver',
                                    "Timesplitting_preds", "Timesplitting_preds+SE",
                                    bquote(AS[~p[~'\u2229']]), 'Virtual Best Solver'))+
      scale_shape_discrete(labels=c(bquote(AS[1]), 'Single Best Solver',
                                    "Timesplitting_preds", "Timesplitting_preds+SE",
                                    bquote(AS[~p[~'\u2229']]), 'Virtual Best Solver'))+
      scale_y_continuous(trans='log10')
    if(save){
      ggsave(dpi = 500, width = 9, height = 5, filename = "IPC2018_line_chart_parallel_runtime.pdf")
    }
  } else if(metric == "MCP"){
    p <- ggplot(results, aes(x=cores, y=MCP, colour = Approach, shape = Approach)) +
      geom_point(size = 3)+
      geom_line(size = 1)+
      # geom_line(aes(linetype="Mean"), size = 1)+
      # geom_point(aes(y=Median),size = 3)+
      # geom_line(aes(y = Median, linetype = "Median"), size = 1)+
      guides(linetype=guide_legend(title="",keywidth = 3, keyheight = 1.5),
             colour = guide_legend(keywidth = 3, keyheight = 1.5))+
      expand_limits(x = 1, y = 0)+ theme(text=element_text(size=22,  family="Times"))+
      labs(x = "Cores", y = "MCP", title = "IPC2018-MAIN")+theme(plot.title = element_text(hjust = 0.5))+
      scale_x_continuous(breaks=c(1:10))+
      scale_color_discrete(labels=c(bquote(AS[1]), 'Single Best Solver',
                                    "Timesplitting_preds", "Timesplitting_preds+SE",
                                    bquote(AS[~p[~'\u2229']]), 'Virtual Best Solver'))+
      scale_shape_discrete(labels=c(bquote(AS[1]), 'Single Best Solver',
                                    "Timesplitting_preds", "Timesplitting_preds+SE",
                                    bquote(AS[~p[~'\u2229']]), 'Virtual Best Solver'))+
      
      scale_y_continuous(trans='log10')
    if(save){
      ggsave(dpi = 500, width = 9, height = 5, filename = "IPC2018_line_chart_parallel_MCP.pdf")
    }
  } else if(metric == "PAR10"){
    p <- ggplot(results, aes(x=cores, y=PAR10, colour = Approach, shape = Approach)) +
      geom_point(size = 3)+
      geom_line(size = 1)+
      # geom_line(aes(linetype="Mean"), size = 1)+
      # geom_point(aes(y=Median),size = 3)+
      # geom_line(aes(y = Median, linetype = "Median"), size = 1)+
      guides(linetype=guide_legend(title="",keywidth = 3, keyheight = 1.5),
             colour = guide_legend(keywidth = 3, keyheight = 1.5))+
      expand_limits(x = 1, y = 0)+ theme(text=element_text(size=22,  family="Times"))+
      labs(x = "Cores", y = "PAR10", title = "IPC2018-MAIN")+theme(plot.title = element_text(hjust = 0.5))+
      scale_x_continuous(breaks=c(1:10))+
      scale_color_discrete(labels=c(bquote(AS[1]), 'Single Best Solver',
                                    "Timesplitting_preds", "Timesplitting_preds+SE",
                                    bquote(AS[~p[~'\u2229']]), 'Virtual Best Solver'))+
      scale_shape_discrete(labels=c(bquote(AS[1]), 'Single Best Solver',
                                    "Timesplitting_preds", "Timesplitting_preds+SE",
                                    bquote(AS[~p[~'\u2229']]), 'Virtual Best Solver'))+
      scale_y_continuous(trans='log10')
    if(save){
      ggsave(dpi = 500, width = 9, height = 5, filename = "IPC2018_line_chart_parallel_PAR10.pdf")
    }
  }
  return(p)
}

plot_all_results_normalized_gap = function(save = FALSE, optimum = 0.59){
  #vbs is 1
  #sbs is 0
  #sbs-value/sbs-vbs
  results = scrape_all_results()
  results[2:9] <- lapply(results[2:9],as.numeric)
  results = results[c(1,2,5,8)]
  par10_sbs = get_top_sbs()$cores_1
  par10_sbs[which(par10_sbs==1800)] <- 18000
  par10_sbs = mean(par10_sbs)
  par10_vbs = get_top_vbs()$cores_1
  par10_vbs[which(par10_vbs==1800)] <- 18000
  par10_vbs = mean(par10_vbs)
  results$PAR10= (par10_sbs - results$PAR10)/(par10_sbs - par10_vbs)
  results$PAR10 = as.numeric(results$PAR10)
  
  p = ggplot(results, aes(x=cores, y=PAR10, colour = Approach, shape = Approach)) +
    geom_point(size = 3)+
    geom_line(size = 1)+
    # geom_line(aes(linetype="Mean"), size = 1)+
    # geom_point(aes(y=Median),size = 3)+
    # geom_line(aes(y = Median, linetype = "Median"), size = 1)+
    guides(linetype=guide_legend(title="",keywidth = 3, keyheight = 1.5), 
           colour = guide_legend(keywidth = 3, keyheight = 1.5))+
    expand_limits(x = 1, y = 0)+ theme(text=element_text(size=22,  family="Times"))+
    labs(x = "Processors", y = "Normalized Gap Closed", title = "IPC2018")+
    theme(plot.title = element_text(hjust = 0.5))+
    scale_x_continuous(breaks=c(1:10))+
    scale_color_discrete(labels=c("3S",bquote(AS[1]), 'SBS',"Time Splitting",
                                  bquote(AS[~p[~'\u2229']]), 'VBS'))+
    scale_shape_discrete(labels=c("3S",bquote(AS[1]), 'SBS',"Time Splitting",
                                  bquote(AS[~p[~'\u2229']]), 'VBS'))
  if(save){
    ggsave(dpi = 500, width = 9, height = 5, filename = "IPC18_line_chart_parallel_NormalizedGap.pdf")  
  }
  return(p)
}

scrape_all_results = function(){
  df_results = data.frame(matrix(nrow = 0, ncol = 9))
  
  top_vbs = get_top_vbs()
  for(c in colnames(top_vbs)[2:ncol(top_vbs)]){
    top_vbs[c][[1]] <- as.numeric(unlist(top_vbs[c][[1]]))
    if(c == "cores_1"){
      par10 = top_vbs$cores_1
      par10[which(par10==1800)] <- 18000
      row = c("VBS", 1, mean(top_vbs$cores_1), 0, mean(par10), median(top_vbs$cores_1), 0, median(par10),"Sequential VBS, Oracle")
      df_results= rbind(df_results,row)
      colnames(df_results) = c("Approach", "cores", "Runtime", "MCP", "PAR10", "median_Runtime", "median_MCP", "median_PAR10","decription")
    } else{
      runtime = top_vbs[c][[1]]
      par10 = runtime
      par10[which(par10==1800)] = 18000
      mcp = runtime - top_vbs$cores_1
      row = c("VBS", str_split(c,"cores_")[[1]][2], 
              mean(runtime), mean(mcp), mean(par10),
              median(runtime), median(mcp), median(par10),
              paste("Parallel VBS,",c))
      df_results= rbind(df_results,row)
    }
  }
  
  top_sbs = get_top_sbs()
  for(c in colnames(top_sbs)[2:ncol(top_sbs)]){
    top_sbs[c][[1]] <- as.numeric(unlist(top_sbs[c][[1]]))
    if(c == "cores_1"){
      
      runtime = top_sbs[c][[1]]
      par10 = top_sbs$cores_1
      par10[which(par10==1800)] <- 18000
      mcp = runtime - top_vbs$cores_1
      row = c("SBS", 1, mean(top_sbs$cores_1), mean(mcp), mean(par10), median(top_sbs$cores_1), median(mcp),median(par10),"Sequential SBS")
      df_results= rbind(df_results,row)
      colnames(df_results) = c("Approach", "cores", "Runtime", "MCP", "PAR10", "median_Runtime", "median_MCP", "median_PAR10","decription")
    } else{
      runtime = top_sbs[c][[1]]
      par10 = runtime
      par10[which(par10==1800)] = 18000
      mcp = runtime - top_vbs$cores_1
      row = c("SBS", str_split(c,"cores_")[[1]][2], 
              mean(runtime), mean(mcp), mean(par10), 
              median(runtime), median(mcp), median(par10), 
              paste("Parallel SBS,",c))
      df_results= rbind(df_results,row)
    }
  }
  
  top_as = get_top_AS_noUncertainty_noSplitting()
  for(c in 1:nrow(top_as[[1]])){
    if(c == 1){
      row = c("AS", 1, top_as[[1]][1,]$Parallel_time, top_as[[2]][1,]$Parallel_time, top_as[[3]][1,]$Parallel_time, top_as[[4]][1,]$Parallel_time, top_as[[5]][1,]$Parallel_time, top_as[[6]][1,]$Parallel_time,"Single Algorithm Selection")
      df_results= rbind(df_results,row)
    } else{ 
      row = c("AS", c, top_as[[1]][c,]$Parallel_time, top_as[[2]][c,]$Parallel_time, top_as[[3]][c,]$Parallel_time,top_as[[4]][c,]$Parallel_time, top_as[[5]][c,]$Parallel_time, top_as[[6]][c,]$Parallel_time, "Algorithm Selection - Top, based on prediction, no uncertainty or time splitting")
      df_results= rbind(df_results,row)
    }
  }
  
  # time_splitting_pred = get_time_splitting_prediction()
  # for(c in 1:nrow(time_splitting_pred[[1]])){
  #   if(c == 1){
  #     row = c("Time Splitting - Prediction", 1, time_splitting_pred[[1]][1,]$Schedule_time, time_splitting_pred[[2]][1,]$Schedule_time, time_splitting_pred[[3]][1,]$Schedule_time,
  #             time_splitting_pred[[4]][1,]$Schedule_time, time_splitting_pred[[5]][1,]$Schedule_time, time_splitting_pred[[6]][1,]$Schedule_time, "Sequential Timesplitting based on Predictions")
  #     df_results= rbind(df_results,row)
  #   } else{
  #     row = c("Time Splitting - Prediction", c, time_splitting_pred[[1]][c,]$Schedule_time, time_splitting_pred[[2]][c,]$Schedule_time, time_splitting_pred[[3]][c,]$Schedule_time,
  #             time_splitting_pred[[4]][c,]$Schedule_time, time_splitting_pred[[5]][c,]$Schedule_time, time_splitting_pred[[6]][c,]$Schedule_time, "Parallel Timesplitting based on Predictions - Grid bin packing")
  #     df_results= rbind(df_results,row)
  #   }
  # }
  time_splitting_predSE = get_time_splitting_prediction_SE()
  for(c in 1:nrow(time_splitting_predSE[[1]])){
    if(c == 1){
      row = c("Time Splitting - Prediction+SE", 1, time_splitting_predSE[[1]][1,]$Schedule_time, time_splitting_predSE[[2]][1,]$Schedule_time, time_splitting_predSE[[3]][1,]$Schedule_time,
              time_splitting_predSE[[4]][1,]$Schedule_time, time_splitting_predSE[[5]][1,]$Schedule_time, time_splitting_predSE[[6]][1,]$Schedule_time,"Sequential Timesplitting based on Predictions+SE")
      df_results= rbind(df_results,row)
    } else{
      row = c("Time Splitting - Prediction+SE", c, time_splitting_predSE[[1]][c,]$Schedule_time, time_splitting_predSE[[2]][c,]$Schedule_time, time_splitting_predSE[[3]][c,]$Schedule_time,
              time_splitting_predSE[[4]][c,]$Schedule_time, time_splitting_predSE[[5]][c,]$Schedule_time, time_splitting_predSE[[6]][c,]$Schedule_time, "Parallel Timesplitting based on Predictions+SE - Grid bin packing")
      df_results= rbind(df_results,row)
    }
  }
  
  # time_splitting_predSE = get_time_splitting_prediction_aSE(a = 2)
  # for(c in 1:nrow(time_splitting_predSE[[1]])){
  #   if(c == 1){
  #     row = c("Time Splitting - Prediction+2SE", 1, time_splitting_predSE[[1]][1,]$Schedule_time, time_splitting_predSE[[2]][1,]$Schedule_time, time_splitting_predSE[[3]][1,]$Schedule_time,
  #             time_splitting_predSE[[4]][1,]$Schedule_time, time_splitting_predSE[[5]][1,]$Schedule_time, time_splitting_predSE[[6]][1,]$Schedule_time,"Sequential Timesplitting based on Predictions+SE")
  #     df_results= rbind(df_results,row)
  #   } else{
  #     row = c("Time Splitting - Prediction+2SE", c, time_splitting_predSE[[1]][c,]$Schedule_time, time_splitting_predSE[[2]][c,]$Schedule_time, time_splitting_predSE[[3]][c,]$Schedule_time,
  #             time_splitting_predSE[[4]][c,]$Schedule_time, time_splitting_predSE[[5]][c,]$Schedule_time, time_splitting_predSE[[6]][c,]$Schedule_time, "Parallel Timesplitting based on Predictions+SE - Grid bin packing")
  #     df_results= rbind(df_results,row)
  #   }
  # }
  # optimum = get_joint_probability_optimum()
  optimum = 0.332
  JoinProbabilityResults = get_joint_probability_results(optimum)
  for(c in 1:nrow(JoinProbabilityResults[[1]])){
    if(c == 1){
      row = c("Uncertainty - JointProbability", 1, JoinProbabilityResults[[1]][1,]$Parallel_time, JoinProbabilityResults[[2]][1,]$Parallel_time, JoinProbabilityResults[[3]][1,]$Parallel_time, 
              JoinProbabilityResults[[4]][1,]$Parallel_time, JoinProbabilityResults[[5]][1,]$Parallel_time, JoinProbabilityResults[[6]][1,]$Parallel_time,"Uncertainty - JointProbability - optimum = 0.549")
      df_results= rbind(df_results,row)
    } else{ 
      row = c("Uncertainty - JointProbability", c, JoinProbabilityResults[[1]][c,]$Parallel_time, JoinProbabilityResults[[2]][c,]$Parallel_time, JoinProbabilityResults[[3]][c,]$Parallel_time, 
              JoinProbabilityResults[[4]][c,]$Parallel_time, JoinProbabilityResults[[5]][c,]$Parallel_time, JoinProbabilityResults[[6]][c,]$Parallel_time, "Uncertainty - JointProbability - optimum = 0.549")
      df_results= rbind(df_results,row)
    }
  }
  
  flexfolio_3s = get_flexfolio_3s_results()
  for(c in 1:nrow(flexfolio_3s[[1]])){
    if(c == 1){
      row = c("3S", 1, flexfolio_3s[[1]][1,]$runtime, flexfolio_3s[[1]][1,]$mcp, flexfolio_3s[[1]][1,]$par10, 
              flexfolio_3s[[2]][1,]$runtime, flexfolio_3s[[2]][1,]$mcp, flexfolio_3s[[2]][1,]$par10,"Flexfolio implemantation of 3S, using sequential scenarios")
      df_results= rbind(df_results,row)
    } else{ 
      row = c("3S", c, flexfolio_3s[[1]][c,]$runtime, flexfolio_3s[[1]][c,]$mcp, flexfolio_3s[[1]][c,]$par10, 
              flexfolio_3s[[2]][c,]$runtime, flexfolio_3s[[2]][c,]$mcp, flexfolio_3s[[2]][c,]$par10,"Flexfolio implemantation of 3S, using parallel scenarios")
      df_results= rbind(df_results,row)
    }
  }
  return(df_results)
}

set_paths()
# check_codes()
# training()

plot_vbs_stats(save = FALSE)
plot_sbs_stats(save = FALSE)

results = scrape_all_results()
results$scenario = "IPC2018"
setwd("~/Documents/OrganizedScripts/results/")
write.csv(results,'summary_results_all_IPC2018.csv',row.names = FALSE)

results[which(results$cores == 10),]
p = plot_all_results_normalized_gap()
p 

ggsave(dpi = 500, width = 9, height = 5, filename = "IPC18_line_chart_parallel_NormalizedGap.pdf")  

p = plot_all_results(metric = "Runtime")
p
ggsave(dpi = 500, width = 9, height = 5, filename = "summary_results_all_runtime.pdf")  

s = plot_all_results(metric = "MCP")
s
ggsave(dpi = 500, width = 9, height = 5, filename = "summary_results_all_MCP.pdf") 
o = plot_all_results(metric = "PAR10")
o

ggsave(dpi = 500, width = 9, height = 5, filename = "summary_results_all_PAR10.pdf") 




