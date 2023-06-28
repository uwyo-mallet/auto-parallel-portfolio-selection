if(Sys.info()['sysname']=="Linux"){
  if(file.exists("/home/haniye/Documents/OrganizedScripts/Tools.R")){
    source("/home/haniye/Documents/OrganizedScripts/Tools.R") 
  }
  else{ 
    source("/gscratch/hkashgar/OrganizedScripts/Tools.R") 
  }
} else{
  source("C:/Users/hnyk9/Thesis/OrganizedScripts/Tools.R")
}

library(stringr)

ParallelLevel <- R6Class(
  classname = "ParallelLevel",
  inherit = Tools,
  public = list(
    cores = NULL,
    cores_str = NULL,
    actual_CSV_path = NULL,
    actual_CSV = NULL,
    par10_CSV = NULL,
    mcp_CSV = NULL,
    n_solvers = NULL,
    n_instances = NULL,
    benchmarks_name = "SAT2018",
    cluster = FALSE, 
    solvers = NULL,
    Cutoff = NULL,
    #constructor
    initialize = function(cores, benchmarks_name = "SAT2018", cluster = FALSE){
      #set cores
      self$cores = cores
      if(cores %in% c(10:14)){
        self$cores = 10
      } else if(cores %in% c(15:24)){
        self$cores = 20
      } else if(cores %in% c(25:31)){
        self$cores = 30
      } else if(cores %in% c(32:39)){
        self$cores = 32
      }
      self$benchmarks_name = benchmarks_name
      self$cluster = cluster
      #set cores_string
      if(benchmarks_name == "SAT2018"){
        if(self$cores == 1) {
          self$cores_str = "-solo" 
        } else { 
          self$cores_str = paste("-",self$cores,"-parallel",sep = "")
        }
        #set scenario path 
        if(Sys.info()['sysname']!="Linux"){
          self$actual_CSV_path = paste("C:/Users/hnyk9/Thesis/PortfolioScheduling/ExperimentResults/csvs/SAT18/teton-SAT2018-37-solvers",self$cores_str,".csv",sep = "")
        } else{
          self$actual_CSV_path = paste("/home/haniye/Documents/PortfolioScheduling/ExperimentResults/csvs/SAT18/teton-SAT2018-37-solvers",self$cores_str,".csv",sep = "")
          if(cluster){
            self$actual_CSV_path = paste("/gscratch/hkashgar/PortfolioScheduling/ExperimentResults/csvs/SAT18/teton-SAT2018-37-solvers",self$cores_str,".csv",sep = "")
          }
        }
        self$Cutoff = 5000
        
      } else if(benchmarks_name == "SAT2016"){
        if(self$cores  == 1) {
          self$cores_str = "-solo" 
        } else { 
          self$cores_str = paste("-",self$cores ,"-parallel",sep = "")
        }
        #set scenario path 
        if(Sys.info()['sysname']!="Linux"){
          self$actual_CSV_path = paste("C:/Users/hnyk9/Thesis/Portfolio-Scheduling/originalCSVs-Teton_SAT16/teton-SAT2016-25-solvers",self$cores_str,".csv",sep = "")
        } else{
          self$actual_CSV_path = paste("/home/haniye/Documents/Portfolio-Scheduling/originalCSVs-Teton_SAT16/teton-SAT2016-25-solvers",self$cores_str,".csv",sep = "")
          if(cluster){
            self$actual_CSV_path = paste("/gscratch/hkashgar/Portfolio-Scheduling/originalCSVs-Teton_SAT16/teton-SAT2016-25-solvers",self$cores_str,".csv",sep = "")
          }
        }
        self$Cutoff = 5000
      } else if(benchmarks_name == "GRAPHS2015"){
        if(cores == 1) {
          self$cores_str = "-solo-replacement" 
        } else { 
          self$cores_str = paste("-",self$cores ,"-parallel-replacement",sep = "")
        }
        #set scenario path 
        if(Sys.info()['sysname']!="Linux"){
          self$actual_CSV_path = paste("C:/Users/hnyk9/Thesis/Portfolio-Scheduling/originalCSVs-Teton_GRAPHS15/teton-GRAPHS2015-7-solvers",self$cores_str,".csv",sep = "")
        } else{
          self$actual_CSV_path = paste("/home/haniye/Documents/Portfolio-Scheduling/originalCSVs-Teton_GRAPHS15/teton-GRAPHS2015-7-solvers",self$cores_str,".csv",sep = "")
          if(cluster){
            self$actual_CSV_path = paste("/gscratch/hkashgar/Portfolio-Scheduling/originalCSVs-Teton_GRAPHS15/teton-GRAPHS2015-7-solvers",self$cores_str,".csv",sep = "")
          }
        }
        self$Cutoff = 100000
      } else if(benchmarks_name == "MAXSAT2019"){
        if(cores == 1) {
          self$cores_str = "-solo"
          # self$cores_str = "-solo" 
        } else { 
          self$cores_str = paste("-",self$cores ,"-parallel",sep = "")
          # self$cores_str = paste("-",self$cores ,"-parallel",sep = "")
        }
        #set scenario path 
        if(Sys.info()['sysname']!="Linux"){
          self$actual_CSV_path = paste("C:/Users/hnyk9/Thesis/PortfolioScheduling/ExperimentResults/csvs/MAXSAT19/teton-MAXSAT2019-7-solvers",self$cores_str,".csv",sep = "")
        } else{
          self$actual_CSV_path = paste("/home/haniye/Documents/PortfolioScheduling/ExperimentResults/csvs/MAXSAT19/teton-MAXSAT2019-7-solvers",self$cores_str,".csv",sep = "")
          # self$actual_CSV_path = paste("/home/haniye/Documents/Parallel_Experiments/MAXSAT2019/resultCSVs_MaxSAT2019_Teton/teton-MAXSAT2019-7-solvers",self$cores_str,".csv",sep = "")
          if(cluster){
            self$actual_CSV_path = paste("/gscratch/hkashgar/PortfolioScheduling/ExperimentResults/csvs/MAXSAT19/teton-MAXSAT2019-7-solvers",self$cores_str,".csv",sep = "")
          }
        }
        self$Cutoff = 3600
      } else if(benchmarks_name == "IPC2018"){
        if(cores == 1) {
          self$cores_str = "-solo"
          # self$cores_str = "-solo" 
        } else { 
          self$cores_str = paste("-",self$cores ,"-parallel",sep = "")
          # self$cores_str = paste("-",self$cores ,"-parallel",sep = "")
        }
        #set scenario path 
        if(Sys.info()['sysname']!="Linux"){
          self$actual_CSV_path = paste("C:/Users/hnyk9/Thesis/PortfolioScheduling/ExperimentResults/csvs/IPC2018/teton-IPC2018-15-solvers",self$cores_str,".csv",sep = "")
        } else{
          self$actual_CSV_path = paste("/home/haniye/Documents/PortfolioScheduling/ExperimentResults/csvs/IPC2018/teton-IPC2018-15-solvers",self$cores_str,".csv",sep = "")
          # self$actual_CSV_path = paste("/home/haniye/Documents/Parallel_Experiments/MAXSAT2019/resultCSVs_MaxSAT2019_Teton/teton-MAXSAT2019-7-solvers",self$cores_str,".csv",sep = "")
          if(cluster){
            self$actual_CSV_path = paste("/gscratch/hkashgar/PortfolioScheduling/ExperimentResults/csvs/IPC2018/teton-IPC2018-15-solvers",self$cores_str,".csv",sep = "")
          }
        }
        self$Cutoff = 1800
      } else if(benchmarks_name == "SAT11-INDU"){
        if(cores == 1) {
          self$cores_str = "-solo"
          # self$cores_str = "-solo" 
        } else { 
          self$cores_str = paste("-",self$cores ,"-parallel",sep = "")
          # self$cores_str = paste("-",self$cores ,"-parallel",sep = "")
        }
        #set scenario path 
        if(Sys.info()['sysname']!="Linux"){
          self$actual_CSV_path = paste("C:/Users/hnyk9/Thesis/PortfolioScheduling/ExperimentResults/csvs/SAT11-INDU/teton-SAT11-INDU-14-solvers",self$cores_str,".csv",sep = "")
        } else{
          self$actual_CSV_path = paste("/home/haniye/Documents/PortfolioScheduling/ExperimentResults/csvs/SAT11-INDU/teton-SAT11-INDU-14-solvers",self$cores_str,".csv",sep = "")
          # self$actual_CSV_path = paste("/home/haniye/Documents/Parallel_Experiments/MAXSAT2019/resultCSVs_MaxSAT2019_Teton/teton-MAXSAT2019-7-solvers",self$cores_str,".csv",sep = "")
          if(cluster){
            self$actual_CSV_path = paste("/gscratch/hkashgar/PortfolioScheduling/ExperimentResults/csvs/SAT11-INDU/teton-SAT11-INDU-14-solvers",self$cores_str,".csv",sep = "")
          }
        }
        self$Cutoff = 5000
      }
      self$get_actual_result_csv()
      invisible(self)
    },
    
    #get actual CSV files
    get_actual_result_csv = function(){
      if(is.null(self$actual_CSV) || nrow(self$actual_CSV) == 0){
        csv = data.frame()
        if(file.exists(self$actual_CSV_path)){
          csv = read.csv(self$actual_CSV_path)
        } else{
          print("The requested file do not exit! ")
        } 
        #if not empty, order by instance name
        if(nrow(csv)>1){
          csv = csv[order(csv$InstanceName),]
          colnames = colnames(csv)[-1]
          colnames = colnames[order(colnames)]
          colnames = append(c("InstanceName"),colnames)
          csv = csv[,colnames]
          self$actual_CSV = csv
          #set number of solvers and instances
          self$n_solvers = ncol(csv) - 1
          self$n_instances = nrow(csv)
          self$solvers = colnames(csv)[-1]
        } else{ 
          print("The requested CSV is empty!")
        }
      } 
      #if the csv is not empty return the existing one
      return(self$actual_CSV)
    },
    
    #get par10 csv 
    get_par10_dataframe = function(){
      csv = as.data.frame(sapply(self$actual_CSV[2:(self$n_solvers+1)],function(x) ifelse(x>=self$Cutoff,self$Cutoff*10,x)))
      csv = cbind(self$actual_CSV$InstanceName, csv)
      colnames(csv)[1] <- "InstanceName"
      self$par10_CSV = csv
      return(self$par10_CSV)
    },
    
    #get mcp csv 
    get_mcp_dataframe = function(sequentialData){
      if(self$n_instances != sequentialData$n_instances){
        print("Differing number of rows: 312, 381")
        return()
      }
      #get vbs values
      VBS = sequentialData$get_VBS()
      VBS = VBS[order(VBS$InstanceName),]
      InstanceName = VBS$InstanceName
      VBS = VBS$VBS_Runtime
      
      #get parallel value
      csvParallel = self$get_actual_result_csv()
      csvParallel = csvParallel[order(csvParallel$InstanceName),]
      csvParallel = csvParallel[-1]
      #mcp = paralle value - vbs
      self$mcp_CSV = csvParallel - VBS
      #ignore negative values 
      self$mcp_CSV[self$mcp_CSV<0] <- 0
      self$mcp_CSV = cbind(InstanceName, self$mcp_CSV)
      return(self$mcp_CSV)
    },
    
    #method to use when we want to ignore the instances solved by vbs
    ignore_instances = function(unsolvedinstances){
      #since mcp needs vbs of sequential run we need the first value of mcp firsy
      if(!(is.null(self$mcp_CSV))) self$mcp_CSV = subset(self$mcp_CSV ,  !(self$mcp_CSV$InstanceName %in% unsolvedinstances))
      else return("Try using get_mcp_dataframe() first")
      #filling par10
      self$get_par10_dataframe()
      #ignore from actual csv and par10
      self$actual_CSV = subset(self$actual_CSV ,!(self$actual_CSV$InstanceName %in% unsolvedinstances))
      self$par10_CSV = subset(self$par10_CSV ,  !(self$par10_CSV$InstanceName %in% unsolvedinstances))
      
      self$n_instances = nrow(self$actual_CSV)
      invisible(self)
    },
    
    #actual optimal schedule
    get_optimal_runtime = function(instanceset = NULL){
      csv = self$actual_CSV
      if(!is.null(instanceset)){
        csv = csv[which(csv$InstanceName %in% instanceset),]
      }
      InstanceName = csv$InstanceName
      solvers = as.vector(apply(csv[,c(-1)], 1, function(x) colnames(csv[,c(-1)])[which.min(x)]))
      minruntime = rowMins(as.matrix(csv[,c(-1)]))
      res = data.frame(InstanceName,solvers, minruntime)
      return(res)
    },
    
    #sometimes vbs is different from the optimal when running in parallel
    #This give the n_th vbs runtime in parallel 
    #note this will not give minimum across vbs1 to vbs_nd, only nd
    get_nd_vbs_runtime = function(instanceset = NULL, ignore_instances = FALSE, nd = 1){
      csv = self$actual_CSV
      sq = SequentialPerformance$new(self$benchmarks_name)
      if(!is.null(instanceset)){
        csv = csv[which(csv$InstanceName %in% instanceset),]
      } else{
        if(ignore_instances == TRUE){ 
          sq$ignore_instances()
        }
      }
      VBS_Solvers = sq$get_nd_VBS(nd = nd)
      if(!is.null(instanceset)){
        VBS_Solvers = VBS_Solvers[which(VBS_Solvers$InstanceName %in% instanceset),]
      }
      InstanceName = VBS_Solvers$InstanceName
      VBS_Solvers = VBS_Solvers$Solvers
      VBS_Runtime = vector()
      for(i in 1:nrow(csv)){
        VBS_Runtime = append(VBS_Runtime, csv[which(csv$InstanceName == InstanceName[i]),VBS_Solvers[i]])
      }
      res = data.frame(InstanceName,VBS_Solvers, VBS_Runtime)
      return(res)
    },
    
    #get vbs solvers and runtime per instance    
    #This give the n_th vbs runtime in parallel 
    #note this will not give minimum across vbs1 to vbs_nd, only nd
    get_nd_optimal_runtime = function(instanceset = NULL, nd = 1){
      #get min runtimes
      Runtime = apply(self$actual_CSV[2:ncol(self$actual_CSV)],1, FUN = function(x) sort(x)[nd])
      #get solvers which gives minimum runtimes
      Solvers = colnames(self$actual_CSV)[sapply(1:nrow(self$actual_CSV),FUN = function(x) which(self$actual_CSV[x,1:ncol(self$actual_CSV)] == Runtime[x])[[1]])]
      #combine both to csv
      res = data.frame(self$actual_CSV$InstanceName, Solvers,Runtime)
      colnames(res)[1] <- "InstanceName"
      if(!is.null(instanceset)){
        res = res[which(res$InstanceName %in% instanceset),]
      }
      return(res)
    }
  )
)
