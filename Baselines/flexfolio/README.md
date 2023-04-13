#flexfolio 
an algorithm selection tool and the successor of claspfolio 2.0 (see POTASSCO)

##LICENSE
  flexfolio is part of the ml4aad project (www.ml4aad.org).
  It is distributed under the GNU Public License. See COPYING for
  details regarding the license.
  
##OVERVIEW
  flexfolio is an algorithm selection tool. 
  It is written in Python (Serie 2.7) and uses external binaries
  as, e.g., clasp to determine an algorithm schedule.
  
  Detailed information, source code, are available at: https://bitbucket.org/mlindauer/flexfolio

##RESTRICTIONS

  flexfolio in the current version only selects algorithms wrt 
  optimization of runtime on decision problems.
  
##REQUIREMENTS:

  * Python 2.7
  * numpy, liac-arff and scikit learn (tested with 0.15.0; http://scikit-learn.org/dev/index.html):
    USE the install script for a virtualenv in virtualenv/python_env.sh
    OR
      "pip install -U scikit-learn"
    Requirements of scikit learn: 
      sudo apt-get install build-essential python-dev python-numpy python-setuptools python-scipy libatlas-dev libatlas3-base
    
  * To use "--approach ASPEED" or "--aspeed-opt", you need to have executable binaries of gringo (Serie 3), clasp (Serie 2.1) 
    and the runsolver (http://www.cril.univ-artois.fr/~roussel/runsolver/) in ./binaries
    In addition, write permissions are needed in the current directory (".") for temporary files
   
  
##PACKAGE CONTENTS
  COPYING      - GNU Public License
  CHANGELOG    - Major changes between versions
  README       - This file
  src/flexfolio.py  - Script to run flexfolio
  src/trainer/main_train.py
  			   - Script to train models for flexfolio
  src/		   - source directory
  binaries/	   - directory with pre-compiled binaries, e.g., clasp
  
##USAGE
      python src/flexfolio_train.py --aslib-dir <ASLIB PATH>/<ASLIB SCENARIO/ --model-dir .
      
      for more options see:
      python src/flexfolio_train.py -h
    
##TRAINING:
  To train flexfolio, a directory with files in the ASlib format (--aslib-dir) has to be provided (see aslib.net). 
  Furthermore, you have to provide a dictionary for model related files:
  	--modeldir 				directory for saving models (ATTENTION: overwrites old files!)
 
##CONTACT:
 	Marius Lindauer
 	University of Freiburg
 	lindauer@cs.uni-freiburg.de
 	
  