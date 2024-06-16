from .library import *
from .variables import *
from .image import *
from .machine_learning import *
from .randompipe import *
from .showscore import *
from .pixelcollision import *
from .checkcrash import *

def mainGame(movementData, displayScreen, clock):
    global fitness
    gameScore = playerIdx = loopCount = 0
    playerIndexGenerator = movementData['playerIndexGen']
    xPositions = []
    yPositions = []
    for index in range(total_models):
        playerX, playerY = int(SCREENWIDTH * 0.2), movementData['playery']
        xPositions.append(playerX)
        yPositions.append(playerY)
    baseXPosition = movementData['basex']
    baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()

    firstPipe = getRandomPipe()
    secondPipe = getRandomPipe()

    upperPipeList = [
        {'x': SCREENWIDTH + 200, 'y': firstPipe[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': secondPipe[0]['y']},
    ]

    lowerPipeList = [
        {'x': SCREENWIDTH + 200, 'y': firstPipe[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': secondPipe[1]['y']},
    ]

    global next_pipe_x
    global next_pipe_hole_y

    next_pipe_x = lowerPipeList[0]['x']
    next_pipe_hole_y = (lowerPipeList[0]['y'] + (upperPipeList[0]['y'] + IMAGES['pipe'][0].get_height())) / 2

    pipeSpeedX = -4

    yVelocities = []
    maxYVelocity = 10
    minYVelocity = -8
    yAccelerations = []
    flapAcceleration = -9
    didFlap = []
    playerAlive = []

    for idx in range(total_models):
        yVelocities.append(-9)
        yAccelerations.append(1)
        didFlap.append(False)
        playerAlive.append(True)

    livePlayers = total_models

    while True:
        for playerIndex in range(total_models):
            if yPositions[playerIndex] < 0 and playerAlive[playerIndex]:
                livePlayers -= 1
                playerAlive[playerIndex] = False
        if livePlayers == 0:
            return {
                'y': 0,
                'groundCrash': True,
                'basex': baseXPosition,
                'upperPipes': upperPipeList,
                'lowerPipes': lowerPipeList,
                'score': gameScore,
                'playerVelY': 0,
            }

        for playerIndex in range(total_models):
            if playerAlive[playerIndex]:
                fitness[playerIndex] += 1
        next_pipe_x += pipeSpeedX

        for playerIndex in range(total_models):
            if playerAlive[playerIndex]:
                if predict_action(yPositions[playerIndex], next_pipe_x, next_pipe_hole_y, playerIndex) == 1:
                    if yPositions[playerIndex] > -2 * IMAGES['player'][0].get_height():
                        yVelocities[playerIndex] = flapAcceleration
                        didFlap[playerIndex] = True

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

        collisionStates = checkCrash({'x': xPositions, 'y': yPositions, 'index': playerIdx},
                                     upperPipeList, lowerPipeList)

        for idx in range(total_models):
            if playerAlive[idx] and collisionStates[idx]:
                livePlayers -= 1
                playerAlive[idx] = False
        if livePlayers == 0:
            return {
                'y': playerY,
                'groundCrash': collisionStates[1],
                'basex': baseXPosition,
                'upperPipes': upperPipeList,
                'lowerPipes': lowerPipeList,
                'score': gameScore,
                'playerVelY': 0,
            }

        for idx in range(total_models):
            if playerAlive[idx]:
                pipeIndex = 0
                playerMidPosition = xPositions[idx]
                for pipe in upperPipeList:
                    pipeMidPosition = pipe['x'] + IMAGES['pipe'][0].get_width()
                    if pipeMidPosition <= playerMidPosition < pipeMidPosition + 4:
                        next_pipe_x = lowerPipeList[pipeIndex + 1]['x']
                        next_pipe_hole_y = (lowerPipeList[pipeIndex + 1]['y'] + (upperPipeList[pipeIndex + 1]['y'] + IMAGES['pipe'][pipeIndex + 1].get_height())) / 2
                        gameScore += 1
                        fitness[idx] += 25
                    pipeIndex += 1

        if (loopCount + 1) % 3 == 0:
            playerIdx = next(playerIndexGenerator)
        loopCount = (loopCount + 1) % 30
        baseXPosition = -((-baseXPosition + 100) % baseShift)

        for idx in range(total_models):
            if playerAlive[idx]:
                if yVelocities[idx] < maxYVelocity and not didFlap[idx]:
                    yVelocities[idx] += yAccelerations[idx]
                if didFlap[idx]:
                    didFlap[idx] = False
                playerHeight = IMAGES['player'][playerIdx].get_height()
                yPositions[idx] += min(yVelocities[idx], BASEY - yPositions[idx] - playerHeight)

        for uPipe, lPipe in zip(upperPipeList, lowerPipeList):
            uPipe['x'] += pipeSpeedX
            lPipe['x'] += pipeSpeedX

        if 0 < upperPipeList[0]['x'] < 5:
            newPipe = getRandomPipe()
            upperPipeList.append(newPipe[0])
            lowerPipeList.append(newPipe[1])

        if upperPipeList[0]['x'] < -IMAGES['pipe'][0].get_width():
            upperPipeList.pop(0)
            lowerPipeList.pop(0)

        displayScreen.blit(IMAGES['background'], (0,0))

        for uPipe, lPipe in zip(upperPipeList, lowerPipeList):
            displayScreen.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
            displayScreen.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

        displayScreen.blit(IMAGES['base'], (baseXPosition, BASEY))
        showScore(gameScore, displayScreen)
        for idx in range(total_models):
            if playerAlive[idx]:
                displayScreen.blit(IMAGES['player'][playerIdx], (xPositions[idx], yPositions[idx]))

        pygame.display.update()
        clock.tick(FPS)
