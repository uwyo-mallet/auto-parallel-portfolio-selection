if(Sys.info()['sysname']=="Linux"){
  if(file.exists("~/Documents/auto-parallel-portfolio-selection/Scripts/OverheadResults.R")){
    source("~/Documents/auto-parallel-portfolio-selection/Scripts/OverheadResults.R")
    Estimate_overhead_on_predictionPath ="~/Documents/OrganizedScripts/MAXSAT2019/Estimate_overhead_on_prediction/"
    actual_overhead_per_solverPlotPath = "~/Documents/OrganizedScripts/MAXSAT2019/actual_overhead_per_solver_perc/plot/"
    actual_overhead_per_solverPath = "~/Documents/OrganizedScripts/MAXSAT2019/actual_overhead_per_solver_perc/"
    actual_overhead_per_corePlotPath = "~/Documents/OrganizedScripts/MAXSAT2019/actual_overhead_per_core_perc/plot/"
    actual_overhead_per_corePath = "~/Documents/OrganizedScripts/MAXSAT2019/actual_overhead_per_core_perc/"
    predictionPath = "~/Documents/OrganizedScripts/MAXSAT2019/preds/"
    selectionPath = "~/Documents/OrganizedScripts/MAXSAT2019/selection/"
    finalSelectionPath = "~/Documents/OrganizedScripts/MAXSAT2019/final/"
    modelPath = "~/Documents/mlr-scripts/MAXSAT2019/Prediction/StandardError/"
    CVsetsPath = "~/Documents/OrganizedScripts/MAXSAT2019/model_cv_all_sets/"
    mcp_results_path = "~/Documents/OrganizedScripts/MAXSAT2019/"
    train_randomForest_validation_setPath = "~/Documents/mlr-scripts/MAXSAT2019/Prediction/StandardError_validation/"
    #preds_path = "~/Documents/OrganizedScripts/MAXSAT2019/preds_valid/"
    #preds_path_valid = "~/Documents/OrganizedScripts/MAXSAT2019/preds_valid/validation/"
    selection_valid_path = "~/Documents/OrganizedScripts/MAXSAT2019/preds_valid/validation/selection/"
    selection_valid_exptected_path = "~/Documents/OrganizedScripts/MAXSAT2019/preds_valid/validation/selectionExpected/"
    expected_pred_path =  "~/Documents/OrganizedScripts/MAXSAT2019/preds_valid/validation/expectedValues/"
    actual_overhead_per_solverPath = "~/Documents/OrganizedScripts/MAXSAT2019/actual_overhead_per_solver_perc"
  } else{
    source("/gscratch/hkashgar/auto-parallel-portfolio-selection/Scripts/OverheadResults.R")
    Estimate_overhead_on_predictionPath ="/gscratch/hkashgar/OrganizedScripts/MAXSAT2019/Estimate_overhead_on_prediction/"
    actual_overhead_per_solverPlotPath = "/gscratch/hkashgar/OrganizedScripts/MAXSAT2019/actual_overhead_per_solver_perc/plot/"
    actual_overhead_per_solverPath = "/gscratch/hkashgar/OrganizedScripts/MAXSAT2019/actual_overhead_per_solver_perc/"
    actual_overhead_per_corePlotPath = "/gscratch/hkashgar/OrganizedScripts/MAXSAT2019/actual_overhead_per_core_perc/plot/"
    actual_overhead_per_corePath = "/gscratch/hkashgar/OrganizedScripts/MAXSAT2019/actual_overhead_per_core_perc/"
    predictionPath = "/gscratch/hkashgar/OrganizedScripts/MAXSAT2019/preds/"
    selectionPath = "/gscratch/hkashgar/OrganizedScripts/MAXSAT2019/selection/"
    finalSelectionPath = "/gscratch/hkashgar/OrganizedScripts/MAXSAT2019/final/"
    modelPath = "/gscratch/hkashgar/mlr-scripts/MAXSAT2019/Prediction/StandardError/"
    CVsetsPath = "/gscratch/hkashgar/OrganizedScripts/MAXSAT2019/model_cv_all_sets/"
    mcp_results_path = "/gscratch/hkashgar/OrganizedScripts/MAXSAT2019/"
    train_randomForest_validation_setPath = "/gscratch/hkashgar/mlr-scripts/MAXSAT2019/Prediction/StandardError_validation/"
    #preds_path = "/gscratch/hkashgar/OrganizedScripts/MAXSAT2019/preds_valid/"
    #preds_path_valid = "/gscratch/hkashgar/OrganizedScripts/MAXSAT2019/preds_valid/validation/"
    selection_valid_path = "/gscratch/hkashgar/OrganizedScripts/MAXSAT2019/preds_valid/validation/selection/"
    selection_valid_exptected_path = "/gscratch/hkashgar/OrganizedScripts/MAXSAT2019/preds_valid/validation/selectionExpected/"
    expected_pred_path =  "/gscratch/hkashgar/OrganizedScripts/MAXSAT2019/preds_valid/validation/expectedValues/"
    actual_overhead_per_solverPath = "/gscratch/hkashgar/OrganizedScripts/MAXSAT2019/actual_overhead_per_solver_perc"
  }
  
} else{
  source("C:/Users/hnyk9/OneDrive - University of Wyoming/auto-parallel-portfolio-selection/Scripts/OverheadResults.R")
  Estimate_overhead_on_predictionPath ="C:/Users/hnyk9/OneDrive - University of Wyoming/OrganizedScripts/MAXSAT2019/Estimate_overhead_on_prediction/"
  actual_overhead_per_solverPlotPath = "C:/Users/hnyk9/OneDrive - University of Wyoming/OrganizedScripts/MAXSAT2019/actual_overhead_per_solver_perc/plot/"
  actual_overhead_per_solverPath = "C:/Users/hnyk9/OneDrive - University of Wyoming/OrganizedScripts/MAXSAT2019/actual_overhead_per_solver_perc/"
  actual_overhead_per_corePlotPath = "C:/Users/hnyk9/OneDrive - University of Wyoming/OrganizedScripts/MAXSAT2019/actual_overhead_per_core_perc/plot/"
  actual_overhead_per_corePath = "C:/Users/hnyk9/OneDrive - University of Wyoming/OrganizedScripts/MAXSAT2019/actual_overhead_per_core_perc/"
  #predictionPath = "C:/Users/hnyk9/OneDrive - University of Wyoming/OrganizedScripts/MAXSAT2019/preds/"
  selectionPath = "C:/Users/hnyk9/OneDrive - University of Wyoming/OrganizedScripts/MAXSAT2019/selection/"
  finalSelectionPath = "C:/Users/hnyk9/OneDrive - University of Wyoming/OrganizedScripts/MAXSAT2019/final/"
  #modelPath = "C:/Users/hnyk9/OneDrive - University of Wyoming/mlr-scripts/Prediction/MAXSAT2019/StandardError/"
  CVsetsPath = "C:/Users/hnyk9/OneDrive - University of Wyoming/OrganizedScripts/MAXSAT2019/model_cv_all_sets/"
  mcp_results_path = "C:/Users/hnyk9/OneDrive - University of Wyoming/OrganizedScripts/MAXSAT2019/"
  train_randomForest_validation_setPath = "C:/Users/hnyk9/OneDrive - University of Wyoming/mlr-scripts/MAXSAT2019/Prediction/StandardError_validation/"
  #preds_path = "C:/Users/hnyk9/OneDrive - University of Wyoming/Documents/OrganizedScripts/MAXSAT2019/preds_valid/"
  #preds_path_valid = "C:/Users/hnyk9/OneDrive - University of Wyoming/Documents/OrganizedScripts/MAXSAT2019/preds_valid/validation/"
  selection_valid_path = "C:/Users/hnyk9/OneDrive - University of Wyoming/Documents/OrganizedScripts/MAXSAT2019/preds_valid/validation/selection/"
  selection_valid_exptected_path = "C:/Users/hnyk9/OneDrive - University of Wyoming/Documents/OrganizedScripts/MAXSAT2019/preds_valid/validation/selectionExpected/"
  expected_pred_path =  "C:/Users/hnyk9/OneDrive - University of Wyoming/Documents/OrganizedScripts/MAXSAT2019/preds_valid/validation/expectedValues/"
  actual_overhead_per_solverPath = "C:/Users/hnyk9/OneDrive - University of Wyoming/Documents/OrganizedScripts/MAXSAT2019/actual_overhead_per_solver_perc"
}


optimum = 0.549
self = PredictionResults$new("MAXSAT2019")
selectionPath = "/home/haniye/Documents/OrganizedScripts/results/MAXSAT2019/time_splitting/"
summary = self$selection_based_on_SE(saveTo = selectionPath,
                                     predictionPath = self$predictionPath,
                                     top_selection = 7, 
                                     ignoreTimeoutsOnVBS = FALSE,
                                     method_number = 5,
                                     JP_limit = optimum,
                                     orderBy = "pred",
                                     getCores = TRUE)
summary$selectedCores = as.numeric(summary$selectedCores)

N_bin = 5
binPack_fixedBinNumber <- function(d, N_bin, weight_pos=NULL, key=NULL, lower_bound=NULL, upper_bound=NULL){
  isdict <- is.list(d) && !is.null(names(d))
  if(!is.vector(d) && !isdict && ncol(d) > 1){
    if(!is.null(weight_pos)){
      key <- function(x) x[weight_pos]
    }
    if(is.null(key)){
      stop("Must provide weight_pos or key for tuple list")
    }
  }
  if(!isdict && !is.null(key)){
    new_dict <- setNames(d, seq_along(d))
    d <- sapply(d, key)
    isdict <- TRUE
    is_tuple_list <- TRUE
  } else{
    is_tuple_list <- FALSE
  }
  if(isdict){
    # get keys and values (weights)
    keys_vals <- d
    keys <- names(keys_vals)
    vals <- unname(keys_vals)
    # sort weights decreasingly
    ndcs <- order(vals, decreasing=TRUE)
    weights <- vals[ndcs]
    keys <- keys[ndcs]
    bins <- vector(mode = "list", length = N_bin)
    for(i in seq_len(N_bin)){
      bins[[i]] <- list()
    }
  } else{
    weights <- sort(d, decreasing=TRUE)
    bins <- vector(mode = "list", length = N_bin)
    for(i in seq_len(N_bin)){
      bins[[i]] <- vector(mode = "list")
    }
  }
  # find the valid indices
  if(!is.null(lower_bound) && !is.null(upper_bound) && lower_bound < upper_bound){
    valid_ndcs <- which(weights > lower_bound & weights < upper_bound)
  } else if(!is.null(lower_bound)){
    valid_ndcs <- which(weights > lower_bound)
  } else if(!is.null(upper_bound)){
    valid_ndcs <- which(weights < upper_bound)
  } else if(is.null(lower_bound) && is.null(upper_bound)){
    valid_ndcs <- seq_along(weights)
  } else if(lower_bound >= upper_bound){
    stop("lower_bound is greater or equal to upper_bound")
  }
  weights <- weights[valid_ndcs]
  if(isdict){
    keys <- keys[valid_ndcs]
  }
  # the total volume is the sum of all weights
  V_total <- sum(weights)
  # the first estimate of the maximum bin volume is
  # the total volume divided to all bins
  V_bin_max <- V_total / N_bin
  # prepare array containing the current weight of the bins
  weight_sum <- rep(0, N_bin)
  for (item in seq_along(weights)) {
    weight = weights[item]
    if (isdict) {
      key = keys[item]
    }
    b = which.min(weight_sum)
    new_weight_sum = weight_sum[b] + weight
    found_bin = FALSE
    while (!found_bin) {
      if (new_weight_sum <= V_bin_max) {
        if (isdict) {
          bins[[b]][[key]] = weight
        } else {
          bins[[b]] = c(bins[[b]], weight)
        }
        weight_sum[b] = new_weight_sum
        found_bin = TRUE
      } else {
        V_bin_max = V_bin_max + sum(weights[item:length(weights)]) / N_bin
      }
    }
  }
  if (!is_tuple_list) {
    for(i in 1:length(bins)){
      bins[i][[1]] = rev(bins[i][[1]])
    }
    return(bins)
  } else {
    new_bins = list()
    for (b in seq_len(N_bin)) {
      new_bins[[b]] = list()
      for (key in names(bins[[b]])) {
        new_bins[[b]] = c(new_bins[[b]], new_dict[[key]])
      }
      for(i in 1:length(new_bins)){
        new_bins[i][[1]] = rev(new_bins[i][[1]])
      }
    }
    return(new_bins)
  }
}

for(i in 1:nrow(summary)){
  instance = summary[i,]$instances
  preds = read.csv(paste(self$predictionPath,instance,".csv",sep=""))
  selection = read.csv(paste(selectionPath,instance,".csv",sep=""))
  cores = summary[i,]$selectedCores
  binsPacked = binPack_fixedBinNumber(preds$PredictedRuntime,cores, upper_bound = self$sequentialData$Cutoff)
  for(b in 1:length(binsPacked)){
    if(length(binsPacked[[b]])==0){
      print(i)
      binsPacked[[b]] = append(binsPacked[[b]],self$sequentialData$Cutoff)
    }
  }
  core = rep(0,nrow(preds))
  order = rep(0,nrow(preds))
  for(c in 1:length(binsPacked)){
    core[which(preds$PredictedRuntime %in% unlist(binsPacked[[c]]))] <- c
    order[which(preds$PredictedRuntime %in% unlist(binsPacked[[c]]))] <- c(1:length(which(preds$PredictedRuntime %in% unlist(binsPacked[[c]]))))
  }
  data = preds[1:5]
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
  data$delta = rep(0, times = nrow(data))
  data$delta_prime = rep(0, times = nrow(data))
  data$alpha = rep(x = 0, times = nrow(data))
  data$JP_limit = rep(x = optimum, times = nrow(data))
  data$method_number = 5
  data$orderBy = 'pred'
  data$core = core
  data$order = order
  
  data$time_split_Runtime = NA
  for(c in 1:cores){
    df = data[which(data$core == c),]
    solved = FALSE
    for(o in 1:max(df$order)){
      if(!solved){
        if(df[which(df$order == o),]$ParallelRuntime <df[which(df$order == o),]$PredictedRuntime){
          solved = TRUE
          sum = sum(df[which(df$order %in% c(1:o)),]$ParallelRuntime)
          data[which(data$core == c & data$order == o),]$time_split_Runtime = sum
        }
      }
    }
  }
  write.csv(data,paste(saveTo,"/",instance,".csv",sep=""),row.names = FALSE)
}

ignoreTimeouts = FALSE
median = FALSE
method_number = 5
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
  min_parallel_min = min(csv$time_split_Runtime, na.rm = TRUE)
  if(is.infinite(min_parallel_min)){
    min_parallel_min = self$sequentialData$Cutoff
  }
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
