from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pyevolve.G1DList import G1DList
from pyevolve.GSimpleGA import GSimpleGA
from pyevolve.Initializators import G1DListInitializatorReal
from pyevolve.Mutators import G1DListMutatorRealGaussian
from pyevolve.Selectors import GRouletteWheel
from math import exp

DS = SupervisedDataSet(1,1)
DS.appendLinked([1],[-1])
DS.appendLinked([-0.83],[0.83])
DS.appendLinked([-0.3],[0.3])
DS.appendLinked([0.3],[-0.3])
DS.appendLinked([0.028], [-0.028])
DS.appendLinked([-1],[1])

def calcError(x, y):
	return abs(x - y) / x

def testNetwork(eVar): # Not super good, as the best value is 0.89 and worst is 0.22
	global net # So that we can look at the network after we're done training
	net = buildNetwork(1,1,1,bias=True,outputbias=True)
	
	net.connections[net['in']][0].params[0] = eVar[0];
	net.connections[net['hidden0']][0].params[0] = eVar[1];
	net.connections[net['bias']][0].params[0] = eVar[2];
	net.connections[net['bias']][1].params[0] = eVar[3];

	res = net.activateOnDataset(DS)
	fitness = 0
	for i in range(len(DS['target'])):
		absError = abs(calcError(res[i], DS['target'][i]))
		if absError < 1:
			fitness += 1 - absError

	return fitness

genome = G1DList(4) # We're only going to change 1 weight
genome.setParams(rangemin=-10,rangemax=10) # The value should be between -1 and 1
genome.initializator.set(G1DListInitializatorReal) # Initializes the genes with a Real value
genome.mutator.set(G1DListMutatorRealGaussian) # Uses a Real value Gaussian mutator
genome.evaluator.set(testNetwork) 
genome.crossover.clear() # Remove the crossover function, not possible as our list has only 1 element
ga = GSimpleGA(genome)
ga.setElitism(True) # Uses Elitism, so a few of the successful inidividuals get carried over
ga.selector.set(GRouletteWheel) # Roulette wheel selector, see http://www.edc.ncl.ac.uk/assets/hilite_graphics/rhjan07g02.png
ga.nGenerations = 100 # Number of generations
ga.evolve(freq_stats=10) # Run 10 generations and then show stats
testNetwork(ga.bestIndividual()) # Just fetch the network of the best individual
for i in range(len(DS)):
	print "Target: %s, Result: %s" % (DS['target'][i], net.activate(DS['input'][i]))