
import os

g = 500
bg = 15
br = 0
ni = 200
np = ni / 10	
b = 'BrainLinear'	
os.system("pypy main.py -s %s_gen%d_ind%d_pred%d_bg%d_br%d.txt -b %s -g %d -ni %d -np %d -bg %d -br %i" % (b,g,ni,np,bg,br,b,g,ni,np,bg,br))
os.system("python stats.py -m disk -l stats_%s_gen%d_ind%d_pred%d_bg%d_br%d.txt -s %s_gen_%d_ind_%d_pred_%d_bg_%d_br_%d" % (b,g,ni,np,bg,br,b,g,ni,np,bg,br))
b = 'BrainRBF'
os.system("pypy main.py -s %s_gen%d_ind%d_pred%d_bg%d_br%d.txt -b %s -g %d -ni %d -np %d -bg %d -br %i" % (b,g,ni,np,bg,br,b,g,ni,np,bg,br))
os.system("python stats.py -m disk -l stats_%s_gen%d_ind%d_pred%d_bg%d_br%d.txt -s %s_gen_%d_ind_%d_pred_%d_bg_%d_br_%d" % (b,g,ni,np,bg,br,b,g,ni,np,bg,br))

# Test:
# Gröna buskar, inga preds x 2 
# Gröna buskar, preds x 2
# Gröna röda buskar x 2
# Random med alla också