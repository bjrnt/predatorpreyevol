#!/usr/bin/env python
from world import World
from creature import Creature
from renderer import Renderer
from bush import Bush

import argparse
import sys
import cProfile
import math, time

def onevsone():
	renderer = Renderer(700,700)

	c1 = Creature([0], 0.2, 0.56)
	c1.speed = 0.05
	c1.rotation = 0
	c2 = Creature([0], 0.8, 0.5)
	c2.speed = 0.05
	c2.rotation = 0.5
	
	world.add_creature(c1)
	world.add_creature(c2)

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
	}

	apply_config(options)

	renderer = Renderer(700,700)

	world = World([0]*10,nticks=1000,max_bush_count=20)

	renderer.play_epoch(world,1)
	#world.run_ticks()

def profile():
	cProfile.run('default()', 'stats.pstats')

def main():
	parser = argparse.ArgumentParser(description='Run the simulation.')
	parser.add_argument('--load',dest='load_path', metavar='File', type=file, help="Path to file with saved state, used to resume simulations.")
	parser.add_argument('--profile',dest='profiling_enabled', help="Use to enable or disable generation of profiling information.", required=False, action='store_const', const=True)
	args = parser.parse_args(sys.argv[1:])
	# args.load_path

	start = time.clock()
	if args.profiling_enabled:
		profile()
	else:
		default()
	end = time.clock()
	print "Done!"
	print "Run-time %f" % (0.0 + end - start)
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
