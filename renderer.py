import pygame,math,world,creature
from pygame.locals import *

class Renderer(object):
	"""docstring for Renderer"""
	def __init__(self, width=700, height=700):
		pygame.init()

		self.width = 700
		self.height = 700

		self.screen = pygame.display.set_mode((self.width,self.height))
		pygame.display.set_caption('Our kEX')
		self.background = pygame.Surface(self.screen.get_size())
		self.background = self.background.convert()
		self.background.fill((0,0,0))
		self.screen.blit(self.background,(0,0))

	def play_epoch(self, world, disp_freq=1):
		for tick in xrange(world.nticks):
			world.run_tick()
			if tick % disp_freq == 0:
				self.render_creatures(world)

	def render_creatures(self, world):	
		self.screen.blit(self.background,(0,0))
		for creature in world.get_creatures():
			pygame.draw.line(self.screen,
				(255,255,255),
				(int(self.width * creature.pos[0]), int(self.height * creature.pos[1])),
				(int(self.width * (creature.pos[0] + creature.antennae_length * math.cos(creature.rotation * 2 * math.pi + creature.antennae_angles[0]))), 
				 int(self.height * (creature.pos[1] + -1 * creature.antennae_length * math.sin(creature.rotation * 2 * math.pi + creature.antennae_angles[0])))),
				)
			pygame.draw.line(self.screen,
				(255,255,255),
				(int(self.width * creature.pos[0]), int(self.height * creature.pos[1])),
				(int(self.width * (creature.pos[0] + creature.antennae_length * math.cos(creature.rotation * 2 * math.pi + creature.antennae_angles[1]))), 
				 int(self.height * (creature.pos[1] + -1 * creature.antennae_length * math.sin(creature.rotation * 2 * math.pi + creature.antennae_angles[1])))),
				)
			pygame.draw.circle(self.screen, 
				[color * 255 for color in creature.get_color()], 
				(int(self.width * creature.pos[0]), int(self.height * creature.pos[1])),
				1 + int(creature.get_radius() * self.height),
				0
				)

		pygame.display.flip()
