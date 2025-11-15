import pygame as pg
import random
import os
from settings import *
from sprites import *
from items import *

class Knight():
    def __init__(self, game, ps):
        self.game = game
        self.attack_delay = 100
        self.last_attack = pg.time.get_ticks()
        self.max_hp = 200
        self.max_fp = 100
        self.coinbag = 100
        self.move_speed = 5
        self.facing = "RIGHT"
        self.walking = False
        self.ps = ps
        self.backpack = []
        self.weapon_type = "sword"
        self.weight_limit = 200
        self.item_limit = 3
        
    def attack(self):
        now = pg.time.get_ticks()
        if now - self.last_attack > self.attack_delay:
            self.last_attack = now
            print("KOL")
            if self.game.player.facing == "RIGHT":
                self.b = Sword(self.game,self.game.player.rect.centerx,self.game.player.rect.centery)
                self.b = Sword(self.game,self.game.player.rect.centerx+(1*TILESIZE),self.game.player.rect.centery)
            elif self.game.player.facing == "DOWN":
                self.b = Sword(self.game,self.game.player.rect.centerx,self.game.player.rect.centery+(1*TILESIZE))
                self.b = Sword(self.game,self.game.player.rect.centerx,self.game.player.rect.centery)
            elif self.game.player.facing == "LEFT":
                self.b = Sword(self.game,self.game.player.rect.centerx-(1*TILESIZE),self.game.player.rect.centery)
                self.b = Sword(self.game,self.game.player.rect.centerx,self.game.player.rect.centery)
            elif self.game.player.facing == "UP":
                self.b = Sword(self.game,self.game.player.rect.centerx,self.game.player.rect.centery-(1*TILESIZE))
                self.b = Sword(self.game,self.game.player.rect.centerx,self.game.player.rect.centery)
                
    def update(self):
        pass
    
    def draw_hud(self):
        pass
    
        
class Sword(pg.sprite.Sprite):
    def __init__(self, game,x,y):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.image.load(os.path.join(knight_folder, "sword.png")).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.duration = 1000
        self.placed_time = pg.time.get_ticks()
        self.game = game
        self.damage = game.player.phys_atk
        
    def update(self):
        self.bullet_walls = pg.sprite.groupcollide(self.game.bullets, self.game.walls, True, False)
        now = pg.time.get_ticks()
        if now - self.placed_time > self.duration:
            self.kill()