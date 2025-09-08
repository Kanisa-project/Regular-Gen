#RUNE BRIDGE/MEMORY GAME
import math
import os

import pygame as pg
import random
from gaims import settings as s
from gaims.CandySlinger import candy_slinger
from gaims.Othaido import sprites as spirites

INSTRUCTIONS = {'objective': 'A game of memory and matching with the Elder Futhark runes.',
                'controls': 'Each tile will flip over and reveal some information about the revealed rune.',
                'scoring': 'The quicker you match with the fewer the flips, the more points you get.'}


class StartScreen:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
        pg.display.set_caption("Othaido")
        self.clock = pg.time.Clock()

        self.mouse_pos = (0, 0)
        self.vsrune = None
        self.rune_image_small = None
        self.rune_image = None
        self.select_aett_three = None
        self.second_aett = None
        self.sa = None
        self.fa = None
        self.select_aett_two = None
        self.select_aett_one = None
        self.findtotal = None
        self.a = 0
        self.p = 0
        self.q = 0
        self.rune_chart_list = None
        self.double_runelist = None
        self.chosen_aett = None
        self.the_aetts = ["Freya", "Hagal", "Tyr"]

    def oneMode(self):
        self.chosen_aett = random.choice(self.the_aetts)
        self.double_runelist = []
        self.rune_chart_list = []
        for item in s.rune_dict[self.chosen_aett]:
            self.double_runelist += item
            self.double_runelist += item
            self.rune_chart_list += item
        print(self.chosen_aett)
        self.p = 4
        self.q = 4
        self.a = 45
        random.shuffle(self.rune_chart_list)
        self.findtotal = 8
        pg.display.set_caption(self.chosen_aett)

    def twoMode(self):
        self.fa = random.randint(0, len(self.the_aetts) - 1)
        self.sa = random.randint(0, len(self.the_aetts) - 1)
        while self.sa == self.fa:
            self.sa = random.randint(0, len(self.the_aetts) - 1)
        self.chosen_aett = self.the_aetts[self.fa]
        self.second_aett = self.the_aetts[self.sa]
        self.double_runelist = []
        self.rune_chart_list = []
        for item in s.rune_dict[self.chosen_aett]:
            self.double_runelist += item
            self.double_runelist += item
            self.rune_chart_list += item
        for item in s.rune_dict[self.second_aett]:
            self.double_runelist += item
            self.double_runelist += item
            self.rune_chart_list += item
        print("self.chosen_aett")
        print("self.second_aett")
        self.p = 4
        self.q = 8
        self.a = 22.5
        random.shuffle(self.rune_chart_list)
        self.findtotal = 16
        pg.display.set_caption(str(self.chosen_aett) + " " + str(self.second_aett))

    def threeMode(self):
        self.double_runelist = []
        self.rune_chart_list = []
        for i in range(0, 3):
            self.chosen_aett = self.the_aetts[i]
            for item in s.rune_dict[self.chosen_aett]:
                self.double_runelist += item
                self.double_runelist += item
                self.rune_chart_list += item
        self.p = 6
        self.q = 8
        self.a = 15
        random.shuffle(self.rune_chart_list)
        self.findtotal = 24
        pg.display.set_caption("Alldem")

    def start_screen(self):
        self.screen.fill(s.BLACK)
        for y in [0, s.SCREEN_HEIGHT - 32]:
            for x in [0, 0]:
                for rune in runes.rune_list:
                    x += 32
                    self.rune_image = rune.elder_form
                    self.rune_image.set_colorkey(s.WHITE)
                    self.rune_image_small = pg.transform.scale(self.rune_image, (32, 32))
                    self.screen.blit(self.rune_image_small, (x, y))
        self.vsrune = pg.image.load(os.path.join(s.img_folder, "vansack.png"))
        self.vsrune.set_colorkey(s.WHITE)
        self.screen.blit(self.vsrune, (22, s.SCREEN_HEIGHT / 2))
        spirites.draw_text(self.screen, "OTHAIDHO", s.WHITE, 64, s.SCREEN_WIDTH / 2, s.SCREEN_HEIGHT / 4)
        spirites.draw_text(self.screen, "Match the runes to their copies", s.WHITE, 22, s.SCREEN_WIDTH / 2,
                           (s.SCREEN_HEIGHT / 2) - 50)
        self.select_aett_one = spirites.select_aett_sprite(self.screen, -90, "oneaett.png")
        self.select_aett_two = spirites.select_aett_sprite(self.screen, 0, "twoaett.png")
        self.select_aett_three = spirites.select_aett_sprite(self.screen, 90, "threeaett.png")
        spirites.draw_text(self.screen, "An \"Aett\" is a portion of a runic alphabet", s.WHITE, 16,
                           s.SCREEN_WIDTH * 4 / 5, 90)
        spirites.draw_text(self.screen, "in this case, an aett is 8 runes", s.WHITE, 16, s.SCREEN_WIDTH * 4 / 5, 110)
        spirites.draw_text(self.screen, "Press 1, 2, or 3 NOT on the keypad", s.WHITE, 16, s.SCREEN_WIDTH / 2,
                           s.SCREEN_HEIGHT * 3 / 4)
        spirites.draw_text(self.screen, "or click single, double, or triple above", s.WHITE, 16, s.SCREEN_WIDTH / 2,
                           (s.SCREEN_HEIGHT * 3 / 4) + 20)
        spirites.draw_text(self.screen, "to pick how many aetts to use", s.WHITE, 16, s.SCREEN_WIDTH / 2,
                           (s.SCREEN_HEIGHT * 3 / 4) + 40)
        pg.display.flip()
        waiting = True
        while waiting:
            self.clock.tick(s.FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.MOUSEMOTION:
                    #GET MOUSE POSITION
                    self.mouse_pos = pg.mouse.get_pos()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.select_aett_one.rect.collidepoint(self.mouse_pos):
                        self.oneMode()
                        waiting = False
                    if self.select_aett_two.rect.collidepoint(self.mouse_pos):
                        self.twoMode()
                        waiting = False
                    if self.select_aett_three.rect.collidepoint(self.mouse_pos):
                        self.threeMode()
                        waiting = False
                if event.type == pg.KEYUP:
                    if event.key == pg.K_1:
                        self.oneMode()
                        waiting = False
                    if event.key == pg.K_2:
                        self.twoMode()
                        waiting = False
                    if event.key == pg.K_3:
                        self.threeMode()
                        waiting = False

    def end_screen(self):
        self.screen.fill(s.WHITE)
        pg.draw.circle(self.screen, s.BLACK, int(int(s.SCREEN_WIDTH / 2), int(s.SCREEN_HEIGHT / 2)), 250, 2)
        for ang in range(0, 360):
            for ang, rune in enumerate(self.rune_chart_list):
                rx = 250 * math.sin(math.radians((ang * self.a))) + s.SCREEN_WIDTH // 2
                ry = 250 * math.cos(math.radians((ang * self.a))) + s.SCREEN_HEIGHT // 2
                self.rune_image = rune.elder_form
                self.rune_image.set_colorkey(s.WHITE)
                self.screen.blit(self.rune_image, (rx - 32, ry - 32))
                if rune in g.founded_list:
                    pg.draw.line(self.screen, s.RANDOM_COLORS[len(g.founded_list)],
                                 (s.SCREEN_WIDTH / 2, s.SCREEN_HEIGHT / 2), (rx, ry), 3)
        pg.display.flip()
        waiting = True
        while waiting:
            self.clock.tick(s.FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                if event.type == pg.KEYUP:
                    waiting = False


class Gaim(candy_slinger.BaseGaim):
    def __init__(self):
        super().__init__()
        self.selected_hexplate = []
        self.plusby = 0
        self.findtotal = 24
        self.founded_list = []
        self.select2_sound = None
        self.select1_sound = None
        self.foundedrunes_group = pg.sprite.Group()
        self.hexboard_group = pg.sprite.Group()
        self.hexboard = spirites.Hexboard(self)
        self.infobox = spirites.Infobox()
        self.timer = spirites.Timer()
        self.all_sprites.add(self.hexboard)
        self.all_sprites.add(self.infobox)
        self.all_sprites.add(self.timer)
        self.running = True
        pg.display.set_caption("Othaido")
        self.appropriate_sounds()
        self.aett_names = ["Freya", "Hagal", "Tyr"]

    def appropriate_sounds(self):
        pg.mixer.music.load(os.path.join('gaims/Othaido/assets', "MysticalTheme.mp3"))
        pg.mixer.music.set_volume(0.6)
        self.select1_sound = pg.mixer.Sound(os.path.join('gaims/Othaido/assets', "Blip_Select3.wav"))
        self.select1_sound.set_volume(0.5)
        self.select2_sound = pg.mixer.Sound(os.path.join('gaims/Othaido/assets', "Blip_Select5.wav"))
        self.select2_sound.set_volume(0.5)
        pg.mixer.music.play()

    def new(self, double_runelist, p, q):
        #create a new game
        self.selected_hexplate = []
        self.founded_list = []
        self.plusby = 0
        self.hexboard.create_grid(double_runelist, p, q)
        self.run()

    def run(self):
        #game loop
        # pg.mixer.music.play()
        while self.running:
            self.clock.tick(s.FPS)
            self.events()
            self.update()
            self.draw()
        pg.quit()

    def events(self):
        #game loop events
        for event in pg.event.get():
            #check for closing the window
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.MOUSEMOTION:
                #GET MOUSE POSITION
                self.mouse_pos = pg.mouse.get_pos()
            elif event.type == pg.MOUSEBUTTONDOWN:
                #====IF LEFT CLICK
                if event.button == 1:
                    if len(self.selected_hexplate) == 0:
                        self.select1_sound.play()
                        for item in self.hexboard.hexboard_list:
                            if item.rect.collidepoint(self.mouse_pos):
                                item.flipselected(self)
                    elif len(self.selected_hexplate) == 1:
                        self.select2_sound.play()
                        for item in self.hexboard.hexboard_list:
                            if item.rect.collidepoint(self.mouse_pos):
                                item.flipselected(self)
                    elif len(self.selected_hexplate) == 2:
                        if self.selected_hexplate[0].rune.germanic == self.selected_hexplate[1].rune.germanic and \
                                self.selected_hexplate[0].rune not in self.founded_list:
                            self.founded_list += [self.selected_hexplate[0].rune]
                            self.foundedrunes_group.add(self.selected_hexplate[0])
                            self.foundedrunes_group.add(self.selected_hexplate[1])
                            self.plusby = self.selected_hexplate[0].rune.numeric_value * 2
                            self.timer.score += self.plusby
                        elif len(self.selected_hexplate) <= 1:
                            pass
                        for item in self.hexboard.hexboard_list:
                            if item.rect.collidepoint(self.mouse_pos):
                                item.flipselected(self)
                if event.button == 9:
                    self.hexboard.update_mousepos()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                self.keystring = pg.key.name(event.key)
                if self.keystring == "e":
                    gss.end_screen()
                for item in self.hexboard.hexboard_list:
                    if self.keystring.upper() == item.rune.phonetic_value and item.rune.germanic not in self.founded_list:
                        self.founded_list += [item.rune]
                        self.foundedrunes_group.add(item)

    def update(self):
        #game loop update
        self.all_sprites.update(self)
        self.foundedrunes_group.update(self)
        self.hexboard_group.update(self)
        if len(self.selected_hexplate) >= 3:
            self.selected_hexplate = []
        if len(self.founded_list) == self.findtotal:
            self.filename = "jak.txt"
            self.savelist = []
            self.savelist += [str(self.timer.minutes) + "m" + str(self.timer.seconds) + "s"]
            self.savelist += [str(self.timer.score) + "points"]
            for item in self.founded_list:
                self.savelist += [item.germanic]
            with open(self.filename, "a") as f:
                f.write(str(self.savelist) + "\n")
                f.close()
            gss.end_screen()
            self.playing = False

    def draw(self):
        #game loop draw
        self.screen.fill(s.WHITE)
        self.all_sprites.draw(self.screen)
        self.foundedrunes_group.draw(self.screen)
        self.hexboard_group.draw(self.screen)
        #after drawing everything, flip the display
        pg.display.flip()


def launch_from_script():
    gss = StartScreen()
    g = Gaim()
    while g.running:
        gss.start_screen()
        g.playing = True
        g.founded_list = []
        while g.playing:
            g.new(gss.double_runelist, gss.p, gss.q)

    pg.quit()


if __name__ == "__main__":
    othaido = Game()
    othaido.run()
