import numpy as np
import world
from numpy import array
from math import sqrt

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