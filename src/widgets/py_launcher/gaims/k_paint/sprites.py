import random

import pygame as pg
import math

from src.domain.resource_loader import ensure_parent_dir
# from .. import settings as s
from src.settings import app_settings as s, themery as t


def nothing():
    pass
#MAIN PAINTING AREA
class Canvas(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((s.SCREEN_WIDTH-100,s.SCREEN_HEIGHT-100))
        self.rect = self.image.get_rect()
        self.pointlist = [(0,0),(0,0),(0,0)]
        self.myfont = pg.font.SysFont("monospace", 15)
        self.rx = 10
        self.ry = 10
        self.rl = 0
        
    def update(self,x,y,brush):
        if brush.precision:
            if brush.chosen_shape == "circle":
                pass
            elif brush.chosen_shape == "line":
                pg.draw.lines(self.image,brush.chosen_color,False,self.pointlist,brush.radius)
            elif brush.chosen_shape == "polygon":
                pass
        else:
            if brush.chosen_shape == "circle":
                pg.draw.circle(self.image,brush.chosen_color,(x,y),brush.radius,2)
            elif brush.chosen_shape == "line":
                pg.draw.lines(self.image,brush.chosen_color,False,self.pointlist,brush.radius)
            elif brush.chosen_shape == "polygon":
                self.polygon_pointlist = polypointlist(brush.sides,0,x,y,brush.radius)
                pg.draw.polygon(self.image,brush.chosen_color,self.polygon_pointlist,2)
        
    def save(self,name):
        pg.image.save(self.image, ensure_parent_dir(f'gaims/kPaint/kre8d/{name}'))
        
    def keystroke(self,txt):
        self.rx += 10
        self.ry += 10
        if self.ry >= s.SCREEN_HEIGHT:
            self.rl += 1
            self.rx = self.rl*22
            self.ry -= s.SCREEN_HEIGHT
        self.label = self.myfont.render(txt,1,(random.randint(0,250),random.randint(0,250),random.randint(0,250)))
        self.image.blit(self.label,(self.rx,self.ry))
        
#COLOR PICKER
class ColorPalette(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((s.SCREEN_WIDTH,100))
        self.image.fill(t.LIGHT_GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = s.SCREEN_HEIGHT - 100
        self.color_group = pg.sprite.Group()
        self.color_palist = []
        self.random_palist = []
        self.x = -20
        self.i = 0
        for item in t.RANDOM_COLORS:
            self.y = -20
            self.x += 40
            self.color_palist += [Colorbox(self.x,self.y,item)]
            self.random_palist += [Colorbox(self.x,self.y-40,(random.randint(0,255), random.randint(0,255), random.randint(0,255)))]
            self.color_group.add(self.color_palist[self.i])
            self.color_group.add(self.random_palist[self.i])
            self.i += 1
        
    def update(self,b,c,g):
        pass
    
#SELECT WHAT BRUSH TO USE
class ToolBox(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((100,s.SCREEN_HEIGHT))
        self.image.fill(t.CYAN)
        self.rect = self.image.get_rect()
        self.rect.x = s.SCREEN_WIDTH - 100
        self.rect.y = 0
        self.tool_group = pg.sprite.Group()
        self.toolbox_list = [Circlebox(), Linebox(), Polybox(), Precisionbox(), circleFoL(), lineFoL(), polyFoL(), Box()]
        for item in self.toolbox_list:
            self.tool_group.add(item)
        self.myfont = pg.font.SysFont("monospace", 15)
        self.label = self.myfont.render("WHAT", 1, t.RED)
        
    def update(self,c,b,g):
        self.image.fill(t.CYAN)
        radlabel = self.myfont.render("Radius: " + str(g.radius), 0, t.BLACK)
        sizelabel = self.myfont.render("Sides: " + str(g.sides), 0, t.BLACK)
        redlabel = self.myfont.render("Red: " + str(g.chosen_color[0]), 0, t.RED)
        grnlabel = self.myfont.render("Green: " + str(g.chosen_color[1]), 0, t.GREEN)
        blulabel = self.myfont.render("Blue: " + str(g.chosen_color[2]), 0, t.BLUE)
        self.image.blit(radlabel, (0, s.SCREEN_HEIGHT - 230))
        self.image.blit(sizelabel, (0, s.SCREEN_HEIGHT - 250))
        self.image.blit(redlabel, (0, s.SCREEN_HEIGHT - 270))
        self.image.blit(grnlabel, (0, s.SCREEN_HEIGHT - 290))
        self.image.blit(blulabel, (0, s.SCREEN_HEIGHT - 310))
    
class Brush:
    def __init__(self):
        self.chosen_shape = "circle"
        self.chosen_color = t.WHITE
        self.precision = True
        self.radius = 42
        self.sides = 6
        self.box_pointlist = []
        
    def update(self,x,y):
        self.x = x
        self.y = y
        self.polygon_pointlist = polypointlist(self.sides,0,self.x,self.y,self.radius)
        for item in self.polygon_pointlist:
            self.polygon2_pointlist = polypointlist(self.sides,0,int(item[0]),int(item[1]),self.radius)
        
    def circlebrush(self,canvas):
        pg.draw.circle(canvas.image,self.chosen_color,(self.x,self.y),self.radius,2)
        
    def linebrush(self,canvas):
        canvas.pointlist += [(self.x,self.y)]
        
    def polybrush(self,canvas):
        pg.draw.polygon(canvas.image,self.chosen_color,self.polygon_pointlist,2)
        
    def circle_fol_brush(self,canvas):
        pg.draw.circle(canvas.image,self.chosen_color,(self.x,self.y),self.radius,2)
        for point in self.polygon_pointlist:
            pg.draw.circle(canvas.image,self.chosen_color,(int(point[0]),int(point[1])),self.radius,2)
            self.polygon_pointlist = polypointlist(self.sides,0,int(point[0]),int(point[1]),self.radius)
            for point in self.polygon_pointlist:
                pg.draw.circle(canvas.image,self.chosen_color,(int(point[0]),int(point[1])),self.radius,2)
                
    def polyFoLbrush(self,canvas):
        pg.draw.polygon(canvas.image,self.chosen_color,self.polygon_pointlist,2)
        for point in self.polygon_pointlist:
            self.polygon2_pointlist = polypointlist(self.sides,0,int(point[0]),int(point[1]),self.radius)
            pg.draw.polygon(canvas.image,self.chosen_color,self.polygon2_pointlist,2)
            for point in self.polygon2_pointlist:
                self.polygon3_pointlist = polypointlist(self.sides,0,int(point[0]),int(point[1]),self.radius)
                pg.draw.polygon(canvas.image,self.chosen_color,self.polygon3_pointlist,2)
                
    def boxbrush(self,canvas):
        if len(self.box_pointlist) == 0:
            self.box_pointlist += [(self.x,self.y)]
        elif len(self.box_pointlist) == 1:
            self.box_pointlist += [(self.x-self.box_pointlist[0][0],self.y-self.box_pointlist[0][1])]
            pg.draw.rect(canvas.image,self.chosen_color,self.box_pointlist,self.sides)
            self.box_pointlist = []
    
class Circlebox(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((42,42))
        self.image.fill(t.BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = s.SCREEN_WIDTH - 100
        self.rect.y = 0
        pg.draw.circle(self.image,t.CYAN,(21,21),15,2)
        self.shape = "circle"
    
    def update(self,brush):
        pass
    
    def selectshape(self,brush,c):
        if self.rect.collidepoint((brush.x,brush.y)):
            brush.chosen_shape = self.shape
        print(brush.chosen_shape)

class Linebox(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((42,42))
        self.image.fill(t.BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = s.SCREEN_WIDTH - 100
        self.rect.y = 50
        pg.draw.line(self.image,t.CYAN,(0,0),(42,42),5)
        self.shape = "line"
        self.listoflines = []
    
    def update(self,brush):
        pass
    
    def selectshape(self,brush,c):
        if self.rect.collidepoint((brush.x,brush.y)):
            brush.chosen_shape = self.shape
        print(brush.chosen_shape)

class Polybox(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((42,42))
        self.image.fill(t.BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = s.SCREEN_WIDTH - 100
        self.rect.y = 100
        self.polygon_pointlist = polypointlist(5,0,21,21,20)
        pg.draw.polygon(self.image,t.CYAN,self.polygon_pointlist,2)
        self.shape = "polygon"
    
    def update(self,brush):
        pass
    
    def selectshape(self,brush,c):
        if self.rect.collidepoint((brush.x,brush.y)):
            brush.chosen_shape = self.shape
        print(brush.chosen_shape)
        
class circleFoL(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((42,42))
        self.image.fill(t.BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = s.SCREEN_WIDTH - 50
        self.rect.y = 0
        pg.draw.circle(self.image,t.GREEN,(21,21),8,2)
        self.shape = "circleFoL"
        self.polygon_pointlist = polypointlist(6,0,21,21,8)
        for item in self.polygon_pointlist:
            pg.draw.circle(self.image,t.CYAN,(int(item[0]),int(item[1])),8,2)
    
    def update(self,brush):
        pass
    
    def selectshape(self,brush,c):
        if self.rect.collidepoint((brush.x,brush.y)):
            brush.chosen_shape = self.shape
        print(brush.chosen_shape)
        
class lineFoL(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((42,42))
        self.image.fill(t.BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = s.SCREEN_WIDTH - 50
        self.rect.y = 50
        pg.draw.line(self.image,t.CYAN,(0,0),(0,42),2)
        self.shape = "lineFoL"
        self.polygon_pointlist = polypointlist(6,0,21,21,8)
    
    def update(self,brush):
        pass
    
    def selectshape(self,brush,c):
        if self.rect.collidepoint((brush.x,brush.y)):
            brush.chosen_shape = self.shape
        print(brush.chosen_shape)
        
class polyFoL(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((42,42))
        self.image.fill(t.BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = s.SCREEN_WIDTH - 50
        self.rect.y = 100
        self.shape = "polyFoL"
        self.polygon_pointlist = polypointlist(6,0,21,21,8)
        for point in self.polygon_pointlist:
            self.polygon2_pointlist = polypointlist(6,0,point[0],point[1],8)
            pg.draw.polygon(self.image,t.CYAN,(self.polygon2_pointlist),2)
        pg.draw.polygon(self.image,t.CYAN,(self.polygon_pointlist),2)
    
    def update(self,brush):
        pass
    
    def selectshape(self,brush,c):
        if self.rect.collidepoint((brush.x,brush.y)):
            brush.chosen_shape = self.shape
        print(brush.chosen_shape)
            
class Box(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((42,42))
        self.image.fill(t.BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = s.SCREEN_WIDTH - 50
        self.rect.y = 150
        self.shape = "box"
        pg.draw.rect(self.image,t.CYAN,(10,10,22,22),3)
    
    def update(self,brush):
        pass
    
    def selectshape(self,brush,c):
        if self.rect.collidepoint((brush.x,brush.y)):
            brush.chosen_shape = self.shape
        print(brush.chosen_shape)
        
class Precisionbox(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((65,22))
        self.image.fill(t.BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = s.SCREEN_WIDTH - 100
        self.rect.y = 200
        self.myfont = pg.font.SysFont("monospace", 15)
        self.label = self.myfont.render("WHAT", 1, t.RED)
        
    def update(self,brush):
        if brush.precision:
            self.image.fill(t.BLACK)
            self.label = self.myfont.render("Precise", 1, t.WHITE)
            self.image.blit(self.label, (0, 0))
            
        else:
            self.image.fill(t.BLACK)
            self.label = self.myfont.render("WiLd", 1,brush.chosen_color, t.WHITE)
            self.image.blit(self.label, (0, 0))
    
    def selectshape(self,brush,c):
        if brush.precision:
            brush.precision = False
        else:
            brush.precision = True
        print(brush.precision)
        
class Colorbox(pg.sprite.Sprite):
    def __init__(self,x,y,color):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((40,40))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x,s.SCREEN_HEIGHT-(100+y))
        self.color = color
        
    def update(self):
        pass
    
    def selectcolor(self,brush):
        self.image.fill(self.color)
        if self.rect.collidepoint((brush.x,brush.y)):
            brush.chosen_color = self.color
        print(brush.chosen_color)
    
def polypointlist(sides,offset,cx,cy,radius):
    step = 2*math.pi/sides
    offset = math.radians(offset)
    pointlist = [ (radius*math.cos(step*n +offset)+cx, radius*math.sin(step*n +offset)+cy) for n in range(0,int(sides)+1) ]
    return pointlist

