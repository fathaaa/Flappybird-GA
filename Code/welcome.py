from .variables import *
from .library import *
from .image import *

def showWelcomeAnimation(): 
    return {'playery': int((SCREENHEIGHT - IMAGES['player'][0].get_height()) / 2),'basex': 0,'playerIndexGen': cycle([0, 1, 2, 1]),}