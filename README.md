# FlappyAI
Flappy Brid AI implemented using a feed forward neural network and trained using particle swarm optimization.
<p align="center">
<img src="https://github.com/Dittam/FlappyAI/blob/master/assets/Title.png" width="358" height="337">
</p>


## File Info

|          File Name          |                                        Description                                       |
|:--------------------:|:------------------------------------------------------------------------------------:|
| FlappyBirdGame.py           | The main program that runs the game and AI                                                                       |
| BirdBrains.py       | Contains the neural network implementation of the "bird brains" i.e the brains of the AI                                              |
| ParticleSwarmOptimizer.py | Contains the optimization algorithm used to train the weights of the neural network,   |
| FitnessGraph.py           | Displays a live graph that shows the realtime highest fitness value of a bird                                                                   |


## Neural Network Architecture:
* 3 layers including 1 hidden layer: 2, 6, 1 neurons respectively
* layer 1 weight matrix: 2x6,  layer 2 weight matrix: 1x6
* The network's input layer takes in 2 inputs; a birds horzontal and verticle distance from the midpoint of the nearest wall. Visualized by the red, green , blue tracers when running FlappyBirdGame.py
* The output layer is a 1x1 matrix that outputs a probability between 0,1 on whether or not the bird should flap
* The activation function used is tanh(x)

<p align="left">
<img src="https://github.com/Dittam/FlappyAI/blob/master/assets/networkDiagram.PNG" width="356" height="209">
</p> 


## Particle Swarm optimization
PSO is a neuro-evolutionary algorithm used to train the weights in each matrix in the network

### Formula:
<p align="left">
<img src="https://github.com/Dittam/FlappyAI/blob/master/assets/PSOAlgo.PNG" width="286" height="201">
</p> 

Note the positions of each particle corresponds to a solution set, i.e. a set of weights for each matrix


## The following pseudocode accurately explains PSO:
<p align="left">
<img src="https://github.com/Dittam/FlappyAI/blob/master/assets/PSOPseudo.PNG" width="245" height="244">
</p> 


## Dependencies:
* Python 3+
* Pygame
* Matplotlib
* Numpy
* scikit-learn
