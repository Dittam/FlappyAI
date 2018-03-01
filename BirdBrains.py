# February 4, 2018

import numpy as np
from sklearn import preprocessing
#from scipy.special import expit
# distx= +180 disty= +400


class BirdBrain(object):
    """nerual network of bird"""

    def __init__(self, name='Unlabelled'):
        self.name = name
        # Hyper parameters
        self.inputLayerNeurons = 2
        self.hiddenLayer1Neurons = 6
        self.outputLayerNeurons = 1

        # Weight/bias matrices
        # 2x6
        self.L1weightMatrix = np.random.randn(
            self.inputLayerNeurons, self.hiddenLayer1Neurons)
        # 1x6
        self.L1BiasMatrix = np.random.randn(1, self.hiddenLayer1Neurons)
        # 6x1
        self.L2weightMatrix = np.random.randn(
            self.hiddenLayer1Neurons, self.outputLayerNeurons)
        # 1x1
        self.L2BiasMatrix = np.random.randn(1, 1)

    # Activation function
    def tanh(self, x):
        # sigmoid doest work well: 1 / (1 + expit(-x))
        return np.tanh(x)

    def normalizeInput(self, data):
        # scale input data to -1 to 1
        normalizedData = preprocessing.normalize(data, norm='l1')
        return normalizedData

    def forward(self, x):
        # Normalize input
        data = self.normalizeInput(x)
        #------hidden layer 1------
        hiddenLayer1 = np.dot(
            data, self.L1weightMatrix) + self.L1BiasMatrix
        # activation of hiddenlayer1
        hiddenLayer1Activated = self.tanh(hiddenLayer1)
        #-----output layer------
        hiddenLayer1Output = np.dot(
            hiddenLayer1Activated, self.L2weightMatrix) + self.L2BiasMatrix
        # activate hiddenlayer1output
        finalOutput = self.tanh(hiddenLayer1Output)
        return finalOutput

    def saveWeightFile(self):
        # export the weight matrices as a npz file
        np.savez('TrainedModels/matrixExport' + self.name + '.npz', self.L1weightMatrix,
                 self.L1BiasMatrix, self.L2weightMatrix, self.L2BiasMatrix)

    def loadWeightFile(self, fileName):
        # load weight matrices from npz file
        file = np.load('TrainedModels/matrixExport' + fileName + '.npz')
        self.L1weightMatrix = file['arr_0']
        self.L1BiasMatrix = file['arr_1']
        self.L2weightMatrix = file['arr_2']
        self.L2BiasMatrix = file['arr_3']

    def loadWeightMatrix(self, l1w, l1b, l2w, l2b):
        # manually load specified load matrices
        # for use with optimization function
        self.L1weightMatrix = l1w
        self.L1BiasMatrix = l1b
        self.L2weightMatrix = l2w
        self.L2BiasMatrix = l2b


if __name__ == '__main__':
    for i in range(30):
        b = BirdBrain()
    # b.loadWeightMatirx()
        print(b.forward(np.array([[680, 902]])))
    # b.saveWeightMatrix()
