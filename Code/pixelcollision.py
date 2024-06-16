from .variables import *
from .library import *
from .image import *
from .machine_learning import *

def pixelCollision(boundingRect1, boundingRect2, collisionMask1, collisionMask2):
    intersectionRect = boundingRect1.clip(boundingRect2)

    if intersectionRect.width == 0 or intersectionRect.height == 0:
        return False

    relativeX1, relativeY1 = intersectionRect.x - boundingRect1.x, intersectionRect.y - boundingRect1.y
    relativeX2, relativeY2 = intersectionRect.x - boundingRect2.x, intersectionRect.y - boundingRect2.y

    for x in range(intersectionRect.width):
        for y in range(intersectionRect.height):
            if collisionMask1[relativeX1 + x][relativeY1 + y] and collisionMask2[relativeX2 + x][relativeY2 + y]:
                return True
    return False
