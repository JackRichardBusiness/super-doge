import pygame
from pygame.locals import *
import sys
from time import sleep
import json
from random import randint

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
                sleep(0.5)
            elif pressedKeys[K_r]:
                level.addRandomBox((self.mouseX / 32) + x_offset, self.mouseY/32)
            elif pressedKeys[K_g]:
                level.addGoomba((self.mouseX / 32) + x_offset, self.mouseY/32)
                sleep(0.5)
            elif pressedKeys[K_k]:
                level.addKoopa((self.mouseX / 32) + x_offset, self.mouseY/32)
                sleep(0.5)
            elif pressedKeys[K_s]:
                print "Saving level..."
                idFile = str(randint(0,999))
                data = {"id": int(idFile), "length": 60, "level": { "layers": { "sky":{ "x":[0,60], "y":[0,13] }, "ground":{"x":[0,60], "y":[14,16]}}, "objects": {"bush":[], "sky":[], "cloud":[], "pipe":[], "ground":[]}, "entities": {"randomBox":[], "coin":[], "Goomba":[], "Koopa":[]}}}
                for item in level.entityList:
                    print "Found " + item.__class__.__name__ + " at " + str(int(item.rect.x / 32)) + "," + str(int(item.rect.y / 32))
                    if not item.__class__.__name__ == "Coin":
                        data["level"]["entities"][item.__class__.__name__].append([int(item.rect.x / 32), int(item.rect.y / 32)])
                    else:
                        data["level"]["entities"][item.__class__.__name__.lower()].append([int(item.rect.x / 32), int(item.rect.y / 32)])
                for x in range(level.levelLength):
                    for y in range(15):
                        if level.level[y][x].sprite == level.sprites.spriteCollection.get("pipeL"):
                            print "Found pipe at " + str(x) + "," + str(y)
                            data["level"]["objects"]["pipe"].append([x, y, 14])
                        elif level.level[y][x].sprite == level.sprites.spriteCollection.get("bush_1"):
                            print "Found bush at " + str(x) + "," + str(y)
                            data["level"]["objects"]["bush"].append([x, y])
                        elif level.level[y][x].sprite == None:
                            print "Found box at " + str(x) + "," + str(y)
                            data["level"]["entities"]["randomBox"].append([x, y])
                        elif level.level[y][x].sprite == level.sprites.spriteCollection.get("cloud0_0"):
                            print "Found cloud at " + str(x) + "," + str(y)
                            data["level"]["objects"]["cloud"].append([x, y])
                        elif level.level[y][x].sprite == level.sprites.spriteCollection.get("ground"):
                            print "Found ground at " + str(x) + "," + str(y)
                            data["level"]["objects"]["ground"].append([x, y])
                with open("level_" + str(randint(0, 999)) + ".json", "w") as write_file:
                    json.dump(data, write_file)
                sleep(1)

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
