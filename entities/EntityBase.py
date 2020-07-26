import pygame

from classes.Maths import vec2D


class EntityBase(object):
    def __init__(self, x, y, gravity, size=32):
        self.vel = vec2D()
        self.rect = pygame.Rect(x * 32, y * 32, size, size)
        self.gravity = gravity
        self.traits = None
        self.alive = True
        self.timeAfterDeath = 5
        self.timer = 0
        self.type = ""
        self.onGround = False
        self.obeygravity = True
        self.size = size
        self.stunned = False
        
    def applyGravity(self):
        if self.obeygravity:
            self.vel.y += self.gravity

    def updateTraits(self):
        for trait in self.traits.values():
            try:
                trait.update()
            except AttributeError:
                pass

    def getPosIndex(self):
        return vec2D(int(self.rect.x / self.size), int(self.rect.y / self.size))

    def getPosIndexAsFloat(self):
        return vec2D((self.rect.x / float(self.size)), (self.rect.y / float(self.size)))
