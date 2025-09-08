import pygame as pg
import settings as s
from summoning_circle import SummoningCircle

OCCUPATIONS = {
    'barbarian': {},
    'ranger': {},
    'warlock': {},
}

class InventoryClay(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((16, 16))
        self.image = pg.image.load('assets/sprites/colored_clay.png')
        self.rect = self.image.get_rect()

    def color_overlay(self, overlay_color):
        overlay = pg.Surface(self.image.get_size(), pg.SRCALPHA)
        overlay.fill(overlay_color)
        self.image.blit(overlay, (0, 0), special_flags=pg.BLEND_RGBA_MULT)


class BaseCharacter(pg.sprite.Sprite):
    def __init__(self, x, y, is_lepht):
        super().__init__()
        self.isPlayer = is_lepht
        self.image = pg.Surface((1, 1))
        self.image.fill((5, 5, 5, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.health = 241
        self.max_color_pouch = [255, 255, 255]
        self.color_pouch = [255, 255, 255]

        # Gem inventory
        self.gems = {
            'ruby': 2,  # Red
            'emerald': 2,  # Green
            'sapphire': 2,  # Blue
            'rubellite': 2,  # Red + Blue
            'citrine': 2,  # Red + Green
            'chrysocolla': 2  # Blue + Green
        }

        self.colored_clay_pouch = {
            "red": 0,
            "green": 0,
            "blue": 0,
            "cyan": 0,
            "magenta": 0,
            "yellow": 0,
            "black": 0,
            "grey": 0,
            "white": 0,
        }
        self.coloring_timer = 0
        self.summon_circles = pg.sprite.Group()
        self.fighters = pg.sprite.Group()
        self.fighters_crossed = 0
        self.score = 0

    def add_to_color_pouch(self, color):
        for i in range(3):
            self.color_pouch[i] = min(self.max_color_pouch[i], self.color_pouch[i] + color[i])

    def can_place_summon_circle(self) -> bool:
        if self.color_pouch[0] >= 170 and self.color_pouch[1] >= 170 and self.color_pouch[2] >= 170:
            return True
        else:
            return False

    def combine_clay_to_gems(self, gem_type):
        """Combine clay to create gems"""
        if gem_type == 'ruby':
            if self.color_pouch[0] >= 240:
                self.color_pouch[0] -= 240  # Red
                self.gems['ruby'] += 3
                return True
        elif gem_type == 'emerald':
            if self.color_pouch[1] >= 240:
                self.color_pouch[1] -= 240  # Green
                self.gems['emerald'] += 3
                return True
        elif gem_type == 'sapphire':
            if self.color_pouch[2] >= 240:
                self.color_pouch[2] -= 240  # Blue
                self.gems['sapphire'] += 3
                return True
        elif gem_type == 'rubellite':
            if self.color_pouch[0] >= 130 and self.color_pouch[2] >= 130:
                self.color_pouch[0] -= 130  # Red
                self.color_pouch[2] -= 130  # Blue
                self.gems['rubellite'] += 3
                return True
        elif gem_type == 'citrine':
            if self.color_pouch[0] >= 130 and self.color_pouch[1] >= 130:
                self.color_pouch[0] -= 130  # Red
                self.color_pouch[1] -= 130  # Green
                self.gems['citrine'] += 3
                return True
        elif gem_type == 'chrysocolla':
            if self.color_pouch[2] >= 130 and self.color_pouch[1] >= 130:
                self.color_pouch[2] -= 130  # Blue
                self.color_pouch[1] -= 130  # Green
                self.gems['chrysocolla'] += 3
                return True
        return False

    def can_combine_clay(self, gem_type):
        """Check if player has enough clay to create gems"""
        if gem_type == 'ruby':
            return self.color_pouch[0] >= 240
        elif gem_type == 'emerald':
            return self.color_pouch[1] >= 240
        elif gem_type == 'sapphire':
            return self.color_pouch[2] >= 240
        elif gem_type == 'rubellite':
            return self.color_pouch[0] >= 130 and self.color_pouch[2] >= 130
        elif gem_type == 'citrine':
            return self.color_pouch[0] >= 130 and self.color_pouch[1] >= 130
        elif gem_type == 'chrysocolla':
            return self.color_pouch[2] >= 130 and self.color_pouch[1] >= 130
        return False

    def place_summon_circle(self, x, y) -> pg.sprite.Sprite:
        """
        Setup, create and return a summoning circle.
        :param y:
        :param x:
        :return:
        """
        self.color_pouch[0] -= 170
        self.color_pouch[1] -= 170
        self.color_pouch[2] -= 170
        summon_circle = SummoningCircle(x, y, 1 if self.isPlayer else -1, self)
        self.summon_circles.add(summon_circle)  # type: ignore
        return summon_circle

    def update(self):
        pass

    def draw(self, screen):
        # Draw the character
        screen.blit(self.image, self.rect)

class PlayerCharacter(BaseCharacter):
    def __init__(self, x, y):
        super().__init__(x, y, True)


class EnemyCharacter(BaseCharacter):
    def __init__(self, x, y):
        super().__init__(x, y, False)
        # AI-specific attributes
        self.ai_decision_timer = 0
        self.ai_decision_interval = 60  # Make decision every 60 frames (adjust as needed)
        self.ai_aggression = 0.7  # 0.0 to 1.0, how aggressive the AI is
        self.ai_resource_threshold = 0.5  # When to use resources (0.0 to 1.0)
        
    def update(self):
        super().update()
        self.ai_decision_timer += 1
        
        if self.ai_decision_timer >= self.ai_decision_interval:
            self.make_ai_decision()
            print("Deciding....")
            self.ai_decision_timer = 0
    
    def make_ai_decision(self):
        """Main AI decision-making logic"""
        import random
        
        # Random chance for different actions based on available resources
        decisions = []
        
        # Check if AI can place summon circle
        if self.can_place_summon_circle():
            # Higher chance if aggressive or has lots of resources
            resource_ratio = min(self.color_pouch) / 255.0
            place_chance = self.ai_aggression * 0.6 + resource_ratio * 0.4
            decisions.append(('place_summon_circle', place_chance))
        
        # Check if AI can combine clay to gems
        gem_types = ['ruby', 'emerald', 'sapphire', 'rubellite', 'citrine', 'chrysocolla']
        for gem_type in gem_types:
            if self.can_combine_clay(gem_type):
                # More likely to combine if has excess resources
                resource_ratio = self.get_resource_ratio_for_gem(gem_type)
                combine_chance = resource_ratio * 0.3 + random.random() * 0.2
                decisions.append(('combine_clay', combine_chance, gem_type))
        
        # If no good decisions, do nothing or gather resources
        if not decisions:
            self.ai_idle_behavior()
            return
        
        # Sort decisions by priority and execute the best one
        decisions.sort(key=lambda x: x[1], reverse=True)
        best_decision = decisions[0]
        
        if best_decision[1] > self.ai_resource_threshold:
            if best_decision[0] == 'place_summon_circle':
                self.ai_place_summon_circle()
            elif best_decision[0] == 'combine_clay':
                self.combine_clay_to_gems(best_decision[2])
    
    def get_resource_ratio_for_gem(self, gem_type):
        """Calculate how much resources the AI has relative to what's needed for a gem"""
        if gem_type == 'ruby':
            return self.color_pouch[0] / 240.0
        elif gem_type == 'emerald':
            return self.color_pouch[1] / 240.0
        elif gem_type == 'sapphire':
            return self.color_pouch[2] / 240.0
        elif gem_type == 'rubellite':
            return min(self.color_pouch[0], self.color_pouch[2]) / 130.0
        elif gem_type == 'citrine':
            return min(self.color_pouch[0], self.color_pouch[1]) / 130.0
        elif gem_type == 'chrysocolla':
            return min(self.color_pouch[1], self.color_pouch[2]) / 130.0
        return 0.0
    
    def ai_place_summon_circle(self):
        """AI logic for placing summon circles"""
        import random
        import settings as s
        
        # Place summon circle at a strategic location
        # For now, place it randomly on the AI's side of the screen
        # x = random.randint(s.SCREEN_WIDTH // 2, s.SCREEN_WIDTH - 100)
        x = random.randint(s.SCREEN_WIDTH-220, s.SCREEN_WIDTH-20)
#         y = random.randint(100, s.SCREEN_HEIGHT - 100)
        y = random.randint(40, 420)
        print("Placing summon circle at", x, y)
        
        return self.place_summon_circle(x, y)
    
    def ai_idle_behavior(self):
        """What AI does when it can't make meaningful decisions"""
        import random
        print("AI is idle...")
        # Small chance to add some random resources (simulating resource gathering)
        if random.random() < 0.1:  # 10% chance per decision cycle
            color_gain = [random.randint(1, 5), random.randint(1, 5), random.randint(1, 5)]
            self.add_to_color_pouch(color_gain)
            print("Added", color_gain, "to resources")
    
    def set_ai_difficulty(self, difficulty):
        """Adjust AI behavior based on difficulty"""
        if difficulty == 'easy':
            self.ai_aggression = 0.3
            self.ai_resource_threshold = 0.7
            self.ai_decision_interval = 90
        elif difficulty == 'medium':
            self.ai_aggression = 0.5
            self.ai_resource_threshold = 0.5
            self.ai_decision_interval = 60
        elif difficulty == 'hard':
            self.ai_aggression = 0.8
            self.ai_resource_threshold = 0.3
            self.ai_decision_interval = 40
