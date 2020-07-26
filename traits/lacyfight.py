from random import randint

from classes.Collider import Collider
from random import randint

class LacyFight:
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
        if self.entity.rect.x > (54*32):
            self.direction = -1
        elif self.entity.vel.x == 0:
            self.direction = 1
        self.entity.vel.x = self.speed * self.direction
        self.moveEntity()
        self.jump(self.entity.inJump)
        
        if abs(self.entity.rect.x - self.level.mario.rect.x) < 150 and not self.entity.inJump:
            if randint(0, 250) == 100 and self.level.mario.rect.y == 384:
                self.jump(True)

    def moveEntity(self):
        self.entity.rect.y += self.entity.vel.y
        self.collDetection.checkY()
        self.entity.rect.x += self.entity.vel.x
        self.collDetection.checkX()

    def jump(self, jumping):
        if jumping:
            if not self.entity.inAir and not self.entity.inJump:
                self.entity.vel.y = self.vertical_speed
                self.entity.inAir = True
                self.initalHeight = self.entity.rect.y
                self.entity.inJump = True
                
        if self.entity.inJump:
            if (self.initalHeight-self.entity.rect.y) >= self.deaccelerationHeight or self.entity.vel.y==0:
                self.entity.inJump = False
                self.reset()

    def reset(self):
        self.entity.inAir = False
        self.level.mario.stun()
