if(Sys.info()['sysname']=="Linux"){
  if(file.exists("~/Documents/OrganizedScripts/OverheadResults.R")){
    source("~/Documents/OrganizedScripts/OverheadResults.R")
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
    source("/gscratch/hkashgar/OrganizedScripts/OverheadResults.R")
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
  source("C:/Users/hnyk9/OneDrive - University of Wyoming/OrganizedScripts/OverheadResults.R")
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

#checking the code
#---------------
# self = SequentialPerformance$new(benchmarks_name = "MAXSAT2019")
# self$benchmarks_name
# self$cores
# self$cores_str
# self$Cutoff
# self$actual_CSV_path
# self$features_path
# self$n_solvers
# self$n_instances
# self$solvers
# self$actual_CSV
# self$get_scenario()
# self$get_actual_result_csv()
# self$get_par10_dataframe()
# self$par10_CSV
# self$get_mcp_dataframe(sequentialData = SequentialPerformance$new(benchmarks_name = "MAXSAT2019"))
# self$mcp_CSV
# self$get_optimal_runtime()
# self$get_solved_instances()
# self$get_unsolved_instances()
# self$unsolvedInstances
# self$solvedInstances
# self$ignore_instances()
# self$get_VBS()
# self$get_VBS_par10()
# self$get_VBS_mcp()
# self$get_solved_instances()
# self$get_unsolved_instances()
# self$get_SBS()
# self$get_solvers_solved_runtime("Open.WBO.ms.pre")
# self$get_actual_result_csv()
# #
# self$get_mcp_dataframe(sequentialData = self)
# self$ignore_instances()
# self$get_features()
# self$features
# self$get_nd_vbs_runtime(nd=2)
# self$get_nd_VBS(nd = 4)
# nrow(self$get_nd_VBS(nd = 4))
#split_dataframe_by_solver should be fixed

#---------------
#training 
#---------------

# self = SequentialPerformance$new(benchmarks_name = "MAXSAT2019")
# self$train_randomForest_aslibLike(savepath = modelPath, ignoreTimeouts = FALSE, train_by_par10 = FALSE)
# predictions = readRDS(paste(modelPath,"/randomForest_predictions.RDS",sep=""))
# predictions$predictions
# self = PredictionResults$new("MAXSAT2019")
# self$get_models_prediction()

# vbs
# self = SequentialPerformance$new(benchmarks_name = "MAXSAT2019")
# vbs = self$get_VBS()
# mean(vbs$VBS_Runtime)
# median(vbs$VBS_Runtime)
# vbs_par10 = self$get_VBS_par10()
# mean(vbs_par10$VBS_Runtime)
# median(vbs_par10$VBS_Runtime)
# vbs_mcp = self$get_VBS_mcp()
# vbs_success = sum(vbs$VBS_Runtime<3600)
# vbs_success/nrow(vbs)*100
# # 
# # 
# # #sbs
# sbs_solver = self$get_SBS()
# sbs = self$actual_CSV[sbs_solver][[1]]
# mean(sbs)
# median(sbs)
# sbs_par10 = self$get_par10_dataframe()[sbs_solver][[1]]
# mean(sbs_par10)
# median(sbs_par10)
# sbs_mcp = self$get_mcp_dataframe(self)[sbs_solver][[1]]
# mean(sbs_mcp)
# median(sbs_mcp)
# sbs_success = sum(sbs<3600)
# sbs_success/length(sbs)*100
# # 
# # # AS
# self = PredictionResults$new("MAXSAT2019")
# as = self$Single_Algorithm_Selection(ignoreTimeoutsOnVBS = FALSE)
# mean(as$ActualRuntime)
# median(as$ActualRuntime)
# mean(as$Par10)
# median(as$Par10)
# mean(as$MCP)
# median(as$MCP)
# sum(as$ActualRuntime<3600)
# sum(as$ActualRuntime<3600)/nrow(as)*100
# 
# # # top vbs 
# self = SequentialPerformance$new(benchmarks_name = "MAXSAT2019")
# range = c(1:self$n_solvers)
# top_vbs = data.frame(matrix(nrow = nrow(vbs), ncol = 0))
# top_vbs = cbind(top_vbs, vbs$InstanceName)
# for(i in range){
#   par = ParallelLevel$new(benchmarks_name = "MAXSAT2019", cores = i)
#   top_n_vbs = vector()
#   for(j in 1:i){
#     nd_vbs = par$get_nd_vbs_runtime(instanceset = vbs$InstanceName, ignore_instances = FALSE, nd = j)
#     top_n_vbs = cbind(top_n_vbs, nd_vbs$VBS_Runtime)
#   }
#   nd_vbs = rowMins(top_n_vbs)
#   top_vbs = cbind(top_vbs,nd_vbs)
# }
# colnames(top_vbs) = c("InstanceName", str_c(rep("cores_",self$n_solvers), c(1:self$n_solvers)))
# write.csv(top_vbs, "~/Documents/OrganizedScripts/results/MAXSAT2019/top_vbs.csv", row.names = FALSE)
# 
# # top sbs
# top_sbs = data.frame(matrix(nrow = nrow(vbs), ncol = 0))
# top_sbs = cbind(top_sbs, vbs$InstanceName)
# for(i in range){
#   solvers = colnames(self$actual_CSV[2:ncol(self$actual_CSV)])
#   means = colMeans(self$actual_CSV[2:ncol(self$actual_CSV)])
#   top_n_sbs = vector()
#   for(j in 1:i){
#     idx = which(means==min(means))
#     top_n_sbs = append(top_n_sbs,solvers[idx])
#     solvers = solvers[-idx]
#     means = means[-idx]
#   }
#   top_n_sbs
#   par = ParallelLevel$new(benchmarks_name = "MAXSAT2019",i)
#   nd_sbs = par$get_actual_result_csv()[top_n_sbs]
#   nd_sbs = rowMins(as.matrix(nd_sbs))
#   print(par$get_actual_result_csv()$InstanceName == vbs$InstanceName)
#   top_sbs = cbind(top_sbs,nd_sbs)
# }
# colnames(top_sbs) = c("InstanceName", str_c(rep("cores_",self$n_solvers), c(1:self$n_solvers)))
# mean(top_sbs$cores_7)
# write.csv(top_sbs, "~/Documents/OrganizedScripts/results/MAXSAT2019/top_sbs.csv", row.names = FALSE)
# # read.cs
# #top AS, no uncertainty just top selected 
#method number help:
# -1 : running all in parallel, no selection just ordering based on prediction, (top_selection, orderBy doesn't work here)
# 0 : algorithm selection, selection besed on predicted runtime, top_selection will choose top algorithms from data frame based on prediction
# 1 : minpred <= pred <= [minpred + delta_prime*SE]
# 2 : lowebound as good as min pred, [pred-delta*SE]<=minpred
# 3 : generalized 2 and 1; p-delta*se <= minP + deltaPrime*SE_min
# 4 : [minpred-delta_prime*SE]<=[pred-delta*SE]<=minpred
# selectionPath = "/home/haniye//Documents/OrganizedScripts/results/MAXSAT2019/selections_algorithmSelection_noUncertainty/7_cores/"
# self = PredictionResults$new("MAXSAT2019")
# summary = self$get_summary_all(method_numbers = 0,top_selections = c(7), selectionPath = selectionPath)
# write.arff(summary,"~/Documents/OrganizedScripts/results/MAXSAT2019/top_as_noUncertainty.arff")


# self=PredictionResults$new("MAXSAT2019")
# self$get_summary_selection_result(selectionPath = "~/Documents/OrganizedScripts/results/MAXSAT2019/selections_different_th/theta_2/",
#                                    ignoreTimeouts = FALSE,
#                                    method_number = 3,
#                                    median = FALSE)


#jointprobability stuff
# self = PredictionResults$new("MAXSAT2019")
# range = seq(0,1,by=0.001)
# min = Inf
# optimum = Inf
# range = range[883:1001]
# for(r in range){
#   dir.create(paste("~/Documents/OrganizedScripts/results/MAXSAT2019/JointProbability/tau_",r,sep = ""))
#   self$selection_based_on_SE(predictionPath = self$predictionPath,
#                              saveTo = paste("~/Documents/OrganizedScripts/results/MAXSAT2019/JointProbability/tau_",r,sep=""),
#                              method_number = 5,
#                              top_selection = 10,
#                              ignoreTimeoutsOnVBS = FALSE,
#                              orderBy = "pred",
#                              delta = 0,
#                              delta_prime = 0,
#                              alpha = 0,
#                              JP_limit = r)
#   summary = self$get_summary_selection_result( paste("~/Documents/OrganizedScripts/results/MAXSAT2019/JointProbability/tau_",r,sep=""),
#                                                ignoreTimeouts = FALSE,
#                                                method_number = 5,
#                                                median = FALSE)
#   print(r)
#   print(summary)
#   if(as.numeric(summary[[1]]$Parallel_time)<=min){
#     min = as.numeric(summary[[1]]$Parallel_time)
#     optimum = r
#   }
# }
# optimum = 0.131
optimum = 0.549
self = PredictionResults$new("MAXSAT2019")
summary = self$get_summary_selection_result(paste("~/Documents/OrganizedScripts/results/MAXSAT2019/JointProbability/tau_",optimum,sep=""),
                                             ignoreTimeouts = FALSE,
                                             method_number = 5,
                                             median = FALSE)

for(i in c(1:7)){
    self$selection_based_on_SE(predictionPath = self$predictionPath,
                               saveTo = paste("~/Documents/OrganizedScripts/results/MAXSAT2019/joint_optimal/",i, "-core",sep=""),
                               method_number = 5,
                               top_selection = i,
                               ignoreTimeoutsOnVBS = FALSE,
                               orderBy = "pred",
                               delta = 0,
                               delta_prime = 0,
                               alpha = 0,
                               JP_limit = optimum)
}
i = 7
summary = self$get_summary_selection_result(paste("~/Documents/OrganizedScripts/results/MAXSAT2019/joint_optimal/",i,"-core",sep=""),
                                            ignoreTimeouts = FALSE,
                                            method_number = 5,
                                            median = FALSE)
summary
# theta = read.csv("~/Documents/OrganizedScripts/results/MAXSAT2019//RandomSearch_MAXSAT2019_combined_allEqual_NOTignoreTO_300.csv")
# theta = theta[which(theta$metric=="Runtime"),]
# theta = theta[which(theta$median==FALSE),]
# plot(x = theta$delta, y = theta$Parallel_time)
# #best =  0.1116461, runtime = 110.3998 
# theta = theta[which(theta$Parallel_time == min(theta$Parallel_time)),]
# theta = theta$delta[1]
# range =c(1:7)
# theta = 0.0625
# selectionPath = "~/Documents/OrganizedScripts/results/MAXSAT2019/selections_optimal_theta_0.0625/selection_optimal_theta_7_cores/"
# self = PredictionResults$new("MAXSAT2019")
# summary = self$get_summary_all(method_numbers = 3,top_selections = 7, predictionPath = self$predictionPath,
# selectionPath = selectionPath, ignoreTimeoutsOnVBS = FALSE, median = FALSE,
# delta = theta, alpha = theta, delta_prime = theta)
# 
# write.arff(summary,"~/Documents/OrganizedScripts/results/MAXSAT2019/top_Uncertainty_Theta_0.1098642_limitingSolvers.arff")

#runtime

setwd("~/Documents/OrganizedScripts/results/MAXSAT2019/")
library(reshape2)
top_vbs = read.csv("top_vbs.csv")
top_vbs[2:8] = apply(top_vbs[2:8],2,as.numeric)

sd = apply(top_vbs[2:8],2,sd)
mean = apply(top_vbs[2:8],2,mean)
median = apply(top_vbs[2:8],2,median)
sum_top_vbs = data.frame(mean = mean, median = median, sd = sd)
sum_top_vbs$cores = c(1:7)
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
p
getwd()
ggsave(dpi = 500, width = 7, height = 5, filename = "VBS_behavior_different_cores_runtime.pdf")

top_sbs = read.csv("top_sbs.csv")
top_sbs[2:8] = apply(top_sbs[2:8],2,as.numeric)

sd = apply(top_sbs[2:8],2,sd)
mean = apply(top_sbs[2:8],2,mean)
median = apply(top_sbs[2:8],2,median)
sum_top_sbs = data.frame(mean = mean, median = median, sd = sd)
sum_top_sbs$cores = c(1:7)
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
p
ggsave(filename = "SBS_behavior_different_cores_runtime.pdf",dpi = 500, width = 7, height = 5)


results = data.frame(matrix(nrow= 0, ncol=4))
approaches = c("Single Best Solver", "Virtual Best Solver",
               "AS_0", "AS_theta")
# aspeed_mean = read.csv("aspeed_1_to_7_cores.csv")
for(approach in approaches){
  sub_df = data.frame(matrix(nrow= 7, ncol=0))
  sub_df$Cores = c(1:7)
  sub_df$Approach = approach
  if(approach == "Virtual Best Solver"){
    sub_df$Mean = as.numeric(sum_top_vbs$mean)
    sub_df$Median = as.numeric(sum_top_vbs$median)
  } else if(approach == "Single Best Solver"){
    sub_df$Mean = as.numeric(sum_top_sbs$mean)
    sub_df$Median = as.numeric(sum_top_sbs$median)
  } else if(approach == "ASPEED"){
    means = vector()
    medians = vector()
    saveCsv = data.frame(matrix(nrow = 572, ncol=0))
    for(c in sub_df$Cores){
      csv = read.csv(paste("~/Documents/OrganizedScripts/results/aspeed_3folds_parallelTestFile/MaxSAT19/MAXSAT2019_",c,"cores_print.error",sep=""))
      aspeed = csv$ASP
      saveCsv[paste("cores_",c,sep="")] = aspeed
      means = append(means, mean(aspeed))
      medians = append(medians, median(aspeed))
    }
    write.csv(saveCsv,"top_aspeed.csv", row.names = FALSE)
    sub_df$Mean = as.numeric(means)
    sub_df$Median = as.numeric(medians)
  } else if(approach == "AS_0"){
    means = vector()
    medians = vector()
    saveCsv = data.frame(matrix(nrow = 572, ncol=0))
    for(c in sub_df$Cores){
      runtimes = vector()
      path = paste("~/Documents/OrganizedScripts/results/MAXSAT2019/selections_algorithmSelection_noUncertainty/",c,"_cores/",sep="")
      csvs = list.files(path,".csv")
      for(csv in csvs){
        df = read.csv(paste(path,csv,sep=""))
        runtime = min(df$ParallelRuntime)
        runtimes = append(runtimes,runtime)
      }
      saveCsv[paste("cores_",c,sep="")] = runtimes
      means = append(means, mean(runtimes))
      medians = append(medians, median(runtimes))
    }
    write.csv(saveCsv,"top_as_0.csv", row.names = FALSE)
    sub_df$Mean = as.numeric(means)
    sub_df$Median = as.numeric(medians)
  } else if(approach == "AS_theta"){
    means = vector()
    medians = vector()
    saveCsv = data.frame(matrix(nrow = 572, ncol=0))
    for(c in sub_df$Cores){
      runtimes = vector()
      path = paste("~/Documents/OrganizedScripts/results/MAXSAT2019/joint_optimal/",c,"-core/",sep="")
      csvs = list.files(path,".csv")
      for(csv in csvs){
        df = read.csv(paste(path,csv,sep=""))
        runtime = min(df$ParallelRuntime)
        runtimes = append(runtimes,runtime)
      }
      saveCsv[paste("cores_",c,sep="")] = runtimes
      means = append(means, mean(runtimes))
      medians = append(medians, median(runtimes))
    }
    write.csv(saveCsv,"top_as_theta.csv", row.names = FALSE)
    sub_df$Mean = as.numeric(means)
    sub_df$Median = as.numeric(medians)
  }
  results = rbind(results,sub_df)
}

results$Mean = as.numeric(results$Mean)
results$Median = as.numeric(results$Median)
ggplot(results, aes(x=Cores, y=Mean, colour = Approach, shape = Approach)) +
  geom_point(size = 3)+
  geom_line(, size = 1)+
  # geom_line(aes(linetype="Mean"), size = 1)+
  # geom_point(aes(y=Median),size = 3)+
  # geom_line(aes(y = Median, linetype = "Median"), size = 1)+
  guides(linetype=guide_legend(title="",keywidth = 3, keyheight = 1.5),
         colour = guide_legend(keywidth = 3, keyheight = 1.5))+
  expand_limits(x = 1, y = 0)+ theme(text=element_text(size=22,  family="Times"))+
  labs(x = "Cores", y = "Runtime (s)", title = "MAXSAT19-UCMS")+theme(plot.title = element_text(hjust = 0.5))+
  scale_x_continuous(breaks=c(1:7))+
  scale_color_discrete(labels=c(bquote(AS[0]), bquote(AS[~theta]), 'ASPEED', 'Single Best Solver','Virtual Best Solver'))+
  scale_shape_discrete(labels=c(bquote(AS[0]), bquote(AS[~theta]), 'ASPEED', 'Single Best Solver','Virtual Best Solver'))+
  scale_y_continuous(trans='log10')

ggsave(dpi = 500, width = 9, height = 5, filename = "MAXSAT19_line_chart_parallel_runtime.pdf")
results[which(results$Cores == 7),]

#MCP 
setwd("~/Documents/OrganizedScripts/results/MAXSAT2019/")
library(reshape2)
top_vbs = read.csv("top_vbs_mcp.csv")
top_vbs[1:7] = apply(top_vbs[1:7],2,as.numeric)

sd = apply(top_vbs[1:7],2,sd)
mean = apply(top_vbs[1:7],2,mean)
median = apply(top_vbs[1:7],2,median)
sum_top_vbs = data.frame(mean = mean, median = median, sd = sd)
sum_top_vbs$cores = c(1:7)
sum_top_vbs = sum_top_vbs[which(!(sum_top_vbs$cores%in% c(11:19,20:29,31, 33:38))),]

p<-ggplot(sum_top_vbs, aes(x=cores, y=mean,colour="Mean VBS MCP")) +
  geom_point()+
  geom_point(aes(y=median,colour="Median VBS MCP"))+
  geom_errorbar(aes(ymin=mean-sd,
                    ymax=mean+sd), width=.2,
                position=position_dodge(0.05))+
  scale_y_continuous(
    name = "MCP"
    #sec.axis = sec_axis( trans=~./self$Cutoff , name="probability of solving instance RegRF prediction")
  )
p
getwd()
ggsave(dpi = 500, width = 7, height = 5, filename = "VBS_behavior_different_cores_MCP.pdf")

top_sbs = read.csv("top_sbs_mcp.csv")
top_sbs[1:7] = apply(top_sbs[1:7],2,as.numeric)

sd = apply(top_sbs[1:7],2,sd)
mean = apply(top_sbs[1:7],2,mean)
median = apply(top_sbs[1:7],2,median)
sum_top_sbs = data.frame(mean = mean, median = median, sd = sd)
sum_top_sbs$cores = c(1:7)
sum_top_sbs = sum_top_sbs[which(!(sum_top_sbs$cores%in% c(11:19,20:29,31, 33:38))),]

p<-ggplot(sum_top_sbs, aes(x=cores, y=mean,colour="Mean SBS MCP")) +
  geom_point()+
  geom_point(aes(y=median,colour="Median SBS MCP"))+
  geom_errorbar(aes(ymin=mean-sd,
                    ymax=mean+sd), width=.2,
                position=position_dodge(0.05))+
  scale_y_continuous(
    name = "MCP"
    #sec.axis = sec_axis( trans=~./self$Cutoff , name="probability of solving instance RegRF prediction")
  )
p
ggsave(filename = "SBS_behavior_different_cores_MCP.pdf",dpi = 500, width = 7, height = 5)


results = data.frame(matrix(nrow= 0, ncol=4))
approaches = c("Single Best Solver", "Virtual Best Solver", "ASPEED", 
               "AS_0", "AS_theta")
for(approach in approaches){
  sub_df = data.frame(matrix(nrow= 7, ncol=0))
  sub_df$Cores = c(1:7)
  sub_df$Approach = approach
  if(approach == "Virtual Best Solver"){
    sub_df$Mean = as.numeric(sum_top_vbs$mean)
    sub_df$Median = as.numeric(sum_top_vbs$median)
  } else if(approach == "Single Best Solver"){
    sub_df$Mean = as.numeric(sum_top_sbs$mean)
    sub_df$Median = as.numeric(sum_top_sbs$median)
  } else if(approach == "ASPEED"){
    aspeed = read.csv("top_aspeed_mcp.csv")
    sub_df$Mean = as.numeric(colMeans(as.matrix(aspeed)))
    sub_df$Median = as.numeric(colMedians(as.matrix(aspeed)))
  } else if(approach == "AS_0"){
    as_0 = read.csv("top_as_0_mcp.csv")
    sub_df$Mean = as.numeric(colMeans(as.matrix(as_0)))
    sub_df$Median = as.numeric(colMedians(as.matrix(as_0)))
  } else if(approach == "AS_theta"){
    as_0 = read.csv("top_as_theta_mcp.csv")
    sub_df$Mean = as.numeric(colMeans(as.matrix(as_0)))
    sub_df$Median = as.numeric(colMedians(as.matrix(as_0)))
  }
  results = rbind(results,sub_df)
}

results$Mean = as.numeric(results$Mean)
results$Median = as.numeric(results$Median)
ggplot(results, aes(x=Cores, y=Mean, colour = Approach, shape = Approach)) +
  geom_point(size = 3)+
  geom_line(aes(linetype="Mean"), size = 1)+
  geom_point(aes(y=Median),size = 3)+
  geom_line(aes(y = Median, linetype = "Median"), size = 1)+
  guides(linetype=guide_legend(title="",keywidth = 3, keyheight = 1.5), 
         colour = guide_legend(keywidth = 3, keyheight = 1.5))+
  expand_limits(x = 1, y = 0)+ theme(text=element_text(size=22,  family="Times"))+
  labs(x = "Cores", y = "MCP (s)", title = "MAXSAT2019")+theme(plot.title = element_text(hjust = 0.5))+
  scale_x_continuous(breaks=c(1:7))
ggsave(dpi = 500, width = 9, height = 5, filename = "MAXSAT19_line_chart_parallel_MCP.pdf")
results[which(results$Cores==7),]



#Par10
setwd("~/Documents/OrganizedScripts/results/MAXSAT2019/")
library(reshape2)
top_vbs = read.csv("top_vbs_par10.csv")
top_vbs[1:7] = apply(top_vbs[1:7],2,as.numeric)
top_vbs = top_vbs[c(2:8)]
sd = apply(top_vbs[1:7],2,sd)
mean = apply(top_vbs[1:7],2,mean)
median = apply(top_vbs[1:7],2,median)
sum_top_vbs = data.frame(mean = mean, median = median, sd = sd)
sum_top_vbs$cores = c(1:7)
sum_top_vbs = sum_top_vbs[which(!(sum_top_vbs$cores%in% c(11:19,20:29,31, 33:38))),]

p<-ggplot(sum_top_vbs, aes(x=cores, y=mean,colour="Mean VBS PAR10")) +
  geom_point()+
  geom_point(aes(y=median,colour="Median VBS PAR10"))+
  geom_errorbar(aes(ymin=mean-sd,
                    ymax=mean+sd), width=.2,
                position=position_dodge(0.05))+
  scale_y_continuous(
    name = "PAR10"
    #sec.axis = sec_axis( trans=~./self$Cutoff , name="probability of solving instance RegRF prediction")
  )
p
getwd()
ggsave(dpi = 500, width = 7, height = 5, filename = "VBS_behavior_different_cores_PAR10.pdf")

top_sbs = read.csv("top_sbs_par10.csv")
top_sbs[1:7] = apply(top_sbs[1:7],2,as.numeric)
top_sbs = top_sbs[c(2:8)]
sd = apply(top_sbs[1:7],2,sd)
mean = apply(top_sbs[1:7],2,mean)
median = apply(top_sbs[1:7],2,median)
sum_top_sbs = data.frame(mean = mean, median = median, sd = sd)
sum_top_sbs$cores = c(1:7)
sum_top_sbs = sum_top_sbs[which(!(sum_top_sbs$cores%in% c(11:19,20:29,31, 33:38))),]

p<-ggplot(sum_top_sbs, aes(x=cores, y=mean,colour="Mean SBS PAR10")) +
  geom_point()+
  geom_point(aes(y=median,colour="Median SBS PAR10"))+
  geom_errorbar(aes(ymin=mean-sd,
                    ymax=mean+sd), width=.2,
                position=position_dodge(0.05))+
  scale_y_continuous(
    name = "PAR10"
    #sec.axis = sec_axis( trans=~./self$Cutoff , name="probability of solving instance RegRF prediction")
  )
p
ggsave(filename = "SBS_behavior_different_cores_PAR10.pdf",dpi = 500, width = 7, height = 5)


results = data.frame(matrix(nrow= 0, ncol=4))
approaches = c("Single Best Solver", "Virtual Best Solver", 
               "AS_0", "AS_theta")
for(approach in approaches){
  sub_df = data.frame(matrix(nrow= 7, ncol=0))
  sub_df$Cores = c(1:7)
  sub_df$Approach = approach
  if(approach == "Virtual Best Solver"){
    sub_df$Mean = as.numeric(sum_top_vbs$mean)
    sub_df$Median = as.numeric(sum_top_vbs$median)
  } else if(approach == "Single Best Solver"){
    sub_df$Mean = as.numeric(sum_top_sbs$mean)
    sub_df$Median = as.numeric(sum_top_sbs$median)
  } else if(approach == "ASPEED"){
    aspeed = read.csv("top_aspeed_par10.csv")
    sub_df$Mean = as.numeric(colMeans(as.matrix(aspeed)))
    sub_df$Median = as.numeric(colMedians(as.matrix(aspeed)))
  } else if(approach == "AS_0"){
    as_0 = read.csv("top_as_0_par10.csv")
    sub_df$Mean = as.numeric(colMeans(as.matrix(as_0)))
    sub_df$Median = as.numeric(colMedians(as.matrix(as_0)))
  } else if(approach == "AS_theta"){
    as_0 = read.csv("top_as_theta_par10.csv")
    sub_df$Mean = as.numeric(colMeans(as.matrix(as_0)))
    sub_df$Median = as.numeric(colMedians(as.matrix(as_0)))
  }
  results = rbind(results,sub_df)
}
library(emojifont)
results$Mean = as.numeric(results$Mean)
results$Median = as.numeric(results$Median)
ggplot(results, aes(x=Cores, y=Mean, colour = Approach, shape = Approach)) +
  geom_point(size = 3)+
  geom_line(size = 1)+
  # geom_line(aes(linetype="Mean"), size = 1)+
  # geom_point(aes(y=Median),size = 3)+
  # geom_line(aes(y = Median, linetype = "Median"), size = 1)+
  guides(linetype=guide_legend(title="",keywidth = 3, keyheight = 1.5), 
         colour = guide_legend(keywidth = 3, keyheight = 1.5))+
  expand_limits(x = 1, y = 0)+ theme(text=element_text(size=22,  family="Times"))+
  labs(x = "Cores", y = "PAR10", title = "MAXSAT19-UCMS")+theme(plot.title = element_text(hjust = 0.5))+
  scale_x_continuous(breaks=c(1:7))+
  scale_y_continuous(trans='log10')
ggsave(dpi = 500, width = 9, height = 5, filename = "MAXSAT19_line_chart_parallel_PAR10.pdf")


results[which(results$Cores==7),]

self = SequentialPerformance$new("MAXSAT2019")
results = results[1:3]
vbs =mean(self$get_VBS_par10()$VBS_Runtime)
sbs = mean(self$get_par10_dataframe()[self$get_SBS()][[1]])


#vbs is 1
#sbs is 0
#sbs-value/sbs-vbs
results$Mean= (sbs - results$Mean)/(sbs - vbs)

results$Mean = as.numeric(results$Mean)

ggplot(results, aes(x=Cores, y=Mean, colour = Approach, shape = Approach)) +
  geom_point(size = 3)+
  geom_line(size = 1)+
  # geom_line(aes(linetype="Mean"), size = 1)+
  # geom_point(aes(y=Median),size = 3)+
  # geom_line(aes(y = Median, linetype = "Median"), size = 1)+
  guides(linetype=guide_legend(title="",keywidth = 3, keyheight = 1.5), 
         colour = guide_legend(keywidth = 3, keyheight = 1.5))+
  expand_limits(x = 1, y = -0.25)+ theme(text=element_text(size=22,  family="Times"))+
  labs(x = "Processors", y = "Normalized Gap", title = "MAXSAT19-UCMS")+
  theme(plot.title = element_text(hjust = 0.5))+
  scale_x_continuous(breaks=c(1:7))+
  scale_color_discrete(labels=c(bquote(AS[1]), bquote(AS[~p[~'\u2229']]), 
                                 'Single Best Solver','Virtual Best Solver'))+
  scale_shape_discrete(labels=c(bquote(AS[1]), bquote(AS[~p[~'\u2229']]), 
                                 'Single Best Solver','Virtual Best Solver'))

ggsave(dpi = 500, width = 9, height = 5, filename = "MAXSAT19_line_chart_parallel_NormalizedGap.pdf")
results[which(results$Cores ==7),]






















#checking the code
# #------------------
# self = PredictionResults$new("MAXSAT2019")
# # self$predictionPath
# #self$get_models_prediction()
# # self$get_VBS_probability_all_instances()
# # self$get_all_preds()
# # self$plot_instances_predictions(predictionPath = self$predictionPath, savePath = "")
# # as = self$Single_Algorithm_Selection()
# # mean(as$Par10)
# # median(as$Par10)
# 
# #self$selection_based_on_SE(method_number = 0, top_selection = 3, saveTo = self$selectionPath)
# 
# #method number help:
# # -1 : running all in parallel, no selection just ordering based on prediction, (top_selection, orderBy doesn't work here)
# # 0 : algorithm selection, selection besed on predicted runtime, top_selection will choose top algorithms from data frame based on prediction
# # 1 : minpred <= pred <= [minpred + delta_prime*SE]
# # 2 : lowebound as good as min pred, [pred-delta*SE]<=minpred
# # 3 : generalized 2 and 1; p-delta*se <= minP + deltaPrime*SE_min
# # 4 : [minpred-delta_prime*SE]<=[pred-delta*SE]<=minpred
# set.seed(1234)
# delta_prime = unlist(lapply(runif(300,-4,2), function(x) {2^(x)}))
# setwd("~/Documents/OrganizedScripts/")
# delta_prime = read.csv("RandomSearch_MAXSAT2019_delta_prime.csv")
# delta_prime = delta_prime$delta_prime
# delta_prime = unique(delta_prime)
# delta_prime = delta_prime[1:30]
# plot(density(delta_prime))
# #res_d_p = self$randomSearch_delta_prime(randomNumbers = delta_prime, method_number = 3, top_selection = 0, selectionPath = self$selectionPath, 
#                                     # orderBy = 'pred', predictionPath = self$predictionPath, ignoreTimeoutsOnVBS = FALSE,
#                                     # alpha = 0, delta = 0, median = FALSE)
# #write.csv(res_d_p,"RandomSearch_MAXSAT2019_delta_prime.csv")
# 
# #set.seed(4321)
# #delta = unlist(lapply(runif(300,-4,2), function(x) {2^(x)}))
# 
# delta = read.csv("RandomSearch_MAXSAT2019_delta.csv")
# delta = delta$delta
# delta = unique(delta)
# delta = delta[1:30]
# # res_d = self$randomSearch_delta(randomNumbers = delta, method_number = 3, top_selection = 0, selectionPath = self$selectionPath, 
# #                                      orderBy = 'pred', predictionPath = self$predictionPath, ignoreTimeoutsOnVBS = FALSE,
# #                                      alpha = 0, delta_prime = 0, median = FALSE)
# # write.csv(res_d,"RandomSearch_MAXSAT2019_delta.csv")
# 
# # res_combined = self$randomSearch_combination(randomNumbers_delta = delta, randomNumbers_delta_prime = delta_prime,
# #                                              method_number = 3, top_selection = 0, selectionPath = self$selectionPath, 
# #                                              predictionPath = self$predictionPath, ignoreTimeoutsOnVBS = FALSE, orderBy = 'pred-se')
# # 
# # print(res_combined)
# # write.csv(res_combined,"RandomSearch_MAXSAT2019_combined_notIgnore.csv")
# 
# a = read.csv("RandomSearch_MAXSAT2019_combined_notIgnore.csv")
# 
# a = a[which(a$metric == "Runtime"),]
# a = a[which(a$median == FALSE),]
# a = a[order(a$Parallel_time),]
# a = a[1:400,]
# library(plotly)
# data <- data.frame(Theta=a$delta,Theta_min=a$delta_prime,Runtime=a$Parallel_time)
# 
# axx <- list(
#   title = "Theta"
# )
# 
# axy <- list(
#   title = "Theta_min"
# )
# 
# axz <- list(
#   title = "Runtime (s)"
# )
# 
# plot_ly() %>% 
#   add_trace(data = data, x=data$Theta, y=data$Theta_min, z=data$Runtime, intensity = data$Runtime, 
#             type="mesh3d", colors = "viridis") %>% 
#   add_trace(x=data[which(data$Runtime == min(data$Runtime)),"Theta"], y = data[which(data$Runtime == min(data$Runtime)),"Theta_min"], 
#             z = data[which(data$Runtime == min(data$Runtime)),"Runtime"], color = "red")%>%
#   layout(title = 'Random Search on MAXSAT2019 for Theta Values',scene = list(xaxis=axx,yaxis=axy,zaxis=axz)) 
#   
# ##################### ignore timeouts 
# res_combined = self$randomSearch_combination(randomNumbers_delta = delta, randomNumbers_delta_prime = delta_prime,
#                                              method_number = 3, top_selection = 0, selectionPath = self$selectionPath, 
#                                              predictionPath = self$predictionPath, ignoreTimeoutsOnVBS = TRUE, orderBy = 'pred-se')
# 
# print(res_combined)
# write.csv(res_combined,"RandomSearch_MAXSAT2019_combined_notIgnore.csv")
# 
# a = read.csv("RandomSearch_MAXSAT2019_combined_notIgnore.csv")
# 
# a = a[which(a$metric == "Runtime"),]
# a = a[which(a$median == FALSE),]
# a = a[order(a$Parallel_time),]
# a = a[1:400,]
# library(plotly)
# data <- data.frame(Theta=a$delta,Theta_min=a$delta_prime,Runtime=a$Parallel_time)
# 
# axx <- list(
#   title = "Theta"
# )
# 
# axy <- list(
#   title = "Theta_min"
# )
# 
# axz <- list(
#   title = "Runtime (s)"
# )
# 
# plot_ly() %>% 
#   add_trace(data = data, x=data$Theta, y=data$Theta_min, z=data$Runtime, intensity = data$Runtime, 
#             type="mesh3d", colors = "viridis") %>% 
#   add_trace(x=data[which(data$Runtime == min(data$Runtime)),"Theta"], y = data[which(data$Runtime == min(data$Runtime)),"Theta_min"], 
#             z = data[which(data$Runtime == min(data$Runtime)),"Runtime"], color = "red")%>%
#   layout(title = 'Random Search on MAXSAT2019 for Theta Values',scene = list(xaxis=axx,yaxis=axy,zaxis=axz)) 
# 
# 
# # 
# # self$selection_based_on_SE(method_number = 3, top_selection = 0, saveTo = self$selectionPath, ignoreTimeoutsOnVBS = FALSE, delta= 0.22, alpha = 0.21, delta_prime = 0.38,
# #                            orderBy = 'pred')
# # self$get_summary_selection_result(self$selectionPath)
# # # self$selection_based_on_SE(method_number = 3, top_selection = 0, saveTo = self$selectionPath, ignoreTimeoutsOnVBS = FALSE, delta = 0.27)
# # # self$get_summary_selection_result(self$selectionPath)
# # # 
# # # self$get_summary_selection_result(self$selectionPath)
# # #self$modelPath
# # #self$get_models_prediction()
# # #self$get_VBS_probability_all_instances()
# # #self$get_all_preds()
# # #self$plot_instances_predictions(predictionPath = self$predictionPath, savePath = "")
# # #self$Single_Algorithm_Selection()
# # #self$get_summary_selection_result(self$selectionPath)
# # # res2018 = self$get_summary_all(predictionPath = self$predictionPath, 
# # #                                selectionPath = self$selectionPath,
# # #                                ignoreTimeoutsOnVBS=TRUE, 
# # #                                method_numbers = c(0:6),
# # #                                top_selections = c(1:8), 
# # #                                median = FALSE)
# # # getwd()
# # # 
# # # write.csv(res2018,"res2018.csv")
# # # #---------------
# # # #work with aslib output for prediction
# # # #---------------
# # # pred = readRDS("~/Documents/models.rds")
# # # a = readRDS("~/Desktop/1.rds")
# # # b = readRDS("~/Documents/mlr-scripts/MAXSAT2019/Prediction/StandardError/abcdsat_r18.rds")
# # # model = pred[[1]]$models[[1]]
# # # pred[[1]]$models
# # # self$get_scenario()
# # # data = self$llamaData
# # # features = data$data[data$features]
# # # solver = self$solvers[1]
# # # solverdata = features
# # # performance = self$get_actual_result_csv()[solver]
# # # solverdata = cbind(solverdata,performance)
# # # solverTask <- makeRegrTask(data = solverdata, target = solver)
# # # predict(model, solverTask)
# # # 
# # # length(unique(pred[[1]]$predictions$algorithm))
# # # 
# # # 
# # # b$pred$data
# # # (a$predictions$iteration)
# # # 
# # # 
# # # scenario = parseASScenario("/home/haniye/Documents/aslib_data/GLUHACK-2018-ALGO/")
# # # data  = convertToLlamaCVFolds(data)
# # # data$algos
