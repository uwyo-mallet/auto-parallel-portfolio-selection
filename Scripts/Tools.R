#Haniye Kashgarani 
#Feb 8th, 2022
#More Organized code

library(checkmate)
library(R6)
library(stringr)
library(aslib)
library(llama)
library(matrixStats)
library(mlr)
library(parallel)
library(parallelMap)
library(plotly)
#library(tidyverse)
library(RWeka)
library(methods)
library(ParamHelpers)
library(batchtools)
library(BBmisc)
library(tidyr)
library(tibble)

Tools <- R6Class(
  classname = "Tools",
  public = list(
    #set working directory
    set_wd = function(path, cluster = FALSE){
      if(Sys.info()['sysname']!="Linux"){
        path = paste("C:/Users/hnyk9/OneDrive - University of Wyoming/",path,sep = "")
        if(dir.exists(path)){
          setwd(path)
        } else {print(paste("Directory '",path,"' doesn't exits!",sep=""))}
      } else{
        path = paste("~/Documents/",path,"/",sep = "")
        if(cluster){
          path = paste("/gscratch/hkashgar/",path,"/",sep = "")
        }
        if(dir.exists(path)){
          setwd(path)
        } else {print(paste("Directory '",path,"' doesn't exits!",sep=""))}
      }
      invisible(self)
    }, 
    
    plot_hist_plotly = function(vector){
      plot_ly(
        x = vector,
        type = "histogram"
      )
    },
    #doesn't work
    plot_dens_plotly = function(dataframe){
      data_long <- gather(dataframe, core, overhead, X2:X32, factor_key=TRUE)
      data_long$core <- gsub("X","",data_long$core)
      data_long$core = as.factor(as.numeric(data_long$core))
      fig <- plot_ly(data = dataframe)
      if(ncol(dataframe>=1)){
        for(i in 1:ncol(dataframe)){
          dens = density(unlist(unname(dataframe[i])))
          fig = add_trace(fig,x = ~dens$x, y = ~dens$y,type = 'scatter',mode = 'lines', name = paste(str_split(colnames(dataframe[i]),"X")[[1]][2],"cores"), fill = 'tozeroy')
        }
      }
      fig <- fig %>% layout(xaxis = list(title = 'Overhead Percentage'),
                            yaxis = list(title = 'Density'))
      fig
    }
    
    #move files
    
    #check if exist 
    
    #latex table
  )
)

