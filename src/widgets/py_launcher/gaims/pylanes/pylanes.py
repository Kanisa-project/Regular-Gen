import pygame as pg

from src.widgets.py_launcher.gaims.base_gaim.base_gaim import BaseGaim
from src.widgets.py_launcher.gaims.pylanes import settings as s
from src.widgets.py_launcher.gaims.pylanes import base_character
import math

INSTRUCTIONS = {'objective': 'Controlling one of the wizards "Lepht" or "Rhite" you will create summoning cirles.',
                     'controls': 'Each summon circle will create a fighter unit to send across the battlefield.',
                     'scoring': 'Each color will boost a different stat of the fighter unit.'}

class HUD(pg.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        pg.font.init()
        self.image = pg.Surface((s.SCREEN_WIDTH, s.SCREEN_HEIGHT//3))
        self.image.fill(s.WHITE)
        self.rect = self.image.get_rect()
        self.rect.y = int(s.SCREEN_HEIGHT*0.667)
        self.font = pg.font.Font("src/widgets/py_launcher/gaims/pylanes/assets/Parkinsans.ttf", 16)
        self.small_font = pg.font.Font("src/widgets/py_launcher/gaims/pylanes/assets/Parkinsans.ttf", 12)
        self.game = game
        self.hud_size = self.image.get_size()
        self.hud_center = (self.hud_size[0]//2 + 120, self.hud_size[1]//2)
        
        # Connection system
        self.selected_point = None
        self.hovering_point = None
        self.selected_gem_type = 'ruby'  # Default gem type for connections

    def draw_colored_clay_pouch(self):
        """Display the player's colored clay pouch and gems"""
        pouch_x = 20
        pouch_y = 20
        
        # Draw background for clay pouch display
        pg.draw.rect(self.image, (200, 200, 200), (pouch_x - 5, pouch_y - 5, 300, 180), border_radius=5)
        pg.draw.rect(self.image, (150, 150, 150), (pouch_x - 5, pouch_y - 5, 300, 180), 2, border_radius=10)
        
        # Title
        title_text = self.font.render("Resources", True, (0, 0, 0))
        self.image.blit(title_text, (pouch_x, pouch_y))
        
        # RGB bars
        bar_width = 150
        bar_height = 12
        bar_y_start = pouch_y + 25
        
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        color_names = ["Red", "Green", "Blue"]
        
        for i, (color, name) in enumerate(zip(colors, color_names)):
            y_pos = bar_y_start + i * 15
            
            # Background bar
            pg.draw.rect(self.image, (100, 100, 100), (pouch_x, y_pos, bar_width, bar_height))
            
            # Filled bar based on color amount
            if self.game.player.color_pouch[i] > 0:
                fill_width = int(bar_width * (self.game.player.color_pouch[i] / self.game.player.max_color_pouch[i]))
                pg.draw.rect(self.image, color, (pouch_x, y_pos, fill_width, bar_height))
            
            # Amount text
            amount_text = self.small_font.render(f"{name}: {self.game.player.color_pouch[i]}", True, (0, 0, 0))
            self.image.blit(amount_text, (pouch_x + bar_width + 10, y_pos))

        # Gem display
        gem_y_start = bar_y_start + 55
        gem_colors = [(255, 100, 100), (100, 255, 100), (100, 100, 255), (255, 100, 255), (255, 255, 100), (100, 255, 255)]
        gem_names = ["Ruby", "Emerald", "Sapphire", "Rubellite", "Citrine", "Chrysocolla"]
        gem_keys = ['ruby', 'emerald', 'sapphire', 'rubellite', 'citrine', 'chrysocolla']
        
        for i, (color, name, key) in enumerate(zip(gem_colors, gem_names, gem_keys)):
            y_pos = gem_y_start + i * 15
            
            # Gem icon
            pg.draw.circle(self.image, color, (pouch_x + 10, y_pos + 6), 6)
            pg.draw.circle(self.image, (0, 0, 0), (pouch_x + 10, y_pos + 6), 6, 2)
            
            # Gem count
            gem_text = self.small_font.render(f"{name}: {self.game.player.gems[key]}", True, (0, 0, 0))
            self.image.blit(gem_text, (pouch_x + 25, y_pos))

    def draw_gem_combinations(self):
        """Display gem combination buttons"""
        combo_x = 350
        combo_y = 30
        
        # Background
        pg.draw.rect(self.image, (220, 220, 220), (combo_x - 5, combo_y - 5, 250, 160), border_radius=5)
        pg.draw.rect(self.image, (150, 150, 150), (combo_x - 5, combo_y - 5, 250, 160), 2, border_radius=10)
        
        # Title
        title_text = self.font.render("Combine Clay", True, (0, 0, 0))
        self.image.blit(title_text, (combo_x, combo_y))
        
        combinations = [
            ('ruby', 'Red 240', (255, 100, 100), [0, 0]),
            ('emerald', 'Green 240', (100, 255, 100), [1, 1]),
            ('sapphire', 'Blue 240', (100, 100, 255), [2, 2]),
            ('rubellite', 'Red + Blue 130ea', (255, 100, 255), [0, 2]),
            ('citrine', 'Red + Green 130ea', (255, 255, 100), [0, 1]),
            ('chrysocolla', 'Blue + Green 130ea', (100, 255, 255), [1, 2])
        ]
        
        for i, (gem_key, combo_text, color, clay_indices) in enumerate(combinations):
            y_pos = combo_y + 25 + i * 20
            
            # Check if combination is possible
            can_combine = self.game.player.can_combine_clay(gem_key)
            text_color = (0, 0, 0) if can_combine else (142, 142, 142)
            
            # Gem preview
            pg.draw.circle(self.image, color, (combo_x + 10, y_pos + 8), 6)
            pg.draw.circle(self.image, (0, 0, 0), (combo_x + 10, y_pos + 8), 6, 2)
            
            # Combination text
            combo_text_render = self.small_font.render(combo_text, True, text_color)
            self.image.blit(combo_text_render, (combo_x + 25, y_pos))
            
            # Store button area for clicking
            if not hasattr(self, 'combo_buttons'):
                self.combo_buttons = []
            
            if i >= len(self.combo_buttons):
                self.combo_buttons.append({
                    'rect': pg.Rect(combo_x, y_pos, 200, 15),
                    'gem_type': gem_key,
                    'can_combine': can_combine
                })
            else:
                self.combo_buttons[i]['can_combine'] = can_combine

    def summon_pattern(self):
        """Draw the selected summoning circle with connection system"""
        if not self.game.selected_summon_circle:
            return
            
        circle = self.game.selected_summon_circle
        
        # Draw main circle
        pg.draw.circle(self.image, tuple(circle.base_color), self.hud_center, 90)
        pg.draw.circle(self.image, s.CYAN, self.hud_center, 90, 3)
        
        # Draw connection points
        for i in range(circle.num_points):
            pos = self.get_hud_point_position(circle, i)
            if pos:
                # Determine point color
                if i == self.selected_point:
                    color = (255, 255, 0)  # Yellow for selected
                elif i == self.hovering_point:
                    color = (255, 200, 100)  # Light orange for hover
                else:
                    color = (200, 200, 200)  # Gray for normal
                
                pg.draw.circle(self.image, color, pos, 8)
                pg.draw.circle(self.image, (0, 0, 0), pos, 8, 2)
                
                # Point number
                num_text = self.small_font.render(str(i), True, (0, 0, 0))
                num_rect = num_text.get_rect(center=pos)
                self.image.blit(num_text, num_rect)

        # Draw existing connections
        for point1_idx, point2_idx in circle.connections:
            pos1 = self.get_hud_point_position(circle, point1_idx)
            pos2 = self.get_hud_point_position(circle, point2_idx)
            if pos1 and pos2:
                pg.draw.line(self.image, (0, 255, 0), pos1, pos2, 3)

        # Draw connection preview if point selected
        if self.selected_point is not None:
            mouse_pos = pg.mouse.get_pos()
            hud_mouse_pos = (mouse_pos[0], mouse_pos[1] - self.rect.y)
            selected_pos = self.get_hud_point_position(circle, self.selected_point)
            if selected_pos:
                pg.draw.line(self.image, (255, 100, 100), selected_pos, hud_mouse_pos, 2)

        # Connection info
        info_y = self.hud_center[1] + 90
        if self.selected_point is not None:
            info_text = self.small_font.render(f"Selected point {self.selected_point}. Click another point to connect.", True, (0, 0, 0))
        else:
            info_text = self.small_font.render("Click points to select them, then click another to connect.", True, (0, 0, 0))
        
        info_rect = info_text.get_rect(center=(self.hud_center[0], info_y))
        self.image.blit(info_text, info_rect)
        
        # Gem selection
        gem_select_y = info_y + 20
        gem_text = self.small_font.render(f"Selected gem: {self.selected_gem_type.title()}", True, (0, 0, 0))
        gem_rect = gem_text.get_rect(center=(self.hud_center[0], gem_select_y))
        self.image.blit(gem_text, gem_rect)

    def get_hud_point_position(self, circle, point_index):
        """Get the HUD position of a connection point"""
        if point_index >= len(circle.connection_points):
            return None
        
        angle = circle.connection_points[point_index]
        radius = 90
        x = self.hud_center[0] + int(radius * math.cos(angle))
        y = self.hud_center[1] + int(radius * math.sin(angle))
        return (x, y)

    def handle_click(self, pos):
        """Handle clicks in the HUD area"""
        hud_pos = (pos[0], pos[1] - self.rect.y)
        
        # Check gem combination buttons
        if hasattr(self, 'combo_buttons'):
            for button in self.combo_buttons:
                if button['rect'].collidepoint(hud_pos) and button['can_combine']:
                    if self.game.player.combine_clay_to_gems(button['gem_type']):
                        return True
        
        # Check circle connection points
        if self.game.selected_summon_circle:
            circle = self.game.selected_summon_circle
            for i in range(circle.num_points):
                point_pos = self.get_hud_point_position(circle, i)
                if point_pos:
                    point_rect = pg.Rect(point_pos[0] - 8, point_pos[1] - 8, 16, 16)
                    if point_rect.collidepoint(hud_pos):
                        if self.selected_point is None:
                            self.selected_point = i
                        elif self.selected_point != i:
                            # Try to connect points
                            if circle.connect_points(self.selected_point, i, self.selected_gem_type):
                                self.selected_point = None
                                return True
                            else:
                                self.selected_point = i
                        else:
                            self.selected_point = None
                        return True
        
        # Check gem type selection (simple cycling for now)
        if hud_pos[1] > self.hud_center[1] + 100:  # Bottom area
            gem_types = ['ruby', 'emerald', 'sapphire', 'rubellite', 'citrine', 'chrysocolla']
            current_idx = gem_types.index(self.selected_gem_type)
            self.selected_gem_type = gem_types[current_idx % len(gem_types)]
            return True
        
        return False

    def draw(self, screen):
        # Clear the HUD surface
        self.image.fill(s.WHITE)
        
        # Always display the colored clay pouch and gems
        self.draw_colored_clay_pouch()
        
        # Draw gem combination interface
        self.draw_gem_combinations()
        
        # Draw selected summoning circle pattern if one is selected
        if self.game.selected_summon_circle:
            self.summon_pattern()
        
        # Blit the HUD to the screen
        screen.blit(self.image, self.rect)
        
        # Draw score text
        player_score_text = self.font.render(f"Score: {int(self.game.player.score)}", True, (0, 0, 0))
        enemy_score_text = self.font.render(f"Score: {int(self.game.enemy.score)}", True, (0, 0, 0))
        screen.blit(player_score_text, (20, s.SCREEN_HEIGHT-32))
        screen.blit(enemy_score_text, (s.SCREEN_WIDTH-260, 526))

class PyLanes(BaseGaim):
    def __init__(self, player_name=None):
        super().__init__(player_name)
        pg.display.set_caption('PyLane Summoners')
        self.all_summon_circles = pg.sprite.Group()
        self.all_fighter_units = pg.sprite.Group()
        self.all_characters = pg.sprite.Group()
        self.coloring_timer = 0
        self.player = base_character.PlayerCharacter(96, s.SCREEN_HEIGHT - 96)
        self.enemy = base_character.EnemyCharacter(s.SCREEN_WIDTH - 96, s.SCREEN_HEIGHT - 96)
        self.enemy.set_ai_difficulty('hard')
        self.all_characters.add(self.player) # type: ignore
        self.all_characters.add(self.enemy) # type: ignore
        self.hud = HUD(self)
        self.selected_summon_circle = None
        self.clock = pg.time.Clock()
        self.running = True
        self.screen = pg.display.set_mode((s.SCREEN_WIDTH, s.SCREEN_HEIGHT))


    def run(self):
        while self.running:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(s.FPS)
        pg.quit()

    def events(self):
        for event in pg.event.get():
            # Handle summoning circle events and update selected circle
            for circle in self.all_summon_circles:
                circle.handle_event(event, self.all_summon_circles)
                if circle.selected:
                    self.selected_summon_circle = circle
            
            if event.type == pg.QUIT:
                self.running = False
                
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                
                # Check if click is in HUD area
                if my > s.SCREEN_HEIGHT * 3 // 4:
                    if self.hud.handle_click((mx, my)):
                        continue  # Skip other click handling if HUD handled the click
                
                # Handle summoning circle placement
                if valid_area(mx, my) and self.player.can_place_summon_circle():
                    new_circle = self.player.place_summon_circle(mx, my)
                    self.all_summon_circles.add(new_circle) # type: ignore
                    
            # if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
            #     mx, my = event.pos
            #     if valid_area(mx, my, False) and self.enemy.can_place_summon_circle():
            #         new_circle = self.enemy.place_summon_circle(mx, my)
            #         self.all_summon_circles.add(new_circle) #type: ignore
            
            # Handle key presses for gem selection
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
                if event.key == pg.K_1:
                    self.hud.selected_gem_type = 'ruby'
                elif event.key == pg.K_2:
                    self.hud.selected_gem_type = 'emerald'
                elif event.key == pg.K_3:
                    self.hud.selected_gem_type = 'sapphire'
                elif event.key == pg.K_4:
                    self.hud.selected_gem_type = 'rubellite'
                elif event.key == pg.K_5:
                    self.hud.selected_gem_type = 'citrine'
                elif event.key == pg.K_6:
                    self.hud.selected_gem_type = 'chrysocolla'

    def update(self):
        self.coloring_timer += 1
        self.enemy.update()
        for circle in self.all_summon_circles:
            circle.update(self.all_fighter_units)
        for unit in self.all_fighter_units:
            unit.update()
        for circle in self.enemy.summon_circles:
            circle.update(self.all_fighter_units)

    def draw(self):
        self.screen.fill((30, 30, 30))
        self.hud.draw(self.screen)
        pg.draw.rect(self.screen, (60, 60, 60), (20, 20, s.SPAWN_RECT_SIZE[0], s.SPAWN_RECT_SIZE[1]), 2)
        pg.draw.rect(self.screen, (60, 60, 60), (s.SCREEN_WIDTH-220, 20, s.SPAWN_RECT_SIZE[0], s.SPAWN_RECT_SIZE[1]), 2)
        self.all_summon_circles.draw(self.screen)
        for unit in self.all_fighter_units:
            unit.draw(self.screen)
        for character in self.all_characters:
            character.draw(self.screen)
        pg.display.flip()

def valid_area(x, y, is_lepht=True) -> bool:
    """
    Checks for validity of placing a summoning circle.
    :param x: x-position
    :param y: y-position
    :param is_lepht: Lepht wizard is placing.
    :return:
    """
    if 20 < y < 448:
        if is_lepht:
            if 20 < x < 220:
                return True
        else:
            if s.SCREEN_WIDTH-220 < x < s.SCREEN_WIDTH-20:
                return True
    return False


if __name__ == "__main__":
    PyLanes().run()