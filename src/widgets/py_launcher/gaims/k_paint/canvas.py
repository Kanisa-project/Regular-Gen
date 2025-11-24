from src.domain.resource_loader import ensure_parent_dir
from src.settings import app_settings as s
import pygame as pg

class Canvas(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((s.SCREEN_WIDTH, s.SCREEN_HEIGHT - 100))
        self.rect = self.image.get_rect()
        self.pointlist = [(0, 0), (0, 0), (0, 0)]
        self.myfont = pg.font.SysFont("monospace", 15)
        self.rx = 10
        self.ry = 10
        self.rl = 0

    def update(self, x, y, brush):
        if brush.isPrecise:
            if brush.isPolygon:
                brush.update_polypointlist()
        else:
            if brush.isPolygon:
                brush.update_polypointlist()
                pg.draw.polygon(self.image, brush.chosen_color, brush.polygon_pointlist, brush.thickness)
            else:
                pg.draw.circle(self.image, brush.chosen_color, (x, y), brush.radius, brush.thickness)

    def save_paint(self, name):
        pg.image.save(self.image, ensure_parent_dir(name))

    # def keystroke(self, txt):
    #     self.rx += 10
    #     self.ry += 10
    #     if self.ry >= s.SCREEN_HEIGHT:
    #         self.rl += 1
    #         self.rx = self.rl * 22
    #         self.ry -= s.SCREEN_HEIGHT
    #     self.label = self.myfont.render(txt, 1,
    #                                     (random.randint(0, 250), random.randint(0, 250), random.randint(0, 250)))
    #     self.image.blit(self.label, (self.rx, self.ry))
