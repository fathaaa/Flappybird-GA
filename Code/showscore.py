from .variables import *
from .library import *
from .image import *
from .machine_learning import *

def showScore(gameScore, display):
    scoreNumbers = [int(num) for num in list(str(gameScore))]
    scoreWidthTotal = 0

    for number in scoreNumbers:
        scoreWidthTotal += IMAGES['numbers'][number].get_width()

    horizontalOffset = (SCREENWIDTH - scoreWidthTotal) / 2

    for number in scoreNumbers:
        display.blit(IMAGES['numbers'][number], (horizontalOffset, SCREENHEIGHT * 0.1))
        horizontalOffset += IMAGES['numbers'][number].get_width()
