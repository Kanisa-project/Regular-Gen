#PAINT TYPE GAME
import random

from src.utils.helpers import clamp
from src.widgets.py_launcher.gaims.base_gaim.base_gaim import BaseGaim
# from src.widgets.py_launcher.gaims.k_paint import sprites as spirites
import pygame as pg
from src.settings import themery as t, app_settings as s
from src.widgets.py_launcher.gaims.k_paint import brush, canvas, palette

import datetime

INSTRUCTIONS = {'objective': 'There will be goals to change the aspect of the brush.',
                     'controls': 'You will need to change the brush settings to match the goal for points.',
                     'scoring': 'The faster you attain the goal, the more points you get.'}

DEFAULT_RULE_DICT = {
    'Q': 'thickness +1',
    'A': f'thickness {random.randint(-3, 3)}',
    'Z': 'thickness -1',
    'W': 'num_sides +1',
    'S': f'num_sides {random.randint(-2, 2)}',
    'X': 'num_sides -1',
    'E': 'radius +7',
    'D': f'radius {random.randint(-7, 7)}',
    'C': 'radius -7',
    'R': 'rot_offset +12',
    'F': f'rot_offset {random.randint(-12, 12)}',
    'V': 'rot_offset -12',
    'T': '',
    'G': '',
    'B': '',
    'Y': '',
    'H': '',
    'N': '',
    'U': '',
    'J': '',
    'M': '',
    'I': 'PRECISION',
    'O': 'POLYGON',
    'P': 'FLOWER',
    'K': 'WILD',
    'L': '',
    '0': '',
    '1': '',
    '2': '',
    '3': '',
    '4': '',
    '5': '',
    '6': '',
    '7': '',
    '8': '',
    '9': ''
}

class Gaim(BaseGaim):
    def __init__(self, player_name):
        super().__init__(player_name)
        self.canvas = canvas.Canvas()
        self.palette = palette.ColorPalette()
        self.brush = brush.Brush()
        self.all_sprites.add(self.canvas)
        self.all_sprites.add(self.palette)

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
                if self.canvas.rect.collidepoint(self.mouse_pos):
                    #====IF LEFT CLICK canvas
                    if event.button == 1:
                        if self.brush.isPolygon:
                            self.brush.polybrush(self.canvas)
                        else:
                            self.brush.circlebrush(self.canvas)
                    #====IF MIDDLE CLICK canvas
                    elif event.button == 2:
                        now = datetime.datetime.now()
                        name_string = f'{now.year}{now.month}{now.day}-{now.hour}{now.minute}{now.second}.png'
                        self.canvas.save_paint(f'filesOutput/Bluebeard/kPaint/{name_string}')
                        print(f"Saved as: {name_string}")
                    #====IF RIGHT CLICK canvas
                    elif event.button == 3:
                        pass

                #IF YOU CLICK ANYWHERE INSIDE OF THE COLOR PALETTE RECT
                if self.palette.rect.collidepoint(self.mouse_pos):
                    #====IF LEFT CLICK
                    if event.button == 1:
                        for i in range(0, len(self.palette.color_palette_list)):
                            if self.palette.color_palette_list[i].rect.collidepoint(self.mouse_pos):
                                self.palette.color_palette_list[i].selectcolor(self.brush, self.mouse_pos)
                    #====IF MIDDLE CLICK
                    elif event.button == 2:
                        for i in range(0, len(self.palette.color_palette_list)):
                            if self.palette.color_palette_list[i].rect.collidepoint(self.mouse_pos):
                                self.canvas.image.fill(self.palette.color_palette_list[i].color)
                    #====IF RIGHT CLICK
                    elif event.button == 3:
                        for item in self.palette.color_palette_list:
                            if item.rect.collidepoint(self.brush.brush_pos):
                                item.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                                item.image.fill(item.color)
                                self.brush.chosen_color = item.color

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
                elif event.key == pg.K_UP:
                    self.brush.y_offset = clamp(self.brush.y_offset-1,
                                                -22, 22, True)
                elif event.key == pg.K_DOWN:
                    self.brush.y_offset = clamp(self.brush.y_offset+1,
                                                -22, 22, True)
                elif event.key == pg.K_LEFT:
                    self.brush.x_offset = clamp(self.brush.x_offset-1,
                                                -22, 22, True)
                elif event.key == pg.K_RIGHT:
                    self.brush.x_offset = clamp(self.brush.x_offset+1,
                                                -22, 22, True)
                #IF A KEY IS PRESSED
                keystring = pg.key.name(event.key)
                try:
                    ruling = DEFAULT_RULE_DICT[keystring.upper()].split()
                    if "thickness" in ruling:
                        self.brush.thickness = clamp(self.brush.thickness + int(ruling[1]),
                                                     0, 32, True)
                    elif "radius" in ruling:
                        self.brush.radius = clamp(self.brush.radius + int(ruling[1]),
                                                     0, 142, True)
                    elif "num_sides" in ruling:
                        self.brush.sides = clamp(self.brush.sides + int(ruling[1]),
                                                 3, 10, True)
                    elif "rot_offset" in ruling:
                        self.brush.polygon_offset = clamp(self.brush.polygon_offset + int(ruling[1]),
                                                 0, 360, True)
                    elif "PRECISION" in ruling:
                        self.brush.isPrecise = not self.brush.isPrecise
                    elif "WILD" in ruling:
                        self.brush.isWild = not self.brush.isWild
                    elif "POLYGON" in ruling:
                        self.brush.isPolygon = not self.brush.isPolygon
                    elif "FLOWER" in ruling:
                        self.brush.isFoL = not self.brush.isFoL
                except Exception as e:
                    print(e)
                self.palette.brush_info(self.brush)

    def update(self):
        #game loop update
        self.all_sprites.update(self.mouse_pos[0], self.mouse_pos[1], self.brush)
        self.palette.color_group.update()
        self.brush.update(self.mouse_pos[0], self.mouse_pos[1])

    def draw(self):
        #game loop draw
        self.screen.fill(t.WHITE)
        self.all_sprites.draw(self.screen)
        self.palette.color_group.draw(self.screen)
        #after drawing everying, flip the display
        pg.display.flip()

if __name__ == "__main__":
    gss = Gaim("Bluebeard")
    gss.run()