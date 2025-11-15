import pygame as pg
import os
from settings import *
from mobs import *

class mobSpawner(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites,game.mobspawners
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.image.load(os.path.join(img_folder, "mobspawner.png")).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.game = game
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.x = x
        self.y = y
        self.spawn_speed = 2000
        self.last_spawn = pg.time.get_ticks()
        self.spawn_spot = (x,y)
        self.hp = 222
        
    def spawn(self, dx=0,dy=0):
        if not self.collide_with_walls(dx,dy) and not self.collide_with_mobs(dx,dy):
            m = Mob(self.game,self.spawn_spot[0]+dx,self.spawn_spot[1]+dy)
        
    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_spawn > self.spawn_speed:
            self.last_spawn = now
            self.spawn(dx=random.randint(-1,1),dy=random.randint(-1,1))
        
    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False
        
class Air_mobSpawner(mobSpawner):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites,game.mobspawners
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.image.load(os.path.join(img_folder, "air_spawner.png")).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.game = game
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.x = x
        self.y = y
        self.spawn_speed = random.randint(1,4)*1000
        #self.spawn_speed = 2000
        self.last_spawn = pg.time.get_ticks()
        self.spawn_spot = (x,y)
        self.hp = 222
        
    def spawn(self, dx=0,dy=0):
        if not self.collide_with_walls(dx,dy) and not self.collide_with_mobs(dx,dy):
            m = Air_mob(self.game,self.spawn_spot[0]+dx,self.spawn_spot[1]+dy)
        
    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_spawn > self.spawn_speed:
            self.last_spawn = now
            self.spawn(dx=random.randint(-1,1),dy=random.randint(-1,1))
        
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
            
class Fire_mobSpawner(mobSpawner):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites,game.mobspawners
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.image.load(os.path.join(img_folder, "fire_spawner.png")).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.game = game
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.x = x
        self.y = y
        self.spawn_speed = random.randint(1,4)*1000
        #self.spawn_speed = 2000
        self.last_spawn = pg.time.get_ticks()
        self.spawn_spot = (x,y)
        self.hp = 222
        
    def spawn(self, dx=0,dy=0):
        if not self.collide_with_walls(dx,dy) and not self.collide_with_mobs(dx,dy):
            m = Fire_mob(self.game,self.spawn_spot[0]+dx,self.spawn_spot[1]+dy)
        
    def update(self):
        #self.image.fill((0,0,self.hp*2))
        now = pg.time.get_ticks()
        if now - self.last_spawn > self.spawn_speed:
            self.last_spawn = now
            self.spawn(dx=random.randint(-1,1),dy=random.randint(-1,1))
        
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
        
class Water_mobSpawner(mobSpawner):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites,game.mobspawners
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.image.load(os.path.join(img_folder, "water_spawner.png")).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.game = game
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.x = x
        self.y = y
        self.spawn_speed = random.randint(1,4)*1000
        #self.spawn_speed = 2000
        self.last_spawn = pg.time.get_ticks()
        self.spawn_spot = (x,y)
        self.hp = 222
        
    def spawn(self, dx=0,dy=0):
        if not self.collide_with_walls(dx,dy) and not self.collide_with_mobs(dx,dy):
            m = Water_mob(self.game,self.spawn_spot[0]+dx,self.spawn_spot[1]+dy)
        
    def update(self):
        #self.image.fill((0,0,self.hp*2))
        now = pg.time.get_ticks()
        if now - self.last_spawn > self.spawn_speed:
            self.last_spawn = now
            self.spawn(dx=random.randint(-1,1),dy=random.randint(-1,1))
        
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
        
class Earth_mobSpawner(mobSpawner):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites,game.mobspawners
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.image.load(os.path.join(img_folder, "earth_spawner.png")).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.game = game
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.x = x
        self.y = y
        self.spawn_speed = random.randint(1,4)*1000
        #self.spawn_speed = 2000
        self.last_spawn = pg.time.get_ticks()
        self.spawn_spot = (x,y)
        self.hp = 222
        
    def spawn(self, dx=0,dy=0):
        if not self.collide_with_walls(dx,dy) and not self.collide_with_mobs(dx,dy):
            m = Earth_mob(self.game,self.spawn_spot[0]+dx,self.spawn_spot[1]+dy)
            print("newearth")
        
    def update(self):
        #self.image.fill((0,0,self.hp*2))
        now = pg.time.get_ticks()
        if now - self.last_spawn > self.spawn_speed:
            self.last_spawn = now
            self.spawn(dx=random.randint(-1,1),dy=random.randint(-1,1))
        
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