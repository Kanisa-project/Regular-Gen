import random

from src.services.utils import polypointlist
from src.settings import themery as t
import pygame as pg

class Brush:
    def __init__(self):
        self.chosen_shape = "circle"
        self.chosen_color = t.WHITE
        self.polygon_pointlist = []

        self.polygon_offset = 0
        self.fol_layers = 0
        self.radius = 42
        self.sides = 6
        self.thickness = 1

        self.isPrecise = True
        self.isWild = True
        self.isFoL = False
        self.isPolygon = False

        self.box_pointlist = []
        self.pos = (0, 0)
        self.x_offset = 0
        self.y_offset = 0
        self.update_polypointlist()

    def update(self, x, y):
        self.pos = (x + self.x_offset,
                    y + self.y_offset)
        if self.isWild:
            self.chosen_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def update_polypointlist(self):
        self.polygon_pointlist = polypointlist(self.sides, self.polygon_offset, self.pos[0], self.pos[1], self.radius)

    def circlebrush(self, canvas):
        pg.draw.circle(canvas.image, self.chosen_color, self.pos, self.radius, self.thickness)
        if self.isFoL:
            self.update_polypointlist()
            for point in self.polygon_pointlist:
                pg.draw.circle(canvas.image, self.chosen_color, point, self.radius, self.thickness)


    def polybrush(self, canvas):
        pg.draw.polygon(canvas.image, self.chosen_color, self.polygon_pointlist, self.thickness)
        if self.isFoL:
            fol_layer_list = []
            for point in self.polygon_pointlist:
                fol_layer_list.append(polypointlist(self.sides, self.fol_layers, int(point[0]), int(point[1]), self.radius))
            for point in fol_layer_list:
                pg.draw.polygon(canvas.image, self.chosen_color, point, self.thickness)

    def circle_fol_brush(self, canvas):
        pg.draw.circle(canvas.image, self.chosen_color, self.pos, self.radius, 2)
        for point in self.polygon_pointlist:
            pg.draw.circle(canvas.image, self.chosen_color, (int(point[0]), int(point[1])), self.radius, 2)
            self.polygon_pointlist = polypointlist(self.sides, 0, int(point[0]), int(point[1]), self.radius)
            for point in self.polygon_pointlist:
                pg.draw.circle(canvas.image, self.chosen_color, (int(point[0]), int(point[1])), self.radius, 2)

    def poly_fol_brush(self, canvas):
        pg.draw.polygon(canvas.image, self.chosen_color, self.polygon_pointlist, 2)
        for point in self.polygon_pointlist:
            self.polygon2_pointlist = polypointlist(self.sides, 0, int(point[0]), int(point[1]), self.radius)
            pg.draw.polygon(canvas.image, self.chosen_color, self.polygon2_pointlist, 2)
            for point in self.polygon2_pointlist:
                self.polygon3_pointlist = polypointlist(self.sides, 0, int(point[0]), int(point[1]), self.radius)
                pg.draw.polygon(canvas.image, self.chosen_color, self.polygon3_pointlist, 2)

    # def boxbrush(self, canvas):
    #     if len(self.box_pointlist) == 0:
    #         self.box_pointlist += [self.pos]
    #     elif len(self.box_pointlist) == 1:
    #         self.box_pointlist += [(self.x - self.box_pointlist[0][0], self.y - self.box_pointlist[0][1])]
    #         pg.draw.rect(canvas.image, self.chosen_color, self.box_pointlist, self.sides)
    #         self.box_pointlist = []
