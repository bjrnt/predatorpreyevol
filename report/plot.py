import matplotlib.pyplot as plt
import math
import numpy as np

def gauss(x, mu, sigma):
	return math.exp(-(x-mu)**2/(2*sigma**2))

x_vals = np.linspace(-7,7,num=150)

p1, = plt.plot(x_vals, [gauss(x, 0, 1) for x in x_vals], linewidth=2.0)
p2, = plt.plot(x_vals, [gauss(x, -4, 0.5) for x in x_vals], linewidth=2.0)
p3, = plt.plot(x_vals, [gauss(x, 1.5, 2) for x in x_vals], linewidth=2.0)
plt.legend([p1,p2,p3],["mu = 0 sigma = 1","mu = -4 sigma = 0.5","mu = 1.5 sigma = 2"])
plt.axis([-7, 7, 0.0, 1.1])
plt.ylabel('y')
plt.xlabel('x')
plt.show()