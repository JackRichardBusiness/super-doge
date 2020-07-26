from classes.Animation import Animation
from classes.Maths import vec2D
from entities.EntityBase import EntityBase
from traits.lacyfight import LacyFight
from time import sleep

class Lacy(EntityBase):
    def __init__(self, screen, spriteColl, x, y, level):
        super(Lacy, self).__init__(y, x - 1, 1.25)
        self.spriteCollection = spriteColl
        self.animation = Animation(
            [
                self.spriteCollection.get("lacy-1").image,
                self.spriteCollection.get("lacy-2").image,
            ]
        )
        self.screen = screen
        self.leftrightTrait = LacyFight(self, level)
        self.type = "Mob"
        self.inAir = False
        self.inJump = False
        self.dashboard = level.dashboard
        self.lives = 3
        self.level = level

    def update(self, camera):
        if self.lives < 1:
            self.drawFlatGoomba(camera)
        if self.alive:
            self.applyGravity()
            self.drawLacy(camera)
            self.leftrightTrait.update()
        else:
            self.onDead(camera)

    def drawLacy(self, camera):
        self.screen.blit(self.animation.image, (self.rect.x + camera.x - 16, self.rect.y - 32))
        self.animation.update()

    def onDead(self, camera):
        if self.timer == 0:
            self.setPointsTextStartPosition(self.rect.x + 3, self.rect.y)
        if self.timer < self.timeAfterDeath:
            self.lives = self.lives - 1
        else:
            self.alive = None
        self.timer += 0.1

    def drawFlatGoomba(self, camera):
        self.level.mario.sound.music_channel.stop()
        self.level.mario.sound.play_sfx(self.level.mario.sound.clear)
        sleep(6.5)
        self.level.mario.restart = True

    def setPointsTextStartPosition(self, x, y):
        self.textPos = vec2D(x, y)

    def movePointsTextUpAndDraw(self, camera):
        self.textPos.y += -0.5
        self.dashboard.drawText("100", self.textPos.x + camera.x, self.textPos.y, 8)
