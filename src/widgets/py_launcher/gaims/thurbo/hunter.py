import pygame as pg
import random
import os
from settings import *
from sprites import *
from items import *

class Hunter():
    def __init__(self, game, ps):
        self.game = game
        self.attack_delay = 100
        self.last_attack = pg.time.get_ticks()
        self.max_hp = 75
        self.max_ap = 50
        self.coinbag = 100
        self.move_speed = 5
        self.facing = "RIGHT"
        self.selected_arrow = ''
        self.walking = False
        self.ps = ps
        self.backpack = []
        self.weapon_type = "bow"
        self.weight_limit = 15
        self.item_limit = 7
        
    def attack(self):
        now = pg.time.get_ticks()
        if now - self.last_attack > self.attack_delay:
            self.last_attack = now
            if self.game.player.arrows >= 1:
                self.game.player.arrows -= 1
                self.b = Arrow(self.game,self.game.player.rect.centerx,self.game.player.rect.centery,self.game.player.facing,self.selected_arrow)
            elif self.game.player.arrows <= 0:
                pass
        
    def update(self):
        if self.facing == "LEFT":
            self.image = pg.image.load(os.path.join(hunter_folder, "face_left.png")).convert()
        elif self.facing == "UP":
            self.image = pg.image.load(os.path.join(hunter_folder, "face_up.png")).convert()
        elif self.facing == "DOWN":
            self.image = pg.image.load(os.path.join(hunter_folder, "face_down.png")).convert()
        elif self.facing == "RIGHT":
            self.image = pg.image.load(os.path.join(hunter_folder, "face_right.png")).convert()
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
        self.image.set_colorkey(WHITE)
            
class Arrow(pg.sprite.Sprite):
    def __init__(self, game, x, y, facing, type):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        if facing == "RIGHT":
            self.image = pg.image.load(os.path.join(hunter_folder, type + "arrow_right.png")).convert()
            self.speedx = 10
            self.speedy = 0
        elif facing == "DOWN":
            self.image = pg.image.load(os.path.join(hunter_folder, type + "arrow_down.png")).convert()
            self.speedx = 0
            self.speedy = 10
        elif facing == "LEFT":
            self.image = pg.image.load(os.path.join(hunter_folder, type + "arrow_left.png")).convert()
            self.speedy = 0
            self.speedx = -10
        elif facing == "UP":
            self.image = pg.image.load(os.path.join(hunter_folder, type + "arrow_up.png")).convert()
            self.speedx = 0
            self.speedy = -10
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.game = game
        self.damage = game.player.phys_atk
        
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        #kill it if it move off top of the screen
        self.bullet_walls = pg.sprite.groupcollide(self.game.bullets, self.game.walls, True, False)