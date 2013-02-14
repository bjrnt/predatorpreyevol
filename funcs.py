from math import sqrt

def dot(v1, v2):
	return sum([a*b for a,b in zip(v1,v2)])

def vlen(v):
	return sqrt(sum([c**2 for c in v]))

def vminus(v1, v2):
	return [a-b for a,b in zip(v1,v2)]

def vplus(v1, v2):
	return [a+b for a,b in zip(v1,v2)]

def sign(f):
	if f < 0:
		return -1
	return 1