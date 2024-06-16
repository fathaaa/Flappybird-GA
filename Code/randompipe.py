from .variables import *
from .library import *
from .image import *
from .machine_learning import *

def getRandomPipe():
    gapPosition = random.randrange(0, int(BASEY * 0.6 - PIPEGAPSIZE))
    gapPosition += int(BASEY * 0.2)
    heightOfPipe = IMAGES['pipe'][0].get_height()
    positionX = SCREENWIDTH + 10

    return [{'x': positionX, 'y': gapPosition - heightOfPipe},  {'x': positionX, 'y': gapPosition + PIPEGAPSIZE},]
