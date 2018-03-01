# 2 HIDDEN LAYER IMPLEMENTATION OF FlappyAI

import numpy as np
import random

#---Neural net matrix dimensions---
# L1weightMatrix: [2x6]
# L1BiasMatrix:   [1x6]
# L2weightMatrix: [6x5]
# L2BiasMatrix:   [1x5]
# L3weightMatrix: [5x1]
# L3BiasMatrix:   [1x1]

# unrolled: 2*6 + 1*6 + 6*5 + 1*5 + 5*1 + 1*1= 59
# 25 dimensions for each particle in swarm

#iters = 1000
#swarmSize = 30
# w = 1                       # Inertial accelerant
# c1 = 2                      # Social accelerant
# c2 = 2                      # Cognitive accelerant
# dimensions = 25             # total weights in all weight matrices


#------Initialize Particles------
class Particle(object):

    def __init__(self, dimension, searchSpace=(-1, 1)):
        self.position = np.random.uniform(
            searchSpace[0], searchSpace[1], (1, dimension))
        self.velocity = np.random.uniform(
            searchSpace[0], searchSpace[1], (1, dimension))
        self.pBestPos = np.zeros(shape=(1, dimension))
        self.fitness = 0
        self.new_fitness = 0

    def updateVelocity(self, c1, c2, w, gBestPos):
        r1 = random.uniform(0, 1)
        r2 = random.uniform(0, 1)

        cognitive = c1 * r1 * (self.pBestPos - self.position)
        social = c2 * r2 * (gBestPos - self.position)

        self.velocity = (w * self.velocity) + cognitive + social

    def updatePosition(self, c1, c2, w, gBestPos):

        self.updateVelocity(c1, c2, w, gBestPos)
        self.position = self.position + self.velocity

    def setFitness(self, fitness_value):
        self.new_fitness = fitness_value

    def evaluateFitness(self,):
        if self.fitness <= self.new_fitness:
            self.fitness = self.new_fitness
            self.pBestPos = self.position

    def rebuildWegihtMatrix(self):
        l1w = np.reshape(self.position[0][:12], (2, 6))
        l1b = np.reshape(self.position[0][12:18], (1, 6))
        l2w = np.reshape(self.position[0][18:48], (6, 5))
        l2b = np.reshape(self.position[0][48:53], (1, 5))
        l3w = np.reshape(self.position[0][53:58], (5, 1))
        l3b = np.reshape(self.position[0][58:], (1, 1))
        return l1w, l1b, l2w, l2b, l3w, l3b


class ParticleSwarm():

    def __init__(self, particles, dimension, w, c1, c2, searchSpace=(-1, 1)):

        self.c1 = c1
        self.c2 = c2
        self.w = w
        self.particles = []
        self.gBestPos = np.zeros(shape=(1, dimension))
        self.gBestFitness = 0
        for i in range(particles):
            self.particles.append(
                Particle(dimension, searchSpace))

    def getBest(self):
        current_fitness = 0
        for particle in self.particles:
            if particle.fitness > current_fitness:
                current_best = particle.pBestPos
        return particle, current_best

    def evaluateFitness(self):
        for particle in self.particles:
            particle.evaluateFitness()
            if particle.fitness >= self.gBestFitness:
                self.gBestFitness = particle.fitness
                self.gBestPos = particle.pBestPos

    def updatePositions(self):
        for particle in self.particles:
            particle.updatePosition(self.c1, self.c2, self.w, self.gBestPos)


if __name__ == '__main__':
    swarm = ParticleSwarm(3, 25, .2, .4, .2, (-100, 100))
    for i in range(3):
        print(swarm.particles[i].velocity)
