import random

from src.widgets.py_launcher.gaims.base_gaim.base_gaim import BaseGaim
import pygame as pg
from .player import Player
from .obstacle import Wall

class AllBallsFall(BaseGaim):
    def __init__(self, player_name):
        super().__init__(player_name)
        self.player_object = "Ball"
        self.obstacle_object = "Platform"
        # self.player_spirite = Player(241, 128, pg.image.load(f"assets/Ball.png"))
        self.player_spirite = Player(241, 128, pg.image.load(f"src/widgets/py_launcher/gaims/all_balls_fall/assets/Ball.png"))
        # self.obstacle_spirite = Wall(241, 512, pg.image.load(f"src/widgets/py_launcher/gaims/all_balls_fall/assets/Platform.png"))
        self.all_sprites.add(self.player_spirite)
        self.floating_walls = []
        self.spawn_obstacles(random.randint(4, 20))

    def update(self):
        self.all_sprites.update()
        for wall in self.floating_walls:
            if self.player_spirite.rect.colliderect(wall):
                self.player_spirite.rect.y -= 6
        if self.player_spirite not in self.all_sprites:
            self.running = False

    def spawn_obstacles(self, num_walls=10):
        for i in range(num_walls):
            self.floating_walls.append(Wall(64*i, 512, pg.image.load(f"src/widgets/py_launcher/gaims/all_balls_fall/assets/Platform.png")))
            self.all_sprites.add(self.floating_walls[i])

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
                elif event.key == pg.K_RIGHT or event.key == pg.K_d:
                    self.player_spirite.rolling_direction = "right"
                elif event.key == pg.K_LEFT or event.key == pg.K_a:
                    self.player_spirite.rolling_direction = "left"
            elif event.type == pg.KEYUP:
                if event.key == pg.K_RIGHT or event.key == pg.K_d:
                    self.player_spirite.rolling_direction = None
                elif event.key == pg.K_LEFT or event.key == pg.K_a:
                    self.player_spirite.rolling_direction = None

    def draw(self):
        self.screen.fill((241, 24, 11))
        self.all_sprites.draw(self.screen)
        pg.display.flip()


if __name__ == "__main__":
    AllBallsFall("Player").run()