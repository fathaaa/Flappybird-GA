import pygame
from sys import exit
import config_modified as config
import components_modified as components
import population_modified as population_mod

pygame.init()
clock = pygame.time.Clock()
population = population_mod.Population(100)
background = pygame.image.load('background.png')  # Adjust with correct path
background = pygame.transform.scale(background, (config.screen_width, config.screen_height))

def spawn_obstacles():
    config.obstacles.append(components.Obstacles(config.screen_width))

def close_game(iteration, points):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('-'*20)
            print(f'ITERATION {iteration}')
            print(f'Score: {points}')
            population.perform_selection(iteration)
            pygame.quit()
            exit()

def main():
    obstacle_timer = 10
    points = 0
    iteration = 0
    while True:
        close_game(iteration, points)
        config.display.blit(background, (0,0))
        config.terrain.render(config.display)

        if obstacle_timer <= 0:
            spawn_obstacles()
            obstacle_timer = 350
        obstacle_timer -= 1

        for obs in config.obstacles:
            obs.render(config.display)
            obs.move()
            if obs.is_off_screen:
                points += 1
                config.obstacles.remove(obs)

        if not population.is_extinct():
            population.update_alive_avatars()
        else:
            temp_points = points
            for obs in config.obstacles:
                if obs.is_passed:
                    temp_points += 1
            config.obstacles.clear()
            print('-'*20)
            print(f'ITERATION {iteration}')
            print(f'Score: {points}')
            population.perform_selection(iteration)

            iteration += 1
            points = 0

        clock.tick(60)
        pygame.display.flip()

main()
