import brain
import random
import pygame
import config
import image

PLAYERS_LIST = (('asset/Images/redbird-upflap.png','asset/Images/redbird-midflap.png','asset/Images/redbird-downflap.png',),
    ('asset/Images/bluebird-upflap.png','asset/Images/bluebird-midflap.png','asset/Images/bluebird-downflap.png',),
    ('asset/Images/yellowbird-upflap.png','asset/Images/yellowbird-midflap.png','asset/Images/yellowbird-downflap.png',),)
class Player:
    def __init__(self):
        self.x, self.y = 50, 200
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)) 
        self.images = random.choice(PLAYERS_LIST)  # Pilih set gambar secara acak
        self.flap_images = [pygame.image.load(img).convert_alpha() for img in self.images]
        self.flap_images = [pygame.transform.scale(img, (34, 24)) for img in self.flap_images]  # Mengubah ukuran gambar
        self.current_image = 0  # Mulai dengan gambar pertama
        self.image = self.flap_images[self.current_image]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.vel = 0
        self.flap = False
        self.alive = True
        self.lifespan = 0
        self.frame_rate = 5  # Mengontrol seberapa cepat gambar berganti
        self.frame_count = 0
        self.score = 0
        self.check_pipe = True

        # AI
        self.decision = None
        self.vision = [0.5, 1, 0.5]
        self.fitness = 0
        self.inputs = 3
        self.brain = brain.Brain(self.inputs)
        self.brain.generate_net()

    def draw(self, window):
        window.blit(self.image, self.rect)

    def ground_collision(self, ground):
        return pygame.Rect.colliderect(self.rect, ground)

    def sky_collision(self):
        return self.rect.y < 30

    def pipe_collision(self):
        for p in config.pipes:
            if pygame.Rect.colliderect(self.rect, p.top_rect) or pygame.Rect.colliderect(self.rect, p.bottom_rect):
                return True
        return False

    def update(self, ground):
        if not (self.ground_collision(ground) or self.pipe_collision()):
            self.vel += 0.25
            self.rect.y += self.vel
            if self.vel > 5:
                self.vel = 5
            self.lifespan += 1


            # Animasi flap
            self.frame_count += 1
            if self.frame_count >= self.frame_rate:
                self.current_image = (self.current_image + 1) % len(self.flap_images)
                self.image = self.flap_images[self.current_image]
                self.frame_count = 0
        else:
            self.alive = False
            self.flap = False
            self.vel = 0

    def bird_flap(self):
        if not self.flap and not self.sky_collision():
            self.flap = True
            self.vel = -5
        if self.vel >= 3:
            self.flap = False

    @staticmethod
    def closest_pipe():
        for p in config.pipes:
            if not p.passed:
                return p

    def look(self):
        closest_pipe = self.closest_pipe()
        if closest_pipe:
            # Line to top pipe
            self.vision[0] = max(0, self.rect.center[1] - closest_pipe.top_rect.bottom) / 500
            pygame.draw.line(config.window, self.color, self.rect.center,
                             (self.rect.center[0], closest_pipe.top_rect.bottom))

            # Line to mid pipe
            self.vision[1] = max(0, closest_pipe.x - self.rect.center[0]) / 500
            pygame.draw.line(config.window, self.color, self.rect.center,
                             (closest_pipe.x, self.rect.center[1]))

            # Line to bottom pipe
            self.vision[2] = max(0, closest_pipe.bottom_rect.top - self.rect.center[1]) / 500
            pygame.draw.line(config.window, self.color, self.rect.center,
                             (self.rect.center[0], closest_pipe.bottom_rect.top))

    def think(self):
        self.decision = self.brain.feed_forward(self.vision)
        if self.decision > 0.73:
            self.bird_flap()

    def calculate_fitness(self):
        self.fitness = self.lifespan

    def clone(self):
        clone = Player()
        clone.fitness = self.fitness
        clone.brain = self.brain.clone()
        clone.brain.generate_net()
        return clone











