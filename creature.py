# Creature:
# Max speed: float ~0.0005/tick
# ANN gives wheel multipliers: float 0-1
# Size: float (radius)
# Positions in X and Y: float 0-1
# Brain: ANN
# Antennae: 2
# Antennae length: 3 * Size
# Antennae angle: 0 - 90 degrees

# Inputs:
# 5 for first antennae, i.e. antennae_angles[0]
# 0: Object detection, 1 if detected 0 if not
# 1: R 0 - 1
# 2: G 0 - 1
# 3: B 0 - 1
# 4: Object detection 2...

from brain import Brain
from inhabitant import Inhabitant
import math, random, funcs

class Creature(Inhabitant):
	"""docstring for ClassName"""
	G_MAX_SPEED = 0.005
	G_MAX_ROTATION = 0.05
	antennae = 2
	antennae_angles = [math.pi/6.0, -1.0 * math.pi/6.0]

	def __init__(self, genes, x=0.0, y=0.0):
		super(Creature, self).__init__([x,y], 
			radius_multiplier=0.5, 
			color=(0.1 + 0.9 * random.random(), 0.01 + 0.09 * random.random(), 0.1 + 0.9 * random.random()))
		self.rotation = 0.0
		self.speed = random.random()
		self.distance = 0.0
		self.antennae_length = self.radius_multiplier * self.G_MAXIMUM_RADIUS * 3.5
		self.brain = Brain(genes)

	def gather_input(self, data):
		self.data = data

	def think(self):
		[d_s, d_r] = self.brain.think(self.data)
		d_s = d_s * 2 - 1
		d_r = d_r * 2 - 1

		self.rotation = funcs.sign(self.rotation + d_r * Creature.G_MAX_ROTATION) * (abs(self.rotation + d_r * Creature.G_MAX_ROTATION) % 1.0)

		self.speed += d_s
		if self.speed > 1:
			self.speed = 1
		if self.speed < -1:
			self.speed = -1

	def move(self):
		d_x = math.cos(self.rotation * 2.0 * math.pi) * self.speed * self.G_MAX_SPEED
		d_y = -1.0 * math.sin(self.rotation * 2.0 * math.pi) * self.speed * self.G_MAX_SPEED
		self.pos[0] += d_x
		if self.pos[0] + self.get_radius() > 1:
			self.pos[0] = 1 - self.get_radius()
		elif self.pos[0] - self.get_radius() < 0:
			self.pos[0] = 0 + self.get_radius()
		self.pos[1] += d_y
		if self.pos[1] + self.get_radius() > 1:
			self.pos[1] = 1 - self.get_radius()
		elif self.pos[1] - self.get_radius() < 0:
			self.pos[1] = 0 + self.get_radius()
		self.distance += math.sqrt(d_x**2 + d_y**2)

	def evaluate(self):
		return self.distance
