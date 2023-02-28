#read data of csv file
library(sys)
library(R.utils)

partitionName <- "teton"
number_of_solvers <-"32"
solverstate <- "actual"

dirpath <- paste("/gscratch/hkashgar/BatchScripts/GRAPHS2015/",partitionName,"-7-solvers-in-parallel-",partitionName,"-",number_of_solvers,"-solvers-GRAPHS2015-November-22-2022",sep="")
setwd(dirpath)

#get names of all files
log_files <- list.files(pattern = "\\.log$")
output_files <- list.files(pattern = "\\.output$")
#error_files <- list.files(pattern = "\\.error$")

log_files_path <- NULL
output_files_path <- NULL
#error_files_path <- NULL

#get path for each file
for(i in log_files){
  log_files_path <- append(log_files_path, paste(dirpath,"/",i,sep=""))
}
for(i in output_files){
  output_files_path <- append(output_files_path, paste(dirpath,"/",i,sep=""))
}
#for(i in error_files){
#  error_files_path <- append(error_files_path, paste(dirpath,"/",i,sep=""))
#}

#do for each csv
solvers <- vector()
dataframes <- vector()

for(file in log_files){
  solver = strsplit(file,"__")[[1]][1]
  solvers <- append(solvers, solver)
  solvers <- unique(solvers)
}

for(solver in solvers)
{
  instances <- vector()
  runtimes <- vector()
  JobIDs <- vector()
  TIMEOUTS <- vector()
  OOMS <- vector()
  UNDef_ERRORS <- vector()
  output_checker <- vector()
  for(file in log_files){
    output_checker <- vector()
    currenctsolver = strsplit(file,"__")[[1]][1]
    if(currenctsolver == solver){
      timeout = FALSE
      oom = FALSE
      undef_error = FALSE
      instance = strsplit(file,"__")[[1]][2]
      instance = strsplit(instance,".log")[[1]][1]
      
      #get error file and check if there is any oom and timeouts
      #error_file <- grep(paste("^",instance,"__",sep = ""), error_files)
      #error_file <- error_files[error_file]
      #jobid <- strsplit(error_file,"__J")[[1]][2]
      #jobid <- strsplit(jobid,".error")[[1]][1]
      #error_file <- readLines(error_file)
      
      
      #append job id
      #JobIDs <- append(JobIDs,jobid)
      
      #get output file and check exit code and sat and unsat
      output_file <- paste(solver,"__",instance,".output",sep = "")
      #output_lastlines <- system(paste("zcat ",output_file," | tail -n 8 > lastlines", sep = ""))
      output_lastlines <- system(paste("cat ",output_file," | tail -n 8 > lastlines", sep = ""))
      output_lastlines <- readLines("./lastlines")
      output_lastline <- output_lastlines[length(output_lastlines)]
      
      if(length(output_lastline)>2)
      {
        output_lastline <- substr(output_lastline, nchar(output_lastline)-2+1, nchar(output_lastline))
      }
      check <- system(paste("grep UNSATISFIABLE ./lastlines > check ",sep=""))
      output_checker <- append(output_checker, any(grepl("UNSATISFIABLE", readLines("check"))))
      check <- system(paste("grep SATISFIABLE ./lastlines > check ",sep=""))
      output_checker <- append(output_checker, any(grepl("SATISFIABLE", readLines("check"))))
      check <- system(paste("grep exit\\ 20 ./lastlines > check ",sep=""))
      output_checker <- append(output_checker, any(grepl("exit 20", readLines("check"))))
      check <- system(paste("grep exit\\ 10 ./lastlines > check ",sep=""))
      output_checker <- append(output_checker, any(grepl("exit 10", readLines("check"))))
      
      output_checker <- append(output_checker, output_lastline == " 0")
      output_checker <- append(output_checker, output_lastline == "0")
        
      #set instance as you want and add to vector
      instance = paste("sat/",instance,".cnf",sep = "")
      instances <- append(instances,instance)
      
      column.names <- c("InstanceName", get('solver'),"JobID", "TIME_OUT_ERROR", "OUT_OF_MEMORY_ERROR", "UNDEFINED_ERROR")
      
      #read log file and check the time saved
      fileinfo = file.info(file)
      mydata = readLines(file)
      a <- strsplit(mydata[1],"user")
      if (file.size(file) == 0)
      {
        runtimes <- append(runtimes, NA)
        #timeout <- any(grep("TIME LIMIT", error_file))
        #oom <- any(grep("oom-kill", error_file))
        #if(timeout == FALSE && oom == FALSE)
        #{
         # undef_error = TRUE
        #}
      }
      else{
        runtime <- strsplit(mydata[1],"user")[[1]][1]
        runtimes <- append(runtimes,runtime)
        if(any(output_checker == TRUE)==FALSE)
        {
          #timeout <- any(grep("TIME LIMIT", error_file))
          #oom <- any(grep("oom-kill", error_file))
          #if(timeout == FALSE && oom == FALSE){
           # undef_error = TRUE
          #}
        }
      }
      
      TIMEOUTS <- append(TIMEOUTS,timeout)
      OOMS <- append(OOMS,oom)
      UNDef_ERRORS <- append(UNDef_ERRORS,undef_error)
    }
  }
  df <- data.frame(
    InstanceName = instances
  )
  df[solver] <- runtimes
  df["JobID"] <- JobIDs
  df["TIME_OUT_ERROR"] <- TIMEOUTS
  df["OUT_OF_MEMORY_ERROR"] <- OOMS
  df["UNDEFINED_ERROR"] <- UNDef_ERRORS
  write.csv(df, paste(partitionName,"_",solver,"_Parallel_",number_of_solvers,"_solvers.csv",sep = ""))
}


listOfCSVs <- list.files(pattern="*[.]csv",full.names=TRUE)
CV.list <- lapply(listOfCSVs, function(file) {
  read.csv(file, header=TRUE, colClasses=c(NA,NA,NA, "NULL", "NULL","NULL","NULL"))
})

#convert list of frames into one dataframe

merged = merge(CV.list[1],CV.list[2],by = "InstanceName",all=TRUE)
merged$X.x = NULL
merged$X.y =NULL

for(i in 3:number_of_solvers){
  merged = merge(merged,CV.list[i],by = "InstanceName",all=TRUE)
  merged$X.x = NULL
  merged$X.y =NULL
}
names(merged)[names(merged)=="Maple_CM_ordUIP."] <- "Maple_CM_ordUIP+"
names(merged)[names(merged)=="Maple_LCM.BCrestart"] <- "Maple_LCM+BCrestart"
names(merged)[names(merged)=="Maple_LCM.BCrestart_M1"] <- "Maple_LCM+BCrestart_M1"

write.csv( merged,paste(partitionName,"-",number_of_solvers,"-",solverstate,"-solvers-parallel.csv",sep = ""))

