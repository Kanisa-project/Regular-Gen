#ThurBo part of Othaidho
import pygame as pg
import random
import os
from settings import *
from sprites import *
from player import *
from knight import *
from hunter import *
from items import *
from runes import *
from mage import *

class SceneBase:
    def __init__(self):
        self.next = self

    def ProcessInput(self,events,pressed_keys):
        print("uhhhhh, change the process input child function")

    def Update(self):
        print("change the update of child")

    def Render(self):
        print("you didnt change the render of child class")

    def SwitchToScene(self, next_scene):
        self.next = next_scene

    def terminate(self):
        self.SwitchToScene(None)

class race_screen():
    def __init__(self,cms):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.screen.fill(RANDOMRED)
        self.clock = pg.time.Clock()
        self.mouse_pos = (0,0)
        self.fairy_button = select_race_sprite(screen,0,0,"fairy.png")
        self.human_button = select_race_sprite(screen,0,64,"human.png")
        self.orc_button = select_race_sprite(screen,0,128,"orc.png")
        pg.display.flip()
        self.waiting = True
        self.run()
        
    def run(self):
        while self.waiting:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            
    def events(self):
        while self.waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.MOUSEMOTION:
                    ##GET MOUSE POSITION
                     self.mouse_pos = pg.mouse.get_pos()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.fairy_button.rect.collidepoint(self.mouse_pos):
                        cms.picked_race = "fairy"
                        self.waiting = False
                    if self.human_button.rect.collidepoint(self.mouse_pos):
                        cms.picked_race = "human"
                        self.waiting = False
                    if self.orc_button.rect.collidepoint(self.mouse_pos):
                        cms.picked_race = "orc"
                        self.waiting = False
    def update(self):
        pass
    
    def draw(self):
        pass
                        
class occupation_screen():
    def __init__(self,cms):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.screen.fill(RANDOMGREEN)
        self.mouse_pos = (0,0)
        self.knight_button = select_occupation_sprite(screen,-64,-5,"knight.png")
        self.hunter_button = select_occupation_sprite(screen,-64,64,"hunter.png")
        self.magician_button = select_occupation_sprite(screen,-64,133,"magician.png")
        self.alchemist_button = select_occupation_sprite(screen,64,-5,"alchemist.png")
        self.priest_button = select_occupation_sprite(screen,64,64,"priest.png")
        self.rogue_button = select_occupation_sprite(screen,64,133,"rogue.png")
        pg.display.flip()
        self.clock = pg.time.Clock()
        self.waiting = True
        self.run()
        
    def run(self):
        while self.waiting:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.MOUSEMOTION:
                ##GET MOUSE POSITION
                 self.mouse_pos = pg.mouse.get_pos()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.knight_button.rect.collidepoint(self.mouse_pos):
                    cms.picked_occupation = "knight"
                    self.waiting = False
                if self.hunter_button.rect.collidepoint(self.mouse_pos):
                    cms.picked_occupation = "hunter"
                    self.waiting = False
                if self.magician_button.rect.collidepoint(self.mouse_pos):
                    cms.picked_occupation = "mage"
                    self.waiting = False
                    
    def update(self):
        pass
    
    def draw(self):
        pass
                        
class rune_screen():
    def __init__(self,cms):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.mouse_pos = (0,0)
        self.screen.fill(RANDOMBLUE)
        self.player_settings = []
        self.carved_runes = []
        self.rune_list = rune_list
        self.card_list = []
        self.faceup_cards = []
        self.selected_cards = []
        self.all_sprites = pg.sprite.Group()
        self.accept_button = start_screen_buttons(self,self.screen,0,"accept.png")
        card_x = 0
        card_y = 0
        num_of_cards = 0
        self.waiting = True
        for i in range(0,8):
            card_x = (i+1) * 64
            for k in range(0,3):
                card_y = (k+1) * 64
                self.rune_insert = random.choice(self.rune_list)
                self.card_list += [RuneCard(self,screen,card_x,card_y,self.rune_insert)]
                self.rune_list.remove(self.rune_insert)
        pg.display.flip()
        self.run()
        
    def run(self):
        while self.waiting: 
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.MOUSEMOTION:
                ##GET MOUSE POSITION
                 self.mouse_pos = pg.mouse.get_pos()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                for card in self.card_list:
                    if card.rect.collidepoint(self.mouse_pos) and not card.isFaceup:
                        card.flipCard(self)
                    if card.rect.collidepoint(self.mouse_pos) and card.isFaceup:
                        card.isSelected = not card.isSelected
                if self.accept_button.rect.collidepoint(self.mouse_pos):
                    for card in self.faceup_cards:
                        if card.isSelected:
                            cms.carved_runes += [card]
                    cms.player_settings = [cms.picked_race,cms.picked_occupation,cms.carved_runes,cms.vfdscore]
                    self.waiting = False
                        
    def update(self):
        self.all_sprites.update()
            
    def draw(self):
        #game loop draw
        self.screen.fill(RANDOMBLUE)
        self.all_sprites.draw(self.screen)
        for card in self.faceup_cards:
            if card.isSelected:
                draw_text(self.screen, str(card.rune.vfdscore), 16, 0, 320,BLACK)
        #after drawing everything, flip the display
        pg.display.flip()
        
class character_maker_screen():
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Stuff.")
        self.all_sprites = pg.sprite.Group()
        self.clock = pg.time.Clock()
        self.picked_race = ""
        self.picked_occupation = ""
        self.vfdscore = [0,0,0]
        self.player_settings = []
        self.rune_list = rune_list
        self.card_list = []
        self.faceup_cards = []
        self.carved_runes = []
        
    def update(self):
        self.all_sprites.update()
        
    def race_screen(self,screen):
        rs = race_screen(self)
                        
    def occupation_screen(self,screen):
        os = occupation_screen(self)
        
    def rune_screen(self,screen):
        rus = rune_screen(self)
                                
class game_start_screen():
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Stuff.")
        self.clock = pg.time.Clock()
        self.all_sprites = pg.sprite.Group()
        
    def start_screen(self):
        self.screen.fill(BLACK)
        self.vsrune = pg.image.load(os.path.join(rune_folder,"vansack.png"))
        self.vsrune.set_colorkey(WHITE)
        self.screen.blit(self.vsrune,(22,HEIGHT/2))
        draw_text(self.screen, "ThurBo", 64, WIDTH / 2, HEIGHT / 4, RANDOMCOLOR)
        self.newGameButton = start_screen_buttons(self,self.screen, -32, "new_game.png")
        self.loadGameButton = start_screen_buttons(self,self.screen, 0, "load_game.png")
        self.settingsButton = start_screen_buttons(self,self.screen, 32, "settings.png")
        self.exitGameButton = start_screen_buttons(self,self.screen, 64, "exit.png")
        pg.display.flip()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.MOUSEMOTION:
                    ##GET MOUSE POSITION
                     self.mouse_pos = pg.mouse.get_pos()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.newGameButton.rect.collidepoint(self.mouse_pos):
                        return True
                    if self.loadGameButton.rect.collidepoint(self.mouse_pos):
                        return False
                if event.type == pg.KEYUP:
                    pass
        
class Game():
    def __init__(self,go):
        #initialize game window
        self.running = True
        self.playing = True
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.mouse_pos = (0,0)
        self.game_over = go
        self.new_floor = True
        pg.key.set_repeat(500,100)
        
    def load_start_map(self,mn):
        self.map_data = []
        for wall in self.walls:
            wall.kill()
        for spawner in self.mobspawners:
            spawner.kill()
        with open(os.path.join(game_folder, 'map' + str(mn) + '.txt'),'rt') as f:
            for line in f:
                self.map_data.append(line)
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == ".":
                    i = random.randint(0,100)
                    if i >= 0 and i < 10:
                        tile = "."
                    if i >= 10 and i < 20:
                        tile = "."
                    if i >= 20 and i < 30:
                        tile = "."
                    if i >= 30 and i < 40:
                        tile = "."
                    if i >= 40 and i < 50:
                        tile = "."
                    if i >= 50 and i < 60:
                        tile = "."
                    if i >= 60 and i < 70:
                        tile = "."
                    if i >= 70 and i < 80:
                        tile = "W"
                    if i >= 80 and i < 90:
                        tile = "t"
                    if i >= 90 and i < 100:
                        tile = "C"
                if tile == "W":
                    Wall(self,col,row,0)
                if tile == "P":
                    self.player.x = col
                    self.player.y = row
                if tile == "A":
                    Air_mobSpawner(self,col,row)
                if tile == "T":
                    Water_mobSpawner(self,col,row)
                if tile == "F":
                    Fire_mobSpawner(self,col,row)
                if tile == "E":
                    Earth_mobSpawner(self,col,row)
                if tile == "a":
                    Air_mob(self,col,row)
                if tile == "t":
                    Water_mob(self,col,row)
                if tile == "f":
                    Fire_mob(self,col,row)
                if tile == "e":
                    Earth_mob(self,col,row)
                if tile == "D":
                    Doorway(self,col,row)
                if tile == "C":
                    Chest(self,col,row)
                if tile == "b":
                    Bread(self,col,row)
        
    def new(self):
        #create a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.foods = pg.sprite.Group()
        self.drinks = pg.sprite.Group()
        self.flooring = pg.sprite.Group()
        self.doors = pg.sprite.Group()
        self.chests = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.mobspawners = pg.sprite.Group()
        self.itemlist = ["apple","bread","milk","water",]
        self.player = Player(self,cms.player_settings)
        if self.new_floor == True:
            for x in range(0,WIDTH-160,TILESIZE):
                for y in range(0,HEIGHT-160,TILESIZE):
                    Floor(self,x,y)
                    self.new_floor = False
        self.map_number = 0
        self.load_start_map(self.map_number)
        self.run()
        
    def run(self):
        #game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            
    def events(self):
        #game loop events
        for event in pg.event.get():
            #check for closing the window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.MOUSEMOTION:
                self.mouse_pos = pg.mouse.get_pos()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for item in self.items:
                        if item.rect.collidepoint((self.mouse_pos)):
                            item.use(self.player)
                    for wall in self.walls:
                        if wall.rect.collidepoint((self.mouse_pos)) and self.player.num_of_walls <= 2 and self.player.coinbag >= 100:
                            self.player.coinbag -= 100
                            self.player.num_of_walls += 1
                            wall.kill()
                    for chest in self.chests:
                        if chest.rect.collidepoint((self.mouse_pos)):
                            if self.player.num_of_walls >= 1 and self.player.coinbag >= 50:
                                self.player.coinbag -= 50
                                Wall(self,chest.x,chest.y)
                                self.player.num_of_walls -= 1   
                pass
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                if event.key == pg.K_SPACE:
                    print("atk")
                    self.player.attack()
                if event.key == pg.K_LEFT:
                   for i in range(0,self.player.move_speed):
                        self.player.move(dx=-1)
                   self.player.facing = "LEFT"
                if event.key == pg.K_RIGHT:
                    for i in range(0,self.player.move_speed):
                        self.player.move(dx=1)
                    self.player.facing = "RIGHT"
                if event.key == pg.K_UP:
                    for i in range(0,self.player.move_speed):
                        self.player.move(dy=-1)
                    self.player.facing = "UP"
                if event.key == pg.K_DOWN:
                    for i in range(0,self.player.move_speed):
                        self.player.move(dy=1)
                    self.player.facing = "DOWN"
                        
    def update(self):
        #game loop update
        self.all_sprites.update()
        #check to see if a bullet hit a mob
        self.mobs_bullets = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in self.mobs_bullets:
            hit.hp -= self.mobs_bullets[hit][0].damage
            print(hit.hp)
            if hit.hp <= 0:
                hit.kill()
        #check to see if a bullet hit a mob spawner
        self.mobspawner_bullets = pg.sprite.groupcollide(self.mobspawners, self.bullets, False, True)
        for hit in self.mobspawner_bullets:
            hit.hp -= self.mobspawner_bullets[hit][0].damage
            if hit.hp <= 0:
                hit.kill()
        #check to see if a player entered a doorway
        #self.doorway_player = pg.sprite.spritecollide(self.player, self.doors, False)
        if self.player.collide_with_doors() == True or self.player.collide_with_doors(dy=-1) == True:
            if self.map_number <= NUMBER_OF_MAPS - 1:
                for mob in self.mobs:
                    mob.kill()
                for chest in self.chests:
                    chest.kill()
                self.next_map()
        #check to see if a mob hit a player
        self.player_mobs = pg.sprite.spritecollide(self.player, self.mobs, False)
        for hit in self.player_mobs:
            if hit.struck == False:
                hit.attack(self.player)
            if self.player.hp <= 0:
                self.player.kill()
                
        #check to see if a player opened a chest
        self.player_chest = pg.sprite.spritecollide(self.player,self.chests,False)
        for chest in self.player_chest:
            if not chest.opened:
                chest.open_chest(self.player)
                chest.kill()
            
    def draw_hud(self,player):
    #draw the health bar and fury, ammo, or mana bar depending on the base class
        self.hp_BAR_LENGTH = 100
        self.mp_BAR_LENGTH = 100
        self.fp_BAR_LENGTH = 100
        self.arrows_BAR_LENGTH = 100
        BAR_HEIGHT = 16
        self.hp_fill = ((player.hp/player.max_hp)) * self.hp_BAR_LENGTH
        hpoutline_rect = pg.Rect(60, 320,self.hp_BAR_LENGTH,BAR_HEIGHT)
        self.hp_fill_rect = pg.Rect(60, 320,self.hp_fill,BAR_HEIGHT)
        pg.draw.rect(self.screen,GREEN,self.hp_fill_rect)
        pg.draw.rect(self.screen,WHITE,hpoutline_rect,2)
        if player.ps[1] == "hunter":
            self.arrows_fill = (player.arrows*.1) * self.arrows_BAR_LENGTH
            aroutline_rect = pg.Rect(60, 336,self.arrows_BAR_LENGTH,BAR_HEIGHT)
            self.arrows_fill_rect = pg.Rect(60, 336,self.arrows_fill,BAR_HEIGHT)
            pg.draw.rect(self.screen,BROWN,self.arrows_fill_rect)
            pg.draw.rect(self.screen,WHITE,aroutline_rect,2)
            draw_text(self.screen, "Arrows: ", 16, 0, 336,LIGHTGREEN)
            draw_text(self.screen, str(player.arrows), 16, 64, 336,LIGHTGREEN)
        #====================================
        elif player.ps[1] == "mage":
            self.mp_fill = (player.mp*.01) * self.mp_BAR_LENGTH
            mpoutline_rect = pg.Rect(60, 336,self.mp_BAR_LENGTH,BAR_HEIGHT)
            self.mp_fill_rect = pg.Rect(60, 336,self.mp_fill,BAR_HEIGHT)
            pg.draw.rect(self.screen,BLUE,self.mp_fill_rect)
            pg.draw.rect(self.screen,WHITE,mpoutline_rect,2)
            draw_text(self.screen, "Mana: ", 16, 0, 336,LIGHTBLUE)
            draw_text(self.screen, str(player.mp) + "|" + str(player.max_mp), 16, 64, 336,LIGHTBLUE)
        #====================================
        draw_text(self.screen, "Health: ", 16, 0, 320,RANDOMCOLOR2)
        draw_text(self.screen, str(player.hp) + "|" + str(player.max_hp), 16, 64, 320,RANDOMCOLOR2)
        draw_text(self.screen, "Coins: " + str(player.coinbag), 16, 64, 352,RANDOMCOLOR2)
        draw_text(self.screen, "map number: " + str(self.map_number), 16, 64, 368,RANDOMCOLOR2)
        draw_text(self.screen, "number of walls: " + str(self.player.num_of_walls), 16, 64, 384,RANDOMCOLOR2)
        draw_text(self.screen, str(self.player.carried_weight) + "/" +str(self.player.weight_limit), 16, 64, 400,RANDOMCOLOR2)
        draw_text(self.screen, "physical power: " + str(self.player.phys_atk) + "|" + str(self.player.phys_def), 16, 716, 332,RANDOMCOLOR2)
        draw_text(self.screen, "magic power: " + str(self.player.magic_atk) + "|" + str(self.player.magic_def), 16, 716, 348,RANDOMCOLOR2)
        draw_text(self.screen, "move speed: " + str(self.player.move_speed), 16, 716, 364,RANDOMCOLOR2)
        
    def draw(self):
        #game loop draw
        self.screen.fill(BGCOLOR)
        self.flooring.draw(self.screen)
        self.draw_hud(self.player)
        self.all_sprites.draw(self.screen)
        #after drawing everything, flip the display
        pg.display.flip()
        
    def next_map(self):
        self.map_number += 1
        self.load_start_map(self.map_number)
        pass
        
    def past_map(self):
        self.map_number -= 1
        self.load_start_map(self.map_number)
        pass
        
    def clear_map(self):
        self.map_number = 0
        self.load_start_map(self.map_number)
        pass
        
        
gss = game_start_screen()
cms = character_maker_screen()
g = Game(True)
while g.running:
    player_choice = gss.start_screen()
    if player_choice == True:
        cms.race_screen(gss.screen)
        cms.occupation_screen(gss.screen)
        cms.rune_screen(gss.screen)
        print(cms.player_settings)
    if player_choice == False:
        print(gss.player_settings)
        cms.loader_screen()
    g.playing = True
    while g.playing:
        g.new()
    
pg.quit()
