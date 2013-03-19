import math
import numpy as np
from numpy import array

def dot(v1, v2):
	return v1.dot(v2)

def vlen(v):
	return np.sqrt(v.dot(v))

def vminus(v1, v2):
	return v1-v2

def vplus(v1, v2):
	return v1+v2

def sign(f):
	if f < 0:
		return -1
	return 1

def gaussian(x, mu, sigma):
	""" definition of the guassian function"""
	y = math.exp( -1.0/2 * ((x - mu + 0.0) / (sigma + 0.000001))**2 )
	return y

def transfer(val):
	return 1.0 / (1.0 + math.exp(-1.0 * val)) * 2 - 1

def fetch_one(enumerable):
	def next_val():
		for e in enumerable:
			yield e
		raise Exception('Too many elements retrieved')

	return next_val().next

