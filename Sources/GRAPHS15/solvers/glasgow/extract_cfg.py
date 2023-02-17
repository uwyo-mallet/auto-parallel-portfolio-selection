import angr
import pickle
import sys

p = angr.Project(sys.argv[1], load_options={'auto_load_libs': False})
cfg = p.analyses.CFGFast()
file_g = open(sys.argv[2], 'wb')
pickle.dump(cfg, file_g)

