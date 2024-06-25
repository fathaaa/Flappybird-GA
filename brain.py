import neuron
import synapse
import random

class NeuralNetwork:
    def __init__(self, sensor_count, is_clone=False):
        self.synapses = []
        self.neurons = []
        self.sensors = sensor_count
        self.neural_layers = []
        self.layer_count = 2

        if not is_clone:
            for i in range(self.sensors):
                self.neurons.append(neuron.Neuron(i))
                self.neurons[i].network_layer = 0
            self.neurons.append(neuron.Neuron(3))
            self.neurons[3].network_layer = 0
            self.neurons.append(neuron.Neuron(4))
            self.neurons[4].network_layer = 1

            for i in range(4):
                self.synapses.append(synapse.Synapse(self.neurons[i], self.neurons[4], random.uniform(-1, 1)))

    def setup_connections(self):
        for neuron in self.neurons:
            neuron.synapses = []

        for synapse in self.synapses:
            synapse.start_neuron.synapses.append(synapse)

    def build_network(self):
        self.setup_connections()
        self.neural_layers = []
        for j in range(self.layer_count):
            for neuron in self.neurons:
                if neuron.network_layer == j:
                    self.neural_layers.append(neuron)

    def process_inputs(self, inputs):
        for i in range(self.sensors):
            self.neurons[i].output = inputs[i]
        self.neurons[3].output = 1

        for neuron in self.neural_layers:
            neuron.fire()

        output = self.neurons[4].output
        for neuron in self.neurons:
            neuron.input = 0

        return output

    def replicate(self):
        replica = NeuralNetwork(self.sensors, True)
        for n in self.neurons:
            replica.neurons.append(n.replicate())

        for s in self.synapses:
            replica.synapses.append(s.replicate(replica.get_neuron(s.start_neuron.id), replica.get_neuron(s.end_neuron.id)))

        replica.layer_count = self.layer_count
        replica.setup_connections()
        return replica

    def get_neuron(self, id):
        for neuron in self.neurons:
            if neuron.id == id:
                return neuron

    def evolve(self):
        if random.uniform(0, 1) < 0.8:
            for synapse in self.synapses:
                synapse.adjust_weight()
