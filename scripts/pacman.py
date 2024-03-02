import pygame
from pygame.locals import *
from scripts.vector import Vector2
from scripts.constants import *
from scripts.entity import Entity
from scripts.sprites import PacmanSprites

class Pacman(Entity):
    def __init__(self, node):
        Entity.__init__(self, node)
        self.name = PACMAN
        self.color = YELLOW
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True
        self.sprites = PacmanSprites(self)
        self.last_dir = STOP

    def reset(self):
        Entity.reset(self)
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True
        self.image = self.sprites.getStartImage()
        self.sprites.reset()
        self.last_dir = STOP

    def die(self):
        self.alive = False
        self.direction = STOP

    def update(self, dt):
        self.sprites.update(dt)
        self.position += self.directions[self.direction] * self.speed * dt
        direction = self.getValidKey()

        if direction != STOP:
            self.last_dir = direction

        next_node = None
        if self.direction != STOP:
            if self.node.neighbors[self.direction] != None:
                next_node = self.node.neighbors[self.direction]


        if next_node != None and self.last_dir != STOP:
            # print(self.validDirectionOfNode(self.last_dir, next_node))
            if self.validDirectionOfNode(self.last_dir, next_node) == True and self.overshotNode(next_node):
                self.node = next_node
                self.direction = self.last_dir
                last_dir = STOP


        if self.overshotTarget():
            self.node = self.target
            if self.node.neighbors[PORTAL] is not None:
                self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)

            if self.target is self.node:
                self.direction = STOP

            self.setPosition()

        else:
            if self.oppositeDirection(direction):
                self.reverseDirection()

    def eatPellets(self, pelletList):
        for pellet in pelletList:
            if self.collideCheck(pellet):
                return pellet
        return None

    def collideGhost(self, ghost):
        return self.collideCheck(ghost)

    def collideCheck(self, other):
        dist = self.position - other.position
        distSquared = dist.magnitudeSquared()
        radSquared = (self.collideRadius + other.collideRadius) ** 2
        if distSquared <= radSquared:
            return True
        return False

    def getValidKey(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            return UP
        if key_pressed[K_DOWN]:
            return DOWN
        if key_pressed[K_LEFT]:
            return LEFT
        if key_pressed[K_RIGHT]:
            return RIGHT
        return STOP
