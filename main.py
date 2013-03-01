#!/usr/bin/env python
from world import World
from creature import Creature
from renderer import Renderer
from bush import Bush
from darwin import Darwin

import argparse, sys, cProfile, math, time

def default():
	options = {
		('World','move'):True,
		('World','think'):True,
		('World','default_input'):True,
		('World','detection'):True,
		('World','collision'):True,
		('World','remove_dead'):True,

		('Creature','Bush','use_energy'):True,
		('Creature','G_MAX_SPEED'):0.005,

		('Darwin','CXPB'):0.0,
		('Darwin','MUTPB'):0.4,

		('Darwin','NGEN'):3,
		('Darwin','NINDS'):30, # Must be a number divisible by 10 and by num_per_sim
		('Darwin','max_bush_count'):10,

		('Darwin','num_per_sim'):10,
		('Darwin','NTICKS'):1000,

		('Darwin','graphics'):False,
		('Renderer','disp_freq'):4,
		('Darwin','enable_multiprocessing'):True,
	}

	apply_config(options)

	darwin = Darwin()
	
	if load_file:
		darwin.load_population(load_file)

	darwin.begin_evolution()

def profile():
	cProfile.run('default()', 'stats.pstats')

def main():
	parser = argparse.ArgumentParser(description='Run the simulation.')
	parser.add_argument('-l',dest='load_file', metavar='file', type=file, help="Path to file with saved state, used to resume simulations.")
	parser.add_argument('--profile',dest='profiling_enabled', help="Use to enable or disable generation of profiling information.", required=False, action='store_const', const=True)
	args = parser.parse_args(sys.argv[1:])

	global load_file

	if args.load_file:
		load_file = args.load_file
	else:
		load_file = None

	if args.profiling_enabled:
		profile()
	else:
		start = time.time()
		default()
		end = time.time()	
		print "Run-time %f" % (0.0 + end - start)

	print "Done!"
	dontexit = raw_input()

def apply_config(config):
	for key in config.keys():
		clses = key[:-1]
		attr = key[-1]
		for cls in clses:
			if cls.istitle():
				setattr(eval(cls),attr,config[key])

if __name__ == '__main__':
	main()
