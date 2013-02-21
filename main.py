import math, time
from world import World
#from config import Config
from creature import Creature
from renderer import Renderer
import cProfile

def onevsone():
	renderer = Renderer(700,700)

	world_spec = {}
	world_spec['disable_think'] = 1

	world = World(world_spec=world_spec, nticks=600)

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
	}

	apply_config(options)

	renderer = Renderer(700,700)

	world = World([0]*10,nticks=1000,max_bush_count=0)

	renderer.play_epoch(world,1)
	#world.run_ticks()

def profile():
	cProfile.run('default()', 'stats.txt')

def main():
	start = time.clock()
	profile()
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
