import math
from world import World
from creature import Creature
from renderer import Renderer

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
	renderer = Renderer(700,700)

	world = World([0]*10,nticks=1000)

	renderer.play_epoch(world,1)


def main():
	default()
	
	print "Done!"
	dontexit = raw_input()

if __name__ == '__main__':
	main()
