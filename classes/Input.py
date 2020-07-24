import pygame
from pygame.locals import *
import sys

from classes.Sprites import Sprites
from classes.Tile import Tile
from entities.Coin import Coin
from entities.Goomba import Goomba
from entities.Koopa import Koopa
from entities.RandomBox import RandomBox


class Input:
    def __init__(self, entity):
        self.mouseX = 0
        self.mouseY = 0
        self.entity = entity

    def checkForInput(self, makermode=False, level=None, player=None):
        self.checkForKeyboardInput(makermode, level, player)
        self.checkForMouseInput()
        self.checkForQuitAndRestartInputEvents()

    def checkForKeyboardInput(self, makermode=False, level=None, player=None):
        pressedKeys = pygame.key.get_pressed()

        if pressedKeys[K_LEFT] or pressedKeys[K_h] and not pressedKeys[K_RIGHT]:
            self.entity.traits["goTrait"].direction = -1
        elif pressedKeys[K_RIGHT] or pressedKeys[K_l] and not pressedKeys[K_LEFT]:
            self.entity.traits["goTrait"].direction = 1
        else:
            self.entity.traits['goTrait'].direction = 0

        isJumping = pressedKeys[K_SPACE] or pressedKeys[K_UP] or pressedKeys[K_k]
        self.entity.traits['jumpTrait'].jump(isJumping)

        self.entity.traits['goTrait'].boost = pressedKeys[K_LSHIFT]

        if makermode and not level == None:
            x_offset = int(player.camera.x / 32) * -1
            if pressedKeys[K_b]:
                level.level[self.mouseY / 32][(self.mouseX / 32) + x_offset] = Tile(
                    level.sprites.spriteCollection.get("ground"),
                    pygame.Rect((self.mouseX / 32) + x_offset, self.mouseY, 32, 32)
                )
            elif pressedKeys[K_c]:
                level.addCloudSprite((self.mouseX / 32) + x_offset, self.mouseY/32)
            elif pressedKeys[K_y]:
                level.addBushSprite((self.mouseX / 32) + x_offset, self.mouseY/32)
            elif pressedKeys[K_p]:
                level.addPipeSprite((self.mouseX / 32) + x_offset, self.mouseY/32, 14)
            elif pressedKeys[K_f]:
                level.level[self.mouseY / 32][(self.mouseX / 32) + x_offset] = Tile(level.sprites.spriteCollection.get("sky"), None)
            elif pressedKeys[K_o]:
                level.addCoin((self.mouseX / 32) + x_offset, self.mouseY/32)
            elif pressedKeys[K_r]:
                level.addRandomBox((self.mouseX / 32) + x_offset, self.mouseY/32)
            elif pressedKeys[K_g]:
                level.addGoomba((self.mouseX / 32) + x_offset, self.mouseY/32)
            elif pressedKeys[K_k]:
                level.addKoopa((self.mouseX / 32) + x_offset, self.mouseY/32)    

    def checkForMouseInput(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        self.mouseX = mouseX
        self.mouseY = mouseY

    def checkForQuitAndRestartInputEvents(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and \
                (event.key == pygame.K_ESCAPE or event.key == pygame.K_F5):
                self.entity.pause = True
                self.entity.pauseObj.createBackgroundBlur()

    def isLeftMouseButtonPressed(self):
        return pygame.mouse.get_pressed()[0]

    def isRightMouseButtonPressed(self):
        return pygame.mouse.get_pressed()[2]
