import random, funcs, math
from brain import Brain
from creature import Creature
from bush import Bush
import numpy as np
from numpy import array

class World(object):
	"""docstring for ClassName"""
	def __init__(self, gene_pool=None, max_bush_count=0, nticks=10000):
		self.creatures = []
		self.dead_creatures = []
		self.bushes = []
		self.nticks = nticks
		if gene_pool != None:
			for gene in gene_pool:
				self.creatures += [Creature(gene, x=random.random(), y=random.random())]
		
		self.max_bush_count = max_bush_count
		#self.spawn_bushes_grid()

	def run_tick(self):
		self.spawn_bushes()

		# Get data for creatures to process
		if World.detection:
			inhabitants = self.bushes # Only detecting/colliding with bushes
			positions = array([inh.get_pos() for inh in inhabitants])
			radii = array([inh.get_radius() for inh in inhabitants])

			for creature in self.creatures:
				creature_got_input = False
				left = [0] * (Brain.G_INPUTNODES/2)
				right = [0] * (Brain.G_INPUTNODES/2)

				if positions != []:
					diffs = positions - creature.get_pos()
					distances = array([funcs.vlen(diff) for diff in diffs] - radii)
					for index, val in enumerate(distances):
						if val <= creature.antennae_length and creature != inhabitants[index]:
							[left, right] = self.check_detection(creature,inhabitants[index])

						if val <= creature.get_radius() and creature != inhabitants[index]:
							creature.on_collision(inhabitants[index])
							inhabitants[index].on_collision(creature)
					
				if creature.get_x() - creature.antennae_length < 0 or creature.get_x() + creature.antennae_length > 1 or creature.get_y() - creature.antennae_length < 0 or creature.get_y() + creature.antennae_length > 1:
					[left, right] = self.detect_walls(creature, left, right)

				if left != [0] * (Brain.G_INPUTNODES/2) or right != [0] * (Brain.G_INPUTNODES/2):
					creature_got_input = True
					creature.gather_input(left + right)

				if World.default_input:
					if not creature_got_input:
						creature.gather_input(left + right)

		if World.think:
			for inhabitant in self.get_inhabitants():
				inhabitant.think()
		
		if World.move:
			for inhabitant in self.get_inhabitants():
				inhabitant.move()

		if World.remove_dead:
			for inhabitant in self.get_inhabitants():
				if inhabitant.alive == False:
					if inhabitant.__class__ == Creature:
						self.creatures.remove(inhabitant)
						self.dead_creatures += [inhabitant]
					if inhabitant.__class__ == Bush:
						self.bushes.remove(inhabitant)

	def run_ticks(self):
		for tick in xrange(self.nticks):
			self.run_tick()

	def detect_walls(self, looker, left, right):
		angle = looker.rotation * 2 * math.pi
		if left == [0] * (Brain.G_INPUTNODES/2):
			v_an1 = [looker.antennae_length * math.cos(angle + looker.antennae_angles[0]),
			-1 * looker.antennae_length * math.sin(angle + looker.antennae_angles[0])]

			antennae_point1 = funcs.vplus(looker.pos, v_an1)

			if antennae_point1[0] < 0 or antennae_point1[0] > 1 or antennae_point1[1] < 0 or antennae_point1[1] > 1:
				left[0] = 1
				left[1], left[2], left[3] = [0,0,1]

		if right == [0] * (Brain.G_INPUTNODES/2):
			v_an2 = [looker.antennae_length * math.cos(angle + looker.antennae_angles[1]),
			-1 * looker.antennae_length * math.sin(angle + looker.antennae_angles[1])]

			antennae_point2 = funcs.vplus(looker.pos, v_an2)

			if antennae_point2[0] < 0 or antennae_point2[0] > 1 or antennae_point2[1] < 0 or antennae_point2[1] > 1:
				right[0] = 1
				right[1], right[2], right[3] = [0,0,1]

		return left, right

	def check_detection(self,looker, target):
		invalid1 = False
		invalid2 = False

		inputs = Brain.G_INPUTNODES/2
		left = [0] * inputs
		right = [0] * inputs

		v_dist = funcs.vminus(target.pos, looker.pos)

		angle = looker.rotation * 2 * math.pi
		v_an1 = array([looker.antennae_length * math.cos(angle + looker.antennae_angles[0]),
			-1 * looker.antennae_length * math.sin(angle + looker.antennae_angles[0])])
		v_an2 = array([looker.antennae_length * math.cos(angle + looker.antennae_angles[1]),
			-1 * looker.antennae_length * math.sin(angle + looker.antennae_angles[1])])
		
		an1_dist_sq = funcs.dot(v_an1, v_dist) / funcs.vlen(v_an1)**2
		an2_dist_sq = funcs.dot(v_an2, v_dist) / funcs.vlen(v_an2)**2
		v_proj1 = array([v_an1[0] * an1_dist_sq, v_an1[1] * an1_dist_sq])
		v_proj2 = array([v_an2[0] * an2_dist_sq, v_an2[1] * an2_dist_sq])

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
				if random.random() < 0.05:
					self.add_bush(Bush(random.uniform(0.05,0.95), random.uniform(0.05,0.95)))

	def spawn_bushes_grid(self):
		for i in xrange(1,5):
			for j in xrange(1,5):
				self.add_bush(Bush(i*0.2, j*0.2))

	def add_bush(self, bush):
		self.bushes += [bush]

	def add_creature(self,creature):
		self.creatures += [creature]

	def get_inhabitants(self):
		return self.creatures + self.bushes

	def get_positions(self):
		return [creature.pos for creature in self.creatures]

	def get_creatures(self):
		return self.creatures + self.dead_creatures

	def get_living_creatures(self):
		return self.creatures

	def get_bushes(self):
		return self.bushes
