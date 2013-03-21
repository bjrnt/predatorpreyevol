import platform
if platform.python_implementation() == 'PyPy':
    import numpypy
else:
    import matplotlib.pyplot as plt 

from cPickle import Pickler,Unpickler
from collections import defaultdict
import numpy as np
import copy, argparse, sys

stats = defaultdict(list)

def add(stat,val):
	stats[stat] += [val]

def get(stat):
	return stats[stat]

def export_stats():
	return stats

def import_stats(stats_dict):
	global stats
	stats = copy.deepcopy(stats_dict)

def save_stats(save_file):
	pickler = Pickler(save_file)
	pickler.dump(stats)
	save_file.close()

def load_stats(load_file):
	unpickler = Unpickler(load_file)
	stats_to_import = unpickler.load()
	import_stats(stats_to_import)
	load_file.close()

def plot_all():
	if platform.python_implementation() == 'PyPy':
		print "Running pypy, cannot plot"
		return

	for stat in stats:
		fig = create_figure(stat)
		fig.show()
		dontexit = raw_input()

def save_all(save_prefix):
	for stat in stats:
		fig = create_figure(stat)
		fig.savefig(save_prefix + "_" + stat + '.png',bbox_inches=0)

def create_figure(stat):
	if platform.python_implementation() == 'PyPy':
		print "Running pypy, cannot plot"
		return

	y_vals = stats[stat]
	x_vals = xrange(1,len(y_vals)+1)

	p1, = plt.plot(x_vals, y_vals, linewidth=2.0)
	plt.legend([p1],[stat])
	plt.axis([1, len(y_vals), min(y_vals)*0.90, max(y_vals)*1.1])
	plt.title(stat)
	plt.ylabel('Value')
	plt.xlabel('Generation #')
	return plt.gcf()

def main():
	parser = argparse.ArgumentParser(description='Stand alone plotting program.')
	parser.add_argument('-m', dest='mode', metavar='str', type=str, help="Run the program in the following mode.")
	parser.add_argument('-l', dest='load_file', metavar='file', type=str, help="The file to load.")
	parser.add_argument('-s', dest='save_prefix', metavar='file', type=str, help="Prefix for saving images.")
	args = parser.parse_args(sys.argv[1:])
	
	if args.mode == 'plot':
		load_stats(open(args.load_file))
		plot_all()
		dontexit = raw_input()
	if args.mode == 'disk':
		load_stats(open(args.load_file))
		save_all(args.save_prefix)



if __name__ == '__main__':
	main()
