# THIS IS PART OF AN EXPERIMENTAL MULTIPROCESSING IMPLEMENTATION OF FlappyAI

import pygame
from pygame.locals import *  # noqa
import sys
import random
import time
import multiprocessing


class FlappyBird:

    def __init__(self, sharedTele, sharedJump, lock):
        self.screen = pygame.display.set_mode((400, 708))
        self.bird = pygame.Rect(65, 50, 50, 50)
        self.background = pygame.image.load("assets/background.png").convert()
        self.birdSprites = [pygame.image.load("assets/1.png").convert_alpha(),
                            pygame.image.load("assets/2.png").convert_alpha(),
                            pygame.image.load("assets/dead.png")]
        self.wallUp = pygame.image.load("assets/bottom.png").convert_alpha()
        self.wallDown = pygame.image.load("assets/top.png").convert_alpha()
        self.gap = 130
        self.offset = random.randint(-110, 110)
        self.wallx = 400
        self.totalx = 0
        self.birdY = 350
        self.jump = 0
        self.jumpSpeed = 10
        self.gravity = 5
        self.dead = False
        self.sprite = 0
        self.counter = 0
        self.speed = 2
        self.sharedTele = sharedTele
        self.sharedJump = sharedJump
        self.lock = lock

    def updateWalls(self):
        self.wallx -= self.speed
        self.totalx += 2
        if self.wallx < -80:
            self.wallx = 400
            self.counter += 1
            self.offset = random.randint(-110, 110)

    def birdUpdate(self):
        if self.jump:
            self.jumpSpeed -= 1
            self.birdY -= self.jumpSpeed
            self.jump -= 1
        else:
            self.birdY += self.gravity
            self.gravity += 0.2
        self.bird[1] = self.birdY
        upRect = pygame.Rect(self.wallx,
                             360 + self.gap - self.offset + 10,
                             self.wallUp.get_width() - 10,
                             self.wallUp.get_height())
        downRect = pygame.Rect(self.wallx,
                               0 - self.gap - self.offset - 10,
                               self.wallDown.get_width() - 10,
                               self.wallDown.get_height())
        if upRect.colliderect(self.bird):
            self.dead = True  # set False to deactivate collisions
        if downRect.colliderect(self.bird):
            self.dead = True  # set False to deactivate collisions
        # bound bird btwn sky and ground
        if not 0 < self.bird[1] < 720:
            self.bird[1] = 50
            self.birdY = 50
            self.dead = False
            self.counter = 0
            self.wallx = 400
            self.totalx = 0
            self.offset = random.randint(-110, 110)
            self.gravity = 5

    def Telemetry(self):
        self.bird_coord = (70, self.birdY)
        self.wall_coord = (self.wallx, 360 + self.gap - self.offset - 65)
        distx = round(self.wall_coord[0] - self.bird_coord[0], 0) + 180
        disty = round(self.wall_coord[1] - self.bird_coord[1], 0) + 400

        # tele_console = 'Dist X:{: <5}|  Dist Y:{: <5}|  TotalX:{: <8} '.format(
        #    int(distx), int(disty), self.totalx) + str(time.ctime())
        # print(tele_console)
        #self.sharedTele.value = [distx, disty]

    def RenderTracers(self):
        # ---Tracer Renders---
        # X vector
        pygame.draw.line(self.screen, (0, 0, 255), (self.bird_coord[
                         0] + 35, self.wall_coord[1]), (self.bird_coord[
                             0] + 35, self.bird_coord[1] + 10), 2)
        # Y vector
        pygame.draw.line(self.screen, (0, 255, 0), (self.bird_coord[
                         0] + 35, self.wall_coord[1]), (self.wall_coord[
                             0], self.wall_coord[1]), 2)
        # resultant vector
        pygame.draw.line(self.screen, (255, 0, 0), (self.bird_coord[
                         0] + 35, self.bird_coord[1] + 10), (self.wall_coord[
                             0], self.wall_coord[1]), 2)
        # mipoint render
        # self.screen.blit(font.render('____',-1,(255, 0, 0)),(self.wallx, 360 + self.gap - self.offset - 117))

    def Progression(self):

        if self.totalx <= 200:
            self.x_old = 0
            self.speed = 2

        if self.totalx - self.x_old > 500 and self.speed < 8:
            self.speed += 0.20
            self.x_old = self.totalx

    def run(self):
        clock = pygame.time.Clock()
        pygame.font.init()
        font = pygame.font.SysFont("Arial", 50)
        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if (event.type == pygame.KEYDOWN or event.type ==
                        pygame.MOUSEBUTTONDOWN) and not self.dead:
                    self.jump = 17
                    self.gravity = 5
                    self.jumpSpeed = 10

            # if self.sharedJump.value and not self.dead:
            #    self.jump = 17
            #    self.gravity = 5
            #    self.jumpSpeed = 10

            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.wallUp,
                             (self.wallx, 360 + self.gap - self.offset))
            self.screen.blit(self.wallDown,
                             (self.wallx, 0 - self.gap - self.offset))
            self.screen.blit(font.render(str(self.counter),
                                         -1,
                                         (255, 255, 255)),
                             (200, 50))

            self.Progression()
            self.Telemetry()
            self.RenderTracers()

            if self.dead:
                self.sprite = 2
            elif self.jump:
                self.sprite = 1
            self.screen.blit(self.birdSprites[self.sprite], (70, self.birdY))
            if not self.dead:
                self.sprite = 0
            self.updateWalls()
            self.birdUpdate()
            pygame.display.update()


if __name__ == '__main__':
    FlappyBird([None, None], None, None).run()
