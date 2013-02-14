import random, funcs, math
from brain import Brain
from creature import Creature
from bush import Bush

class World(object):
	"""docstring for ClassName"""
	def __init__(self, gene_pool=None, max_bush_count=0, world_spec=None, nticks=10000):
		self.creatures = []
		self.bushes = []
		self.nticks = nticks
		if gene_pool != None:
			for gene in gene_pool:
				self.creatures += [Creature(gene, x=random.random(), y=random.random())]
		
		self.max_bush_count = max_bush_count
		
		if world_spec != None:
			self.world_spec = world_spec
		else:
			self.world_spec = {}

	def run_tick(self):
		self.spawn_bushes()

		# Get data for creatures to process
		for creature in self.creatures:
			creature_got_input = False
			
			if 'disable_detection' not in self.world_spec.keys():
				for inhabitant in self.get_inhabitants():
					if inhabitant != creature:
						[left, right] = self.check_detection(creature,inhabitant)

						if left != [0] * (Brain.G_INPUTNODES/2) or right != [0] * (Brain.G_INPUTNODES/2):
							creature_got_input = True
				[left, right] = self.detect_walls(creature, left, right)

				creature.gather_input(left + right)

			if 'disable_default_input' not in self.world_spec.keys():
				if not creature_got_input:
					creature.gather_input([0] * Brain.G_INPUTNODES)

		if 'disable_think' not in self.world_spec.keys():
			for inhabitant in self.get_inhabitants():
				inhabitant.think()
		
		if 'disable_move' not in self.world_spec.keys():
			for inhabitant in self.get_inhabitants():
				inhabitant.move()
		
	def run_ticks(self):
		for tick in xrange(self.nticks):
			self.run_tick()
		return [creature.evaluate() for creature in self.creatures]

	def detect_walls(self, looker, left, right):
		if left == [0] * (Brain.G_INPUTNODES/2):
			v_an1 = [looker.antennae_length * math.cos(looker.rotation * 2 * math.pi + looker.antennae_angles[0]),
			-1 * looker.antennae_length * math.sin(looker.rotation * 2 * math.pi + looker.antennae_angles[0])]

			antennae_point1 = funcs.vplus(looker.pos, v_an1)

			if antennae_point1[0] < 0 or antennae_point1[0] > 1 or antennae_point1[1] < 0 or antennae_point1[1] > 1:
				left[0] = 1
				left[1], left[2], left[3] = [1,1,1]
				print "Wall detection 1"

		if right == [0] * (Brain.G_INPUTNODES/2):
			v_an2 = [looker.antennae_length * math.cos(looker.rotation * 2 * math.pi + looker.antennae_angles[1]),
			-1 * looker.antennae_length * math.sin(looker.rotation * 2 * math.pi + looker.antennae_angles[1])]

			antennae_point2 = funcs.vplus(looker.pos, v_an2)

			if antennae_point2[0] < 0 or antennae_point2[0] > 1 or antennae_point2[1] < 0 or antennae_point2[1] > 1:
				right[0] = 1
				right[1], right[2], right[3] = [1,1,1]
				print "Wall detection 2"

		return left, right

	def check_detection(self,looker, target):
		"""Todo: detection doesn't work well, at all"""
		invalid1 = False
		invalid2 = False

		left = [0] * (Brain.G_INPUTNODES/2)
		right = [0] * (Brain.G_INPUTNODES/2)

		v_dist = funcs.vminus(target.pos, looker.pos)
		v_an1 = [looker.antennae_length * math.cos(looker.rotation * 2 * math.pi + looker.antennae_angles[0]),
			-1 * looker.antennae_length * math.sin(looker.rotation * 2 * math.pi + looker.antennae_angles[0])]
		v_an2 = [looker.antennae_length * math.cos(looker.rotation * 2 * math.pi + looker.antennae_angles[1]),
			-1 * looker.antennae_length * math.sin(looker.rotation * 2 * math.pi + looker.antennae_angles[1])]
		
		v_proj1 = [v_an1[0] * funcs.dot(v_an1, v_dist) / funcs.vlen(v_an1)**2, v_an1[1] * funcs.dot(v_an1, v_dist) / funcs.vlen(v_an1)**2]
		v_proj2 = [v_an2[0] * funcs.dot(v_an2, v_dist) / funcs.vlen(v_an2)**2, v_an2[1] * funcs.dot(v_an2, v_dist) / funcs.vlen(v_an2)**2]

		# If the projection points in the exact opposite direction of the antenna no detection is possible
		if v_an1[0] > 0 and v_proj1[0] < 0 or v_an1[0] < 0 and v_proj1[0] > 0:
			invalid1 = True
		if v_an2[0] > 0 and v_proj2[0] < 0 or v_an2[0] < 0 and v_proj2[0] > 0:
			invalid2 = True


		# If the projection is longer than the antennae we pretend that the antennae is the projection to avoid false positives
		if funcs.vlen(v_proj1) > funcs.vlen(v_an1): 
			v_proj1 = v_an1
		if funcs.vlen(v_proj2) > funcs.vlen(v_an2):
			v_proj2 = v_an2

		dist_from_proj1 = funcs.vminus(v_proj1, v_dist)
		dist_from_proj2 = funcs.vminus(v_proj2, v_dist)

		if funcs.vlen(dist_from_proj1) < target.get_radius() and not invalid1:
			left[0] = 1
			left[1],left[2],left[3] = target.get_color()

		if funcs.vlen(dist_from_proj2) < target.get_radius() and not invalid2:
			right[0] = 1
			right[1],right[2],right[3] = target.get_color()
		
		return left, right

	def spawn_bushes(self):
		if len(self.get_bushes()) < self.max_bush_count:
			for i in xrange(self.max_bush_count - len(self.get_bushes())):
				if random.random() < 0.01:
					self.add_bush(Bush(random.random(), random.random()))

	def add_bush(self, bush):
		self.bushes += [bush]

	def add_creature(self,creature):
		self.creatures += [creature]

	def get_inhabitants(self):
		return self.creatures + self.bushes


	def get_positions(self):
		return [creature.pos for creature in self.creatures]

	def get_creatures(self):
		return self.creatures

	def get_bushes(self):
		return self.bushes