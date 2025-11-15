from settings import *

class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.image.load(os.path.join(img_folder, "mob.png")).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.game = game
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.x = x
        self.y = y
        self.move_speed = 250
        self.attack_delay = 100
        self.last_move = pg.time.get_ticks()
        self.hp = 100
        self.struck = False
        
    def attack(self,player):
        if self.struck == False:
            player.hp -= 30
            self.struck = True
        
    def move(self,dx=0,dy=0):
        if not self.collide_with_walls(dx,dy) and not self.collide_with_player(dx,dy) and not self.collide_with_mobs(dx,dy):
            self.x += dx
            self.y += dy
        
    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False
        
    def collide_with_player(self, dx=0, dy=0):
        if self.game.player.x == self.x + dx and self.game.player.y == self.y + dy:
            return True
        return False
        
    def collide_with_mobs(self, dx=0, dy=0):
        for mob in self.game.mobs:
            if mob.x == self.x + dx and mob.y == self.y + dy:
                return True
        return False
        
    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
        now = pg.time.get_ticks()
        if now - self.last_move > self.move_speed:
            self.last_move = now
            self.move(dx=random.randint(-1,1),dy=random.randint(-1,1))
            
class Air_mob(Mob):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.image.load(os.path.join(img_folder, "air_mob.png")).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.game = game
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.x = x
        self.y = y
        self.move_speed = 250
        self.attack_delay = 100
        self.last_move = pg.time.get_ticks()
        self.hp = 100
        self.struck = False
        
    def attack(self,player):
        if self.struck == False:
            player.hp -= 30
            self.struck = True
        
    def move(self,dx=0,dy=0):
        if not self.collide_with_walls(dx,dy) and not self.collide_with_player(dx,dy) and not self.collide_with_mobs(dx,dy):
            self.x += dx
            self.y += dy
        
    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False
        
    def collide_with_player(self, dx=0, dy=0):
        if self.game.player.x == self.x + dx and self.game.player.y == self.y + dy:
            return True
        return False
        
    def collide_with_mobs(self, dx=0, dy=0):
        for mob in self.game.mobs:
            if mob.x == self.x + dx and mob.y == self.y + dy:
                return True
        return False
        
    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
        self.hp_BAR_LENGTH = 32
        BAR_HEIGHT = 4
        self.hp_fill = (self.hp*.01) * self.hp_BAR_LENGTH
        self.hp_fill_rect = pg.Rect(0,0,self.hp_fill,BAR_HEIGHT)
        pg.draw.rect(self.image,(self.hp*2,self.hp/2,self.hp/2),self.hp_fill_rect)
            
class Fire_mob(Mob):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.image.load(os.path.join(img_folder, "fire_mob.png")).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.game = game
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.x = x
        self.y = y
        self.move_speed = 250
        self.attack_delay = 100
        self.last_move = pg.time.get_ticks()
        self.hp = 100
        self.struck = False
        pass
        
    def attack(self,player):
        if self.struck == False:
            player.hp -= 30
            self.struck = True
        
    def move(self,dx=0,dy=0):
        if not self.collide_with_walls(dx,dy) and not self.collide_with_player(dx,dy) and not self.collide_with_mobs(dx,dy):
            self.x += dx
            self.y += dy
        
    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False
        
    def collide_with_player(self, dx=0, dy=0):
        if self.game.player.x == self.x + dx and self.game.player.y == self.y + dy:
            return True
        return False
        
    def collide_with_mobs(self, dx=0, dy=0):
        for mob in self.game.mobs:
            if mob.x == self.x + dx and mob.y == self.y + dy:
                return True
        return False
        
    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
        self.hp_BAR_LENGTH = 32
        BAR_HEIGHT = 4
        self.hp_fill = (self.hp*.01) * self.hp_BAR_LENGTH
        self.hp_fill_rect = pg.Rect(0,0,self.hp_fill,BAR_HEIGHT)
        pg.draw.rect(self.image,(self.hp*2,self.hp/2,self.hp/2),self.hp_fill_rect)
            
class Water_mob(Mob):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.image.load(os.path.join(img_folder, "water_mob.png")).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.game = game
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.x = x
        self.y = y
        self.move_speed = 250
        self.attack_delay = 100
        self.last_move = pg.time.get_ticks()
        self.hp = 100
        self.struck = False
        pass
        
    def attack(self,player):
        if self.struck == False:
            player.hp -= 30
            self.struck = True
        
    def move(self,dx=0,dy=0):
        if not self.collide_with_walls(dx,dy) and not self.collide_with_player(dx,dy) and not self.collide_with_mobs(dx,dy):
            self.x += dx
            self.y += dy
        
    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False
        
    def collide_with_player(self, dx=0, dy=0):
        if self.game.player.x == self.x + dx and self.game.player.y == self.y + dy:
            return True
        return False
        
    def collide_with_mobs(self, dx=0, dy=0):
        for mob in self.game.mobs:
            if mob.x == self.x + dx and mob.y == self.y + dy:
                return True
        return False
        
    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
        self.hp_BAR_LENGTH = 32
        BAR_HEIGHT = 4
        self.hp_fill = (self.hp*.01) * self.hp_BAR_LENGTH
        self.hp_fill_rect = pg.Rect(0,0,self.hp_fill,BAR_HEIGHT)
        pg.draw.rect(self.image,(self.hp*2,self.hp/2,self.hp/2),self.hp_fill_rect)
    
class Earth_mob(Mob):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.image.load(os.path.join(img_folder, "earth_mob.png")).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.game = game
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.x = x
        self.y = y
        self.move_speed = 250
        self.attack_delay = 100
        self.last_move = pg.time.get_ticks()
        self.hp = 100
        self.struck = False
        pass
        
    def attack(self,player):
        if self.struck == False:
            player.hp -= 30
            self.struck = True
        
    def move(self,dx=0,dy=0):
        if not self.collide_with_walls(dx,dy) and not self.collide_with_player(dx,dy) and not self.collide_with_mobs(dx,dy):
            self.x += dx
            self.y += dy
        
    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False
        
    def collide_with_player(self, dx=0, dy=0):
        if self.game.player.x == self.x + dx and self.game.player.y == self.y + dy:
            return True
        return False
        
    def collide_with_mobs(self, dx=0, dy=0):
        for mob in self.game.mobs:
            if mob.x == self.x + dx and mob.y == self.y + dy:
                return True
        return False
        
    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
        self.hp_BAR_LENGTH = 32
        BAR_HEIGHT = 4
        self.hp_fill = (self.hp*.01) * self.hp_BAR_LENGTH
        self.hp_fill_rect = pg.Rect(0,0,self.hp_fill,BAR_HEIGHT)
        pg.draw.rect(self.image,(self.hp*2,self.hp/2,self.hp/2),self.hp_fill_rect)