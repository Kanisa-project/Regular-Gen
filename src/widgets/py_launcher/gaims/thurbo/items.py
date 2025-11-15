import pygame as pg
import random
import os
from settings import *
from sprites import *
from knight import *
from hunter import *
from mage import *


class Food(pg.sprite.Sprite):
    def __init__(self,game,food_type):
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.food_dict = {"bread": (30,20,15,"f"), "apple": (60,30,25,"f"), "milk": (25,40,30,"d"), "water": (50,50,40,"d")}
        self.image = pg.image.load(os.path.join(items_folder, food_type + ".png")).convert()
        self.rect = self.image.get_rect()
        self.image.set_colorkey(WHITE)
        self.food_type = food_type
        self.x = 8
        self.y = 352
        self.i = len(game.player.backpack)
        self.rect.x = self.x*TILESIZE + (self.i*TILESIZE)
        self.rect.y = self.y*TILESIZE + (self.i*TILESIZE)
        
    def use(self,player,arg1):
        if arg1 in player.backpack:
            player.backpack.remove(arg1)
            player.move_speed += 1
            if self.food_dict[arg1.food_type][3] == "f":
                player.hp += self.food_dict[arg1.food_type][0]
                if player.hp > player.max_hp:
                    player.hp = player.max_hp
            elif self.food_dict[arg1.food_type][3] == "d" and player.ps[0] == "magic":
                player.mp += self.food_dict[arg1.food_type][0]
                if player.mp > player.max_mp:
                    player.mp = player.max_mp
        
    def update(self):
        self.rect.x = self.x*TILESIZE + (self.i*TILESIZE)
        self.rect.y = self.y * TILESIZE
    

class Bread(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.items, game.foods
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.image.load(os.path.join(items_folder, "bread.png")).convert()
        self.rect = self.image.get_rect()
        self.image.set_colorkey(WHITE)
        self.game = game
        self.x = x
        self.y = y
        self.i = len(game.player.backpack)
        self.health_restored = 30
        game.player.carried_weight += 5
        
    def use(self,player):
        if self in player.backpack:
            player.backpack.remove(self)
            player.hp += self.health_restored
            self.image = pg.image.load(os.path.join(items_folder, "blank.png")).convert()
            self.image.set_colorkey(WHITE)
            self.game.player.carried_weight -= 5
            if player.hp > player.max_hp:
                player.hp = player.max_hp
        
    def update(self):
        self.rect.x = self.x*TILESIZE + (self.i*TILESIZE)
        self.rect.y = self.y*TILESIZE
        
class Apple(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.items, game.foods
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.image.load(os.path.join(items_folder, "apple.png")).convert()
        self.rect = self.image.get_rect()
        self.image.set_colorkey(WHITE)
        self.game = game
        self.x = x
        self.y = y
        self.i = len(game.player.backpack)
        self.health_restored = 60
        game.player.carried_weight += 5
        
    def use(self,player):
        if self in player.backpack:
            player.backpack.remove(self)
            player.hp += self.health_restored
            self.image = pg.image.load(os.path.join(items_folder, "blank.png")).convert()
            self.image.set_colorkey(WHITE)
            self.game.player.carried_weight -= 5
            if player.hp > player.max_hp:
                player.hp = player.max_hp
        
    def update(self):
        self.rect.x = self.x*TILESIZE + (self.i*TILESIZE)
        self.rect.y = self.y*TILESIZE
        
class Milk(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.items, game.drinks
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.image.load(os.path.join(items_folder, "milk.png")).convert()
        self.rect = self.image.get_rect()
        self.image.set_colorkey(WHITE)
        self.x = x
        self.y = y
        self.i = len(game.player.backpack)
        self.game = game
        self.mana_restored = 30
        game.player.carried_weight += 5
        
    def use(self,player):
        if self in player.backpack:
            player.backpack.remove(self)
            player.mp += self.mana_restored
            self.image = pg.image.load(os.path.join(items_folder, "blank.png")).convert()
            self.image.set_colorkey(WHITE)
            self.game.player.carried_weight -= 5
            if player.mp > player.max_mp:
                player.mp = player.max_mp
        
    def update(self):
        self.rect.x = self.x*TILESIZE + (self.i*TILESIZE)
        self.rect.y = self.y*TILESIZE
        
class Water(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.items, game.drinks
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.image.load(os.path.join(items_folder, "water.png")).convert()
        self.rect = self.image.get_rect()
        self.image.set_colorkey(WHITE)
        self.game = game
        self.x = x
        self.y = y
        self.i = len(game.player.backpack)
        self.mana_restored = 60
        game.player.carried_weight += 5
        
    def use(self,player):
        if self in player.backpack:
            player.backpack.remove(self)
            player.mp += self.mana_restored
            self.image = pg.image.load(os.path.join(items_folder, "blank.png")).convert()
            self.image.set_colorkey(WHITE)
            self.game.player.carried_weight -= 5
            if player.mp > player.max_mp:
                player.mp = player.max_mp
        
    def update(self):
        self.rect.x = self.x*TILESIZE + (self.i*TILESIZE)
        self.rect.y = self.y*TILESIZE
    
class Potion(pg.sprite.Sprite):
    def __init__(self,game,pot_type):
        self.groups = game.all_sprites, game.items
        self.pot_dict = {"health potion": (10,25,15), "attack potion": (2,40,30), "defence potion": (2,50,40)}
        self.image = pg.image.load(os.path.join(items_folder, pot_type + ".png")).convert()
        self.rect = self.image.get_rect()
        self.image.set_colorkey(WHITE)
        self.pot_type = pot_type
        self.x = 8
        self.y = 11
        self.i = len(game.player.backpack)
        self.rect.x = self.x*TILESIZE + (self.i*TILESIZE)
        self.rect.y = self.y*TILESIZE + (self.i*TILESIZE)
        
    def use(self,player,arg1):
        if arg1 in player.backpack:
            if arg1 + "potion" == "health potion":
                player.backpack.remove(arg1)
                player.max_hp += self.pot_dict[arg1.pot_type][0]
        
class min_hp_potion(pg.sprite.Sprite):
    def __init__(self):
        pass