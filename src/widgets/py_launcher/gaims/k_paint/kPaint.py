#PAINT TYPE GAME
import random

from src.widgets.py_launcher.gaims.base_gaim.base_gaim import BaseGaim
from src.widgets.py_launcher.gaims.k_paint import sprites as spirites
import pygame as pg
from src.settings import themery as t, app_settings as s

import datetime

INSTRUCTIONS = {'objective': 'There will be goals to change the aspect of the brush.',
                     'controls': 'You will need to change the brush settings to match the goal for points.',
                     'scoring': 'The faster you attain the goal, the more points you get.'}

class Gaim(BaseGaim):
    def __init__(self, player_name):
        super().__init__(player_name)
        pg.display.set_caption('k_paint')
        self.canvas = spirites.Canvas()
        self.palette = spirites.ColorPalette()
        self.toolbox = spirites.ToolBox()
        self.brush = spirites.Brush()
        self.all_sprites.add(self.canvas)
        self.all_sprites.add(self.palette)
        self.all_sprites.add(self.toolbox)

    def run(self):
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
                #GET MOUSE POSITION AND SET THE BRUSH POSITION TO MOUSE POSITION
                self.mouse_pos = pg.mouse.get_pos()
                self.brush.brush_pos = self.mouse_pos
            elif event.type == pg.MOUSEBUTTONDOWN:
                #IF YOU CLICK ANYWHERE INSIDE OF THE CANVAS
                if self.canvas.rect.collidepoint(self.brush.brush_pos):
                    #====IF LEFT CLICK
                    if event.button == 1:
                        if self.brush.chosen_shape == "circle":
                            self.brush.circlebrush(self.canvas)
                        elif self.brush.chosen_shape == "line":
                            self.brush.linebrush(self.canvas)
                        elif self.brush.chosen_shape == "polygon":
                            self.brush.polybrush(self.canvas)
                        elif self.brush.chosen_shape == "circleFoL":
                            self.brush.circle_fol_brush(self.canvas)
                        elif self.brush.chosen_shape == "polyFoL":
                            self.brush.polyFoLbrush(self.canvas)
                        elif self.brush.chosen_shape == "box":
                            self.brush.boxbrush(self.canvas)
                    #====IF MIDDLE CLICK
                    elif event.button == 2:
                        now = datetime.datetime.now()
                        name_string = f'{now.year}{now.month}{now.day}-{now.hour}{now.minute}{now.second}.png'
                        self.canvas.save(f'{name_string}')
                        print("Saved as: gaims/k_paint/img/" + name_string)
                    #====IF RIGHT CLICK
                    elif event.button == 3:
                        pass
                    #====IF SCROLL UP
                    elif event.button == 4:
                        self.brush.radius += 1
                    #====IF SCROLL DOWN
                    elif event.button == 5:
                        if self.brush.radius > 10:
                            self.brush.radius -= 1
                    #====IF SIDE BACK BUTTON
                    elif event.button == 8:
                        if self.brush.sides > 2:
                            self.brush.sides -= 1
                    elif event.button == 9:
                        #====IF SIDE FRONT BUTTON
                        self.brush.sides += 1

                #IF YOU CLICK ANYWHERE INSIDE OF THE COLOR PALETTE RECT
                if self.palette.rect.collidepoint(self.brush.brush_pos):
                    #====IF LEFT CLICK
                    if event.button == 1:
                        for i in range(0, len(self.palette.color_palist)):
                            if self.palette.color_palist[i].rect.collidepoint(self.mouse_pos):
                                self.palette.color_palist[i].selectcolor(self.brush)
                            elif self.palette.random_palist[i].rect.collidepoint(self.mouse_pos):
                                self.palette.random_palist[i].selectcolor(self.brush)
                    #====IF MIDDLE CLICK
                    elif event.button == 2:
                        for i in range(0, len(self.palette.color_palist)):
                            if self.palette.color_palist[i].rect.collidepoint(self.mouse_pos):
                                self.canvas.image.fill(self.palette.color_palist[i].color)
                            elif self.palette.random_palist[i].rect.collidepoint(self.mouse_pos):
                                self.canvas.image.fill(self.palette.random_palist[i].color)
                    #====IF RIGHT CLICK
                    elif event.button == 3:
                        for item in self.palette.random_palist:
                            if item.rect.collidepoint(self.brush.brush_pos):
                                item.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                                item.image.fill(item.color)
                                self.brush.chosen_color = item.color

                #IF YOU CLICK ANYWHERE INSIDE OF TOOLBOX RECT
                elif self.toolbox.rect.collidepoint(self.brush.brush_pos):
                    #====IF LEFT CLICK
                    if event.button == 1:
                        for item in self.toolbox.toolbox_list:
                            if item.rect.collidepoint(self.mouse_pos):
                                item.selectshape(self.brush, self.canvas)

                    if event.button == 3:
                        if self.toolbox.toolbox_list[1].rect.collidepoint(self.mouse_pos):
                            self.canvas.pointlist = [(0, 0), (0, 0), (0, 0)]

            elif event.type == pg.KEYDOWN:
                #IF A KEY IS PRESSED
                # self.keystring = pg.key.name(event.key)
                # for item in runes.rune_list:
                #     if item.phonetic_value == self.keystring.upper():
                #         self.canvas.keystroke(item.germanic)
                #         self.label = self.canvas.myfont.render(item.germanic)
                #         self.canvas.blit(self.label,(random.randint(200,500),random.randint(200,500)))
                if event.key == pg.K_UP:
                    self.brush.sides += 1
                if event.key == pg.K_DOWN and self.brush.sides >= 2:
                    self.brush.sides -= 1
                #if event.key == pg.K_RIGHT:
                #self.brush.thickness += 1
                #if event.key == pg.K_LEFT and self.brush.thickness >= 2:
                #self.brush.thickness -= 1

    def update(self):
        #game loop update
        self.all_sprites.update(self.mouse_pos[0], self.mouse_pos[1], self.brush)
        self.palette.color_group.update()
        self.toolbox.tool_group.update(self.brush)
        self.brush.update(self.mouse_pos[0], self.mouse_pos[1])

    def draw(self):
        #game loop draw
        self.screen.fill(t.WHITE)
        self.all_sprites.draw(self.screen)
        self.palette.color_group.draw(self.screen)
        self.toolbox.tool_group.draw(self.screen)
        #after drawing everying, flip the display
        pg.display.flip()

if __name__ == "__main__":
    gss = Gaim("Bluebeard")
    gss.run()