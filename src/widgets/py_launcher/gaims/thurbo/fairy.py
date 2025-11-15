import pygame as pg
import random
import os
from settings import *
from sprites import *
from items import *

class Fairy():
    def __init__(self, game, ps):
        self.game = game
        self.attack_delay = 100
        self.last_attack = pg.time.get_ticks()
        self.max_hp = 50
        self.coinbag = 100
        self.move_speed = 5
        self.facing = "RIGHT"
        self.walking = False
        self.ps = ps
        self.backpack = []
        self.weight_limit = 10 
        self.item_limit = 3