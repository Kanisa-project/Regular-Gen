#Settings for Othaidho
import random
import os
import runes
import pygame as pg

TITLE = "`-,StF,-`"
WIDTH = 890
HEIGHT = 640
FPS = 30


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (146, 0, 0)
GREEN = (0, 146, 0)
BLUE = (0, 0, 146)
LIGHTRED = (255, 146, 146)
LIGHTGREEN = (146, 255, 146)
LIGHTBLUE = (146, 146, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
PURPLE = (255, 0, 255)
DARKGREY = (36, 36, 36)
LIGHTGREY = (146, 146, 146)
RANDOMCOLOR = (random.randint(0,256), random.randint(0,256), random.randint(0,256))
RANDOMCOLOR2 = (random.randint(0,256), random.randint(0,256), random.randint(0,256))

COLORLIST = [WHITE,BLACK,RED,GREEN,BLUE,LIGHTRED,LIGHTGREEN,LIGHTBLUE,YELLOW,CYAN,PURPLE,DARKGREY,LIGHTGREY,RANDOMCOLOR,RANDOMCOLOR2]

#Setup asset folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")
snd_folder = os.path.join(game_folder, "snd")


fontname = pg.font.match_font('arial')

rune_dict = {}
rune_dict["Freya"] = []
rune_dict["Hagal"] = []
rune_dict["Tyr"] = []
rune_dict["Freya"].append([runes.fehurune,runes.uruzrune,runes.thurisazrune,runes.ansuzrune,runes.raidhorune,runes.kenazrune,runes.geborune,runes.wunjorune])
rune_dict["Hagal"].append([runes.hagalazrune,runes.nauthizrune,runes.isarune,runes.jerarune,runes.eihwazrune,runes.perthrorune,runes.elhazrune,runes.sowilorune])
rune_dict["Tyr"].append([runes.tiwazrune,runes.berkanorune,runes.ehwazrune,runes.mannazrune,runes.laguzrune,runes.ingwazrune,runes.othalarune,runes.dagazrune])