from Code import *

def main():
    global SCREEN, FPSCLOCK
    initiate_models(total_models)
    load_pool(total_models)
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((int(SCREENWIDTH), int(SCREENHEIGHT)))
    pygame.display.set_caption('Flappy Bird')
    IMAGES['numbers'] = (
        pygame.image.load('asset/Images/0.png').convert_alpha(),
        pygame.image.load('asset/Images/1.png').convert_alpha(),
        pygame.image.load('asset/Images/2.png').convert_alpha(),
        pygame.image.load('asset/Images/3.png').convert_alpha(),
        pygame.image.load('asset/Images/4.png').convert_alpha(),
        pygame.image.load('asset/Images/5.png').convert_alpha(),
        pygame.image.load('asset/Images/6.png').convert_alpha(),
        pygame.image.load('asset/Images/7.png').convert_alpha(),
        pygame.image.load('asset/Images/8.png').convert_alpha(),
        pygame.image.load('asset/Images/9.png').convert_alpha())
    IMAGES['gameover'] = pygame.image.load('asset/Images/gameover.png').convert_alpha()
    IMAGES['message'] = pygame.image.load('asset/Images/message.png').convert_alpha()
    IMAGES['base'] = pygame.image.load('asset/Images/base.png').convert_alpha()
    if 'win' in sys.platform:
        soundExtension = '.wav'
    else:
        soundExtension = '.ogg'
    SOUNDS['die'] = pygame.mixer.Sound('asset/Sounds/die' + soundExtension)
    SOUNDS['hit'] = pygame.mixer.Sound('asset/Sounds/hit' + soundExtension)
    SOUNDS['point'] = pygame.mixer.Sound('asset/Sounds/point' + soundExtension)
    SOUNDS['swoosh'] = pygame.mixer.Sound('asset/Sounds/swoosh' + soundExtension)
    SOUNDS['wing'] = pygame.mixer.Sound('asset/Sounds/wing' + soundExtension)
    while True:
        backgroundIndex = random.randint(0, len(BACKGROUNDS_LIST) - 1)
        IMAGES['background'] = pygame.image.load(BACKGROUNDS_LIST[backgroundIndex]).convert()
        playerIndex = random.randint(0, len(PLAYERS_LIST) - 1)
        IMAGES['player'] = (
            pygame.image.load(PLAYERS_LIST[playerIndex][0]).convert_alpha(),
            pygame.image.load(PLAYERS_LIST[playerIndex][1]).convert_alpha(),
            pygame.image.load(PLAYERS_LIST[playerIndex][2]).convert_alpha(),)
        pipeIndex = random.randint(0, len(PIPES_LIST) - 1)
        IMAGES['pipe'] = (
            pygame.transform.rotate(pygame.image.load(PIPES_LIST[pipeIndex]).convert_alpha(), 180),pygame.image.load(PIPES_LIST[pipeIndex]).convert_alpha(),)
        HITMASKS['pipe'] = (getHitmask(IMAGES['pipe'][0]),getHitmask(IMAGES['pipe'][1]),)
        HITMASKS['player'] = (getHitmask(IMAGES['player'][0]),getHitmask(IMAGES['player'][1]),getHitmask(IMAGES['player'][2]),)
        introData = showWelcomeAnimation()
        global fitness
        for modelIdx in range(total_models):
            fitness[modelIdx] = 0
        crashData = mainGame(introData, SCREEN, FPSCLOCK)
        showGameOverScreen(crashData)

if __name__ == '__main__':
    main()
