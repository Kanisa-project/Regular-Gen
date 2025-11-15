import pygame as pg
import random
import os
from settings import *
from sprites import *
from items import *

class Mage():
    def __init__(self, game, ps):
        self.game = game
        self.attack_delay = 100
        self.last_attack = pg.time.get_ticks()
        self.coinbag = 100
        self.move_speed = 5
        self.max_hp = 50
        self.max_mp = 100
        self.facing = "RIGHT"
        self.walking = False
        self.ps = ps
        self.backpack = []
        self.weapon_type = "staff"
        self.weight_limit = 10
        self.item_limit = 5
        
    def attack(self):
        now = pg.time.get_ticks()
        if now - self.last_attack > self.attack_delay:
            self.last_attack = now
            if self.game.player.mp >= 10:
                self.game.player.mp -= 10
                self.b = Firebolt(self.game,self.game.player.rect.centerx,self.game.player.rect.centery,self.facing)
            elif self.game.player.mp <= 0:
                self.b = Icebolt(self.game,self.game.player.rect.centerx,self.game.player.rect.centery,self.facing)
        
    def update(self):
        if self.game.player.facing == "LEFT":
            self.image = pg.image.load(os.path.join(mage_folder, "face_left.png")).convert()
        elif self.game.player.facing == "UP":
            self.image = pg.image.load(os.path.join(mage_folder, "face_up.png")).convert()
        elif self.game.player.facing == "DOWN":
            self.image = pg.image.load(os.path.join(mage_folder, "face_down.png")).convert()
        elif self.game.player.facing == "RIGHT":
            self.image = pg.image.load(os.path.join(mage_folder, "face_right.png")).convert()
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
        self.image.set_colorkey(WHITE)
        
    def draw_hud(self):
        pass
            
class Firebolt(pg.sprite.Sprite):
    def __init__(self, game, x, y,facing):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if self.game.player.facing == "RIGHT":
            self.image = pg.image.load(os.path.join(mage_folder, "firebolt.png")).convert()
            self.speedx = 10
            self.speedy = 0
        elif self.game.player.facing == "DOWN":
            self.image = pg.image.load(os.path.join(mage_folder, "firebolt.png")).convert()
            self.speedx = 0
            self.speedy = 10
        elif self.game.player.facing == "LEFT":
            self.image = pg.image.load(os.path.join(mage_folder, "firebolt.png")).convert()
            self.speedy = 0
            self.speedx = -10
        elif self.game.player.facing == "UP":
            self.image = pg.image.load(os.path.join(mage_folder, "firebolt.png")).convert()
            self.speedx = 0
            self.speedy = -10
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.damage = 50
        self.mp_cost = 10
        
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        #kill it if it move off top of the screen
        self.bullet_walls = pg.sprite.groupcollide(self.game.bullets, self.game.walls, True, False)
            
class Icebolt(pg.sprite.Sprite):
    def __init__(self, game, x, y,facing):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if self.game.player.facing == "RIGHT":
            self.image = pg.image.load(os.path.join(mage_folder, "icebolt.png")).convert()
            self.speedx = 10
            self.speedy = 0
        elif self.game.player.facing == "DOWN":
            self.image = pg.image.load(os.path.join(mage_folder, "icebolt.png")).convert()
            self.speedx = 0
            self.speedy = 10
        elif self.game.player.facing == "LEFT":
            self.image = pg.image.load(os.path.join(mage_folder, "icebolt.png")).convert()
            self.speedx = -10
            self.speedy = 0
        elif self.game.player.facing == "UP":
            self.image = pg.image.load(os.path.join(mage_folder, "icebolt.png")).convert()
            self.speedx = 0
            self.speedy = -10
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.damage = self.game.player.magic_atk
        self.mp_cost = 3
        
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        #kill it if it move off top of the screen
        self.bullet_walls = pg.sprite.groupcollide(self.game.bullets, self.game.walls, True, False)