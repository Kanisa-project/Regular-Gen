import pygame as pg

class SpiriteMerge:
    def __init__(self):
        self.sprite = None

    def load_sprite(self, file_path: str):
        pass

    def load_spirit(self, file_path: str):
        pass

    def full_spirite(self) -> pg.sprite.Sprite:
        pass

class BaseGaim:
    def __init__(self, player_name, is_new_game=False, window_size=(1280, 768)):
        pg.mixer.pre_init()
        pg.init()
        pg.font.init()
        pg.mixer.init()
        self.player_name = player_name
        self.font = pg.font.SysFont("Parkinsans", 16)
        self.screen = pg.display.set_mode(window_size)
        self.clock = pg.time.Clock()
        self.all_sprites = pg.sprite.Group()
        self.running = True
        self.mouse_pos = (0, 0)

    def save_gaim(self):
        pass

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()
        pg.quit()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False

    def update(self):
        pass

    def draw(self):
        self.screen.fill((74, 14, 90))
        pg.display.flip()
