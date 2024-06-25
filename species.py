import operator
import random

class Species:
    def __init__(self, avatar):
        self.avatars = []
        self.avg_fitness = 0
        self.similarity_threshold = 1.2
        self.avatars.append(avatar)
        self.benchmark_fitness = avatar.efficiency
        self.benchmark_brain = avatar.brain.replicate()
        self.champion = avatar.replicate()
        self.stagnation = 0

    def check_similarity(self, brain):
        difference = self.weight_difference(self.benchmark_brain, brain)
        return self.similarity_threshold > difference

    @staticmethod
    def weight_difference(brain1, brain2):
        total_difference = 0
        for i in range(len(brain1.synapses)):
            for j in range(len(brain2.synapses)):
                if i == j:
                    total_difference += abs(brain1.synapses[i].weight - brain2.synapses[j].weight)
        return total_difference

    def add_to_clan(self, avatar):
        self.avatars.append(avatar)

    def rank_by_fitness(self):
        self.avatars.sort(key=operator.attrgetter('efficiency'), reverse=True)
        if self.avatars[0].efficiency > self.benchmark_fitness:
            self.stagnation = 0
            self.benchmark_fitness = self.avatars[0].efficiency
            self.champion = self.avatars[0].replicate()
        else:
            self.stagnation += 1

    def compute_avg_fitness(self):
        total_fitness = 0
        for avatar in self.avatars:
            total_fitness += avatar.efficiency
        self.avg_fitness = int(total_fitness / len(self.avatars)) if self.avatars else 0

    def create_offspring(self):
        baby = self.avatars[random.randint(1, len(self.avatars)) - 1].replicate()
        baby.brain.evolve()
        return baby
