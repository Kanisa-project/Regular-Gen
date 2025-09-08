import random

import pygame as pg
import settings as s

class FighterUnit(pg.sprite.Sprite):
    """
    A basic fighting unit for sending to your enemy.
    """
    def __init__(self, x, y, coloration, direction, all_units, is_enemy, wiz_master):
        super().__init__()
        self.image = pg.Surface((32, 32))
        self.image.fill(coloration)
        self.rect = self.image.get_rect(midleft=(x, y))
        self.direction = direction
        self.all_units = all_units
        self.is_enemy = is_enemy

        self.coloring = coloration
        self.max_health = self.coloring[1] * 2.2
        self.health = self.max_health
        self.offense = self.coloring[0]//10
        self.defense = self.coloring[2]//10
        self.detect_range = self.coloring[1] * 3.5
        self.attack_range = self.coloring[1]
        self.max_mana = self.coloring[2] * 2.2
        self.mana = self.max_mana
        self.focus = (self.coloring[0]+self.coloring[1])//16
        self.luck = (self.coloring[1]+self.coloring[2])//16
        self.cast_speed = (self.coloring[0]+self.coloring[1]+self.coloring[2])//32
        self.attack_speed = (self.coloring[0]+self.coloring[1]+self.coloring[2])//22
        self.movement_speed = (self.coloring[0]+self.coloring[1]+self.coloring[2])//62
        self.prev_attack_tick = 0
        self.wiz_master = wiz_master

    def draw_health_bar(self, screen):
        bar_width = self.rect.width
        bar_height = 5
        bar_x = self.rect.x
        bar_y = self.rect.y - bar_height - 2
        hp_percent = self.health / self.max_health
        hp_bar_width = int(bar_width * hp_percent)
        pg.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
        pg.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, hp_bar_width, bar_height))

    def update(self):
        enemies = self.get_enemies_by_distance()
        if enemies:
            # print(enemies)
            # print(f'founded {enemies}\nenemies')
            nearest_enemy, nearest_distance = enemies[0]
            direction = (pg.math.Vector2(nearest_enemy.rect.center) -
                         pg.math.Vector2(self.rect.center)).normalize()
            if nearest_distance <= self.attack_range:
                self.attack_enemy(nearest_enemy)
            else:
                self.rect.x += self.movement_speed * direction.x
                self.rect.y += self.movement_speed * direction.y
        else:
            self.rect.x += self.movement_speed * self.direction
        self.death_check()

    def die(self):
        self.wiz_master.add_to_color_pouch((random.randint(0, 5), random.randint(0, 5), random.randint(0, 5)))
        self.kill()

    def death_check(self):
        if self.rect.right < 0 or self.rect.left > s.SCREEN_WIDTH:
            self.wiz_master.score += self.health
            self.wiz_master.fighters_crossed += 1
            self.die()
        elif self.health <= 0:
            self.die()

    def attack_enemy(self, enemy):
        self.prev_attack_tick += 1
        if self.prev_attack_tick >= self.attack_speed:
            enemy.health -= self.offense
            self.prev_attack_tick = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.draw_health_bar(screen)
        # pg.draw.circle(screen, (0, 0, 0), self.rect.center, self.detect_range, 3)
        # pg.draw.circle(screen, (255, 255, 255), self.rect.center, self.attack_range, 3)

    def get_enemies_by_distance(self):
        my_pos = pg.math.Vector2(self.rect.center)
        detected = []
        for unit in self.all_units:
            if unit is self or unit.is_enemy == self.is_enemy:
                continue
            enemy_pos = pg.math.Vector2(unit.rect.center)
            distance = my_pos.distance_to(enemy_pos)
            if distance <= self.detect_range and distance != 0.0:
                # print(f'detected {unit} at distance: {distance}')
                detected.append((unit, distance))
        detected.sort(key=lambda tup: tup[1])
        return detected
