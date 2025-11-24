import random

from src.domain.resource_loader import ensure_parent_dir
from src.widgets.py_launcher.gaims.base_gaim.base_gaim import BaseGaim
import pygame as pg
from .player import Player
from .obstacle import Wall

class AllBallsFall(BaseGaim):
    def __init__(self, player_name, window_size=(640, 960)):
        super().__init__(player_name, window_size=window_size)
        self.time_sec = 0
        self.milli_sec = 0
        self.score = 0
        self.player_object = "Ball"
        self.obstacle_object = "Platform"
        # self.player_spirite = Player(241, 228, pg.image.load(f"assets/Ball.png"))
        self.player_spirite = Player(241, 128, pg.image.load(f"src/widgets/py_launcher/gaims/all_balls_fall/assets/Ball.png"))
        self.all_sprites.add(self.player_spirite)
        self.floating_walls = []
        self.right_line = window_size[0]
        self.bottom_line = window_size[1]
        self.spawn_obstacles(random.randint(4, 8))

    def update(self):
        self.all_sprites.update()
        self.score += 0.5
        self.milli_sec += 1
        if self.milli_sec >= 60:
            self.time_sec += 1
            self.milli_sec = 0
        for wall in self.floating_walls:
            if self.player_spirite.rect.colliderect(wall):
                self.player_spirite.rect.y -= 6
        if self.player_spirite.rect.y <= 0 or self.player_spirite.rect.y >= self.bottom_line:
            with open(ensure_parent_dir("src/widgets/py_launcher/gaims/all_balls_fall/assets/abf_scores.txt"), "a") as f:
                f.write(f"{self.player_name} got {self.score} points in {self.time_sec} seconds.\n")
            self.player_spirite.kill()
        elif self.player_spirite.rect.x < 0:
            self.player_spirite.rect.x = self.right_line
        elif self.player_spirite.rect.x > self.right_line:
            self.player_spirite.rect.x = 0
        if self.player_spirite not in self.all_sprites:
            self.running = False

    def spawn_obstacles(self, num_walls=10):
        for i in range(num_walls):
            # self.floating_walls.append(Wall(64*i, self.bottom_line, pg.image.load(f"assets/Platform.png")))
            self.floating_walls.append(Wall(64*i, self.bottom_line, pg.image.load(f"src/widgets/py_launcher/gaims/all_balls_fall/assets/Platform.png")))
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
        score_lbl = self.font.render(f"Score: {self.score}", 1, (255, 255, 255))
        time_lbl = self.font.render(f"Time: {self.time_sec}", 1, (255, 255, 255))
        self.screen.blit(score_lbl, (10, 10))
        self.screen.blit(time_lbl, (10, 22))
        self.all_sprites.draw(self.screen)
        pg.display.flip()


if __name__ == "__main__":
    AllBallsFall("Player").run()