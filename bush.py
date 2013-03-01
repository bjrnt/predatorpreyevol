from inhabitant import Inhabitant
from creature import Creature

class Bush(Inhabitant):
	"""docstring for Bush"""
	def __init__(self, x=0, y=0):
		super(Bush, self).__init__([x,y], radius_multiplier=0.1, color=(0.0,1.0,0.0), energy=10)

	def think(self):
		if self.radius_multiplier < 0.4:
			self.radius_multiplier += 0.01

		if Bush.use_energy:
			if self.energy < 100:
				self.energy += 1

		#if self.color[1] < 1:
		#	self.color = (0.1,self.color[1] + 0.01, 0.1)

	def on_collision(self, target):
		if Bush.use_energy and target.__class__ == Creature:
			target.energy += self.energy
			target.consumed_energy += self.energy

		if target.__class__ == Creature:
			self.alive = 0