import pygame as pg
import random
import os
from gaims import settings as s
    
def draw_text(surf, text, color, size, x, y):
    font = pg.font.Font(pg.font.match_font('parkinsans'), size)
    text_surface = font.render(text,True,color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x,y)
    surf.blit(text_surface, text_rect)

class Hexplate(pg.sprite.Sprite):
    def __init__(self,radius,x,y,rune):
        pg.sprite.Sprite.__init__(self)
        self.rune = rune
        self.image = pg.image.load(os.path.join(s.img_folder, "hexplate.png")).convert()
        self.image.set_colorkey(s.LIGHT_GREY)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        
    def update(self,game):
        if self in game.selected_hexplate or self in game.foundedrunes_group:
            self.image = pg.image.load(os.path.join(s.img_folder, self.rune.germanic.lower() + ".png")).convert()
            self.image.set_colorkey(s.WHITE)
        else:
            self.image = pg.image.load(os.path.join(s.img_folder, "hexplate.png")).convert()
            self.image.set_colorkey(s.LIGHT_GREY)
            
    def flip_selected(self,game):
        if self in game.selected_hexplate:
            game.selected_hexplate.remove(self)
        elif self not in game.selected_hexplate:
            game.selected_hexplate += [self]
            
    def scatter_away(self):
        if random.random() >= 0.22:
            while self.rect.x < s.SCREEN_WIDTH:
                self.rect.x += 5
    
class Hexboard(pg.sprite.Sprite):
    def __init__(self,game):
        pg.sprite.Sprite.__init__(self)
        self.double_runelist = None
        self.mousepos_label = None
        self.image = pg.Surface((s.SCREEN_WIDTH-300,s.SCREEN_HEIGHT-100))
        self.image.fill(s.WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.game = game
        self.hexboard_list = []
        self.hx = 64
        self.hy = 64
        
    def update_mousepos(self):
        self.image.fill(s.WHITE)
        self.mousepos_label = str(self.game.mouse_pos)
        draw_text(self.image,self.mousepos_label, s.CYAN,25,s.SCREEN_WIDTH-350,s.SCREEN_HEIGHT-125)
        
    def update(self,game):
        pass
    
    def create_grid(self,double_runelist,p,q):
        self.double_runelist = double_runelist
        for i in range(0,p):
            self.hy = (i+1)*64
            for k in range(0,q):
                if k % 2 == 0:
                    self.hx = (k+1)*64
                    self.hy += 32
                else:
                    self.hx = (k+1)*64
                    self.hy -= 32
                self.rune_insert = random.choice(double_runelist)
                self.hexboard_list += [Hexplate(32,self.hx,self.hy,self.rune_insert)]
                self.game.all_sprites.add(self.hexboard_list)
                self.game.hexboard_group.add(self.hexboard_list)
                self.double_runelist.remove(self.rune_insert)
                
class Infobox(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.ty = None
        self.image = pg.Surface((s.SCREEN_WIDTH-300,s.SCREEN_HEIGHT))
        self.image.fill(s.BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = s.SCREEN_WIDTH - 300
        self.rect.y = 0
        
    def update(self,game):
        #====WHEN NO HEXPLATES ARE FLIPPED OVER
        if len(game.selected_hexplate) == 0:
            self.image.fill(s.BLACK)
        #====WHEN ONLY ONE HEXPLATE IS FLIPPED OVER DISPLAY THE BRIGHT KEYWORDS ON TOP
        elif len(game.selected_hexplate) == 1:
            draw_text(self.image,game.selected_hexplate[0].rune.germanic + "   " + str(game.selected_hexplate[0].rune.numeric_value), s.WHITE, 20, 150, 30)
            self.ty = 50
            for item in game.selected_hexplate[0].rune.bright_keywords:
                self.ty += 20
                draw_text(self.image,item,s.GREEN,15,150,self.ty)
        #====WHEN TWO HEXPLATES ARE FLIPPED OVER DISPLAY THE MURKY KEYWORDS ON BOTTOM
        elif len(game.selected_hexplate) == 2:
            draw_text(self.image,game.selected_hexplate[1].rune.germanic + "   " + str(game.selected_hexplate[1].rune.numeric_value), s.WHITE, 20, 150, 360)
            self.ty = 380
            for item in game.selected_hexplate[1].rune.murky_keywords:
                self.ty += 20
                draw_text(self.image,item, s.RED,15,150,self.ty)
            
class Timer(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.score_label = None
        self.timer_label = None
        self.image = pg.Surface((s.SCREEN_WIDTH-100,s.SCREEN_HEIGHT-100))
        self.image.fill(s.BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = s.SCREEN_HEIGHT - 100
        self.onesecond = 1000
        self.seconds = 0
        self.minutes = 0
        self.score = 0
        self.last_now = pg.time.get_ticks()
        
    def update(self,game):
        now = pg.time.get_ticks()
        if now - self.last_now >= self.onesecond:
            self.last_now = now
            self.image.fill(s.BLACK)
            self.seconds += 1
            if self.seconds >= 60:
                self.seconds = 0
                self.minutes += 1
        if self.seconds <= 9 and self.minutes <= 9:
            self.timer_label = "0" + str(self.minutes) + ":0" + str(self.seconds)
        elif self.minutes <= 9:
            self.timer_label = "0" + str(self.minutes) + ":" + str(self.seconds)
        self.score_label = str(self.score) + "   +" + str(game.plusby)
        draw_text(self.image,self.timer_label,s.WHITE,35,75,50)
        draw_text(self.image,self.score_label,s.WHITE,35,75,75)
        
        
class select_aett_sprite(pg.sprite.Sprite):
    def __init__(self,surf,x,aett_image):
        pg.sprite.Sprite.__init__(self)
        #self.image = pg.Surface((64,64))
        self.image = pg.image.load(os.path.join(s.img_folder, aett_image)).convert()
        self.image.set_colorkey(s.BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = (s.SCREEN_WIDTH // 2) + x
        self.rect.y = (s.SCREEN_HEIGHT // 2) + 15
        surf.blit(self.image,(self.rect.x,self.rect.y))
        
    def update(self,game):
        pass