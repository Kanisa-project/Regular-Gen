from src.settings import app_settings as s, themery as t
import pygame as pg


class ColorPalette(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.top_row = "qwertyuiop"
        self.mid_row = "asdfghjkl"
        self.bot_row = "zxcvbnm"
        self.image = pg.Surface((s.SCREEN_WIDTH, 142))
        self.image.fill(t.LIGHT_GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = s.SCREEN_HEIGHT - 100
        self.color_group = pg.sprite.Group()
        self.color_palette_list = []
        self.random_palette_list = []
        self.x = -20
        self.i = 0
        self.font = pg.font.SysFont("monospace", 15)
        self.setup_key_colored_word(self.top_row)
        self.setup_key_colored_word(self.mid_row, -60)
        self.setup_key_colored_word(self.bot_row, -100)

    def update(self, b, c, g):
        pass

    def setup_key_colored_word(self, colored_word='abc', y_set=-20):
        for letter in colored_word:
            key_color = t.ALPHANUMERIC_COLORS[letter]
            self.x += 40
            self.color_palette_list += [Colorbox(self.x, y_set, key_color, letter)]
            self.color_group.add(self.color_palette_list[self.i])
            self.i += 1
        self.x = -20

    def brush_info(self, brush):
        self.image.fill(t.LIGHT_GREEN)
        brush_radius = self.font.render(f"Radius: {brush.radius}", 1, t.BLACK)
        brush_x_offset = self.font.render(f"x-offset: {brush.x_offset}", 1, t.BLACK)
        brush_y_offset = self.font.render(f"y-offset: {brush.y_offset}", 1, t.BLACK)
        brush_thickness = self.font.render(f"Thickness: {brush.thickness}", 1, t.BLACK)
        brush_num_sides = self.font.render(f"# of Sides: {brush.sides}", 1, t.BLACK)
        brush_is_polygon = self.font.render(f"isPolygon: {brush.isPolygon}", 1, t.BLACK)
        brush_is_precise = self.font.render(f"isPrecise: {brush.isPrecise}", 1, t.BLACK)
        brush_is_wild = self.font.render(f"isWild: {brush.isWild}", 1, t.BLACK)
        brush_is_fol = self.font.render(f"isFoL: {brush.isFoL}", 1, t.BLACK)
        self.image.blit(brush_radius, (500, 10))
        self.image.blit(brush_x_offset, (500, 22))
        self.image.blit(brush_y_offset, (500, 34))
        self.image.blit(brush_thickness, (500, 46))
        self.image.blit(brush_num_sides, (500, 58))
        self.image.blit(brush_is_polygon, (500, 70))
        self.image.blit(brush_is_precise, (500, 82))
        self.image.blit(brush_is_wild, (500, 94))
        self.image.blit(brush_is_fol, (500, 106))



class Colorbox(pg.sprite.Sprite):
    def __init__(self, x, y, color, letter_key=None):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((40, 40))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, s.SCREEN_HEIGHT - (100 + y))
        self.color = color
        if letter_key and isinstance(letter_key, str):
            font = pg.font.SysFont("monospace", 15)
            self.label = font.render(letter_key, 1, t.BLACK)
            self.image.blit(self.label, (10, 10))

    def update(self):
        pass

    def selectcolor(self, brush, true_pos):
        # self.image.fill(self.color)
        if self.rect.collidepoint(true_pos):
            brush.chosen_color = self.color
        print(brush.chosen_color)
