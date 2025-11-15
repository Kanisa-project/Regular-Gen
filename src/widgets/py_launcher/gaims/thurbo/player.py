import pygame as pg
import random
import os
from knight import *
from hunter import *
from mage import *
from fairy import *
from human import *
from orc import *
from settings import *
from sprites import *
from items import *


class Player(pg.sprite.Sprite):
    def __init__(self, game, ps):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.player_folder = os.path.join(races_folder, ps[0])
        self.player_folder = os.path.join(self.player_folder, ps[1])
        self.image = pg.image.load(os.path.join(self.player_folder,ps[0] + "_" + ps[1] + "_face_right.png")).convert()
        self.rect = self.image.get_rect()
        self.image.set_colorkey(WHITE)
        self.attack_delay = 100
        self.last_attack = pg.time.get_ticks()
        self.max_hp = 100
        self.coinbag = 100
        self.species = ps[0]
        self.occupation = ps[1]
        self.carved_runes = ps[2]
        self.vfdscore = ps[3]
        self.item_limit = 1
        self.weight_limit = 0
        self.carried_weight = 0
        self.num_of_walls = 0
        if self.species == "fairy":
            self.race = Fairy(game, ps)
            self.max_hp += self.race.max_hp
            self.vfdscore[0] += 1
            self.vfdscore[1] += 4
            self.vfdscore[2] += 4
        if self.species == "human":
            self.race = Human(game, ps)
            self.max_hp += self.race.max_hp
            self.vfdscore[0] += 3
            self.vfdscore[1] += 3
            self.vfdscore[2] += 3
        if self.species == "orc":
            self.race = Orc(game, ps)
            self.max_hp += self.race.max_hp
            self.vfdscore[0] += 5
            self.vfdscore[1] += 2
            self.vfdscore[2] += 2
        if self.occupation == "knight":
            self.job = Knight(game, ps)
            self.max_hp += self.job.max_hp
            self.hp = self.max_hp
            self.max_fp = self.job.max_fp
            self.fp = self.max_fp
            self.vfdscore[0] += 6
            self.vfdscore[1] += 2
            self.vfdscore[2] += 1
        if self.occupation == "hunter":
            self.job = Hunter(game, ps)
            self.arrows = 10
            self.max_hp += self.job.max_hp
            self.hp = self.max_hp
            self.max_ap = self.job.max_ap
            self.ap = self.max_ap
            self.vfdscore[0] += 4
            self.vfdscore[1] += 4
            self.vfdscore[2] += 1
        if self.occupation == "mage":
            self.job = Mage(game, ps)
            self.max_hp += self.job.max_hp
            self.hp = self.max_hp
            self.max_mp = self.job.max_mp
            self.mp = self.max_mp
            self.vfdscore[0] += 1
            self.vfdscore[1] += 2
            self.vfdscore[2] += 6
        self.item_limit += self.race.item_limit
        self.item_limit += self.job.item_limit
        self.weight_limit += self.race.weight_limit
        self.weight_limit += self.job.weight_limit
        self.facing = "RIGHT"
        self.walking = False
        self.move_speed = self.vfdscore[1] + 2
        self.phys_atk = self.vfdscore[0] + 3
        self.phys_def = self.vfdscore[0] + 2
        self.magic_atk = self.vfdscore[2] + 2
        self.magic_def = self.vfdscore[2] + 2
        self.weight_limit += self.vfdscore[0] * 5
        self.ps = ps
        self.vx = 0
        self.vy = 0
        self.backpack = []
        
    def attack(self):
        now = pg.time.get_ticks()
        if now - self.last_attack > self.attack_delay:
            self.last_attack = now
            self.job.attack()
        for mob in self.game.mobs:
            mob.struck = False
                 
    def move(self,dx=0,dy=0):
        if not self.collide_with_walls(dx,dy):
            self.x += dx
            self.y += dy
            
    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False
        
    def collide_with_mobs(self, dx=0, dy=0):
        for mob in self.game.mobs:
            if mob.x == self.x + dx and mob.y == self.y + dy:
                return True
        return False        
        
    def collide_with_doors(self, dx=0, dy=0):
        for door in self.game.doors:
            if door.x == self.x + dx and door.y == self.y + dy:
                return True
        return False
        
    def collide_with_chests(self, dx=0, dy=0):
        for chest in self.game.chests:
            if chest.x == self.x + dx and chest.y == self.y + dy:
                return True
        return False
        
    def update(self):
        if self.facing == "LEFT":
            self.image = pg.image.load(os.path.join(self.player_folder, self.species + "_" + self.occupation + "_face_left.png")).convert()
        elif self.facing == "UP":
            self.image = pg.image.load(os.path.join(self.player_folder, self.species + "_" + self.occupation + "_face_up.png")).convert()
        elif self.facing == "DOWN":
            self.image = pg.image.load(os.path.join(self.player_folder, self.species + "_" + self.occupation + "_face_down.png")).convert()
        elif self.facing == "RIGHT":
            self.image = pg.image.load(os.path.join(self.player_folder, self.species + "_" + self.occupation + "_face_right.png")).convert()
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
        self.image.set_colorkey(WHITE)