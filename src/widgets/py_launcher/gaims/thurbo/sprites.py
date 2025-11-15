#SPRITES FOR THURBO
import pygame as pg
import random
import math
import os
from settings import *
from items import *
from spawners import *
from settings import *
    
def draw_text(surf, text, size, x, y, color):
    font = pg.font.Font(fontname, size)
    text_surface = font.render(text,True,color)
    text_rect = text_surface.get_rect()
    text_rect.x = x
    text_rect.y = y
    surf.blit(text_surface, (text_rect))
            
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y,color_int=random.randint(0,23)-1):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load(os.path.join(img_folder, "wall" + str(random.randint(1,NUMBER_OF_WALLSPACES)) + ".png")).convert()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
        
    def update(self):
        pass
        
class Chest(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.chests
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load(os.path.join(img_folder, "closed_chest2.png")).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
        self.opened = False
        if self.game.player.occupation == "knight":
            self.full_item_list = ["apple","bread"]
        if self.game.player.occupation == "hunter":
            self.full_item_list = ["apple","bread"]
        if self.game.player.occupation == "mage":
            self.full_item_list = ["apple","bread","water","milk"]
        self.num_of_items = random.randint(1,5)
        self.item_list = []
        for i in range(self.num_of_items):
            self.item_list += [self.full_item_list[random.randint(0,len(self.full_item_list)-1)]]
    def update(self):
        if self.opened:
            self.image = pg.image.load(os.path.join(img_folder, "opened_chest.png")).convert()
        else:
            self.image = pg.image.load(os.path.join(img_folder, "closed_chest.png")).convert()
        
    def open_chest(self,player):
        self.opened = True
        player.coinbag += 10 * player.vfdscore[1]
        for item in self.item_list:
            if item == "apple" and player.carried_weight < player.weight_limit and len(player.backpack) < player.item_limit:
                player.backpack += [Apple(self.game,8,11)]
            if item == "bread" and player.carried_weight < player.weight_limit and len(player.backpack) < player.item_limit:
                player.backpack += [Bread(self.game,8,11)]
            if item == "milk" and player.carried_weight < player.weight_limit and len(player.backpack) < player.item_limit:
                player.backpack += [Milk(self.game,8,11)]
            if item == "water" and player.carried_weight < player.weight_limit and len(player.backpack) < player.item_limit:
                player.backpack += [Water(self.game,8,11)]
        self.kill()
            
class Doorway(pg.sprite.Sprite):
    def __init__(self, game, x, y,color_int=random.randint(0,23)-1):
        self.groups = game.all_sprites, game.doors
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load(os.path.join(img_folder, "doorway.png")).convert()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
        
    def update(self):
        pass
    
    def player_activate(self):
        if self.game.player.rect.x == self.rect.x and self.game.player.rect.y == self.rect.y and self.x > WIDTH/2:
            self.game.next_map()
        elif self.game.player.rect.x == self.rect.x and self.game.player.rect.y == self.rect.y and self.x < WIDTH/2:
            self.game.past_map()
        pass
        
class Floor(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.flooring
        pg.sprite.Sprite.__init__(self, self.groups)
        for i in range(1,NUMBER_OF_FLOORSPACES):
            pg.image.load(os.path.join(img_folder, "stone_tile" + str(i) + ".png")).convert()
        self.game = game
        self.image = pg.image.load(os.path.join(img_folder, "stone_tile" + str(random.randint(1,NUMBER_OF_FLOORSPACES)) + ".png")).convert()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y 
        
    def update(self):
        pass
        
class rune_symbols(pg.sprite.Sprite):
    def __init__(self,surf,x,y,rune):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(os.path.join(rune_folder,rune + ".png")).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        surf.blit(self.image,(self.rect.x,self.rect.y))
        self.rune = rune
        self.selected = False
        
    def update(self):
        if self.selected == False:
            self.image = pg.image.load(os.path.join(rune_folder,self.rune + ".png")).convert()
        if self.selected == True:
            self.image = pg.image.load(os.path.join(rune_folder,self.rune + "_selected")).convert()
        pass
        
        
class start_screen_buttons(pg.sprite.Sprite):
    def __init__(self,game,surf,y,button):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.image.load(os.path.join(img_folder,button)).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = (WIDTH / 2)
        self.rect.y = (HEIGHT / 2) + y
        surf.blit(self.image,(self.rect.x,self.rect.y))
        
    def update(self):
        pass
        
class select_occupation_sprite(pg.sprite.Sprite):
    def __init__(self,surf,x,y,class_image):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(os.path.join(professions_folder, class_image)).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = (WIDTH / 2) + x
        self.rect.y = (HEIGHT / 3) + y
        surf.blit(self.image,(self.rect.x,self.rect.y))
        
    def update(self,game):
        pass
        
class select_race_sprite(pg.sprite.Sprite):
    def __init__(self,surf,x,y,race_image):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(os.path.join(races_folder, race_image)).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = (WIDTH / 2) + x
        self.rect.y = (HEIGHT / 2) + y
        surf.blit(self.image,(self.rect.x,self.rect.y))
        
    def update(self,game):
        pass

class RuneCard(pg.sprite.Sprite):
    def __init__(self,game,surf,x,y,rune):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.rune = rune
        self.image = pg.image.load(os.path.join(rune_folder, "rune_back.png")).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.isFaceup = False
        self.isSelected = False
        
    def update(self):
        if self.isFaceup:
            if not self.isSelected:
                self.image = pg.image.load(os.path.join(rune_folder, self.rune.germanic.lower() + ".png"))
            elif self.isSelected and self.isFaceup:
                self.image = pg.image.load(os.path.join(rune_folder, self.rune.germanic.lower() + "_selected.png"))
            
    def flipCard(self,game):
        self.isFaceup = not self.isFaceup
        game.faceup_cards += [self]