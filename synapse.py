import random

class Synapse:
    def __init__(self, start_neuron, end_neuron, initial_weight):
        self.start_neuron = start_neuron
        self.end_neuron = end_neuron
        self.weight = initial_weight

    def adjust_weight(self):
        if random.uniform(0, 1) < 0.1:
            self.weight = random.uniform(-1, 1)
        else:
            self.weight += random.gauss(0, 1) / 10
            if self.weight > 1:
                self.weight = 1
            elif self.weight < -1:
                self.weight = -1

    def replicate(self, new_start_neuron, new_end_neuron):
        return Synapse(new_start_neuron, new_end_neuron, self.weight)
