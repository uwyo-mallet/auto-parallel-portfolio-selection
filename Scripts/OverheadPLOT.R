if(Sys.info()['sysname']=="Linux"){
  source("/home/haniye/Documents/OrganizedScripts/OverheadResults.R")
} else{
  source("C:/Users/hnyk9/OneDrive - University of Wyoming/OrganizedScripts/OverheadResults.R")
}

#Estimate_overhead_on_predictionPath ="C:/Users/hnyk9/OneDrive - University of Wyoming/OrganizedScripts/Estimate_overhead_on_prediction/"

actual_overhead_per_core_seconds_Path = "C:/Users/hnyk9/OneDrive - University of Wyoming/OrganizedScripts/actual_overhead_per_core_seconds/"
actual_overhead_per_core_seconds_PlotPath = "C:/Users/hnyk9/OneDrive - University of Wyoming/OrganizedScripts/actual_overhead_per_core_seconds/plot/"
actual_overhead_per_core_perc_Path = "C:/Users/hnyk9/OneDrive - University of Wyoming/OrganizedScripts/actual_overhead_per_core_perc/"
actual_overhead_per_core_perc_PlotPath = "C:/Users/hnyk9/OneDrive - University of Wyoming/OrganizedScripts/actual_overhead_per_core_perc/plot/"
actual_overhead_per_solver_seconds_Path = "C:/Users/hnyk9/OneDrive - University of Wyoming/OrganizedScripts/actual_overhead_per_solver_seconds/"
actual_overhead_per_solver_seconds_PlotPath = "C:/Users/hnyk9/OneDrive - University of Wyoming/OrganizedScripts/actual_overhead_per_solver_seconds/plot/"
actual_overhead_per_solver_perc_Path = "C:/Users/hnyk9/OneDrive - University of Wyoming/OrganizedScripts/actual_overhead_per_solver_perc/"
actual_overhead_per_solver_perc_PlotPath = "C:/Users/hnyk9/OneDrive - University of Wyoming/OrganizedScripts/actual_overhead_per_solver_perc/plot/"

self = OverheadResults$new()
type = "percentage-change"
#self$actual_overhead_per_core(ignoreTimeouts = TRUE, savePath = actual_overhead_per_core_perc_Path,type = type, savePlot=TRUE, plotPath =actual_overhead_per_core_perc_PlotPath)
#self$actual_overhead_per_solver(cores_overhead_path = actual_overhead_per_core_perc_Path,type = type,savePath = actual_overhead_per_solver_perc_Path, ignoreTimeouts = TRUE,  savePlot=TRUE, plotPath =actual_overhead_per_solver_perc_PlotPath)


type = "seconds"
#self$actual_overhead_per_core(ignoreTimeouts = TRUE, savePath = actual_overhead_per_core_seconds_Path,type = type, savePlot=TRUE, plotPath =actual_overhead_per_core_seconds_PlotPath)
#self$actual_overhead_per_solver(cores_overhead_path = actual_overhead_per_core_seconds_Path,type = type,savePath = actual_overhead_per_solver_seconds_Path, ignoreTimeouts = TRUE,  savePlot=TRUE, plotPath =actual_overhead_per_solver_seconds_PlotPath)

library(tidyr)
solver = read.csv(paste(actual_overhead_per_solver_perc_Path,self$sequentialData$solvers[2],".csv",sep=""))
data_long <- gather(solver, core, overhead, X2:X32, factor_key=TRUE)
data_long$core <- gsub("X","",data_long$core)
data_long$core = as.factor(as.numeric(data_long$core))
boxplot(data_long$overhead,horizontal = TRUE)
par(mfcol = c(5, 2))
without_names = solver[-1]
for(i in 1:9){
  boxplot(without_names[i],horizontal = TRUE, xlab= paste("Overhead (", i+1, " cores )"), ylim = c(1,6))
}

#stripchart(without_names[i], method="stack", xlab="overhead")

par(mfcol = c(5, 2))
for(i in 1:9){
  hist(unlist(without_names[i]),xlab= paste("Overhead (", i+1, " cores )"), xlim = c(1,4),breaks = 20,freq = FALSE,main = "")
}

#stem(solver$X2)
#quantile(solver$X2)

library(plotly)

fig <- plot_ly(x = ~density(solver$X2)$x, y = ~density(solver$X2)$y, type = 'scatter', mode = 'lines', name = '2 cores', fill = 'tozeroy')
fig <- fig %>% add_trace(x = ~density(solver$X3)$x, y = ~density(solver$X3)$y, name = '3 cores', fill = 'tozeroy')
fig <- fig %>% add_trace(x = ~density(solver$X4)$x, y = ~density(solver$X4)$y, name = '4 cores', fill = 'tozeroy')
fig <- fig %>% add_trace(x = ~density(solver$X5)$x, y = ~density(solver$X5)$y, name = '5 cores', fill = 'tozeroy')
fig <- fig %>% add_trace(x = ~density(solver$X6)$x, y = ~density(solver$X6)$y, name = '6 cores', fill = 'tozeroy')
fig <- fig %>% add_trace(x = ~density(solver$X7)$x, y = ~density(solver$X7)$y, name = '7 cores', fill = 'tozeroy')
fig <- fig %>% add_trace(x = ~density(solver$X8)$x, y = ~density(solver$X8)$y, name = '8 cores', fill = 'tozeroy')
fig <- fig %>% add_trace(x = ~density(solver$X9)$x, y = ~density(solver$X9)$y, name = '9 cores', fill = 'tozeroy')
fig <- fig %>% add_trace(x = ~density(solver$X10)$x, y = ~density(solver$X10)$y, name = '10 cores', fill = 'tozeroy')
fig <- fig %>% layout(xaxis = list(title = 'Overhead Percentage'),
                      yaxis = list(title = 'Density'))

fig


library(sm)
attach(data_long)
# create value labels
core.f <- factor(core, levels= c(2:10,20,30,32),
                labels = c("2 cores", "3 cores", "4 cores",
                           "5 cores", "6 cores", "7 cores",
                           "8 cores", "9 cores", "10 cores",
                           "20 cores", "30 cores", "32 cores"))

# plot densities
sm.density.compare(overhead, core, xlab="Overhead")
title(main="Cadical Overhead Distribution by Cores")
legend("topright", legend = levels(core),
       lty = 1, col = 1:12)
  data = solver$X10
  alpha = mean(data)^2/var(data)
  beta = var(data)/mean(data)
  mean = mean(data)
#mean = alpha*beta
std.dv = sqrt(alpha*(beta^2))
mean_percentile = pgamma(mean,shape = alpha,rate = 1/beta) #probability of x < value
value_prob = qgamma(mean_percentile,shape=alpha, scale = beta) # what is x if the probability is folan
value_prob = qgamma(0.5,shape=alpha, scale = beta) # what is x if the probability is folan
value_prob = qgamma(0.75,shape=alpha, scale = beta) # what is x if the probability is folan


library(MASS)

# Plot density as points

fit.params <- fitdistr(data, "gamma", lower = c(0, 0))

pdf_gamma <- function(x){
  a = alpha
  t = 1/beta
  w = 1/(gamma(a)*t^a)*x^(a-1)*exp(-x/t)
  return(w)
}
pdf_gamma(solver$X10)


















library(ggplot2)
library(scales)

## Rate parameter of the exponential distribution to be simulated
lambda <- 1/mean

exponential_sample = as.numeric(solver$X10)
ggplot() +
  geom_histogram(
    mapping = aes(x = exponential_sample),
    color = "gray50",
    bins = 50
  )+
  scale_y_continuous(labels = comma) +
  labs(
    title = "Exponential Distribution Sample",
    x = "value",
    y = "number of occurences"
  )+
  stat_function(
    mapping = aes(x = exponential_sample),
    fun = function(x)
    {
      dexp(x = x, rate = lambda) * length(exponential_sample)
    }
  ) 

library(fitdistrplus)
z = dgamma(data,shape = alpha,scale=1/beta)
z = sort(z)
print(z)
summary(z)

fit <- fitdist(data,"gamma")
summary(fit)
plot(fit)





histDenNorm <- function (x, main = "") {
  alpha = mean(x)^2/var(x)
  beta = var(x)/mean(x)
  range = seq(0,12,0.01)
  y = dgamma(range, alpha, scale = beta)
  hist(x, prob = TRUE, main = main,breaks = 50,xlim = c(0,12)) # Histogram
  grid(nx = NA, ny = NULL, lty = 2, col = "gray", lwd = 1)
  lines(y,ylim  = c(0,max(y)+0.01), xlim = c(0,12), col = "brown",lwd = 1)
  lines(density(x), col = "blue", lwd = 1) # Density 
  lines(density(rgamma(100,shape = alpha, scale =1/beta)+1), col="green",lwd=1)
  x2 <- seq(min(x), max(x), length = 40)
  f <- dnorm(x2, mean(x), sd(x))
  lines(x2, f, col = "red", lwd = 1) # Normal
  legend("topright", c("Histogram", "Density", "Normal","Gamma"), box.lty = 0,
         lty = 1, col = c("black", "blue", "red","green"), lwd = c(1, 1, 1, 1))
}

par(mfcol = c(1, 2))

histDenNorm((solver$X2), main = "Histogram of X")

par(mfcol = c(1, 1))


library(fitdistrplus)
data = solver$X4


fitGamma = fitdist(data,"gamma")
fitCauchy = fitdist(data,"cauchy")
fitWeibull = fitdist(data,"weibull")
fitLnorm = fitdist(data,"lnorm")
fitNorm = fitdist(data,"norm")
fitExp = fitdist(data,"exp")
fitLogis = fitdist(data,"logis")
fitUnif = fitdist(data,"unif")
#fitWilcox = fitdist(data,"wilcox")
#fitSignrank = fitdist(data,"signrank")
#fitT = fitdist(data,"T")
#fitPois = fitdist(data,"pois")
#fitMultinom = fitdist(data,"multinom")
#fitHyper = fitdist(data,"hyper")
#fitBeta = fitdist(data,"beta")
#fitNbinom = fitdist(data,"nbinom")
#fitGeom = fitdist(data,"geom")
#fitBinom = fitdist(data,"binom")
#fitChisq = fitdist(data,"chisq")


summary(fitGamma)
summary(fitCauchy)
summary(fitWeibull)
summary(fitLnorm)
summary(fitNorm)
summary(fitExp)
summary(fitLogis)

data_long = data_long[-1]
attach(data_long)
fit = lm(overhead~core)

par(mfcol = c(2, 2))
plot(fit)
plot(fitCauchy,demp=TRUE)
plot(fitWeibull,demp=TRUE)
plot(fitLnorm,demp=TRUE)
plot(fitNorm,demp=TRUE)
plot(fitExp,demp=TRUE)
plot(fitGamma,demp=TRUE)
plot(fitLogis,demp=TRUE)

cdfcomp(fitGamma,addlegend = FALSE)
denscomp(fitGamma)
ppcomp(fitGamma)
qqcomp(fitGamma)


for(solver in solvers){
  dist = "cauchy"
  mainDir = "C:/Users/hnyk9/OneDrive - University of Wyoming/OrganizedScripts/fitting_Distributions/"
  subDir = paste(solver)
  dir.create(file.path(mainDir, subDir), showWarnings = FALSE)
  mainDir = paste(mainDir,subDir,"/",sep = "")
  subDir = dist
  dir.create(file.path(mainDir, subDir), showWarnings = FALSE)
  setwd(file.path(mainDir, subDir))
  csv = read.csv(paste(actual_overhead_per_solver_perc_Path,solver,".csv",sep=""))
  for(i in c("X2","X3","X4","X5","X6","X7","X8","X9","X10","X20","X30","X32"))
  {
    data = csv[i]
    data = data[[1]]
    fit = fitdist(data,dist)
    png(file = paste(str_split(i,"X")[[1]][2],"_cores.png",sep=""),1222,907)
    plot(fit,demp=TRUE)
    dev.off()
  }
}
getwd()

library(fitdistrplus)
par(mfcol = c(4, 3))
data = solver$X2
alpha = mean(data)^2/var(data)
beta = var(data)/mean(data)
mean = mean(data)
#mean = alpha*beta
std.dv = sqrt(alpha*(beta^2))
x = 1
range = seq(0,12,0.01)
param = MASS::fitdistr(data,"gamma")
y = dgamma(range, param$estimate[1], rate = param$estimate[1])
plot(range, y,type="l",ylim  = c(0,4), xlim = c(0,4),main = "2 cores", ylab = "density",xlab = "overhead")
hist(data,freq = FALSE,add=TRUE)


x <- seq(min(data), max(data), length.out = 100)
hist(data, breaks = 30, freq = FALSE, col = "grey", ylim = c(0, 12))
curve(dgamma(x, shape = param$estimate[1], rate = param$estimate[2]), add = TRUE)
lines(sort(data), dgamma(sort(data), shape = 1),
      col = "red", lty = "dotted")

data = solver$X3
alpha = mean(data)^2/var(data)
beta = var(data)/mean(data)
mean = mean(data)
#mean = alpha*beta
std.dv = sqrt(alpha*(beta^2))
x = 1
range = seq(0,12,0.01)
y = dgamma(range, alpha, scale = beta)
plot(range, y,type="l",ylim  = c(0,max(y)+0.01), xlim = c(0,12),main = "3 cores", ylab = "density",xlab = "overhead")

data = solver$X4
alpha = mean(data)^2/var(data)
beta = var(data)/mean(data)
mean = mean(data)
#mean = alpha*beta
std.dv = sqrt(alpha*(beta^2))
x = 1
range = seq(0,12,0.01)
y = dgamma(range, alpha, scale = beta)
plot(range, y,type="l",ylim  = c(0,max(y)+0.01), xlim = c(0,12),main = "4 cores", ylab = "density",xlab = "overhead")

data = solver$X5
alpha = mean(data)^2/var(data)
beta = var(data)/mean(data)
mean = mean(data)
#mean = alpha*beta
std.dv = sqrt(alpha*(beta^2))
x = 1
range = seq(0,12,0.01)
y = dgamma(range, alpha, scale = beta)
plot(range, y,type="l",ylim  = c(0,max(y)+0.01), xlim = c(0,12),main = "5 cores", ylab = "density",xlab = "overhead")

data = solver$X6
alpha = mean(data)^2/var(data)
beta = var(data)/mean(data)
mean = mean(data)
#mean = alpha*beta
std.dv = sqrt(alpha*(beta^2))
x = 1
range = seq(0,12,0.01)
y = dgamma(range, alpha, scale = beta)
plot(range, y,type="l",ylim  = c(0,0.4), xlim = c(0,12),main = "6 cores", ylab = "density",xlab = "overhead")

data = solver$X7
alpha = mean(data)^2/var(data)
beta = var(data)/mean(data)
mean = mean(data)
#mean = alpha*beta
std.dv = sqrt(alpha*(beta^2))
x = 1
range = seq(0,12,0.01)
y = dgamma(range, alpha, scale = beta)
plot(range, y,type="l",ylim  = c(0,0.4), xlim = c(0,12),main = "7 cores", ylab = "density",xlab = "overhead")

data = solver$X8
alpha = mean(data)^2/var(data)
beta = var(data)/mean(data)
mean = mean(data)
#mean = alpha*beta
std.dv = sqrt(alpha*(beta^2))
x = 1
range = seq(0,12,0.01)
y = dgamma(range, alpha, scale = beta)
plot(range, y,type="l",ylim  = c(0,0.4), xlim = c(0,12),main = "8 cores", ylab = "density",xlab = "overhead")

data = solver$X9
alpha = mean(data)^2/var(data)
beta = var(data)/mean(data)
mean = mean(data)
#mean = alpha*beta
std.dv = sqrt(alpha*(beta^2))
x = 1
range = seq(0,12,0.01)
y = dgamma(range, alpha, scale = beta)
plot(range, y,type="l",ylim  = c(0,0.4), xlim = c(0,12),main = "9 cores", ylab = "density",xlab = "overhead")

data = solver$X10
alpha = mean(data)^2/var(data)
beta = var(data)/mean(data)
mean = mean(data)
#mean = alpha*beta
std.dv = sqrt(alpha*(beta^2))
x = 1
range = seq(0,12,0.01)
y = dgamma(range, alpha, scale = beta)
plot(range, y,type="l",ylim  = c(0,0.4), xlim = c(0,12),main = "10 cores", ylab = "density",xlab = "overhead")

data = solver$X20
alpha = mean(data)^2/var(data)
beta = var(data)/mean(data)
mean = mean(data)
#mean = alpha*beta
std.dv = sqrt(alpha*(beta^2))
x = 1
range = seq(0,12,0.01)
y = dgamma(range, alpha, scale = beta)
plot(range, y,type="l",ylim  = c(0,0.4), xlim = c(0,12),main = "20 cores", ylab = "density",xlab = "overhead")

data = solver$X30
alpha = mean(data)^2/var(data)
beta = var(data)/mean(data)
mean = mean(data)
#mean = alpha*beta
std.dv = sqrt(alpha*(beta^2))
x = 1
range = seq(0,12,0.01)
y = dgamma(range, alpha, scale = beta)
plot(range, y,type="l",ylim  = c(0,0.4), xlim = c(0,12),main = "30 cores", ylab = "density",xlab = "overhead")

data = solver$X30
alpha = mean(data)^2/var(data)
beta = var(data)/mean(data)
mean = mean(data)
#mean = alpha*beta
std.dv = sqrt(alpha*(beta^2))
x = 1
range = seq(0,12,0.01)
y = dgamma(range, alpha, scale = beta)
plot(range, y,type="l",ylim  = c(0,0.4), xlim = c(0,12),main = "32 cores", ylab = "density",xlab = "overhead")


