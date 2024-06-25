import pygame
import random

class Terrain:
    surface_level = 500

    def __init__(self, screen_width):
        self.x, self.y = 0, Terrain.surface_level
        self.barrier = pygame.Rect(self.x, self.y, screen_width, 5)

    def render(self, display):
        pygame.draw.rect(display, (255, 255, 255), self.barrier)


class Obstacles:
    thickness = 15
    gap = 100

    def __init__(self, screen_width):
        self.x = screen_width
        self.lower_height = random.randint(10, 300)
        self.upper_height = Terrain.surface_level - self.lower_height - Obstacles.gap
        self.lower_barrier, self.upper_barrier = pygame.Rect(0, 0, 0, 0), pygame.Rect(0, 0, 0, 0)
        self.is_passed = False
        self.is_off_screen = False

    def render(self, display):
        self.lower_barrier = pygame.Rect(self.x, Terrain.surface_level - self.lower_height, Obstacles.thickness, self.lower_height)
        pygame.draw.rect(display, (255, 255, 255), self.lower_barrier)

        self.upper_barrier = pygame.Rect(self.x, 0, Obstacles.thickness, self.upper_height)
        pygame.draw.rect(display, (255, 255, 255), self.upper_barrier)

    def move(self):
        self.x -= 1
        if self.x + Obstacles.thickness <= 50:
            self.is_passed = True
        if self.x <= -Obstacles.thickness:
            self.is_off_screen = True
