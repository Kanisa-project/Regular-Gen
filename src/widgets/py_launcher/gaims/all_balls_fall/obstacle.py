import random

import pygame as pg

class Wall(pg.sprite.Sprite):
    def __init__(self,x,y,image):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def update(self, *args, **kwargs):
        self.rect.y -= 3
        if self.rect.y < 0:
            self.rect.y = 512
            self.rect.x = 64 * random.randint(0, 10)
