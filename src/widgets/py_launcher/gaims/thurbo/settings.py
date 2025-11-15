#Settings for Thurbo
import random
import os
import pygame as pg

TITLE = "`-,StF,-`"
WIDTH = 960 #=25+5 tiles
HEIGHT = 480 #=10+5 tiles
FPS = 60
NUMBER_OF_MAPS = 6
NUMBER_OF_MAP_LINES = 20
NUMBER_OF_FLOORSPACES = 12
NUMBER_OF_WALLSPACES = 8


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (146, 0, 0)
GREEN = (0, 146, 0)
BLUE = (0, 0, 146)
BROWN = (90, 39, 41)
LIGHTRED = (255, 146, 146)
LIGHTGREEN = (146, 255, 146)
LIGHTBLUE = (146, 146, 255)
LIGHTBROWN = (185, 156, 107)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
PURPLE = (255, 0, 255)
DARKGREY = (36, 36, 36)
LIGHTGREY = (146, 146, 146)
RANDOMCOLOR = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
RANDOMCOLOR2 = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
RANDOMCOLOR3 = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
RANDOMRED = (random.randint(123,255), random.randint(0,156), random.randint(0,156))
RANDOMGREEN = (random.randint(0,156), random.randint(123,255), random.randint(0,156))
RANDOMBLUE = (random.randint(0,156), random.randint(0,156), random.randint(123,255))

COLORLIST = [WHITE,BLACK,RED,GREEN,BLUE,LIGHTRED,LIGHTGREEN,LIGHTBLUE,YELLOW,CYAN,PURPLE,DARKGREY,LIGHTGREY,RANDOMCOLOR,RANDOMCOLOR2,RANDOMCOLOR3,RANDOMRED,RANDOMGREEN,RANDOMBLUE]

#Setup asset folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")
rune_folder = os.path.join(img_folder, "runes")
items_folder = os.path.join(img_folder, "items")
professions_folder = os.path.join(game_folder, "professions")
knight_folder = os.path.join(professions_folder, "knight")
hunter_folder = os.path.join(professions_folder, "hunter")
mage_folder = os.path.join(professions_folder, "mage")
races_folder = os.path.join(game_folder, "races")
fairy_folder = os.path.join(races_folder, "fairy")
human_folder = os.path.join(races_folder, "human")
orc_folder = os.path.join(races_folder, "orc")


fontname = pg.font.match_font('arial')
TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE
BGCOLOR = BLACK