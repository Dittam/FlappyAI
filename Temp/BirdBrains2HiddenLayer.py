# 2 HIDDEN LAYER IMPLEMENTATION OF FlappyAI

import numpy as np
from sklearn import preprocessing
from scipy.special import expit
# distx= +180 disty= +400


class BirdBrain(object):
    """nerual network of bird"""

    def __init__(self, name='Unlabelled'):
        self.name = name
        # Hyper parameters
        self.inputLayerNeurons = 2
        self.hiddenLayer1Neurons = 6
        self.hiddenLayer2Neurons = 5
        self.outputLayerNeurons = 1

        # Weight/bias matrices
        self.L1weightMatrix = np.random.randn(
            self.inputLayerNeurons, self.hiddenLayer1Neurons)

        self.L1BiasMatrix = np.random.randn(1, self.hiddenLayer1Neurons)

        self.L2weightMatrix = np.random.randn(
            self.hiddenLayer1Neurons, self.hiddenLayer2Neurons)

        self.L2BiasMatrix = np.random.randn(1, self.hiddenLayer2Neurons)

        self.L3weightMatrix = np.random.randn(
            self.hiddenLayer2Neurons, self.outputLayerNeurons)

        self.L3BiasMatrix = np.random.randn(1, 1)

    # Activation function
    def sigmoid(self, x):
        o = 1 / (1 + expit(-x))
        return o

    def normalizeInput(self, data):
        normalizedData = preprocessing.normalize(data, norm='l1')
        return normalizedData

    def forward(self, x):
        # Normalize input
        data = self.normalizeInput(x)
        #------hidden layer 1------
        hiddenLayer1 = np.dot(
            data, self.L1weightMatrix) + self.L1BiasMatrix
        hiddenLayer1Activated = self.sigmoid(hiddenLayer1)
        #------hidden layer 2------
        hiddenLayer2 = np.dot(hiddenLayer1Activated,
                              self.L2weightMatrix) + self.L2BiasMatrix
        hiddenLayer2Activated = self.sigmoid(hiddenLayer2)
        #-----output layer------
        hiddenLayer2Output = np.dot(
            hiddenLayer2Activated, self.L3weightMatrix) + self.L3BiasMatrix

        finalOutput = self.sigmoid(hiddenLayer2Output)
        return finalOutput

    def saveWeightMatrix(self):
        np.savez('TrainedModels/matrixExport' + self.name + '.npz', self.L1weightMatrix,
                 self.L1BiasMatrix, self.L2weightMatrix, self.L2BiasMatrix)

    def loadWeightFile(self):

        file = np.load('TrainedModels/matrixExport' + self.name + '.npz')
        self.L1weightMatrix = file['arr_0']
        self.L1BiasMatrix = file['arr_1']
        self.L2weightMatrix = file['arr_2']
        self.L2BiasMatrix = file['arr_3']

    def loadWeightMatrix(self, l1w, l1b, l2w, l2b, l3w, l3b):
        self.L1weightMatrix = l1w
        self.L1BiasMatrix = l1b
        self.L2weightMatrix = l2w
        self.L2BiasMatrix = l2b
        self.L3weightMatrix = l3w
        self.L3BiasMatrix = l3b


if __name__ == '__main__':
    for i in range(30):
        b = BirdBrain()
    # b.loadWeightMatirx()
        print(b.forward(np.array([[680, 902]])))
    # b.saveWeightMatrix()
