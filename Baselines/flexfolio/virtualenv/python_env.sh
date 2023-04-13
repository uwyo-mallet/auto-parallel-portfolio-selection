# builds a python virtual environment with all required packages for flexfolio

virtualenv .
./bin/pip install -I numpy==1.9.2 
./bin/pip install -I scipy==0.15.1
./bin/pip install -I matplotlib==1.4.3 
./bin/pip install -U liac-arff 
./bin/pip install -I scikit-learn==0.15.0
