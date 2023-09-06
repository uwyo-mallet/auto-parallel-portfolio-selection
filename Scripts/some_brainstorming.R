setwd("Documents/auto-parallel-portfolio-selection/Scripts/")
source("OverheadResults.R")
library(corrplot)
library(dplyr)
library(shiny)
library(shinydashboard)

self = PredictionResults$new("SAT2018")

range = c(1:10)
df_results = data.frame(matrix(nrow = 0, ncol=10))
for(i in range){
    selectionPath = paste("/home/haniye//Documents/OrganizedScripts/results/SAT2018//selections_algorithmSelection_noUncertainty/",i,"_cores/",sep="")
    selectionResults = self$get_selection_result_all_instances(ignoreTimeouts = FALSE,
                                                selectionPath = selectionPath,
                                                median = FALSE, 
                                                method_number = 0)
    selectionResults$cores = i
    colnames(df_results)= colnames(selectionResults)
    df_results = rbind(df_results,selectionResults)
}

instances = unique(df_results$InstanceName)

get_best_core = data.frame(matrix(nrow = 0, ncol = 10))
for(i in instances){
  get_best_core = rbind(get_best_core, df_results[which(df_results$InstanceName == i & df_results$min_parallel_runtime == min(df_results[which(df_results$InstanceName == i),]$min_parallel_runtime)),])
}

a = get_best_core[duplicated(get_best_core$InstanceName) | duplicated(get_best_core$InstanceName, fromLast = TRUE), ]
get_best_core = get_best_core[which(!get_best_core$InstanceName %in% a$InstanceName),]

for(i in unique(a$InstanceName)){
  get_best_core = rbind(get_best_core, a[which(a$InstanceName == i & a$n_selected_solvers == min(as.numeric(a[which(a$InstanceName == i),]$n_selected_solvers))),])
}

get_best_core = get_best_core[order(get_best_core$n_selected_solvers),]
get_best_core$VBSRuntime = as.numeric(get_best_core$VBSRuntime)
get_best_core$min_sequential_runtimes = as.numeric(get_best_core$min_sequential_runtimes)
get_best_core$min_parallel_runtime = as.numeric(get_best_core$min_parallel_runtime)
get_best_core$n_selected_solvers = as.numeric(get_best_core$n_selected_solvers)
get_best_core$delta = as.numeric(get_best_core$delta)
get_best_core$delta_prime = as.numeric(get_best_core$delta_prime)
get_best_core$cores = as.numeric(get_best_core$cores)

get_best_core = get_best_core[which(get_best_core$min_parallel_runtime != self$sequentialData$Cutoff),]


summary(get_best_core[which(get_best_core$cores == 1),])
summary(get_best_core[which(get_best_core$cores == 2),])
summary(get_best_core[which(get_best_core$cores == 3),])
summary(get_best_core[which(get_best_core$cores == 4),])
summary(get_best_core[which(get_best_core$cores == 5),])
summary(get_best_core[which(get_best_core$cores == 6),])
summary(get_best_core[which(get_best_core$cores == 7),])
summary(get_best_core[which(get_best_core$cores == 8),])
summary(get_best_core[which(get_best_core$cores == 9),])
summary(get_best_core[which(get_best_core$cores == 10),])


get_best_core
library(ggplot2)
colnames(get_best_core)
ggplot(get_best_core, aes(x = cores, y = min_parallel_runtime)) + 
  geom_point()
library(png)
library(Hmisc)
# par(mfrow = c(1, 1))
features = self$sequentialData$get_features()
cor_list = list()
for(i in 1:10){
  corebests = get_best_core[which(get_best_core$cores == i),]$InstanceName
  #core1bests = get_best_core$InstanceName
  corebests = sub("\\.csv$", "", corebests)
  corebests = paste0("sat/", corebests)
  corebestf = features[which(features$benchmark %in% corebests),]
  correlation = cor(corebestf[2:55])
  cor_list = append(cor_list, list(correlation))
}

ui <- dashboardPage(
  dashboardHeader(title = "Correlation Matrices"),
  dashboardSidebar(
    selectInput("matrixDropdown", 
                "Select Matrix:", 
                choices = 1:length(cor_list), 
                selected = 1)
  ),
  dashboardBody(
    plotlyOutput("corMatrixPlot", height = "1050px", width = "1150px")
  )
)

server <- function(input, output, session) {
  output$corMatrixPlot <- renderPlotly({
    selected_matrix <- cor_list[[as.integer(input$matrixDropdown)]]
    
    p <- plot_ly(
      x = colnames(selected_matrix),
      y = rownames(selected_matrix),
      z = selected_matrix,
      type = 'heatmap'
    )
    
    # Adjust margins
    p <- layout(p, margin = list(l = 40, r = 40, b = 40, t = 40, pad = 4))
    
    return(p)
  })
}


shinyApp(ui, server)


corrplot()