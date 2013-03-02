import multiprocessing
import platform
import random
import itertools
import time

from deap import base,creator,tools
from brain import Brain
from world import World
from creature import Creature
from cPickle import Pickler, Unpickler
from numpy import array
	
if platform.python_implementation() != 'PyPy':
	from renderer import Renderer
	renderer_available = True
else:
	renderer_available = False

try:
	# Note, cTools are not compatible with PyPy
	from deap import cTools 
	cTools_available = True
except ImportError:
	cTools_available = False

def simulate(creatures, nticks=None, max_bush_count=None):
	"""Used to run a simulation, placed outside of class to enable multiprocessing"""
	w = World(gene_pool=creatures,nticks=nticks,max_bush_count=max_bush_count)
	w.run_ticks()
	return w.get_creatures()

class Darwin(object):
	"""docstring for Darwin"""
	def __init__(self):

		if Darwin.graphics and renderer_available:
			self.renderer = Renderer(700,700)

		self.toolbox = base.Toolbox()
		self.gen_start_number = 1

		creator.create("FitnessMax", base.Fitness, weights=(1.0,))
		creator.create("Individual", list, fitness=creator.FitnessMax)

		self.toolbox.register("attr_float", random.uniform, -1, 1)
		self.toolbox.register("individual", tools.initRepeat, creator.Individual, self.toolbox.attr_float, Brain.G_TOTAL_CONNECTIONS + 3)
		self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

		self.toolbox.register("mate", tools.cxUniform, indpb=0.5)
		self.toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.3, indpb=2.0/Brain.G_TOTAL_CONNECTIONS)
		
		self.toolbox.register("selectBest", tools.selBest)
		self.toolbox.register("simulate", simulate, nticks=Darwin.NTICKS, max_bush_count=Darwin.max_bush_count)

		if cTools_available:
			self.toolbox.register("select", cTools.selNSGA2)
		else:
			self.toolbox.register("select", tools.selNSGA2)

		self.pop = self.toolbox.population(n=Darwin.NINDS)

		if Darwin.enable_multiprocessing:
			self.pool = multiprocessing.Pool(processes=3)
			self.toolbox.register("map",self.pool.map)
		else:
			self.toolbox.register("map",map)

	def evaluate(self, ind):
		return ind.consumed_energy / 5.0

	def begin_evolution(self):

		# Begin actual evolution
		start_time = time.time()
		for g in xrange(self.gen_start_number,self.gen_start_number+Darwin.NGEN+1):
			pop = self.pop

			creatures = self.simulate()

			fitnesses = [self.evaluate(creature) for creature in creatures]
			for ind,fit in zip(pop, fitnesses):
				ind.fitness.values = fit,

			self.printStats(pop,g)
			if g % 20 == 0:
				self.printTimeStats(start_time,g)

			bestInds = self.toolbox.selectBest(pop, len(pop)/10)
			bestInds = list(self.toolbox.map(self.toolbox.clone, bestInds))
			offspring = self.toolbox.select(pop, len(pop)/10 * 9)
			offspring = list(self.toolbox.map(self.toolbox.clone, offspring))

			for child1,child2 in zip(offspring[::2],offspring[1::2]):
				if random.random() < Darwin.CXPB:
					self.toolbox.mate(child1,child2)
					del child1.fitness.values
					del child2.fitness.values

			for mutant in offspring:
				if random.random() < Darwin.MUTPB:
					self.toolbox.mutate(mutant)

			self.pop[:] = bestInds + offspring
			for ind in self.pop:
				del ind.fitness.values

		self.gen_start_number = g
		f = open('save.txt','w')
		self.save_population(f)

	def printTimeStats(self,start_time,gen):
		time_spent = time.time() - start_time
		avg = time_spent / (gen + 1 - self.gen_start_number)
		generations_left = (self.gen_start_number + Darwin.NGEN - gen)
		print '\033[95m' + "# Time stats: Spent: %2.2f s, Avg/gen: %2.2f s" % (time_spent, avg)
		print "# Time to run %i gens: %2.2f s" % (generations_left, generations_left * avg), '\033[0m'

	def printStats(self,pop,gen):
		fits = [ind.fitness.values[0] for ind in pop]
		mean = sum(fits) / len(pop)
		print ("(%3i): Max: %6.2f, Avg: %6.2f, Min: %5.2f" % (gen, max(fits), mean, min(fits)))

	def simulate(self):
		res = []
		if len(self.pop) > Darwin.num_per_sim:
			inputs = [self.pop[i*Darwin.num_per_sim:(i+1)*Darwin.num_per_sim] for i in xrange(0,len(self.pop)/Darwin.num_per_sim)]
			if Darwin.graphics and renderer_available:
				res += list(itertools.chain(*self.toolbox.map(self.toolbox.simulate, inputs[1:])))
				res += self.renderer.play_epoch(World(gene_pool=inputs[0], nticks=Darwin.NTICKS, max_bush_count=Darwin.max_bush_count))
			else:
				res = list(itertools.chain(*self.toolbox.map(self.toolbox.simulate, inputs)))
		else:
			if Darwin.graphics and renderer_available:
				res = self.renderer.play_epoch(World(gene_pool=self.pop, nticks=Darwin.NTICKS, max_bush_count=Darwin.max_bush_count))
			else:
				res = self.toolbox.simulate(self.pop)

		return res

	def save_population(self,save_file):
		pickler = Pickler(save_file)
		data = (self.pop, self.gen_start_number + 1)
		pickler.dump(data)
		save_file.close()

	def load_population(self,load_file):
		unpickler = Unpickler(load_file)
		self.pop, self.gen_start_number = unpickler.load()
		load_file.close()
