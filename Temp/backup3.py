import pygame
from pygame.locals import *  # noqa
import sys
import random
import BirdBrains
from ParticleSwarmOptimizer import *
import numpy as np


FPS = 60
MODELS = 10
SCREEN = pygame.display.set_mode((400, 700))  # 400x708
BACKGROUND = pygame.image.load("assets/backgroundold.png").convert()
WALL_IMAGE = [pygame.image.load("assets/bottom.png").convert_alpha(),
              pygame.image.load("assets/top.png").convert_alpha()]

BIRD_IMAGES = [pygame.image.load("assets/1.png").convert_alpha(),
               pygame.image.load("assets/2.png").convert_alpha(),
               pygame.image.load("assets/dead.png")]

WALL_IMAGES = [pygame.image.load("assets/bottom.png").convert_alpha(),
               pygame.image.load("assets/top.png").convert_alpha()]


class Bird(pygame.sprite.Sprite):

    def __init__(self, screen, walls):
        super().__init__()

        self.image = BIRD_IMAGES[0]
        self.screen = screen
        self.rect = pygame.Rect(65, 50, 50, 50)
        self.y = random.randint(325, 375)
        self.x = 70
        self.fitness = 0
        self.distx = 0
        self.disty = 0
        self.jump = 0
        self.jumpSpeed = 10
        self.gravity = 5
        self.dead = False
        self.brain = BirdBrains.BirdBrain()
        self.walls = walls
        self.action = 0

    def update(self,):

        self.NeuralNet()

        if self.jump:
            self.jumpSpeed -= 1
            self.y -= self.jumpSpeed
            self.jump -= 1
        else:
            self.y += self.gravity
            self.gravity += 0.4
        self.rect[1] = self.y

        upRect = pygame.Rect(self.walls.x,
                             360 + self.walls.gap - self.walls.offset + 10,
                             WALL_IMAGES[0].get_width() - 10,
                             WALL_IMAGES[0].get_height())
        downRect = pygame.Rect(self.walls.x,
                               0 - self.walls.gap - self.walls.offset - 10,
                               WALL_IMAGES[1].get_width() - 10,
                               WALL_IMAGES[1].get_height())

        if upRect.colliderect(self.rect) or downRect.colliderect(self.rect):
            self.dead = True

        if not 0 < self.rect[1] < 720:
            self.dead = True
            birdgroup.remove(self)
            deadgroup.add(self)

        if self.dead:
            self.image = BIRD_IMAGES[2]

        self.fitness = self.walls.totalx
        self.Telemetry()
        self.RenderTracers()

    def doJump(self):
        self.jump = 17
        self.gravity = 5
        self.jumpSpeed = 10

    def checkDead(self):
        return self.dead

    def doneDeadAnimation(self):
        return self.dead and self.y > 708

    def RenderTracers(self):
        # ---Tracer Renders---
        # Y vector
        pygame.draw.line(self.screen, (0, 0, 255),
                         (self.x + 35, self.walls.y),
                         (self.x + 35, self.y + 10), 2)
        # X vector
        pygame.draw.line(self.screen, (0, 255, 0),
                         (self.x + 35, self.walls.y),
                         (self.walls.x, self.walls.y), 2)
        # resultant vector
        pygame.draw.line(self.screen, (255, 0, 0), (self.x + 35, self.y + 10),
                         (self.walls.x, self.walls.y), 2)

    def Telemetry(self):
        self.distx = self.walls.x - self.x  # + 180
        self.disty = self.walls.y - self.y  # + 400
        # print(self.distx - 180, self.disty - 400)

    def NeuralNet(self):
        self.action = self.brain.forward(np.array([[self.distx, self.disty]]))
        # print(action)
        if self.action > 0.5 and not self.dead:
            self.doJump()


class Walls():

    def __init__(self, screen):
        self.screen = screen
        self.gap = 130
        self.x = 400
        self.totalx = 0
        self.y = 0
        self.counter = 0
        self.offset = random.randint(-110, 110)

    def updateWalls(self):
        self.x -= 2
        self.totalx += 2
        if self.x < -80:
            self.x = 400
            self.counter += 1
            self.offset = random.randint(-160, 160)

        self.screen.blit(WALL_IMAGE[0],
                         (self.x, 360 + self.gap - self.offset))
        self.screen.blit(WALL_IMAGE[1],
                         (self.x, 0 - self.gap - self.offset))
        self.y = 360 + self.gap - self.offset - 65


def paused(clock):
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        pygame.display.update()
        clock.tick(1)


def run():
    generation = 0
    timer = 0
    clock = pygame.time.Clock()
    pygame.font.init()
    font = pygame.font.SysFont("Arial", 50)
    font2 = pygame.font.SysFont("Arial", 16)

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused(clock)
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            for bird in birdgroup.sprites():
                if (event.type == pygame.KEYDOWN or event.type ==
                        pygame.MOUSEBUTTONDOWN) and not bird.checkDead():
                    bird.doJump()
                # if bird.doneDeadAnimation():
                #    birdgroup.remove(bird)
                #    deadgroup.add(bird)
                if bird.dead:
                    birdgroup.remove(bird)
                    deadgroup.add(bird)

        TOTAL_BIRDS = 0
        for birds in birdgroup.sprites():
            TOTAL_BIRDS += 1
        # print(TOTAL_BIRDS)

        if TOTAL_BIRDS == 0:
            w.counter = 0
            w.totalx = 0
            generation += 1

            i = 0
            for bird in deadgroup:
                swarm.particles[i].setFitness(bird.fitness)
                i += 1

            deadgroup.empty()
            swarm.evaluateFitness()
            swarm.updatePositions()
            w.x = 400

            for i in range(MODELS):
                bird = Bird(SCREEN, w)
                l1w, l1b, l2w, l2b = swarm.particles[i].rebuildWegihtMatrix(
                )
                bird.brain.loadWeightMatrix(l1w, l1b, l2w, l2b)
                birdgroup.add(bird)
        #-----Telemetry------
        if timer % 30 == 0:
            #----get best bird---
            bestBird = None
            for b in birdgroup:
                fit = 0
                if b.fitness >= fit:
                    fit = b.fitness
                bestBird = b
            p = swarm.getBest()
            print('Gen:', generation, 'Fitness:', p.fitness)
            print(p.position)

        if timer % 10 == 0:
            print(bestBird.x, bestBird.y)
        timer += 1

        coord = 'Postion: {} {}'.format(str(bestBird.x), str(bestBird.y))
        active = 'Activation: ' + str(bestBird.action)
        gen = 'Generation: ' + str(generation)
        fit = 'Best Fitness: ' + str(p.fitness)
        matrix = 'Weight Matrix: ' + str(p.position[0][:3]) + '...'
        #------Rendering------
        SCREEN.fill((255, 255, 255))
        SCREEN.blit(BACKGROUND, (0, 0))
        w.updateWalls()
        SCREEN.blit(font.render(str(w.counter), -
                                1, (0, 0, 0)), (200, 15))
        SCREEN.blit(font2.render(str(gen), -1, (120, 0, 0)), (15, 20))
        SCREEN.blit(font2.render(str(active), -1, (120, 0, 0)), (15, 35))
        SCREEN.blit(font2.render(str(fit), -1, (120, 0, 0)), (15, 50))
        SCREEN.blit(font2.render(str(coord), -1, (120, 0, 0)), (15, 65))
        SCREEN.blit(font2.render(str(matrix), -1, (120, 0, 0)), (15, 80))

        # ----midpoint----
        # SCREEN.blit(font.render('----', -1, (255, 0, 0)),
        #            (w.x, 360 + w.gap - w.offset - 95))

        birdgroup.update()
        birdgroup.draw(SCREEN)
        pygame.display.update()


if __name__ == "__main__":
    w = Walls(SCREEN)
    birdgroup = pygame.sprite.Group()
    deadgroup = pygame.sprite.Group()
    swarm = ParticleSwarm(MODELS, 25, 0.4, 1, 2, (-20, 20))
    for i in range(MODELS):
        bird = Bird(SCREEN, w)
        l1w, l1b, l2w, l2b = swarm.particles[i].rebuildWegihtMatrix()
        bird.brain.loadWeightMatrix(l1w, l1b, l2w, l2b)
        birdgroup.add(Bird(SCREEN, w))

    run()
