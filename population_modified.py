import config_modified as config
import gamer as player_mod
import math
import species as species_mod
import operator

class Population:
    def __init__(self, count):
        self.avatars = []
        self.generation_number = 1
        self.clans = []
        self.count = count
        self.best_score = 0
        self.avg_fitness = 0
        self.alive_count = self.count
        for i in range(self.count):
            self.avatars.append(player_mod.Avatar())

    def update_alive_avatars(self):
        self.alive_count = 0
        for avatar in self.avatars:
            if avatar.is_alive:
                self.alive_count += 1
                avatar.observe()
                avatar.decide()
                avatar.display(config.display)
                avatar.update_movement(config.terrain)

    def display_stats(self, iteration):
        print(f'Fitness:            {self.best_score}')
        print(f'Average Fitness:    {self.avg_fitness}')
        print()

    def perform_selection(self, iteration):
        self.assign_to_clans()
        self.calculate_fitness()
        self.display_stats(iteration)
        self.remove_extinct_clans()
        self.remove_stale_clans()
        self.rank_clans_by_fitness()
        self.create_next_generation()

    def assign_to_clans(self):
        for clan in self.clans:
            clan.avatars = []

        for avatar in self.avatars:
            found_clan = False
            for clan in self.clans:
                if clan.check_similarity(avatar.brain):
                    clan.add_to_clan(avatar)
                    found_clan = True
                    break
            if not found_clan:
                self.clans.append(species_mod.Species(avatar))

    def calculate_fitness(self):
        self.best_score = 0
        self.avg_fitness = 0
        for avatar in self.avatars:
            avatar.assess_fitness()
            if avatar.efficiency > self.best_score:
                self.best_score = avatar.efficiency
            self.avg_fitness += avatar.efficiency
        self.avg_fitness /= self.count
        for clan in self.clans:
            clan.compute_avg_fitness()

    def remove_extinct_clans(self):
        extinct = []
        for clan in self.clans:
            if len(clan.avatars) == 0:
                extinct.append(clan)
        for clan in extinct:
            self.clans.remove(clan)

    def remove_stale_clans(self):
        stagnant = []
        for clan in self.clans:
            if clan.stagnation >= 8:
                if len(self.clans) > len(stagnant) + 1:
                    stagnant.append(clan)
                    for avatar in clan.avatars:
                        self.avatars.remove(avatar)
                else:
                    clan.stagnation = 0
        for clan in stagnant:
            self.clans.remove(clan)

    def rank_clans_by_fitness(self):
        for clan in self.clans:
            clan.rank_by_fitness()
        self.clans.sort(key=operator.attrgetter('benchmark_fitness'), reverse=True)

    def create_next_generation(self):
        offspring = []
        for clan in self.clans:
            offspring.append(clan.champion.replicate())

        offspring_per_clan = math.floor((self.count - len(self.clans)) / len(self.clans))
        for clan in self.clans:
            for _ in range(offspring_per_clan):
                offspring.append(clan.create_offspring())

        while len(offspring) < self.count:
            offspring.append(self.clans[0].create_offspring())

        self.avatars = []
        for child in offspring:
            self.avatars.append(child)
        self
