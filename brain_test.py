import unittest
import random
import operator
from brain_linear import BrainLinear
from brain_rbf import BrainRBF

class BrainLinearTest(unittest.TestCase):
	def setUp(self):
		self.brain = BrainLinear()

	def test_zeroed_brain(self):
		ins = BrainLinear.G_INPUTNODES
		self.brain.import_genes([0] * BrainLinear.G_TOTAL_CONNECTIONS)
		#print "Zeroed tests:"
		self.assertEqual(self.brain.think([0] * ins), (0.005,0), 'Output when detecting nothing is incorrect.')
		self.assertEqual(self.brain.think([1] * ins), (0,0), 'Output with full input incorrect.')
		self.assertEqual(self.brain.think([1] * (ins/2) + [0] * (ins/2)), (0,0), 'Output with full input to left incorrect.')
		self.assertEqual(self.brain.think([0] * (ins/2) + [1] * (ins/2)), (0,0), ' Output with full input to right incorrect.')

		self.assertEqual(self.brain.think([1] * 2 + [0] * (ins - 2)), (0,0), 'Output when not detecting 1 color incorrect.')
		self.assertEqual(self.brain.think([1] + [0] + [1] + [0] * (ins - 3)), (0,0), 'Output when not detecting 1 color incorrect.')
		self.assertEqual(self.brain.think([1] + [0] * 2 + [1] + [0] * (ins - 4)), (0,0), 'Output when not detecting 1 color incorrect.')

		self.assertEqual(self.brain.think([0] * (ins / 2) + [1] * 2 + [0] * 2), (0,0), 'Output when not detecting 1 color incorrect.')
		self.assertEqual(self.brain.think([0] * (ins / 2) + [1] + [0] + [1] + [0]), (0,0), 'Output when not detecting 1 color incorrect.')
		self.assertEqual(self.brain.think([0] * (ins / 2) + [1] + [0] * 2 + [1]), (0,0), 'Output when not detecting 1 color incorrect.')

	def test_left_antenna(self):
		ins = BrainLinear.G_INPUTNODES
		self.brain.import_genes([1] * (BrainLinear.G_TOTAL_CONNECTIONS / 2) + [0] * (BrainLinear.G_TOTAL_CONNECTIONS / 2))
		#print "Left tests:"
		self.assertEqual(self.brain.think([0] * ins), (0.005,0), 'Output when detecting nothing is incorrect.')
		self.assertEqual(self.brain.think([1] * ins), (0.5,0.5), 'Output with full input incorrect.')
		self.assertEqual(self.brain.think([1] * (ins/2) + [0] * (ins/2)), (0.5,0.5), 'Output with full input to left incorrect.')
		self.assertEqual(self.brain.think([0] * (ins/2) + [1] * (ins/2)), (0,0), 'Output with full input to right incorrect.')		

		self.assertEqual(self.brain.think([1] * 2 + [0] * (ins - 2)), (0.5/3,0.5/3), 'Output when only detecting 1 color incorrect.')
		self.assertEqual(self.brain.think([1] + [0] + [1] + [0] * (ins - 3)), (0.5/3,0.5/3), 'Output when only detecting 1 color incorrect.')
		self.assertEqual(self.brain.think([1] + [0] * 2 + [1] + [0] * (ins - 4)), (0.5/3,0.5/3), 'Output when only detecting 1 color incorrect.')

		self.assertEqual(self.brain.think([0] * (ins / 2) + [1] * 2 + [0] * 2), (0,0), 'Output when not detecting 1 color incorrect.')
		self.assertEqual(self.brain.think([0] * (ins / 2) + [1] + [0] + [1] + [0]), (0,0), 'Output when not detecting 1 color incorrect.')
		self.assertEqual(self.brain.think([0] * (ins / 2) + [1] + [0] * 2 + [1]), (0,0), 'Output when not detecting 1 color incorrect.')

	def test_right_antenna(self):
		ins = BrainLinear.G_INPUTNODES
		self.brain.import_genes([0] * (BrainLinear.G_TOTAL_CONNECTIONS / 2) + [1] * (BrainLinear.G_TOTAL_CONNECTIONS / 2))
		#print "Right tests:"
		self.assertEqual(self.brain.think([0] * ins), (0.005,0), 'Output when detecting nothing is incorrect.')
		self.assertEqual(self.brain.think([1] * ins), (0.5,0.5), 'Output with full input incorrect.')
		self.assertEqual(self.brain.think([1] * (ins/2) + [0] * (ins/2)), (0,0), 'Output with full input to left incorrect.')
		self.assertEqual(self.brain.think([0] * (ins/2) + [1] * (ins/2)), (0.5,0.5), 'Output with full input to right incorrect.')				

		self.assertEqual(self.brain.think([1] * 2 + [0] * (ins - 2)), (0,0), 'Output when not detecting 1 color incorrect.')
		self.assertEqual(self.brain.think([1] + [0] + [1] + [0] * (ins - 3)), (0,0), 'Output when not detecting 1 color incorrect.')
		self.assertEqual(self.brain.think([1] + [0] * 2 + [1] + [0] * (ins - 4)), (0,0), 'Output when not detecting 1 color incorrect.')

		self.assertEqual(self.brain.think([0] * (ins / 2) + [1] * 2 + [0] * 2), (0.5/3,0.5/3), 'Output when only detecting 1 color incorrect.')
		self.assertEqual(self.brain.think([0] * (ins / 2) + [1] + [0] + [1] + [0]), (0.5/3,0.5/3), 'Output when only detecting 1 color incorrect.')
		self.assertEqual(self.brain.think([0] * (ins / 2) + [1] + [0] * 2 + [1]), (0.5/3,0.5/3), 'Output when only detecting 1 color incorrect.')
	def test_fuzz(self):
		num_tests = 10000
		ins = BrainLinear.G_INPUTNODES
		res = [0]*num_tests 
		for i in xrange(num_tests) :
			
			self.brain.import_genes(map(lambda x: random.random()*x*2-1, [1]*BrainLinear.G_TOTAL_CONNECTIONS))
			res[i] = self.brain.think(map(lambda x: random.random()*x, [1]*ins))
			
		#print 'random weights, random input %d vs %d' % (len([ds for (ds,dr) in res if ds > 0]) , num_tests - len([ds for (ds,dr) in res if ds > 0]))
		self.assertTrue(len([ds for (ds,dr) in res if ds > 0]) / float(num_tests) > 0.45 and len([ds for (ds,dr) in res if ds > 0]) / float(num_tests) < 0.55, "fuzz testing gave abnormal distribution of results")

	def tearDown(self):
		del self.brain

class BrainRBFTest(unittest.TestCase):
	def setUp(self):
		self.brain = BrainRBF()

	def test_fuzz(self):
		num_tests = 10000
		ins = BrainRBF.G_INPUTNODES
		res = [0]*num_tests 
		for i in xrange(num_tests) :
			
			self.brain.import_genes(map(lambda x: random.random()*x*2-1, [1]*BrainRBF.G_TOTAL_CONNECTIONS))
			res[i] = self.brain.think(map(lambda x: random.random()*x, [1]*ins))
			
		#print 'random weights, random input %d vs %d' % (len([ds for (ds,dr) in res if ds > 0]) , num_tests - len([ds for (ds,dr) in res if ds > 0]))
		self.assertTrue(len([ds for (ds,dr) in res if ds > 0]) / float(num_tests) > 0.45 and len([ds for (ds,dr) in res if ds > 0]) / float(num_tests) < 0.55, "fuzz testing gave abnormal distribution of results")

	def tearDown(self):
		pass

if __name__ == '__main__':
	unittest.main()
