# Inputs:
# 5 for first antennae, i.e. antennae_angles[0]
# 0: Object detection, 1 if detected 0 if not
# 1: R 0 - 1
# 2: G 0 - 1
# 3: B 0 - 1
# 4: Object detection 2...

class Brain(object):
	"""docstring for Brain"""
	G_INPUTNODES = 8
	G_TOTAL_CONNECTIONS = 12

	def __init__(self, genes=None):
		if genes != None:
			self.import_genes(genes)

	def think(self, data):
		genes = self.genes

		if data[0] == 0 and data[4] == 0:
			return (0.005, 0)
		
		else:
			if data[0] == 1 and data[4] == 1:
				
				left = (data[1] * genes[0] + data[2] * genes[1] + data[3] * genes[2],
					data[1] * genes[3] + data[2] * genes[4] + data[3] * genes[5])
				
				right = (data[5] * genes[6] + data[6] * genes[7] + data[7] * genes[8],
					data[5] * genes[9] + data[6] * genes[10] + data[7] * genes[11])
				
				return (left[0] + right[0], left[1] + right[1])

			elif data[0] == 1:
				return (data[1] * genes[0] + data[2] * genes[1] + data[3] * genes[2],
					data[1] * genes[3] + data[2] * genes[4] + data[3] * genes[5])

			else:
				return (data[5] * genes[6] + data[6] * genes[7] + data[7] * genes[8],
					data[5] * genes[9] + data[6] * genes[10] + data[7] * genes[11])
				
	def import_genes(self, genes):
		self.genes = genes		
