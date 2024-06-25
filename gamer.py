BIRDS = (
    ('asset/Images/redbird-upflap.png', 'asset/Images/redbird-midflap.png', 'asset/Images/redbird-downflap.png'),
    ('asset/Images/bluebird-upflap.png', 'asset/Images/bluebird-midflap.png', 'asset/Images/bluebird-downflap.png'),
    ('asset/Images/yellowbird-upflap.png', 'asset/Images/yellowbird-midflap.png', 'asset/Images/yellowbird-downflap.png'),
)

class Avatar:
    def __init__(self):
        self.x, self.y = 50, 200
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        self.images = random.choice(BIRDS)
        self.flaps = [pygame.image.load(img).convert_alpha() for img in self.images]
        self.flaps = [pygame.transform.scale(img, (34, 24)) for img in self.flaps]
        self.image_index = 0
        self.image = self.flaps[self.image_index]
        self.boundary = self.image.get_rect(topleft=(self.x, self.y))
        self.velocity = 0
        self.is_flapping = False
        self.is_alive = True
        self.age = 0
        self.frame_rate = 5
        self.frame_counter = 0
        self.score = 0
        self.check_obstacle = True

        # AI
        self.thought = None
        self.sensors = [0.5, 1, 0.5]
        self.efficiency = 0
        self.sensor_count = 3
        self.brain = nn.NeuralNetwork(self.sensor_count)
        self.brain.build_network()

    def display(self, window):
        window.blit(self.image, self.boundary)

    def check_terrain_collision(self, terrain):
        return pygame.Rect.colliderect(self.boundary, terrain)

    def check_ceiling_collision(self):
        return self.boundary.y < 30

    def check_obstacle_collision(self):
        for obs in config.obstacles:
            if pygame.Rect.colliderect(self.boundary, obs.upper_barrier) or pygame.Rect.colliderect(self.boundary, obs.lower_barrier):
                return True
        return False

    def update_movement(self, terrain):
        if not (self.check_terrain_collision(terrain) or self.check_obstacle_collision()):
            self.velocity += 0.25
            self.boundary.y += self.velocity
            if self.velocity > 5:
                self.velocity = 5
            self.age += 1

            # Flap animation
            self.frame_counter += 1
            if self.frame_counter >= self.frame_rate:
                self.image_index = (self.image_index + 1) % len(self.flaps)
                self.image = self.flaps[self.image_index]
                self.frame_counter = 0
        else:
            self.is_alive = False
            self.is_flapping = False
            self.velocity = 0

    def flap(self):
        if not self.is_flapping and not self.check_ceiling_collision():
            self.is_flapping = True
            self.velocity = -5
        if self.velocity >= 3:
            self.is_flapping = False

    @staticmethod
    def nearest_obstacle():
        for obs in config.obstacles:
            if not obs.is_passed:
                return obs

    def observe(self):
        closest = self.nearest_obstacle()
        if closest:
            self.sensors[0] = max(0, self.boundary.center[1] - closest.upper_barrier.bottom) / 500
            self.sensors[1] = max(0, closest.x - self.boundary.center[0]) / 500
            self.sensors[2] = max(0, closest.lower_barrier.top - self.boundary.center[1]) / 500

    def decide(self):
        self.thought = self.brain.process_inputs(self.sensors)
        if self.thought > 0.73:
            self.flap()

    def assess_fitness(self):
        self.efficiency = self.age

    def replicate(self):
        clone = Avatar()
        clone.efficiency = self.efficiency
        clone.brain = self.brain.replicate()
        clone.brain.build_network()
        return clone