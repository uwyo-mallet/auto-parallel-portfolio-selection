#!/bin/bash

python transform_satzilla12.py --file SATzilla2012_data/SATALL12S.csv --fgroup satzilla11_data/f_group_dict.json --cutoff 1200 --dir sat12-all/ --fcutoff 1200 --name SAT12-ALL --listfile SATzilla2012_data/INSTANCE.csv
python transform_satzilla12.py --file SATzilla2012_data/SATHAND12S.csv --fgroup satzilla11_data/f_group_dict.json --cutoff 1200 --dir sat12-hand/ --fcutoff 1200 --name SAT12-HAND --listfile SATzilla2012_data/INSTANCE.csv
python transform_satzilla12.py --file SATzilla2012_data/SATINDU12S.csv --fgroup satzilla11_data/f_group_dict.json --cutoff 1200 --dir sat12-indu/ --fcutoff 1200 --name SAT12-INDU --listfile SATzilla2012_data/INSTANCE.csv
python transform_satzilla12.py --file SATzilla2012_data/SATRAND12S.csv --fgroup satzilla11_data/f_group_dict.json --cutoff 1200 --dir sat12-rand/ --fcutoff 1200 --name SAT12-RAND --listfile SATzilla2012_data/INSTANCE.csv
