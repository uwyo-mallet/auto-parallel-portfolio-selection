if(Sys.info()['sysname']=="Linux"){
  if(file.exists("/home/haniye/Documents/OrganizedScripts/PredictionResults.R")){
    source("/home/haniye/Documents/OrganizedScripts/PredictionResults.R") 
  }
  else{ 
    source("/gscratch/hkashgar/OrganizedScripts/PredictionResults.R") 
  }
} else{
  source("C:/Users/hnyk9/OneDrive - University of Wyoming/OrganizedScripts/PredictionResults.R")
}

library(reshape)
#library(tidyverse)
library(ggplot2)
library(gtools)
library(fitdistrplus)
library(reshape2)
OverheadResults = R6Class(
  classname = "OverheadResults",
  inherit = PredictionResults,

  public = list(
    benchmarks_name = "SAT2018",
    sequentialData = NULL,
    cluster = NULL,
    actualOverheadPercore_secondsPath = NULL,
    actualOverheadPercore_secondsPlotPath = NULL,
    actualOverheadPercore_percPath = NULL,
    actualOverheadPercore_percPlotPath = NULL,
    actualOverheadPersolver_secondsPath = NULL,
    actualOverheadPersolver_secondsPlotPath = NULL,
    actualOverheadPersolver_percPath = NULL,
    actualOverheadPersolver_percPlotPath = NULL,
    initialize = function(benchmarks_name="SAT2018", cluster = FALSE){
      self$benchmarks_name = benchmarks_name
      self$sequentialData = SequentialPerformance$new(benchmarks_name, cluster)
      self$cluster = cluster
      if(Sys.info()['sysname']=="Linux"){
        self$actualOverheadPercore_secondsPath = paste("/home/haniye/Documents/OrganizedScripts/",self$benchmarks_name,"/actual_overhead_per_core_seconds/",sep = "")
        self$actualOverheadPercore_secondsPlotPath = paste("/home/haniye/Documents/OrganizedScripts/",self$benchmarks_name,"/actual_overhead_per_core_seconds/plot/",sep = "")
        self$actualOverheadPercore_percPath = paste("/home/haniye/Documents/OrganizedScripts/",self$benchmarks_name,"/actual_overhead_per_core_perc/",sep = "")
        self$actualOverheadPercore_percPlotPath = paste("/home/haniye/Documents/OrganizedScripts/",self$benchmarks_name,"/actual_overhead_per_core_perc/plot/",sep = "")
        
        self$actualOverheadPersolver_secondsPath = paste("/home/haniye/Documents/OrganizedScripts/",self$benchmarks_name,"/actual_overhead_per_solver_seconds/",sep = "")
        self$actualOverheadPersolver_secondsPlotPath = paste("/home/haniye/Documents/OrganizedScripts/",self$benchmarks_name,"/actual_overhead_per_solver_seconds/plot/",sep = "")
        self$actualOverheadPersolver_percPath = paste("/home/haniye/Documents/OrganizedScripts/",self$benchmarks_name,"/actual_overhead_per_solver_perc/",sep = "")
        self$actualOverheadPersolver_percPlotPath = paste("/home/haniye/Documents/OrganizedScripts/",self$benchmarks_name,"/actual_overhead_per_solver_perc/plot/",sep = "")
        if(cluster){
          self$actualOverheadPercore_secondsPath = paste("/gscratch/hkashgar/OrganizedScripts/",self$benchmarks_name,"/actual_overhead_per_core_seconds/",sep = "")
          self$actualOverheadPercore_secondsPlotPath = paste("/gscratch/hkashgar/OrganizedScripts/",self$benchmarks_name,"/actual_overhead_per_core_seconds/plot/",sep = "")
          self$actualOverheadPercore_percPath = paste("/gscratch/hkashgar/OrganizedScripts/",self$benchmarks_name,"/actual_overhead_per_core_perc/",sep = "")
          self$actualOverheadPercore_percPlotPath = paste("/gscratch/hkashgar/OrganizedScripts/",self$benchmarks_name,"/actual_overhead_per_core_perc/plot/",sep = "")
        
          self$actualOverheadPersolver_secondsPath = paste("/gscratch/hkashgar/OrganizedScripts/",self$benchmarks_name,"/actual_overhead_per_solver_seconds/",sep = "")
          self$actualOverheadPersolver_secondsPlotPath = paste("/gscratch/hkashgar/OrganizedScripts/",self$benchmarks_name,"/actual_overhead_per_solver_seconds/plot/",sep = "")
          self$actualOverheadPersolver_percPath = paste("/gscratch/hkashgar/OrganizedScripts/",self$benchmarks_name,"/actual_overhead_per_solver_perc/",sep = "")
          self$actualOverheadPersolver_percPlotPath = paste("/gscratch/hkashgar/OrganizedScripts/",self$benchmarks_name,"/actual_overhead_per_solver_perc/plot/",sep = "")
        }
      } else{
        self$actualOverheadPercore_secondsPath = paste("C:/Users/hnyk9/OneDrive - University of Wyoming/OrganizedScripts/",self$benchmarks_name,"/actual_overhead_per_core_seconds/",sep = "")
        self$actualOverheadPercore_secondsPlotPath = paste("C:/Users/hnyk9/OneDrive - University of Wyoming/OrganizedScripts/",self$benchmarks_name,"/actual_overhead_per_core_seconds/plot/",sep = "")
        self$actualOverheadPercore_percPath = paste("C:/Users/hnyk9/OneDrive - University of Wyoming/OrganizedScripts/",self$benchmarks_name,"/actual_overhead_per_core_perc/",sep = "")
        self$actualOverheadPercore_percPlotPath = paste("C:/Users/hnyk9/OneDrive - University of Wyoming/OrganizedScripts/",self$benchmarks_name,"/actual_overhead_per_core_perc/plot/",sep = "")
        
        self$actualOverheadPersolver_secondsPath = paste("C:/Users/hnyk9/OneDrive - University of Wyoming/OrganizedScripts/",self$benchmarks_name,"/actual_overhead_per_solver_seconds/",sep = "")
        self$actualOverheadPersolver_secondsPlotPath = paste("C:/Users/hnyk9/OneDrive - University of Wyoming/OrganizedScripts/",self$benchmarks_name,"/actual_overhead_per_solver_seconds/plot/",sep = "")
        self$actualOverheadPersolver_percPath = paste("C:/Users/hnyk9/OneDrive - University of Wyoming/OrganizedScripts/",self$benchmarks_name,"/actual_overhead_per_solver_perc/",sep = "")
        self$actualOverheadPersolver_percPlotPath = paste("C:/Users/hnyk9/OneDrive - University of Wyoming/OrganizedScripts/",self$benchmarks_name,"/actual_overhead_per_solver_perc/plot/",sep = "")
      }
      if(is.null(self$sequentialData$scenario)) self$sequentialData$get_scenario()
    },  
    #type can be "seconds" or "percentage_change"
    actual_overhead_per_core = function(ignoreTimeouts = FALSE, 
                                        type = "percentage-change", 
                                        savePath, savePlot=TRUE, plotPath ="",
                                        cores = c(2:10,20,30,32),
                                        log = FALSE){
      solo_runtime = self$sequentialData$actual_CSV
      solo_runtime = solo_runtime[order(solo_runtime$InstanceName),]
      if(is.null(self$sequentialData$solvedInstances)) self$sequentialData$get_VBS()
      solved_instances = self$sequentialData$solvedInstances
      if(ignoreTimeouts){
        solo_runtime = solo_runtime[which(solo_runtime$InstanceName %in% solved_instances),]
        solo_runtime = solo_runtime[order(solo_runtime$InstanceName),]
      }
      overhead = data.frame(matrix(nrow = nrow(solo_runtime),ncol=(self$sequentialData$n_solvers+1)))
      colnames(overhead) = colnames(solo_runtime)
      overhead$InstanceName = solo_runtime$InstanceName
      path = self$sequentialData$actual_CSV_path
      path = str_split(path,"/")[[1]]
      path = path[-length(path)]
      path = paste(path, collapse = '/') 
      for(c in cores){
        csv = ParallelLevel$new(c, self$benchmarks_name, self$cluster)$actual_CSV
        csv = csv[order(csv$InstanceName),]
        if(ignoreTimeouts){
          csv = csv[which(csv$InstanceName %in% solved_instances),]
        }
        # csv[csv==self$sequentialData$Cutoff]<-NA
        if(type == "percentage-change"){
          overhead[2:(self$sequentialData$n_solvers+1)] = ((csv [2:(self$sequentialData$n_solvers+1)] - solo_runtime[2:(self$sequentialData$n_solvers+1)])/solo_runtime[2:(self$sequentialData$n_solvers+1)]) +1
          # overhead[,2:(self$sequentialData$n_solvers+1)][overhead[,2:(self$sequentialData$n_solvers+1)]<1] <- 1 
        } else if(type == "seconds"){
          overhead[2:(self$sequentialData$n_solvers+1)] = (csv [2:(self$sequentialData$n_solvers+1)] - solo_runtime[2:(self$sequentialData$n_solvers+1)])
          # overhead[,2:(self$sequentialData$n_solvers+1)][overhead[,2:(self$sequentialData$n_solvers+1)]<0] <- 0
        }
        solvers = self$sequentialData$solvers
        write.csv(overhead,paste(savePath,"/",c,"-cores-",type,"-overhead.csv",sep = ""),row.names = FALSE)
        #plot
        if(savePlot){
          if(plotPath != "") self$visualize_actual_overhead_per_core(overhead = overhead, plotPath = plotPath, core = c,type = type, log= log)
          else print("identify a path for plots")
        }
      }
    },
    
    #is used in actual_overhead_per_core
    visualize_actual_overhead_per_core = function(overhead,plotPath,core,type, log ){
      long_data <- melt(data = overhead, id = "InstanceName")
      colnames(long_data)[2] = "solvers"
      colnames(long_data)[3] = "overhead"
      if(type == "percentage-change"){
        #convert to percentage
        long_data$overhead = long_data$overhead 
      }
      p <- ggplot(long_data, aes(factor(solvers), overhead)) 
      p <- p + geom_boxplot() + 
        theme(axis.text.x = element_text(angle=90, vjust=.5, hjust=1))
      p<- p+ stat_summary(fun=mean, geom="point", shape=20, color = "red", size = 4)
      p<- p + scale_y_continuous(trans = "log10")
      if(log) p <- p + scale_y_continuous(trans='log10')
      ggsave(paste(plotPath,"/",core,"-cores-",type,"-overhead.png",sep = ""),plot = p,width = 10,height = 7, dpi = 150)
      return(plotPath)
    },
    
    #get overhead per solver 
    actual_overhead_per_solver = function(cores_overhead_path,savePath, ignoreTimeouts = TRUE, type = "percentage-change", savePlot=TRUE, plotPath ="", log=FALSE){
      #sort the file names 
      files = mixedsort(sort(list.files(cores_overhead_path,pattern = ".csv", full.names = TRUE)))
      csvs = lapply(files, read.csv)
      solo_runtime = self$sequentialData$actual_CSV
      solo_runtime = solo_runtime[order(solo_runtime$InstanceName),]
      if(is.null(self$sequentialData$solvedInstances)) self$sequentialData$get_VBS()
      solved_instances = self$sequentialData$solvedInstances
      if(ignoreTimeouts){
        solo_runtime = solo_runtime[which(solo_runtime$InstanceName %in% solved_instances),]
        solo_runtime = solo_runtime[order(solo_runtime$InstanceName),]
      }
      for(solver in self$sequentialData$solvers){
        solo = solo_runtime
        if(ignoreTimeouts){
          solo = solo[which(solo[solver]<self$sequentialData$Cutoff),]
        }
        solver_overhead = data.frame(matrix(nrow = nrow(solo),ncol = length(cores)+1))
        colnames(solver_overhead) = c("InstanceName",cores)
        solver_overhead$InstanceName = solo$InstanceName
        for(i in c(1:length(cores))){
          temp = csvs[[i]][which(csvs[[i]]$InstanceName %in% solo$InstanceName),]
          solver_overhead[i+1] = temp[solver]
        }
        write.csv(solver_overhead,paste(savePath,"/",solver,".csv",sep = ""),row.names = FALSE)
        #solver_overhead = solver_overhead[which(solver_overhead[2:13]!=c(rep(0,12))),]
        #solver_overhead = na.omit(solver_overhead)
        if(savePlot){
          if(plotPath != "") self$visualize_actual_overhead_per_solver(solver_overhead = solver_overhead,plotPath = plotPath,solver = solver, type = type, log = log)
          else print("identify a path for plots")
        }
      }
    },
    
    #visualize the actual overhead 
    visualize_actual_overhead_per_solver = function(solver_overhead,plotPath,solver,type, log=FALSE){
      long_data <- melt(solver_overhead)
      colnames(long_data)[2]<-"cores"
      colnames(long_data)[3] = "overhead"
      if(type == "percentage-change"){
        #convert to percentage
        long_data$overhead = long_data$overhead 
      }
      p <- ggplot(long_data, aes(factor(cores), overhead)) 
      p <- p + geom_boxplot()
      p <- p+ stat_summary(fun=mean, geom="point", shape=20, color = "red", size = 4)
      if(log) p <- p + scale_y_continuous(trans='log10')
      ggsave(paste(plotPath,"/",type,"-",solver,".png",sep = ""), plot = p, width = 10, height = 7, dpi = 150) 
      return(plotPath)
    },
    
    #maybe not useful but used to compare mean and median, percentage and seconds methods 
    #mean(overhead)|median(overhead) + solo 
    Estimate_overhead_on_sequential = function(savePath, stat = "median",cores = c(32,30,20,10:2),solver_overhead_path, type = "percentage-change"){
      files = list.files(solver_overhead_path,".csv")
      #actual solo
      solo_runtime = self$sequentialData$actual_CSV
      solo_runtime = solo_runtime[order(solo_runtime$InstanceName),]
      
      for(solver in self$sequentialData$solvers){
        file = paste(solver_overhead_path,"/",solver,".csv",sep = "")
        overhead_solver = read.csv(file)
        overhead_solver = overhead_solver[rowSums(overhead_solver[2:13])>0,]
        overhead_solver = overhead_solver[order(overhead_solver$InstanceName),]
        solo_reduced = solo_runtime[is.element(solo_runtime$InstanceName, overhead_solver$InstanceName),]
        solo_reduced = solo_reduced[order(solo_reduced$InstanceName),]
        csv_stat = data.frame(matrix(ncol = 0,nrow = nrow(overhead_solver)))
        csv_stat = cbind(csv_stat,overhead_solver$InstanceName)
        if(stat == "mean"){
          stat_for_cores = self$solver_mean(file)
        } else if(stat == "median"){
          stat_for_cores = self$solver_median(file)
        } else { return("wrong stat, should be mean or median!") }
        for(core in cores){
          if(type == "percentage-change"){
            overhead_estimates = solo_reduced[solver] * as.numeric(stat_for_cores[paste("X",core,sep = "")])
            overhead_estimates[overhead_estimates>5000] <- 5000
          } else{
            overhead_estimates = solo_reduced[solver] + as.numeric(stat_for_cores[paste("X",core,sep = "")])
            overhead_estimates[overhead_estimates>5000] <- 5000
          }
          csv_stat = cbind(csv_stat,overhead_estimates)
        }
        colnames(csv_stat) <- c("InstanceName",cores)
        write.csv(csv_stat,paste(savePath,"/","Estimate_overhead_performance_",stat,"_",type,"_",solver,'.csv',sep = ""),row.names = FALSE)
      }
    },
    
    #need to be fixed
    visualize_comparison_overhead_estimation_per_solver = function(solver_overhead_path, cores = c(32,30,20,10:2),overhead_performance_mean_path, overhead_performance_median_path){
      self$Estimate_overhead_performance_per_solver(savePath = overhead_performance_mean_path,stat = "mean",solver_overhead_path = solver_overhead_path)
      self$Estimate_overhead_performance_per_solver(savePath = overhead_performance_median_path,stat = "median",solver_overhead_path = solver_overhead_path)
      files_mean = list.files(overhead_performance_mean_path,".csv",full.names = TRUE)
      files_median = list.files(overhead_performance_median_path,".csv",full.names = TRUE)
      path = self$sequentialData$actual_CSV_path
      path = str_split(path,"/")[[1]]
      path = path[-length(path)]
      path = paste(path, collapse = '/') 
      for(solver in self$sequentialData$solvers){
        csv_mean = read.csv(files_mean[which(grepl(solver, files_mean))])
        csv_median = read.csv(files_median[which(grepl(solver, files_median))])
        csv_parallel_file = mixedsort(sort(list.files(path,"replacement.csv",full.names = TRUE)))[-13]
        
        csv_parallel = lapply(csv_parallel_file, function(x){
           temp = read.csv(x)[c("InstanceName",solver)]
           temp = temp[which(temp$InstanceName %in% csv_mean$InstanceName),]
           return(temp)
        })
        
        bind_rows(csv_parallel, .id = "InstanceName")
        overhead_difference_mean_actual = compute_difference(csv_mean,overhead_solver)
        overhead_difference_median_actual = compute_difference(csv_median,overhead_solver)
        colnames(overhead_difference_mean_actual) <- c("InstanceName",cores)
        colnames(overhead_difference_median_actual) <- c("InstanceName",cores)
        overhead_difference_mean_actual_plot = gather(overhead_difference_mean_actual, core,overhead_diffence,2:13)
        overhead_difference_mean_actual_plot <- cbind(overhead_difference_mean_actual_plot,"overhead_difference_mean_actual")
        overhead_difference_median_actual_plot = gather(overhead_difference_median_actual, core,overhead_diffence,2:13)
        overhead_difference_median_actual_plot <- cbind(overhead_difference_median_actual_plot,"overhead_difference_median_actual")
        colnames(overhead_difference_median_actual_plot)[4]<-"estimation_method"
        colnames(overhead_difference_mean_actual_plot)[4]<-"estimation_method"
        
        plot = rbind(overhead_difference_mean_actual_plot,overhead_difference_median_actual_plot)
        
        p <- ggplot(plot, aes(x = factor(as.numeric(core)), y = overhead_diffence, color = estimation_method)) 
        p <- p + geom_boxplot()
        p + stat_summary(fun=mean, geom="point", shape=20, size=4,color="black")
      }
     
      #ggsave(paste("./../visualization_estimate_overhead_per_solver/",solver,".png",sep = ""),plot = p )
    },
    
    #calculate fractional mcp (percentage-change) of selected solvers on each core based on AS using estimated overhead (median/mean)
    get_mcp_for_all_top_porfolios_actualRuntime_estimated_overhead = function(predictionPath,overheadPath,saveTo, stat = "median",distr = "emp", type = "percentage-change"){
      self$sequentialData$ignore_instances()
      instances = self$sequentialData$get_solved_instances()
      solvers = self$sequentialData$solvers
      vbs_all = self$sequentialData$get_VBS()
      All_instances_mcp = data.frame(matrix(nrow = 0,ncol=(self$sequentialData$n_solvers+1)))
      parallelStartSocket(cpus = detectCores())
      overhead_files = list.files(overheadPath,".csv",full.names = TRUE )
      
      for(instance in instances){
        preds = read.csv(paste(predictionPath,"/",
                               str_split(instance,"sat/")[[1]][2],".csv",sep=""))
        preds = preds[order(preds$PredictedRuntime),]
        solver_order = preds$Solver
        vbs = vbs_all[which(vbs_all$InstanceName ==instance),]
        mcps = vector()
        for(i in 1:length(solvers)){
          get_top = preds[1:i,]
          if(i>1){
            core = i 
            if(core>=32){
              core = 32
            } else if(core<=10){
              core = core
            } else {
              core = round(core,-1)
            }
            for(solver in get_top$Solver){
              file = overhead_files[which(overhead_files ==paste(overheadPath,solver,".csv",sep = ""))]
              overhead = read.csv(file)
              overhead = overhead[order(overhead$InstanceName),]
              if(stat=="median"){
                stat_for_cores = self$solver_median(file)
              } else if(stat=="mean"){
                stat_for_cores = self$solver_mean(file)
              } else {
                #stat should be a number ...
                stat_for_cores = self$solver_quantile(file,distr=distr,quan = stat)
              }
              stat_for_cores = as.numeric(stat_for_cores[paste("X",core,sep = "")])
              if(type == "percentage-change"){
                get_top$ActualRuntime[which(get_top$Solver == solver)] = get_top$ActualRuntime[which(get_top$Solver == solver)] * stat_for_cores
              } else if(type == "seconds"){
                get_top$ActualRuntime[which(get_top$Solver == solver)] = get_top$ActualRuntime[which(get_top$Solver == solver)] + stat_for_cores
              }
              get_top$ActualRuntime[which(get_top$Solver == solver && get_top$ActualRuntime>5000)]<- 5000
            }
          }
          top = get_top[which(get_top$ActualRuntime == min(get_top$ActualRuntime)),]
          if(nrow(top)>0){ top = top[1,]}
          
          mcp = (top$ActualRuntime - vbs$VBS_Runtime)/vbs$VBS_Runtime + 1
          #print(mcp)
          mcps = append(mcps,mcp)
          
        }
        colnames(All_instances_mcp) <- c("InstanceName",c(1:39))
        if(!instance %in% All_instances_mcp$InstanceName){
          All_instances_mcp = rbind(All_instances_mcp,c(instance,mcps))
        }
      }
      colnames(All_instances_mcp) <- c("InstanceName",c(1:39))
      write.csv(All_instances_mcp,paste(saveTo,"/mcp_all_selections_actualruntime_estimatedoverhead.csv",sep=""),
                row.names = FALSE)
      parallelStop()
      return(All_instances_mcp)
    },
    
    #calculate fractional mcp (percentage-change) of selected solvers on each core based on AS using estimated overhead (median/mean)
    get_mcp_for_all_top_porfolios_actualRuntime_estimated_overhead2 = function(predictionPath,overheadPath,saveTo, stat = "median",distr = "emp", type = "percentage-change"){
      self$sequentialData$ignore_instances()
      instances = sapply(list.files(predictionPath,".csv"),function(x) paste("sat/",str_split(x,".csv")[[1]][1],sep=""),USE.NAMES = FALSE)
      solvers = self$sequentialData$solvers
      vbs_all = self$sequentialData$get_VBS()
      vbs_all = vbs_all[which(vbs_all$InstanceName %in% instances),]
      All_instances_mcp = data.frame(matrix(nrow = 0,ncol=(self$sequentialData$n_solvers+1)))
      All_instances_mcp_sec = data.frame(matrix(nrow = 0,ncol=(self$sequentialData$n_solvers+1)))
      All_instances_expectedpred = data.frame(matrix(nrow = 0,ncol=(self$sequentialData$n_solvers+1)))
      All_instances_expectedmcp = data.frame(matrix(nrow = 0,ncol=(self$sequentialData$n_solvers+1)))
      All_instances_expectedpredslowerbound = data.frame(matrix(nrow = 0,ncol=(self$sequentialData$n_solvers+1)))
      All_instances_solver_order = data.frame(matrix(nrow = 0,ncol=(self$sequentialData$n_solvers+1)))
      parallelStartSocket(cpus = detectCores())
      overhead_files = list.files(overheadPath,".csv",full.names = TRUE )
      
      for(instance in instances){
        preds = read.csv(paste(predictionPath,"/",
                               str_split(instance,"sat/")[[1]][2],".csv",sep=""))
        preds = preds[order(preds$ExpectedLowebound),]
        solver_order = preds$Solver
        vbs = vbs_all[which(vbs_all$InstanceName ==instance),]
        mcps = vector()
        mcps_sec = vector()
        expectedpreds = vector()
        expectedmcps = vector()
        expectedpredslowerbounds = vector()
        solverorders = vector()
        runtimes = vector()
        for(i in 1:nrow(preds)){
          get_top = preds[1:i,]
          if(i>1){
            core = i 
            if(core>=32){
              core = 32
            } else if(core<=10){
              core = core
            } else {
              core = round(core,-1)
            }
            for(solver in get_top$Solver){
              file = overhead_files[which(overhead_files == paste(overheadPath,"/",solver,".csv",sep = ""))]
              overhead = read.csv(file)
              overhead = overhead[order(overhead$InstanceName),]
              if(stat=="median"){
                stat_for_cores = self$solver_median(file)
              } else if(stat=="mean"){
                stat_for_cores = self$solver_mean(file)
              } else {
                #stat should be a number ...
                stat_for_cores = self$solver_quantile(file,distr=distr,quan = stat)
              }
              stat_for_cores = as.numeric(stat_for_cores[paste("X",core,sep = "")])
              if(type == "percentage-change"){
                get_top$ExpectedPrediction[which(get_top$Solver == solver)] = get_top$ExpectedPrediction[which(get_top$Solver == solver)] * stat_for_cores
                get_top$ExpectedLowebound[which(get_top$Solver == solver)] = get_top$ExpectedLowebound[which(get_top$Solver == solver)] * stat_for_cores
              } else if(type == "seconds"){
                get_top$ExpectedPrediction[which(get_top$Solver == solver)] = get_top$ExpectedPrediction[which(get_top$Solver == solver)] + stat_for_cores
                get_top$ExpectedLowebound[which(get_top$Solver == solver)] = get_top$ExpectedLowebound[which(get_top$Solver == solver)] + stat_for_cores
              }
              get_top$ExpectedPrediction[which(get_top$Solver == solver && get_top$ExpectedPrediction>5000)]<- 5000
            }
          }
          #top = get_top[which(get_top$ExpectedPrediction == min(get_top$ExpectedPrediction)),]
          top = get_top[which(get_top$ExpectedLowebound == min(get_top$ExpectedLowebound)),]
          
          if(nrow(top)>0){ top = top[1,]}
          
          actualmcp = (top$ParallelRuntime - vbs$VBS_Runtime)/vbs$VBS_Runtime + 1
          actualmcp_sec = (top$ParallelRuntime - vbs$VBS_Runtime)
          expectedmcp = (top$ExpectedPrediction - vbs$VBS_Runtime)/vbs$VBS_Runtime + 1
          expectedpred = (top$ExpectedPrediction)
          expectedpredslowerbound = (top$ExpectedLowebound)
          solverorder= top$Solver
          #print(mcp)
          mcps = append(mcps,actualmcp)
          mcps_sec = append(mcps_sec,actualmcp_sec)
          expectedmcps = append(expectedmcps,expectedmcp)
          expectedpreds = append(expectedpreds,expectedpred)
          expectedpredslowerbounds = append(expectedpredslowerbounds,expectedpredslowerbound)
          solverorders = append(solverorders,solverorder)
        }
        colnames(All_instances_mcp) <- c("InstanceName",c(1:39))
        colnames(All_instances_mcp_sec) <- c("InstanceName",c(1:39))
        colnames(All_instances_expectedmcp) <- c("InstanceName",c(1:39))
        colnames(All_instances_expectedpred) <- c("InstanceName",c(1:39))
        colnames(All_instances_expectedpredslowerbound) <- c("InstanceName",c(1:39))
        colnames(All_instances_solver_order) <- c("InstanceName",c(1:39))
        All_instances_mcp = rbind(All_instances_mcp,c(instance,mcps_sec,rep(NA,(39-length(mcps)))))
        All_instances_mcp_sec = rbind(All_instances_mcp_sec,c(instance,mcps,rep(NA,(39-length(mcps)))))
        All_instances_expectedpred = rbind(All_instances_expectedpred,c(instance,expectedpreds,rep(NA,(39-length(expectedpreds)))))
        All_instances_expectedpredslowerbound = rbind(All_instances_expectedpredslowerbound,c(instance,expectedpredslowerbounds,rep(NA,(39-length(expectedpredslowerbounds)))))
        All_instances_solver_order = rbind(All_instances_solver_order,c(instance,solverorders,rep(NA,(39-length(solverorders)))))
        All_instances_expectedmcp = rbind(All_instances_expectedmcp,c(instance,expectedmcps,rep(NA,(39-length(expectedmcps)))))
        
      }
      colnames(All_instances_mcp) <- c("InstanceName",c(1:39))
      colnames(All_instances_mcp_sec) <- c("InstanceName",c(1:39))
      colnames(All_instances_expectedpred) <- c("InstanceName",c(1:39))
      colnames(All_instances_expectedpredslowerbound) <- c("InstanceName",c(1:39))
      colnames(All_instances_solver_order) <- c("InstanceName",c(1:39))
      write.csv(All_instances_mcp,paste(saveTo,"/mcp_all_selections_actualruntime_estimatedoverhead.csv",sep=""),
                row.names = FALSE)
      write.csv(All_instances_mcp_sec,paste(saveTo,"/mcp_all_selections_sec_actualruntime_estimatedoverhead.csv",sep=""),
                row.names = FALSE)
      write.csv(All_instances_expectedpred,paste(saveTo,"/mcp_all_selections_predictedruntime_estimatedoverhead.csv",sep=""),
                                            row.names = FALSE)
      write.csv(All_instances_expectedpredslowerbound,paste(saveTo,"/mcp_all_selections_predlowerboundruntime_estimatedoverhead.csv",sep=""),
                row.names = FALSE)
      write.csv(All_instances_solver_order,paste(saveTo,"/mcp_all_selections_predruntime_solverorder_estimatedoverhead.csv",sep=""),
                row.names = FALSE)
      write.csv(All_instances_expectedmcp,paste(saveTo,"/expectedmcp_all_selections_predictedruntime_estimatedoverhead.csv",sep=""),
                row.names = FALSE)
      parallelStop()
      return(All_instances_mcp)
    },
    
    #calculate fractional mcp (percentage-change) of selected solvers on each core based on AS using actual overhead value
    get_mcp_for_all_top_porfolios_actualRuntime_actual_overhead = function(predictionPath,overheadPath,saveTo, stat = "median",distr = "emp", type = "percentage-change"){
      self$sequentialData$ignore_instances()
      instances = self$sequentialData$get_solved_instances()
      solvers = self$sequentialData$solvers
      vbs_all = self$sequentialData$get_VBS()
      All_instances_mcp = data.frame(matrix(nrow = 0,ncol=(self$sequentialData$n_solvers+1)))
      parallelStartSocket(cpus = detectCores())
      overhead_files = list.files(overheadPath,".csv",full.names = TRUE )
      
      for(instance in instances){
        preds = read.csv(paste(predictionPath,"/",
                               str_split(instance,"sat/")[[1]][2],".csv",sep=""))
        preds = preds[order(preds$PredictedRuntime),]
        solver_order = preds$Solver
        vbs = vbs_all[which(vbs_all$InstanceName ==instance),]
        mcps = vector()
        for(i in 1:length(solvers)){
          get_top = preds[1:i,]
          if(i>1){
            core = i 
            if(core>=32){
              core = 32
            } else if(core<=10){
              core = core
            } else {
              core = round(core,-1)
            }
            for(solver in get_top$Solver){
              file = overhead_files[which(overhead_files ==paste(overheadPath,solver,".csv",sep = ""))]
              overhead = read.csv(file)
              overhead = overhead[order(overhead$InstanceName),]
              overhead = overhead[which(overhead$InstanceName == instance),paste("X",core,sep = "")]
              if(length(overhead)<1){
                get_top$ActualRuntime[which(get_top$Solver == solver)]<- 5000
              }
              else{
                if(type == "percentage-change"){
                  get_top$ActualRuntime[which(get_top$Solver == solver)] = get_top$ActualRuntime[which(get_top$Solver == solver)] * overhead
                } else if(type == "seconds"){
                  get_top$ActualRuntime[which(get_top$Solver == solver)] = get_top$ActualRuntime[which(get_top$Solver == solver)] + overhead
                }
              }
              get_top$ActualRuntime[which(get_top$Solver == solver && get_top$ActualRuntime>5000)]<- 5000
            }
          }
          top = get_top[which(get_top$ActualRuntime == min(get_top$ActualRuntime)),]
          if(nrow(top)>0){ top = top[1,]}
          
          mcp = (top$ActualRuntime - vbs$VBS_Runtime)/vbs$VBS_Runtime + 1
          #print(mcp)
          mcps = append(mcps,mcp)
          
        }
        
        colnames(All_instances_mcp) <- c("InstanceName",c(1:39))
        if(!instance %in% All_instances_mcp$InstanceName){
          All_instances_mcp = rbind(All_instances_mcp,c(instance,mcps))
        }
      }
      colnames(All_instances_mcp) <- c("InstanceName",c(1:39))
      write.csv(All_instances_mcp,paste(saveTo,"mcp_all_selections_actualruntime_actualoverhead.csv",sep=""),
                row.names = FALSE)
      parallelStop()
      return(All_instances_mcp)
    },
    
    get_optimum_core = function(mcp_results_path,saveTo){
      mcp_frac = read.csv(paste(mcp_results_path,"/mcp_all_selections_actualruntime_estimatedoverhead.csv",sep = ""))
      mcp_frac = mcp_frac[order(mcp_frac$InstanceName),]
      instances = mcp_frac$InstanceName
      
      df = data.frame(matrix(nrow = nrow(mcp_frac),ncol = 0))
      df$InstanceName = instances
      df$min_number_cores  <- apply(mcp_frac, 1, function(x) colnames(mcp_frac)[which.min(x)])
      df$min_number_cores = str_remove(df$min_number_cores,"X")
      df$mcp_frac  <- apply(mcp_frac, 1, function(x) min(x))
      self$sequentialData$ignore_instances()
      vbs_all = self$sequentialData$get_VBS()
      df$vbs = vbs_all$VBS_Runtime
      runtime = as.numeric(df$vbs)*as.numeric(df$mcp_frac)
      df$mcp = runtime - df$vbs
      df$par10 = runtime
      df$par10[which(df$par10>=4999)] <- 50000
      is_vbs = vector()
      for(row in 1:nrow(df)){
        core = df[row,]$min_number_cores
        if(core>=32){
          core = 32
        } else if(core<=10){
          core = core
        } else {
          core = round(core,-1)
        }
        if(core == 1 && df[row,]$mcp_frac ==1){
          is_vbs = append(is_vbs)
        }
        else{
          overhead_core = read.csv(paste(actual_overhead_per_corePath,"/",core,"-cores-percentage-change-overhead.csv",sep=""))
        }
      }
      write.csv(df,paste(saveTo,"/actualRuntime_estimatedmeanOverhead_mcp.csv",sep = ""),row.names = FALSE)
    },
    #use median overhead estimation for each solver in percentage rate and multiply by each column of solvers -- will create csv for each core
    #you can change the overhead estimation here! 
    #you can use mean instead of median overhead
    #you can use mean and median overhead seconds
    Estimate_overhead_on_prediction = function(predictionPath, cores = c(32,30,20,10:2), overheadPath,saveTo,ignoreTimeouts = TRUE,stat = "median", distr = "emp", type = "percentage-change"){
      prediction = self$get_all_preds(predictionPath)
      if(ignoreTimeouts){
        if(is.null(self$sequentialData$solvedInstances)){
          self$sequentialData$get_VBS()
        }
        prediction = prediction[which(prediction$InstanceName %in% self$sequentialData$solvedInstances),]
      }
      prediction = prediction[order(prediction$InstanceName),]
      rownames(prediction)<- NULL
      solvers = self$sequentialData$solvers
      overhead_files = list.files(overheadPath,".csv",full.names = TRUE )
      for(core in cores){
        overhead_csv = prediction
        for(solver in solvers){
          #get overhead estimation percetange change, median
          file = overhead_files[which(overhead_files ==paste(overheadPath,solver,".csv",sep = ""))]
          overhead = read.csv(file)
          overhead = overhead[order(overhead$InstanceName),]
          if(stat=="median"){
            stat_for_cores = self$solver_median(file)
          } else if(stat=="mean"){
            stat_for_cores = self$solver_mean(file)
          } else {
            #stat should be a number ...
            stat_for_cores = self$solver_quantile(file,distr=distr,quan = stat)
          }
          stat_for_cores = as.numeric(stat_for_cores[paste("X",core,sep = "")])
          if(type == "percentage-change"){
            overhead_csv[solver] = overhead_csv[solver] * stat_for_cores
          } else if(type == "seconds"){
            overhead_csv[solver] = overhead_csv[solver] + stat_for_cores
          }
          overhead_csv[which(overhead_csv[solver]>5000),solver]<- 5000
        }
        write.csv(overhead_csv, paste(saveTo,"/","prediction_overhead_persolver_",core,".csv",sep = ""),row.names = FALSE)
      }
    },
    
    Estimate_actual_overhead_on_prediction = function(predictionPath, cores = c(32,30,20,10:2), overheadPath,saveTo,ignoreTimeouts = TRUE, type = "percentage-change"){
      prediction = self$get_all_preds(predictionPath)
      if(ignoreTimeouts){
        if(is.null(self$sequentialData$solvedInstances)){
          self$sequentialData$get_VBS()
        }
        prediction = prediction[which(prediction$InstanceName %in% self$sequentialData$solvedInstances),]
      }
      prediction = prediction[order(prediction$InstanceName),]
      rownames(prediction)<- NULL
      solvers = self$sequentialData$solvers
      overhead_files = list.files(overheadPath,".csv",full.names = TRUE )
      for(core in cores){
        overhead_csv = prediction
        for(solver in solvers){
          #get overhead estimation percetange change, median
          file = overhead_files[which(overhead_files ==paste(overheadPath,solver,".csv",sep = ""))]
          overhead = read.csv(file)
          overhead = overhead[order(overhead$InstanceName),]
          column = overhead[paste("X",core,sep = "")]
          if(type == "percentage-change"){
            overhead_csv[which(overhead_csv$InstanceName %in% overhead$InstanceName),solver] <- (overhead_csv[which(overhead_csv$InstanceName %in% overhead$InstanceName),solver] * column)
            overhead_csv[which(!(overhead_csv$InstanceName %in% overhead$InstanceName)),solver] <- 5000
            
          } else if(type == "seconds"){
            overhead_csv[which(overhead_csv$InstanceName %in% overhead$InstanceName),solver] <- (overhead_csv[which(overhead_csv$InstanceName %in% overhead$InstanceName),solver] + column)
            overhead_csv[which(!(overhead_csv$InstanceName %in% overhead$InstanceName)),solver] <- 5000
            
            
          }
          overhead_csv[which(overhead_csv[solver]>5000),solver]<- 5000
        }
        write.csv(overhead_csv, paste(saveTo,"/","prediction_overhead_persolver_",core,".csv",sep = ""),row.names = FALSE)
      }
    },
  
    predicted_overhead_per_solver = function(modelPath,saveTo, cores = c(32,30,20,10:2)){
      predicted_overheads = list.files(modelPath,".csv",full.names = TRUE)
      predicted_overheads = predicted_overheads[which(!grepl("wide_",predicted_overheads))]
      for(solver in predicted_overheads){
        csv = read.csv(solver)
        csv = csv[c(1,2,4)]
        if(length(csv[which(csv$response<1),]$response)>0) csv[which(csv$response<1),]$response <- 1
        csv = csv %>% spread(core,response)
        write.csv(csv,paste(saveTo,"/","wide_",tail(str_split(solver,"/")[[1]],1),sep=""),row.names = FALSE)
      }
    },
    
    Estimated_overhead_on_prediction = function(predictionPath, cores = c(32,30,20,10:2), overheadPredictionPath,saveTo,ignoreTimeouts = TRUE, type = "percentage-change"){
      prediction = self$get_all_preds(predictionPath)
      if(ignoreTimeouts){
        if(is.null(self$sequentialData$solvedInstances)){
          self$sequentialData$get_VBS()
        }
        prediction = prediction[which(prediction$InstanceName %in% self$sequentialData$solvedInstances),]
      }
      prediction = prediction[order(prediction$InstanceName),]
      rownames(prediction)<- NULL
      solvers = self$sequentialData$solvers
      overhead_files = list.files(overheadPredictionPath,".csv",full.names = TRUE )
      overhead_files = overhead_files[which(grepl("wide_",overhead_files))]
      for(core in cores){
        overhead_csv = prediction
        for(solver in solvers){
          #get overhead estimation percetange change, median
          file = overhead_files[which(overhead_files == paste(overheadPredictionPath,"wide_",solver,".csv",sep = ""))]
          overhead = read.csv(file)
          overhead = overhead[order(overhead$InstanceName),]
          column = overhead[paste("X",core,sep = "")]
          if(type == "percentage-change"){
            overhead_csv[which(overhead_csv$InstanceName %in% overhead$InstanceName),solver] <- (overhead_csv[which(overhead_csv$InstanceName %in% overhead$InstanceName),solver] * column)
            overhead_csv[which(!(overhead_csv$InstanceName %in% overhead$InstanceName)),solver] <- 5000
          } else if(type == "seconds"){
            overhead_csv[which(overhead_csv$InstanceName %in% overhead$InstanceName),solver] <- (overhead_csv[which(overhead_csv$InstanceName %in% overhead$InstanceName),solver] + column)
            overhead_csv[which(!(overhead_csv$InstanceName %in% overhead$InstanceName)),solver] <- 5000
          }
          overhead_csv[which(overhead_csv[solver]>5000),solver]<- 5000
        }
        write.csv(overhead_csv, paste(saveTo,"/","prediction+predictedoverhead_persolver_",core,".csv",sep = ""),row.names = FALSE)
      }
    },
    
    #here are the steps
    #I have considered results of 10 cores for 10 to 15 cores
    #I have considered results of 20 cores for 16 to 24 cores
    #I have considered results of 30 cores for 25 to 31 cores
    #I have considered results of 10 cores for 32 to 39 cores 
    #for each selection based on "min+preds in SE" method 
    #I multiplied the median overhead value (percentage) to the predicted value
    #ignored solvers which their overhead value is higher than 5000
    #limited the sum of estimated times to 10 cores * 5000 seconds
    #then ignores solvers with higher times.
    
    Do_selection_considering_overhead_and_prediction = function(selectionPath, predictionOverheadPath, saveTo, top_selection = 10){
      instance_csvs = list.files(selectionPath,".csv")
      for(instance_csv in instance_csvs){
        csv = read.csv(paste(selectionPath,instance_csv,sep = ""))
        count_solvers = nrow(csv)
        minpredictedrow = csv[which(csv$PredictedRuntime == min(csv$PredictedRuntime)),]
        while(count_solvers>1){
          if(count_solvers>=32){
            count_solvers = 32
          } else if(count_solvers<=10){
            count_solvers = count_solvers
          } else {
            count_solvers = round(count_solvers,-1)
          }
          overhead_csv = read.csv(paste(predictionOverheadPath,"/prediction_overhead_persolver_"
                                        ,count_solvers,".csv",sep = ""))
          min_predictedOverhead = overhead_csv[which(overhead_csv$InstanceName == paste("sat/",str_split(instance_csv,".csv")[[1]][1],sep="")),minpredictedrow$Solver]
          minpredictedrow$overhead_values = min_predictedOverhead
          selected_solvers = csv$Solver
          related_overhead_row = overhead_csv[which(overhead_csv$InstanceName == paste("sat/",str_split(instance_csv,".csv")[[1]][1],sep="")),] 
          overhead_values <- vector()
          for(solver in selected_solvers){
            overhead_values = append(overhead_values,related_overhead_row[solver])
          }
          overhead_values <- unname(unlist(overhead_values))
          csv$overhead_values <- overhead_values
          csv = csv[order(csv$overhead_values),]
          temp = csv[which(!csv$Solver %in% minpredictedrow$Solver),]
          #if(sum(csv$overhead_values)> nrow(csv)*5000 || nrow(csv)>top_selection){
          if(5000 %in% temp$overhead_values || nrow(csv)>top_selection){
            temp = head(temp,-1)
            if(minpredictedrow$Solver %in% temp$Solver){
              csv = temp
            }
            else{
              csv = rbind(temp,minpredictedrow)
            }
            count_solvers = nrow(csv)    
          }
          else{
            break
          }
        }
        path = self$sequentialData$actual_CSV_path
        path = str_split(path,"/")[[1]]
        path = path[-length(path)]
        path = paste(path, collapse = '/') 
        if(count_solvers !=0){
          if(count_solvers == 1){
            actual_parallel = read.csv(paste(path,"/teton-SAT2018-39-solvers-solo-replacement.csv",sep = ""))
          } else{
            actual_parallel = read.csv(paste(path,"/teton-SAT2018-39-solvers-",
                                           count_solvers,"-parallel-replacement.csv",sep = ""))
          }
          related_row = actual_parallel[which(actual_parallel$InstanceName==paste("sat/",str_split(instance_csv,".csv")[[1]][1],sep="")),]
          for(solver in csv$Solver){
            csv[which(csv$Solver == solver),6]<- related_row[solver]
          }
        }
        write.csv(csv,paste(saveTo,"/",instance_csv,sep = ""),row.names = FALSE)
      }
    },
    
    
    Do_selection_considering_overhead_and_prediction_probability = function(selectionPath, predictionOverheadPath, saveTo, top_selection = 10){
      instance_csvs = list.files(selectionPath,".csv")
      instance_csvs = instance_csvs[1:3]
      for(instance_csv in instance_csvs){
        csv = read.csv(paste(selectionPath,instance_csv,sep = ""))
        count_solvers = nrow(csv)
        minpredictedrow = csv[which(csv$PredictedRuntime == min(csv$PredictedRuntime)),]
        while(count_solvers>1){
          if(count_solvers>=32){
            count_solvers = 32
          } else if(count_solvers<=10){
            count_solvers = count_solvers
          } else {
            count_solvers = round(count_solvers,-1)
          }
          overhead_csv = read.csv(paste(predictionOverheadPath,"/prediction_overhead_persolver_"
                                        ,count_solvers,".csv",sep = ""))
          minpredictedrow$overhead_values = overhead_csv[which(overhead_csv$InstanceName == paste("sat/",str_split(instance_csv,".csv")[[1]][1],sep="")),minpredictedrow$Solver]
          selected_solvers = csv$Solver
          related_overhead_row = overhead_csv[which(overhead_csv$InstanceName == paste("sat/",str_split(instance_csv,".csv")[[1]][1],sep="")),] 
          overhead_values <- vector()
          for(solver in selected_solvers){
            overhead_values = append(overhead_values,related_overhead_row[solver])
          }
          overhead_values <- unname(unlist(overhead_values))
          csv$overhead_values <- overhead_values
          csv = csv[order(csv$overhead_values),]
          probability = vector()
          for(row in 1:nrow(csv)){
            solver = csv[row,]$Solver
            time = csv[row,]$overhead_values
            core = count_solvers
            probability = append(probability,self$probability_solver_time(predictionOverheadPath, solver, time, core))
          }
          csv$Probability = probability
          two = combn(probability,2)
          union_prob = vector()
          for(col in 1:ncol(two)){
            val = sum(two[,col]) - prod(two[,col])
            union_prob = append(union_prob,val)
          }
          max_col_two = two[,which(union_prob == max(union_prob))]
          max_prob_two  = max(union_prob)
          three = combn(probability,3)
          union_prob = vector()
          for(col in 1:ncol(three)){
            val = sum(three[,col]) - prod(three[c(1,2),col]) - prod(three[c(1,3),col]) - prod(three[c(2,3),col]) + prod(three[,col]) 
            union_prob = append(union_prob,val)
          }
          max_col_three = three[,which(union_prob == max(union_prob))]
          max_prob_three  = max(union_prob)
          
          
          
          #temp = csv[which(!csv$Solver %in% minpredictedrow$Solver),]
          #if(sum(csv$overhead_values)> nrow(csv)*5000 || nrow(csv)>top_selection){
          if(5000 %in% temp$overhead_values || nrow(csv)>top_selection){
            #temp = head(temp,-1)
            csv = head(temp,-1)
            #if(minpredictedrow$Solver %in% temp$Solver){
            #  csv = temp
            #}
            #else{
            #  csv = rbind(temp,minpredictedrow)
            #}
            count_solvers = nrow(csv)    
          }
          else{
            break
          }
        }
        path = self$sequentialData$actual_CSV_path
        path = str_split(path,"/")[[1]]
        path = path[-length(path)]
        path = paste(path, collapse = '/') 
        if(count_solvers !=0){
          if(count_solvers == 1){
            actual_parallel = read.csv(paste(path,"/teton-SAT2018-39-solvers-solo-replacement.csv",sep = ""))
          } else{
            actual_parallel = read.csv(paste(path,"/teton-SAT2018-39-solvers-",
                                             count_solvers,"-parallel-replacement.csv",sep = ""))
          }
          related_row = actual_parallel[which(actual_parallel$InstanceName==paste("sat/",str_split(instance_csv,".csv")[[1]][1],sep="")),]
          for(solver in csv$Solver){
            csv[which(csv$Solver == solver),6]<- related_row[solver]
          }
        }
        write.csv(csv,paste(saveTo,"/",instance_csv,sep = ""),row.names = FALSE)
      }
    },
    
    
    Do_selection_considering_predicted_overhead_and_prediction = function(selectionPath, OverheadOnPredictionPath, saveTo, top_selection = 10){
      instance_csvs = list.files(selectionPath,".csv")
      for(instance_csv in instance_csvs){
        csv = read.csv(paste(selectionPath,instance_csv,sep = ""))
        count_solvers = nrow(csv)
        while(count_solvers>1){
          if(count_solvers>=32){
            count_solvers = 32
          } else if(count_solvers<=10){
            count_solvers = count_solvers
          } else {
            count_solvers = round(count_solvers,-1)
          }
          overhead_csv = read.csv(paste(predictionOverheadPath,"/prediction+predictedoverhead_persolver_"
                                        ,count_solvers,".csv",sep = ""))
          overhead_csv[is.na(overhead_csv)] <- 5000
          selected_solvers = csv$Solver
          related_overhead_row = overhead_csv[which(overhead_csv$InstanceName == paste("sat/",str_split(instance_csv,".csv")[[1]][1],sep="")),] 
          overhead_values <- vector()
          for(solver in selected_solvers){
            overhead_values = append(overhead_values,related_overhead_row[solver])
          }
          overhead_values <- unname(unlist(overhead_values))
          csv<- cbind(csv,overhead_values)  
          if(sum(csv$overhead_values)> nrow(csv)*5000 || nrow(csv)>top_selection){
            csv = csv[order(csv$overhead_values),]
            csv = head(csv,-1)
            count_solvers = nrow(csv)    
          }
          else{
            break
          }
        }
        path = self$sequentialData$actual_CSV_path
        path = str_split(path,"/")[[1]]
        path = path[-length(path)]
        path = paste(path, collapse = '/') 
        if(count_solvers !=0){
          if(count_solvers == 1){
            actual_parallel = read.csv(paste(path,"/teton-SAT2018-39-solvers-solo-replacement.csv",sep = ""))
          } else{
            actual_parallel = read.csv(paste(path,"/teton-SAT2018-39-solvers-",
                                             count_solvers,"-parallel-replacement.csv",sep = ""))
          }
          related_row = actual_parallel[which(actual_parallel$InstanceName==paste("sat/",str_split(instance_csv,".csv")[[1]][1],sep="")),]
          for(solver in csv$Solver){
            csv[which(csv$Solver == solver),6]<- related_row[solver]
          }
        }
        write.csv(csv,paste(saveTo,"/",instance_csv,sep = ""),row.names = FALSE)
      }
    },
    
    Summary_results_selection = function(finalSelectionPath){
      instance_csvs = list.files(finalSelectionPath,".csv",full.names = TRUE)
      overhead_runtimes = vector()
      sequential_runtimes = vector()
      vbs_runtime = vector()
      nrows = vector()
      data = data.frame(matrix(nrow=0,ncol=5))
      for(instance in instance_csvs){
        csv = read.csv(instance)
        if(nrow(csv)>0){
          min_estimation_runtime = min(csv$overhead_values)
          min_actual_parallel_runtime = min(csv$ParallelRuntime)
          min_sequential_runtimes = min(csv$SequentialRuntime)
          vbs_runtime = csv$VBSRuntime[1]
          n_selected_solvers = nrow(csv)
        } else{
          min_estimation_runtime = 5000
          min_sequential_runtimes = 5000
          min_actual_parallel_runtime = 5000
          vbs_runtime = self$sequentialData$get_VBS()
          vbs_runtime = vbs_runtime[which(vbs_runtime$InstanceName == paste("sat/",str_split(tail(str_split(instance,"/")[[1]],1),".csv")[[1]][1],sep = "")),]$VBS_Runtime
          n_selected_solvers = 0
        }
        row = c(str_split(tail(str_split(instance,"/")[[1]],1),".csv")[[1]][1],vbs_runtime,min_sequential_runtimes,min_actual_parallel_runtime,min_estimation_runtime,n_selected_solvers)
        data = rbind(row,data)
      }
      colnames(data)= c("instance","vbs_runtime","min_sequential_runtimes","min_actual_parallel_runtime","min_estimation_runtime","n_selected_solvers")
      #vbs_not_selected= data[which(data$vbs_runtime!=data$min_sequential_runtimes),]
      method = 1
      directory = "./min + preds in SE"
      vbs = as.numeric(data$vbs_runtime)
      selec_seq = as.numeric(data$min_sequential_runtimes)
      selec_est = as.numeric(data$min_estimation_runtime)
      selec_par = as.numeric(data$min_actual_parallel_runtime)
      
      table = data.frame(matrix(nrow=0,ncol = 8))
      #success
      rowSuccess <- c("Success",directory,method,mean(vbs<5000),mean(selec_seq<5000),mean(selec_par<5000),mean(selec_est<5000),
                      mean(as.numeric(data$n_selected_solvers)),median(as.numeric(data$n_selected_solvers)),mean(selec_seq == vbs))
      table = rbind(table,rowSuccess)
      rowMCP <- c("MCP",directory,method,0,mean(selec_seq-vbs),mean(selec_par-vbs),mean(selec_est-vbs),
                  mean(as.numeric(data$n_selected_solvers)),median(as.numeric(data$n_selected_solvers)),mean(selec_seq == vbs))
      table = rbind(table,rowMCP)
      vbs[which(vbs>=5000)]<-50000
      selec_seq[which(selec_seq>=5000)]<-50000
      selec_par[which(selec_par>=5000)]<-50000
      selec_est[which(selec_est>=5000)]<-50000
      rowPar10 <- c("Par10",directory,method,mean(vbs),mean(selec_seq),mean(selec_par),mean(selec_est),
                    mean(as.numeric(data$n_selected_solvers)),median(as.numeric(data$n_selected_solvers)),mean(selec_seq == vbs))
      table = rbind(table,rowPar10)
      
      colnames(table) <- c("Metric","directory","selectionMethod","VBS","SQUENTIAL","PARALLEL","ESTIMATED","N_SOLVERS_MEAN","N_SOLVERS_MEDIAN","VBS_SELECTION")
      return(table)
      },
    
    #get solver csv
    #overhead computations
    #used second if you want overhead in terms of seconds
    
    probability_solver_time = function(Estimate_overhead_on_predictionPath, solver, time, core){
      library(EnvStats)
      overhead_csv = read.csv(paste(Estimate_overhead_on_predictionPath,"/prediction_overhead_persolver_"
                                    ,core,".csv",sep = ""))
      overhead_csv = overhead_csv[solver]
      prob = pemp(time,unlist(overhead_csv))
      return(prob)
    },
    
    solver_mean = function(file) {
      csv = read.csv(file)
      mean = colMeans(csv[2:13])
      mean <- append(file,mean)
      return(mean)
    },
    
    solver_median = function(file) {
      csv = read.csv(file)
      median = apply(csv[2:13],2, median)
      median <- append(file,median)
      return(median)
    },
    
    solver_quantile = function(file,distr="emp",quan) {
      csv = read.csv(file)
      result = vector()
      if(distr == "cauchy"){
        fitDist = apply(csv[2:13],2, fitdist,distr = distr)
        for(i in 1:length(fitDist)){
          result = append(result,qcauchy(quan,location = fitDist[[i]]$estimate[1], scale = fitDist[[i]]$estimate[2]))
        }
      } else if(distr == "gamma"){
        fitDist = apply(csv[2:13],2, fitdist,distr = distr)
        for(i in 1:length(fitDist)){
          result = append(result,qgamma(quan,shape = fitDist[[i]]$estimate[1], rate = fitDist[[i]]$estimate[2]))
        }
      } else if(distr =="exp"){
        fitDist = apply(csv[2:13],2, fitdist,distr = distr)
        for(i in 1:length(fitDist)){
          result = append(result,qexp(quan,rate = fitDist[[i]]$estimate[1]))
        }
      } else if(distr == "emp"){
        result = apply(csv[2:13],2,quantile,quan)
      }
      names(result) <- c("X2","X3","X4","X5","X6","X7","X8","X9","X10","X20","X30","X32")
      result <- append(file,result)
      return(result)
    },
    
    compute_difference = function(csv1,csv2) {
      csv = data.frame(matrix(nrow = nrow(csv1),ncol = 13))
      csv[1] = csv1[1]
      csv[2:13] = abs((csv1[2:13] - csv2[2:13]))
      return(csv)
    },
    
    train_overhead_model = function(solver_overhead_path,ignoreTimeouts=TRUE,trainingcsvPath,modelPath,type = "percentage-change"){
      solvers = list.files(solver_overhead_path,pattern = ".csv",full.names = TRUE)
      c = c(2:10,20,30,32)
      if(ignoreTimeouts) self$sequentialData$ignore_instances()
      instance_features = self$sequentialData$get_features()
      colnames(instance_features)[1] = "InstanceName"
      for(solver in solvers){
        csv_solver = read.csv(solver)
        csv_solver = csv_solver[order(csv_solver$InstanceName),]
        solved_instances = instance_features[is.element(instance_features$InstanceName,csv_solver$InstanceName),]
        colnames(csv_solver)<- c("InstanceName",c)
        if(type == "percentage-change"){
          csv_solver = gather(csv_solver,cores,overhead_percentage,2:13,factor_key = TRUE)
          csv_solver = merge(solved_instances,csv_solver,by = "InstanceName")
          #remove timeouts
          csv_solver = csv_solver[which(csv_solver$overhead_percentage!=0),]
          #reduced overheads
          if(length(csv_solver[which(csv_solver$overhead_percentage<1),]$overhead_percentage)>0) csv_solver[which(csv_solver$overhead_percentage<1),]$overhead_percentage <- 1
        } else if(type == "seconds"){
          csv_solver = gather(csv_solver,cores,overhead_seconds,2:13,factor_key = TRUE)
          csv_solver = merge(solved_instances,csv_solver,by = "InstanceName")
          #reduced overheads
          if(length(csv_solver[which(csv_solver$overhead_percentage<0),]$overhead_seconds)>0) csv_solver[which(csv_solver$overhead_percentage<0),]$overhead_seconds <- 0
        }
        write.csv(csv_solver,paste(trainingcsvPath,"/", tail(str_split(solver,"/")[[1]],1),sep = ""),row.names = FALSE)
      }
      solvers = list.files(trainingcsvPath,pattern = ".csv",full.names = TRUE)
      for(solver in solvers){
        solverdata = read.csv(solver)
        instances = solverdata[1]
        cores = solverdata$cores
        solverdata = solverdata[-1]
        solvername = str_split(tail(str_split(solver,"/")[[1]],1),".csv")[[1]][1]
        colnames(solverdata)[56]<- solvername
        solverTask <- makeRegrTask(data = solverdata, target = solvername)
        Learner = makeLearner("regr.randomForest",predict.type = "se")
        #forestParamSpace <- makeParamSet(makeIntegerParam("ntree", lower = 1, upper = 50),
        #                                  makeIntegerParam("mtry", lower = 1, upper = 50))
        #randSearch <- makeTuneControlRandom(maxit = 100)
        #cvForTuning <- makeResampleDesc("CV", iters = 5)
        CV = makeResampleDesc("CV",iters=10 ,predict = "both")
        #parallelStartSocket(cpus = detectCores())
        #tunedForestPars <- tuneParams(Learner, task = solverTask, resampling = cvForTuning, par.set = forestParamSpace, control = randSearch)
        #parallelStop() 
        
        parallelStartSocket(cpus = detectCores())
        #tunedForest <- setHyperPars(Learner, par.vals = tunedForestPars$x) 
        model <- resample(Learner, solverTask,resampling = CV,models = TRUE)
        parallelStop() 
        preds = model$pred$data
        preds = preds[order(preds$id),]
        preds = preds[which(preds$set == "test"),]
        rownames(preds) <- NULL
        preds = cbind(cores,preds)
        preds = cbind(instances,preds)
        preds = preds[-3]
        #res = resample(Learner,solverTask,resampling = CV ,models = TRUE)
        saveRDS(model,paste(modelPath,"/",str_split(tail(str_split(solver,"/")[[1]],1),".csv")[[1]][1],".rds",sep = ""))
        write.csv(preds , paste(modelPath,"/",str_split(tail(str_split(solver,"/")[[1]],1),".csv")[[1]][1],".csv",sep = ""),row.names = FALSE)
      }
      
    },
    
    train_overhead_model_seprated_cores = function(solver_overhead_path,cores = c(32,30,20,10:2), ignoreTimeouts=TRUE,trainingcsvPath,modelPath,type = "percentage-change"){
      solvers = list.files(solver_overhead_path,pattern = ".csv",full.names = TRUE)
      if(ignoreTimeouts) self$sequentialData$ignore_instances()
      instance_features = self$sequentialData$get_features()
      colnames(instance_features)[1] = "InstanceName"
      for(solver in solvers){
        csv_solver = read.csv(solver)
        csv_solver = csv_solver[order(csv_solver$InstanceName),]
        for(core in cores){
          csv_core = csv_solver[c("InstanceName",paste("X",core,sep = ""))]
          solved_instances = instance_features[is.element(instance_features$InstanceName,csv_core$InstanceName),]
          colnames(csv_core)<- c("InstanceName",core)
          if(type == "percentage-change"){
            csv_core = merge(solved_instances,csv_core,by = "InstanceName")
            colnames(csv_core)[ncol(csv_core)] <- "overhead_percentage"
            #remove timeouts
            csv_core = csv_core[which(csv_core$overhead_percentage!=0),]
            #reduced overheads
            if(length(csv_core[which(csv_core$overhead_percentage<1),]$overhead_percentage)>0) csv_core[which(csv_core$overhead_percentage<1),]$overhead_percentage <- 1
          } else if(type == "seconds"){
            csv_core = merge(solved_instances,csv_core,by = "InstanceName")
            colnames(csv_core)[ncol(csv_core)] <- "overhead_seconds"
            #reduced overheads
            if(length(csv_core[which(csv_core$overhead_percentage<0),]$overhead_seconds)>0) csv_core[which(csv_core$overhead_percentage<0),]$overhead_seconds <- 0
          }
          write.csv(csv_core,paste(trainingcsvPath,"/",core,"_", tail(str_split(solver,"/")[[1]],1),sep = ""),row.names = FALSE)
        }
      }
      solvers = list.files(trainingcsvPath,pattern = ".csv",full.names = TRUE)
      for(solver in solvers){
        solverdata = read.csv(solver)
        instances = solverdata[1]
        solverdata = solverdata[-1]
        solvername = str_split(tail(str_split(solver,"/")[[1]],1),".csv")[[1]][1]
        solvername = 
          
        colnames(solverdata)[ncol(solverdata)]<- solvername
        solverTask <- makeRegrTask(data = solverdata, target = solvername)
        Learner = makeLearner("regr.randomForest",predict.type = "se")
        #forestParamSpace <- makeParamSet(makeIntegerParam("ntree", lower = 1, upper = 50),
        #                                  makeIntegerParam("mtry", lower = 1, upper = 50))
        #randSearch <- makeTuneControlRandom(maxit = 100)
        #cvForTuning <- makeResampleDesc("CV", iters = 5)
        CV = makeResampleDesc("CV",iters=10 ,predict = "both")
        #parallelStartSocket(cpus = detectCores())
        #tunedForestPars <- tuneParams(Learner, task = solverTask, resampling = cvForTuning, par.set = forestParamSpace, control = randSearch)
        #parallelStop() 
        
        parallelStartSocket(cpus = detectCores())
        #tunedForest <- setHyperPars(Learner, par.vals = tunedForestPars$x) 
        model <- resample(Learner, solverTask,resampling = CV,models = TRUE)
        parallelStop() 
        preds = model$pred$data
        preds = preds[order(preds$id),]
        preds = preds[which(preds$set == "test"),]
        rownames(preds) <- NULL
        preds = cbind(cores,preds)
        preds = cbind(instances,preds)
        preds = preds[-3]
        #res = resample(Learner,solverTask,resampling = CV ,models = TRUE)
        saveRDS(model,paste(modelPath,"/",str_split(tail(str_split(solver,"/")[[1]],1),".csv")[[1]][1],".rds",sep = ""))
        write.csv(preds , paste(modelPath,"/",str_split(tail(str_split(solver,"/")[[1]],1),".csv")[[1]][1],".csv",sep = ""),row.names = FALSE)
      }
      
    }
  )
)
