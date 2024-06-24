import pygame
from sys import exit
import config
import components
import population

pygame.init()
clock = pygame.time.Clock()
population = population.Population(100)
background_image = pygame.image.load('background.png')  # Sesuaikan dengan path yang tepat
background_image = pygame.transform.scale(background_image, (config.win_width, config.win_height))

def generate_pipes():
    config.pipes.append(components.Pipes(config.win_width))

def quit_game(i, score):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('-'*20)
            print(f'ITERASI KE-{i}')
            print()
            print(f'Score:              {score}')
            population.natural_selection(i)
            pygame.quit()
            exit()

def main():
    pipes_spawn_time = 10
    score = 0
    i = 0
    while True:
        quit_game(i, score)
        

        config.window.blit(background_image,(0,0))

        # Spawn Ground
        config.ground.draw(config.window)

        # Spawn Pipes
        if pipes_spawn_time <= 0:
            generate_pipes()
            pipes_spawn_time = 350
        pipes_spawn_time -= 1

        for p in config.pipes:
            p.draw(config.window)
            p.update()
            if p.off_screen:
                score += 1
                config.pipes.remove(p)

        if not population.extinct():
            population.update_live_players()
        else:
            temp = score
            for p in config.pipes:
                if p.passed:
                    temp += 1
            config.pipes.clear()
            print('-'*20)
            print(f'ITERASI KE-{i}')
            print()
            print(f'Score:              {score}')
            population.natural_selection(i)

            i += 1
            score = 0

        clock.tick(60)
        pygame.display.flip()

main()