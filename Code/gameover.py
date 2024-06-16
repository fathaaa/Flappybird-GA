from .variables import *
from .library import *
from .image import *
from .machine_learning import *

def showGameOverScreen(collisionData):
    global current_pool
    global fitness
    global generation
    newGenWeights = []
    sumFitness = 0
    for modelIdx in range(total_models):
        sumFitness += fitness[modelIdx]
    for modelIdx in range(total_models):
        fitness[modelIdx] /= sumFitness
        if modelIdx > 0:
            fitness[modelIdx] += fitness[modelIdx - 1]
    for modelIdx in range(int(total_models / 2)):
        parentOne = random.uniform(0, 1)
        parentTwo = random.uniform(0, 1)
        parentOneIdx = -1
        parentTwoIdx = -1
        for idx in range(total_models):
            if fitness[idx] >= parentOne:
                parentOneIdx = idx
                break
        for idx in range(total_models):
            if fitness[idx] >= parentTwo:
                parentTwoIdx = idx
                break
        crossedWeights = model_crossover(parentOneIdx, parentTwoIdx)
        mutatedWeightFirst = model_mutate(crossedWeights[0])
        mutatedWeightSecond = model_mutate(crossedWeights[1])
        newGenWeights.append(mutatedWeightFirst)
        newGenWeights.append(mutatedWeightSecond)
    for idx in range(len(newGenWeights)):
        fitness[idx] = -100
        current_pool[idx].set_weights(newGenWeights[idx])
    if save_current_pool == 1:
        save_pool()
    generation += 1
    return
