import components_modified as components
import pygame

screen_height = 720
screen_width = 550
display = pygame.display.set_mode((screen_width, screen_height))

terrain = components.Terrain(screen_width)
obstacles = []
