from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer

DS = SupervisedDataSet(1,1)
DS.appendLinked([1],[-1])
DS.appendLinked([0],[0])
DS.appendLinked([-0.3],[0.3])
DS.appendLinked([0.3],[-0.3])
DS.appendLinked([-1],[1])

net = buildNetwork(1,1,1,bias=True,outputbias=True)

print net.params

trainer = BackpropTrainer(net, DS)

for i in range(1000):
	trainer.train()

print net.activateOnDataset(DS)

for layer in ['bias', 'hidden0', 'in', 'out']:
	print "Layer %s has %d connections." % (layer, len(net.connections[net[layer]]))
	for connection in net.connections[net[layer]]:
		print connection.params