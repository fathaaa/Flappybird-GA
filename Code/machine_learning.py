from .library import *
from .variables import *

def save_pool():
    for modelIndex in range(total_models):
        current_pool[modelIndex].save_weights("current_model/model_new" + str(modelIndex) + ".weights.h5")
    print("Saved current pool!")

def model_crossover(firstModelIndex, secondModelIndex):
    global current_pool
    firstModelWeights = current_pool[firstModelIndex].get_weights()
    secondModelWeights = current_pool[secondModelIndex].get_weights()
    newFirstWeights = firstModelWeights
    newSecondWeights = secondModelWeights
    newFirstWeights[0] = secondModelWeights[0]
    newSecondWeights[0] = firstModelWeights[0]
    print(newFirstWeights)
    print(newSecondWeights)
    return newFirstWeights, newSecondWeights

def model_mutate(modelWeights):
    for layerIndex in range(len(modelWeights)):
        for weightIndex in range(len(modelWeights[layerIndex])):
            if random.uniform(0, 1) > 0.85:
                mutationChange = random.uniform(-0.5, 0.5)
                modelWeights[layerIndex][weightIndex] += mutationChange
    return modelWeights

def predict_action(birdHeight, pipeDistance, pipeElevation, modelIndex):
    global current_pool
    normalizedHeight = min(SCREENHEIGHT, birdHeight) / SCREENHEIGHT - 0.5
    normalizedDistance = pipeDistance / 450 - 0.5
    normalizedElevation = min(SCREENHEIGHT, pipeElevation) / SCREENHEIGHT - 0.5
    neuralInput = np.asarray([normalizedHeight, normalizedDistance, normalizedElevation])
    neuralInput = np.atleast_2d(neuralInput)
    modelPrediction = current_pool[modelIndex].predict(neuralInput, 1, verbose=0)[0]
    if modelPrediction[0] <= 0.5:
        return 1
    return 2

def initiate_models(modelCount):
    for modelIdx in range(modelCount):
        newModel = Sequential()
        newModel.add(Dense(units=7, input_dim=3))
        newModel.add(Activation("sigmoid"))
        newModel.add(Dense(units=1))
        newModel.add(Activation("sigmoid"))

        optimizer = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
        newModel.compile(loss="mse", optimizer=optimizer, metrics=["accuracy"])
        current_pool.append(newModel)
        fitness.append(-100)

def load_pool(modelCount):
    if load_saved_pool:
        for modelIdx in range(modelCount):
            current_pool[modelIdx].load_weights("current_Model/model_new" + str(modelIdx) + ".keras")

    for modelIdx in range(modelCount):
        print(current_pool[modelIdx].get_weights())
