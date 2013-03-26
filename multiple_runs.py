
import os


g = 300
bg = 18
#br = 10
#ni = 200
#np = 20
for ni in xrange(100,201,100):
	np = ni / 10	
	for bg in xrange(10,21,5):
		for br in xrange(2,13,5):
			b = 'BrainLinear'	
			os.system("pypy main.py -s %s_gen_%d_ind_%d_pred_%d_bg_%d_br_%d.txt -b %s -g %d -ni %d -np %d -bg %d -br %i" % (b,g,ni,np,bg,br,b,g,ni,np,bg,br))
			os.system("python stats.py -m disk -l stats_%s_gen_%d_ind_%d_pred_%d_bg_%d_br_%d.txt -s %s_gen_%d_ind_%d_pred_%d_bg_%d_br_%d" % (b,g,ni,np,bg,br,b,g,ni,np,bg,br))
			b = 'BrainRBF'
			os.system("pypy main.py -s %s_gen_%d_ind_%d_pred_%d_bg_%d_br_%d.txt -b %s -g %d -ni %d -np %d -bg %d -br %i" % (b,g,ni,np,bg,br,b,g,ni,np,bg,br))
			os.system("python stats.py -m disk -l stats_%s_gen_%d_ind_%d_pred_%d_bg_%d_br_%d.txt -s %s_gen_%d_ind_%d_pred_%d_bg_%d_br_%d" % (b,g,ni,np,bg,br,b,g,ni,np,bg,br))

