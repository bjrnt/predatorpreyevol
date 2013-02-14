from pybrain.structure import LinearLayer, SigmoidLayer, FeedForwardNetwork, FullConnection, BiasUnit

class Brain(object):
	"""docstring for Brain"""
	G_INPUTNODES = 8
	G_HIDDENNODES = 15
	
	def __init__(self, genes):
		self.net = FeedForwardNetwork()
		inLayer = LinearLayer(self.G_INPUTNODES, name='input')
		hiddenLayer = SigmoidLayer(self.G_HIDDENNODES, name='hidden')
		outLayer = SigmoidLayer(2, name='out')

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

	def think(self, data):
		return self.net.activate(data)

	def examine_brain(self):
		modules = self.net.modules
		
		connections = self.net.connections

		print " == Creature == "
		for module in modules:
			print "%s:" % module
			for conn in connections[module]:
				print " 	%s" % conn
				print "%s" % conn.params
