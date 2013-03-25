
import os


g = 500
bg = 18
br = 0

for i in xrange(60,241,60):
	b = 'BrainLinear'	
	os.system("pypy main.py -s %s_gen_%d_ind_%d_bg_%d_br_%d.txt -b %s -g %d -i %d -bg %d -br %i" % (b,g,i,bg,br,b,g,i,bg,br))
	os.system("python stats.py -m disk -l stats_%s_gen_%d_ind_%d_bg_%d_br_%d.txt -s %s_gen_%d_ind_%d_bg_%d_br_%d" % (b,g,i,bg,br,b,g,i,bg,br))
	b = 'BrainRBF'
	os.system("pypy main.py -s %s_gen_%d_ind_%d_bg_%d_br_%d.txt -b %s -g %d -i %d -bg %d -br %i" % (b,g,i,bg,br,b,g,i,bg,br))
	os.system("python stats.py -m disk -l stats_%s_gen_%d_ind_%d_bg_%d_br_%d.txt -s %s_gen_%d_ind_%d_bg_%d_br_%d" % (b,g,i,bg,br,b,g,i,bg,br))

