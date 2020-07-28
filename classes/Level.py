import json
import pygame

from classes.Sprites import Sprites
from classes.Tile import Tile
from entities.Coin import Coin
from entities.Goomba import Goomba
from entities.Koopa import Koopa
from entities.RandomBox import RandomBox
from entities.Lacy import Lacy
from entities.Sal import Sal

class Level:
    def __init__(self, screen, sound, dashboard):
        self.sprites = Sprites()
        self.dashboard = dashboard
        self.sound = sound
        self.screen = screen
        self.level = None
        self.levelLength = 0
        self.entityList = []
        self.makermode = False
        self.mario = None

    def loadLevel(self, levelname):
        with open("./levels/{}.json".format(levelname)) as jsonData:
            worldNum = int(levelname.split("Level")[1].split("-")[0])
            if worldNum == 2:
                self.sound.music_channel.stop()
                self.sound.play_music(self.sound.desert)
                self.sprites = Sprites("Desert")
            if worldNum == 3:
                self.sound.music_channel.stop()
                self.sound.play_music(self.sound.snow)
                self.sprites = Sprites("Snow")
            if worldNum == 4:
                self.sound.music_channel.stop()
                self.sound.play_music(self.sound.haunted)
            if worldNum == 5:
                self.sound.music_channel.stop()
                self.sound.play_music(self.sound.underwater)
            if worldNum == 6:
                self.sound.music_channel.stop()
                self.sound.play_music(self.sound.castle)
            data = json.load(jsonData)
            self.loadLayers(data)
            self.loadObjects(data)
            self.loadEntities(data, levelname)
            self.levelLength = data["length"]
            if levelname == "Level0-0":
                self.makermode = True
            
    def loadEntities(self, data, levelname=""):
        try:
            [self.addRandomBox(x, y) for x, y in data["level"]["entities"]["randomBox"]]
            [self.addGoomba(x, y) for x, y in data["level"]["entities"]["Goomba"]]
            [self.addKoopa(x, y) for x, y in data["level"]["entities"]["Koopa"]]
            [self.addCoin(x, y) for x, y in data["level"]["entities"]["coin"]]
            world = int(levelname.split("Level")[1].split("-")[0])
            level = int(levelname.split("Level")[1].split("-")[1])
            if level == 6:
                print "Boss level detected."
                if world == 1:
                    self.addLacy(13, 51)
                elif world == 2:
                    self.addSal(13, 51)
        except Exception as e:
            print e
            #if no entities in Level
            pass

    def loadLayers(self, data):
        layers = []
        for x in range(*data["level"]["layers"]["sky"]["x"]):
            layers.append(
                (
                    [
                        Tile(self.sprites.spriteCollection.get("sky"), None)
                        for y in range(*data["level"]["layers"]["sky"]["y"])
                    ]
                    + [
                        Tile(
                            self.sprites.spriteCollection.get("ground"),
                            pygame.Rect(x * 32, (y - 1) * 32, 32, 32),
                        )
                        for y in range(*data["level"]["layers"]["ground"]["y"])
                    ]
                )
            )
        self.level = list(map(list, zip(*layers)))

    def loadObjects(self, data):
        for x, y in data["level"]["objects"]["bush"]:
            self.addBushSprite(x, y)
        for x, y in data["level"]["objects"]["cloud"]:
            self.addCloudSprite(x, y)
        for x, y, z in data["level"]["objects"]["pipe"]:
            self.addPipeSprite(x, y, z)
        for x, y in data["level"]["objects"]["sky"]:
            self.level[y][x] = Tile(self.sprites.spriteCollection.get("sky"), None)
        for x, y in data["level"]["objects"]["ground"]:
            self.level[y][x] = Tile(
                self.sprites.spriteCollection.get("ground"),
                pygame.Rect(x * 32, y * 32, 32, 32),
            )

    def updateEntities(self, cam):
        for entity in self.entityList:
            entity.update(cam)
            if entity.alive is None:
                self.entityList.remove(entity)

    def drawLevel(self, camera):
        try:
            for y in range(0, 15):
                for x in range(0 - int(camera.pos.x + 1), 20 - int(camera.pos.x - 1)):
                    if self.level[y][x].sprite is not None:
                        if self.level[y][x].sprite.redrawBackground:
                            self.screen.blit(
                                self.sprites.spriteCollection.get("sky").image,
                                ((x + camera.pos.x) * 32, y * 32),
                            )
                        self.level[y][x].sprite.drawSprite(
                            x + camera.pos.x, y, self.screen
                        )
            self.updateEntities(camera)
        except IndexError:
            return

    def addCloudSprite(self, x, y):
        try:
            for yOff in range(0, 2):
                for xOff in range(0, 3):
                    self.level[y + yOff][x + xOff] = Tile(
                        self.sprites.spriteCollection.get(
                            "cloud{}_{}".format(yOff + 1, xOff + 1)
                        ),
                        None,
                    )
        except IndexError:
            return

    def addPipeSprite(self, x, y, length=2):
        try:
            # add Pipe Head
            self.level[y][x] = Tile(
                self.sprites.spriteCollection.get("pipeL"),
                pygame.Rect(x * 32, y * 32, 32, 32),
            )
            self.level[y][x + 1] = Tile(
                self.sprites.spriteCollection.get("pipeR"),
                pygame.Rect((x + 1) * 32, y * 32, 32, 32),
            )
            # add pipe Body
            for i in range(1, length + 20):
                self.level[y + i][x] = Tile(
                    self.sprites.spriteCollection.get("pipe2L"),
                    pygame.Rect(x * 32, (y + i) * 32, 32, 32),
                )
                self.level[y + i][x + 1] = Tile(
                    self.sprites.spriteCollection.get("pipe2R"),
                    pygame.Rect((x + 1) * 32, (y + i) * 32, 32, 32),
                )
        except IndexError:
            return

    def addBushSprite(self, x, y):
        try:
            self.level[y][x] = Tile(self.sprites.spriteCollection.get("bush_1"), None)
            self.level[y][x + 1] = Tile(
                self.sprites.spriteCollection.get("bush_2"), None
            )
            self.level[y][x + 2] = Tile(
                self.sprites.spriteCollection.get("bush_3"), None
            )
        except IndexError:
            return

    def addRandomBox(self, x, y):
        self.level[y][x] = Tile(None, pygame.Rect(x * 32, y * 32 - 1, 32, 32))
        self.entityList.append(
            RandomBox(
                self.screen,
                self.sprites.spriteCollection,
                x,
                y,
                self.sound,
                self.dashboard,
            )
        )

    def addCoin(self, x, y):
        self.entityList.append(Coin(self.screen, self.sprites.spriteCollection, x, y))

    def addGoomba(self, x, y):
        self.entityList.append(
            Goomba(self.screen, self.sprites.spriteCollection, x, y, self)
        )

    def addLacy(self, x, y):
        self.entityList.append(
            Lacy(self.screen, self.sprites.spriteCollection, x, y, self)
        )

    def addSal(self, x, y):
        self.entityList.append(
            Sal(self.screen, self.sprites.spriteCollection, x, y, self)
        )

    def addKoopa(self, x, y):
        self.entityList.append(
            Koopa(self.screen, self.sprites.spriteCollection, x, y, self)
        )
