import math

class Neuron:
    def __init__(self, neuron_id):
        self.id = neuron_id
        self.network_layer = 0
        self.input = 0
        self.output = 0
        self.synapses = []

    def fire(self):
        def sigmoid(x):
            return 1 / (1 + math.exp(-x))

        if self.network_layer == 1:
            self.output = sigmoid(self.input)

        for synapse in self.synapses:
            synapse.end_neuron.input += synapse.weight * self.output

    def replicate(self):
        clone = Neuron(self.id)
        clone.network_layer = self.network_layer
        return clone
