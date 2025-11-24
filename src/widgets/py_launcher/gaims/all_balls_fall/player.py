import pygame as pg

class Player(pg.sprite.Sprite):
    def __init__(self,x,y,image):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.rolling_direction = None

    def move(self):
        if self.rolling_direction == "left":
            self.rect.x -= 5
        elif self.rolling_direction == "right":
            self.rect.x += 5

    def update(self, *args, **kwargs):
        self.rect.y += 2
        self.move()

    def collide_with_obstacle(self, obstacle):
        return self.rect.colliderect(obstacle.rect)