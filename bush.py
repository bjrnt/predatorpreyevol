from inhabitant import Inhabitant

class Bush(Inhabitant):
	"""docstring for Bush"""
	def __init__(self, x=0, y=0):
		super(Bush, self).__init__([x,y], radius_multiplier=0.1, color=(0.1,0.4,0.1), energy=10)

	def think(self):
		if self.radius_multiplier < 0.4:
			self.radius_multiplier += 0.01

		if self.energy < 100:
			self.energy += 1

		if self.color[1] < 1:
			self.color = (0.1,self.color[1] + 0.01, 0.1)
