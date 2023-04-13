#!/bin/bash

python2.7 transform_satzilla11.py --file satzilla11_data/SATRAND11.csv --listfile satzilla11_data/random.list --fgroup satzilla11_data/f_group_dict.json --dir sat11-rand/ --cutoff 5000 --fcutoff 5000 --name SAT11-RANDOM
python2.7 transform_satzilla11.py --file satzilla11_data/SATINDU11.csv --listfile satzilla11_data/indus.list --fgroup satzilla11_data/f_group_dict.json --dir sat11-indu --cutoff 5000 --fcutoff 5000 --name SAT11-INDU
python2.7 transform_satzilla11.py --file satzilla11_data/SATHAND11.csv --listfile satzilla11_data/crafted.list --fgroup satzilla11_data/f_group_dict.json --dir sat11-hand/ --cutoff 5000 --fcutoff 5000 --name SAT11-HAND

