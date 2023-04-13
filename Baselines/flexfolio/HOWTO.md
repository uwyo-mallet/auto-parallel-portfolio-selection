# HOWTO

## How to add a new algorithm selection (AS) approach?

The code of new AS selection approaches should live in :
 1. src/trainer/selection/ for the training methods
 2. src/selector/ for testing/running 
 
We assume that AS approaches are decoupled from the concrete machine learning method;
in particular, the testing method does normally not know what ML method was used. 
 
Training and testing communicate over a dictionary (saved as JSON).
Therefore, the training method has to return a "sel_dict" the following structure:

        sel_dic = {
                   "approach": {
                                "approach" : "<NAME>",
                                },
                   "normalization" : {
                                      "filter"  : f_indicator                           
                                 },
                   "configurations": conf_dic                        
                   } 
 
You can add further data under "approach", e.g., parameters of your approach.
 
To use new AS approaches, you have to add it in several places:
 1. src/trainer/taining_parser/cmd_training_parser.py 
    Add the AS approach in the parameter "--approach"
 2. src/flexfolio_train.py 
   1. __init__(): self.selection_methods in the same way as it registered in the command line parser
   2. train(): somewhere in the huge if statement
 3. src/selector/selectionApp.py
   add the name of your approach and the class this implements the testing in "selector"
   
    
   