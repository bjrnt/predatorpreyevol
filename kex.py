from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer

DS = SupervisedDataSet(3,3)
DS.appendLinked([1,0,0],[0,0,1])
DS.appendLinked([0,1,0],[0,1,0])
DS.appendLinked([0,0,1],[1,0,0])

net = buildNetwork(3,3,3)

print net.params

trainer = BackpropTrainer(net, DS)

for i in range(1000):
	trainer.train()

for data in DS:
	print net.activate(data[0])