from random import randint

from classes.Collider import Collider
from random import randint

class HenriettaFight:
    def __init__(self, entity, level):
        self.direction = -1 if randint(0, 1) == 0 else 1
        self.entity = entity
        self.collDetection = Collider(self.entity, level)
        self.speed = 1
        self.entity.vel.x = self.speed * self.direction
        self.level = level

        self.vertical_speed = -12
        self.jumpHeight = 120
        self.entity = entity
        self.initalHeight = 384
        self.deaccelerationHeight = self.jumpHeight - ((self.vertical_speed*self.vertical_speed)/(2*self.entity.gravity))
        
    def update(self):
        self.moveEntity()

    def moveEntity(self):
        self.entity.rect.y += self.entity.vel.y
        self.collDetection.checkY()
        self.entity.rect.x += self.entity.vel.x
        self.collDetection.checkX()
