# February 6, 2018

import numpy as np
import random

#---Neural net matrix dimensions---
# L1weightMatrix: [2x6]
# L1BiasMatrix:   [1x6]
# L2weightMatrix: [6x1]
# L2BiasMatrix:   [1x1]

# unrolled: 2*6 + 1*6 + 6*1 + 1*1= 25
# 25 dimensions for each particle in swarm

# w = 1                       # Inertial accelerant
# c1 = 2                      # Social accelerant
# c2 = 2                      # Cognitive accelerant
# dimensions = 25             # total weights in all weight matrices


#------Initialize Particles------
class Particle(object):
    '''Class representing each particle in a swarm'''

    def __init__(self, dimension, searchSpace=(-1, 1)):
        # init random vector of <dimension> for postion and velocity
        self.position = np.random.uniform(
            searchSpace[0], searchSpace[1], (1, dimension))
        self.velocity = np.random.uniform(
            searchSpace[0], searchSpace[1], (1, dimension))
        self.pBestPos = np.zeros(shape=(1, dimension))  # personal best pos
        self.fitness = 0  # current best fitness
        self.new_fitness = 0  # fitness after each generation

    def updateVelocity(self, c1, c2, w, gBestPos):
        # update the velocity according to PSO equation
        r1 = random.uniform(0, 1)
        r2 = random.uniform(0, 1)

        cognitive = c1 * r1 * (self.pBestPos - self.position)
        social = c2 * r2 * (gBestPos - self.position)

        self.velocity = (w * self.velocity) + cognitive + social

    def updatePosition(self, c1, c2, w, gBestPos):
        # update the postion according to PSO equation
        # new pos is just a resultant vector of old pos + new velocity
        self.updateVelocity(c1, c2, w, gBestPos)
        self.position = self.position + self.velocity

    def setFitness(self, fitness_value):
        self.new_fitness = fitness_value

    # Assuming greater fitness value is better
    def evaluateFitness(self,):
        # if the new fitness is better than current best fitness of particle
        if self.fitness <= self.new_fitness:
            # update best fitness and best postion
            self.fitness = self.new_fitness
            self.pBestPos = self.position

    def rebuildWegihtMatrix(self):
        # unflatten the psotion vector into the required matrices of BirdBrain
        l1w = np.reshape(self.position[0][:12], (2, 6))
        l1b = np.reshape(self.position[0][12:18], (1, 6))
        l2w = np.reshape(self.position[0][18:24], (6, 1))
        l2b = np.reshape(self.position[0][24:], (1, 1))
        return l1w, l1b, l2w, l2b


class ParticleSwarm():
    '''Class representing a swarm of particles'''

    def __init__(self, numParticles, dimension,
                 w, c1, c2, searchSpace=(-1, 1)):
        # init hyper-parameters
        self.c1 = c1
        self.c2 = c2
        self.w = w
        self.particles = []  # list of all Particle objects in swarm
        # global best position vector of <dimension>, initially zero vector
        self.gBestPos = np.zeros(shape=(1, dimension))
        # global best fitness of the entire swarm
        self.gBestFitness = 0
        # generate <numParticles> amount of Particle objects
        for i in range(numParticles):
            self.particles.append(
                Particle(dimension, searchSpace))

    def getBest(self):
        # find the fittest particle in the swarm
        current_fitness = 0
        for particle in self.particles:
            if particle.fitness > current_fitness:
                current_fitness = particle.fitness
        return particle

    def evaluateFitness(self):
        # after each generation evaluate the fitness of each Particle in swarm
        for particle in self.particles:
            particle.evaluateFitness()
            # if particle is better than the global best
            if particle.fitness >= self.gBestFitness:
                # update the global best fitness and position vector
                self.gBestFitness = particle.fitness
                self.gBestPos = particle.pBestPos

    def updatePositions(self):
        # update the postion vector of each Particle object in swarm
        for particle in self.particles:
            particle.updatePosition(self.c1, self.c2, self.w, self.gBestPos)


if __name__ == '__main__':
    swarm = ParticleSwarm(3, 25, .2, .4, .2, (-100, 100))
    for i in range(3):
        print(swarm.particles[i].velocity)
