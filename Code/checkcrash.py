from .variables import *
from .library import *
from .image import *
from .machine_learning import *
from .pixelcollision import *

def checkCrash(bird, upperPipes, lowerPipes):
    collisionStatus = []
    for modelIndex in range(total_models):
        collisionStatus.append(False)

    for modelIndex in range(total_models):
        collisionStatus[modelIndex] = False 
        playerIndex = bird['index']
        bird['width'] = IMAGES['player'][0].get_width()
        bird['height'] = IMAGES['player'][0].get_height()
        if bird['y'][modelIndex] + bird['height'] >= BASEY - 1:
            collisionStatus[modelIndex] = True
        birdRectangle = pygame.Rect(bird['x'][modelIndex], bird['y'][modelIndex], bird['width'], bird['height'])
        pipeWidth = IMAGES['pipe'][0].get_width()
        pipeHeight = IMAGES['pipe'][0].get_height()

        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipeRect = pygame.Rect(upperPipe['x'], upperPipe['y'], pipeWidth, pipeHeight)
            lowerPipeRect = pygame.Rect(lowerPipe['x'], lowerPipe['y'], pipeWidth, pipeHeight)
            playerHitmask = HITMASKS['player'][playerIndex]
            upperHitmask = HITMASKS['pipe'][0]
            lowerHitmask = HITMASKS['pipe'][1]
            collisionUpper = pixelCollision(birdRectangle, upperPipeRect, playerHitmask, upperHitmask)
            collisionLower = pixelCollision(birdRectangle, lowerPipeRect, playerHitmask, lowerHitmask)

            if collisionUpper or collisionLower:
                collisionStatus[modelIndex] = True
    return collisionStatus
