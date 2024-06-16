def getHitmask(imageResource):
    collisionMask = []
    for widthIndex in range(imageResource.get_width()):
        collisionMask.append([])
        for heightIndex in range(imageResource.get_height()):
            collisionMask[widthIndex].append(bool(imageResource.get_at((widthIndex, heightIndex))[3]))
    return collisionMask
