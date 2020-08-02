import pygame


class Tile:
    def __init__(self, sprite, rect, canUse=False):
        self.sprite = sprite
        self.rect = rect
        self.canUse = canUse

    def drawRect(self, screen):
        try:
            pygame.draw.rect(screen, pygame.Color(255, 0, 0), self.rect, 1)
        except Exception:
            pass
