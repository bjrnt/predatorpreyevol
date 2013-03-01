class Brain(object):
	"""docstring for Brain"""
	G_INPUTNODES = 8
	G_TOTAL_CONNECTIONS = 14

	def __init__(self, genes=None):
		if genes != None:
			self.import_genes(genes)

	def think(self, data):
		genes = self.genes

		if data[0] == 0 and data[5] == 0:
			return (0.005, 0)
		
		else:
			if data[0] == 1 and data[4] == 1:
				
				left = (data[1] * genes[2] + data[2] * genes[3] + data[3] * genes[4],
					data[1] * genes[8] + data[2] * genes[9] + data[3] * genes[10])
				
				right = (data[5] * genes[5] + data[6] * genes[6] + data[7] * genes[7],
					data[5] * genes[11] + data[6] * genes[12] + data[7] * genes[13])
				
				return (left[0] + right[0], left[1] + right[1])

			elif data[1] == 1:
				return (data[1] * genes[2] + data[2] * genes[3] + data[3] * genes[4],
					data[1] * genes[8] + data[2] * genes[9] + data[3] * genes[10])

			else:
				return (data[5] * genes[5] + data[6] * genes[6] + data[7] * genes[7],
					data[5] * genes[11] + data[6] * genes[12] + data[7] * genes[13])

	def import_genes(self, genes):
		self.genes = genes		
