from deap import base,creator,tools
from brain import Brain
from world import World
from renderer import Renderer
from creature import Creature
#from deap import dtm
from deap.tools import History
from cPickle import Pickler, Unpickler

import matplotlib.pyplot as plt
import networkx
import random

class Darwin(object):
	"""docstring for Evolver"""
	def __init__(self):
		self.renderer = Renderer(700,700)

		#self.history = History()
		self.toolbox = base.Toolbox()

		creator.create("FitnessMax", base.Fitness, weights=(1.0,))
		creator.create("Individual", list, fitness=creator.FitnessMax)

		self.toolbox.register("attr_float", random.uniform, -1, 1)
		self.toolbox.register("individual", tools.initRepeat, creator.Individual, self.toolbox.attr_float, Brain.G_TOTAL_CONNECTIONS + 3)
		self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
		self.toolbox.register("mate", tools.cxUniform, indpb=0.5)
		#self.toolbox.register("mutate", Darwin.mutate_nodes, sigma=0.3, indpb=0.2)
		self.toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.5, indpb=0.2)
		self.toolbox.register("select", tools.selRoulette)
		self.toolbox.register("selectBest", tools.selBest)
		self.toolbox.register("map",map)

		#self.toolbox.decorate("mate", self.history.decorator)
		#self.toolbox.decorate("mutate", self.history.decorator)

		self.pop = self.toolbox.population(n=Darwin.NINDS)

	# layers = [
	# 	Brain.G_HIDDENNODES_L1, 
	# 	Brain.G_HIDDENNODES_L2, 
	# 	Brain.G_OUTPUTNODES, 
	# 	Brain.G_HIDDENNODES_L1*Brain.G_HIDDENNODES_L2, 
	# 	Brain.G_INPUTNODES*Brain.G_HIDDENNODES_L1, 
	# 	Brain.G_HIDDENNODES_L2*Brain.G_OUTPUTNODES]

	# offsets = [0, 
	# 	layers[0] - 1, 
	# 	sum(layers[0:2]) - 1, 
	# 	sum(layers[0:3]) - 1, 
	# 	sum(layers[0:4]) - 1,
	# 	sum(layers[0:5]) - 1,
	# 	sum(layers[0:6]) - 1,
	# 	sum(layers) - 1]

	# num_nodes_in_layer = [1, 1, 1, Brain.G_HIDDENNODES_L2, Brain.G_HIDDENNODES_L1, Brain.G_OUTPUTNODES]

	# @staticmethod
	# def mutate_nodes(ind, sigma, indpb):
	# 	# bias -> hidden1
	# 	# bias -> hidden2
	# 	# bias -> out
	# 	# hidden1 -> hidden2
	# 	# input -> hidden1
	# 	# hidden2 -> out
	# 	has_changed = False

	# 	for layer_number in xrange(0,len(Darwin.layers)):
	# 		weights_per_node = Darwin.layers[layer_number] / Darwin.num_nodes_in_layer[layer_number]

	# 		for node in xrange(Darwin.num_nodes_in_layer[layer_number]):
	# 			if random.random() < indpb:
	# 				has_changed = True

	# 				mutation = random.gauss(0,sigma)

	# 				for weight_number in xrange(weights_per_node):
	# 					ind[Darwin.offsets[layer_number] + weights_per_node * node + weight_number] += mutation

	# 	if has_changed:
	# 		ind[-3],ind[-2],ind[-1] = tools.mutGaussian(ind[-3:], 0, 0.6, 0.33)[0]

	# 	return ind

	def evaluate(self, ind):
		return ind.consumed_energy / 5.0

	def begin_evolution(self):
		# Begin actual evolution
		for g in xrange(1,Darwin.NGEN):
			pop = self.pop
			#self.history.update(pop)

			if g % 1 == 0 and g != 0:
				creatures = self.simulate(True)
			else:
				creatures = self.simulate(False)

			fitnesses = [self.evaluate(creature) for creature in creatures]
			for ind,fit in zip(pop, fitnesses):
				ind.fitness.values = fit,
				#print "%s %s" % (sum(ind), fit)

			print "--Generation %d (size: %d) --" % (g, len(pop))
			self.printStats(pop)

			bestInds = self.toolbox.selectBest(pop, len(pop)/10 * 2)
			bestInds = list(self.toolbox.map(self.toolbox.clone, bestInds))
			#print bestInds[0]
			#print bestInds[1]
			offspring = self.toolbox.select(pop, len(pop)/10 * 8)
			offspring = list(self.toolbox.map(self.toolbox.clone, offspring))

			for child1,child2 in zip(offspring[::2],offspring[1::2]):
				if random.random() < Darwin.CXPB:
					self.toolbox.mate(child1,child2)
					del child1.fitness.values
					del child2.fitness.values

			for mutant in offspring:
				if random.random() < Darwin.MUTPB:
					self.toolbox.mutate(mutant)
					#del mutant.fitness.values

			self.pop[:] = bestInds + offspring
			for ind in self.pop:
				#print "%s" % (sum(ind))
				del ind.fitness.values

		f = open('save.txt','w')
		self.save_population(f)
		# Done evolving
		#print self.history.genealogy_tree
		#graph = networkx.DiGraph(self.history.genealogy_tree)
		#graph = graph.reverse()     # Make the grah top-down
		#colors = [self.toolbox.evaluate(self.history.genealogy_history[i])[0] for i in graph]
		#networkx.draw(graph)
		#plt.show()

	def printStats(self,pop):
		fits = [ind.fitness.values[0] for ind in pop]
		mean = sum(fits) / len(pop)
		print ("Max: %s, Avg: %s, Min: %s" % (max(fits), mean, min(fits)))

	def simulate(self, draw=False):
		world = World(gene_pool=self.pop,nticks=Darwin.NTICKS,max_bush_count=10)

		if draw:
			self.renderer.play_epoch(world, 1)
		else:
			world.run_ticks()

		return world.get_creatures()

	def save_population(self,save_file):
		pickler = Pickler(save_file)
		pickler.dump(self.pop)
		save_file.close()

	def load_population(self,load_file):
		unpickler = Unpickler(load_file)
		self.pop = unpickler.load()
		load_file.close()
