# Inputs:
# 5 for first antennae, i.e. antennae_angles[0]
# 0: Object detection, 1 if detected 0 if not
# 1: R 0 - 1
# 2: G 0 - 1
# 3: B 0 - 1
# 4: Object detection 2...

class BrainLinear(object):
	"""docstring for Brain"""
	G_INPUTNODES = 8
	G_TOTAL_CONNECTIONS = 12
	G_REGION_SIZE = 3

	def __init__(self, genes=None):
		if genes != None:
			self.import_genes(genes)

	def think(self, data):
		self.gene_index = 0
		f = self.apply_genes

		if data[0] == 0 and data[4] == 0:
			left = (0.0025 * 6, 0)
			right = (0.0025 * 6, 0)
		
		else:
			if data[0] != 0:
				left = (f(data[1]) + f(data[2]) + f(data[3]),
					f(data[1]) + f(data[2]) + f(data[3]))
			else:
				self.gene_index += 6
				left = (0,0)

			if data[4] != 0:
				right = (f(data[5]) + f(data[6]) + f(data[7]),
					f(data[5]) + f(data[6]) + f(data[7]))
			else:
				right = (0,0)
			
		print "# Input: %s" % data
		print "# Output: (%s,%s)" % ((left[0] + right[0]) / 6, (left[1] + right[1]) / 6)
		return ((left[0] + right[0]) / 6, (left[1] + right[1]) / 6)

	def import_genes(self, genes):
		self.genes = genes		

	def apply_genes(self, data):
		self.gene_index += 1
		return (0.0 + self.genes[self.gene_index - 1] * data)
