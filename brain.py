from pybrain.structure import LinearLayer, SigmoidLayer, FeedForwardNetwork, FullConnection, BiasUnit

class Brain(object):
	"""docstring for Brain"""
	G_INPUTNODES = 8
	G_HIDDENNODES = 15
	G_OUTPUTNODES = 2
	G_TOTAL_CONNECTIONS = G_INPUTNODES * G_HIDDENNODES + G_HIDDENNODES * G_OUTPUTNODES + G_HIDDENNODES + G_OUTPUTNODES

	def __init__(self, genes=None):
		self.net = FeedForwardNetwork()

		inLayer = LinearLayer(Brain.G_INPUTNODES, name='input')
		hiddenLayer = SigmoidLayer(Brain.G_HIDDENNODES, name='hidden')
		outLayer = SigmoidLayer(Brain.G_OUTPUTNODES, name='out')
		bias = BiasUnit(name='bias')

		self.net.addInputModule(inLayer)
		self.net.addModule(hiddenLayer)
		self.net.addModule(bias)
		self.net.addOutputModule(outLayer)

		in_to_hidden = FullConnection(inLayer, hiddenLayer)
		hidden_to_out = FullConnection(hiddenLayer, outLayer)
		bias_to_hidden = FullConnection(bias, hiddenLayer)
		bias_to_out = FullConnection(bias, outLayer)
		
		self.net.addConnection(in_to_hidden)
		self.net.addConnection(hidden_to_out)
		self.net.addConnection(bias_to_hidden)
		self.net.addConnection(bias_to_out)

		self.net.sortModules()

		if genes != None:
			self.import_genes(genes)

	def think(self, data):
		return self.net.activate(data)

	def import_genes(self, genes):
		modules = self.net.modules
		connections = self.net.connections
		consumed_params = 0

		for module in modules:
			for conn in connections[module]:
				for i in xrange(len(conn.params)):
					conn.params[i] = genes[consumed_params]	
					consumed_params += 1

	def examine_brain(self):
		modules = self.net.modules
		
		connections = self.net.connections

		print " == Creature == "
		for module in modules:
			print "%s:" % module
			for conn in connections[module]:
				print " 	%s" % conn
				print "%s" % conn.params
