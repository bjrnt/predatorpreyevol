#!/usr/bin/env python
from world import World
from creature import Creature
from renderer import Renderer
from bush import Bush
from darwin import Darwin
from disker import Disker
#from deap import dtm

import argparse, sys, cProfile, math, time

def onevsone():
	renderer = Renderer(700,700)

	options = {
		('World','move'):True,
		('World','think'):False,
		('World','default_input'):True,
		('World','detection'):True,
		('World','collision'):True,
		('World','remove_dead'):True,
		('Creature','Bush','use_energy'):False,
		('Creature','G_MAX_SPEED'):0.08,
	}

	apply_config(options)

	world = World()

	b1 = Bush(0.5, 0.65)
	for x in xrange(100):
		b1.think()

	c1 = Creature(None, 0.2, 0.60)
	c1.speed = 0.05
	c1.rotation = 0
	c2 = Creature(None, 0.8, 0.8)
	c2.speed = 0.05
	c2.rotation = 0.5
	
	world.add_creature(c1)
	world.add_creature(c2)
	world.add_bush(b1)

	renderer.play_epoch(world,1)

def default():
	options = {
		('World','move'):True,
		('World','think'):True,
		('World','default_input'):True,
		('World','detection'):True,
		('World','collision'):True,
		('World','remove_dead'):True,
		('Creature','Bush','use_energy'):True,
		('Creature','G_MAX_SPEED'):0.006,
		('Darwin','NGEN'):300,
		('Darwin','CXPB'):0.25,
		('Darwin','MUTPB'):0.5,
		('Darwin','NINDS'):10,
		('Darwin','NTICKS'):1000,
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
		start = time.clock()
		default()
		end = time.clock()	
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
