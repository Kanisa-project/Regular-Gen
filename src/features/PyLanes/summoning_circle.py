import random
import math
import pygame as pg
import settings as s
from fighter_unit import FighterUnit

class SummoningCircle(pg.sprite.Sprite):
    def __init__(self, x, y, direction, circle_crafter):
        super().__init__()
        self.image = pg.Surface((40, 40), pg.SRCALPHA)
        pg.draw.circle(self.image, (51, 51, 51), (20, 20), 20, 3)
        self.rect = self.image.get_rect(center=(x, y))
        # self.lane = lane
        self.direction = direction
        self.spawn_timer = 0
        self.base_color = [51, 51, 51]
        self.circle_crafter = circle_crafter
        self.selected = False
        
        # Connection system
        self.num_points = 9
        # self.num_points = random.randint(3, 9)
        self.connection_points = []
        self.connections = []  # List of tuples (point1_index, point2_index)
        
        # Generate connection points around the circle
        self._generate_connection_points()
        self.redraw()

    def _generate_connection_points(self):
        """Generate random connection points around the circle"""
        self.connection_points = []
        for i in range(self.num_points):
            angle = (i * 360 / self.num_points) * math.pi / 180
            # Add some randomness to the angle for variety
            # angle += random.uniform(-0.00013, 0.00013)
            self.connection_points.append(angle)
        
        # Sort angles to maintain consistent ordering
        self.connection_points.sort()

    def get_point_position(self, point_index, radius=15):
        """Get the screen position of a connection point"""
        if point_index >= len(self.connection_points):
            return None
        
        angle = self.connection_points[point_index]
        x = self.rect.centerx + int(radius * math.cos(angle))
        y = self.rect.centery + int(radius * math.sin(angle))
        return (x, y)

    def can_connect_points(self, point1_idx, point2_idx):
        """Check if two points can be connected"""
        if point1_idx == point2_idx:
            return False
        if (point1_idx, point2_idx) in self.connections or (point2_idx, point1_idx) in self.connections:
            return False
        return True

    def get_connection_cost(self, point1_idx, point2_idx):
        """Calculate the cost to connect two points"""
        base_clay_cost = 20
        base_gem_cost = 1
        
        # Calculate distance between points (affects cost)
        angle1 = self.connection_points[point1_idx]
        angle2 = self.connection_points[point2_idx]
        angle_diff = abs(angle1 - angle2)
        if angle_diff > math.pi:
            angle_diff = 2 * math.pi - angle_diff
        
        # Normalize to 0-1 range and use as multiplier
        distance_multiplier = angle_diff / math.pi
        
        clay_cost = int(base_clay_cost + (base_clay_cost * distance_multiplier))
        gem_cost = base_gem_cost + int(distance_multiplier * 2)
        
        return clay_cost, gem_cost

    def connect_points(self, point1_idx, point2_idx, gem_type):
        """Connect two points using clay and gems"""
        if not self.can_connect_points(point1_idx, point2_idx):
            return False
            
        clay_cost, gem_cost = self.get_connection_cost(point1_idx, point2_idx)
        
        # Check if player has enough resources
        total_clay = sum(self.circle_crafter.color_pouch)
        if total_clay < clay_cost or self.circle_crafter.gems[gem_type] < gem_cost:
            return False
        
        # Deduct resources (prioritize highest clay color)
        remaining_cost = clay_cost
        for i in range(3):
            color_idx = [0, 1, 2][i]  # Red, Green, Blue
            available = self.circle_crafter.color_pouch[color_idx]
            deduct = min(remaining_cost, available)
            self.circle_crafter.color_pouch[color_idx] -= deduct
            remaining_cost -= deduct
            if remaining_cost <= 0:
                break
        
        # Deduct gems
        self.circle_crafter.gems[gem_type] -= gem_cost
        
        # Create connection
        self.connections.append((point1_idx, point2_idx))
        
        # Apply connection effect to circle based on gem type
        self._apply_connection_effect(gem_type)
        
        self.redraw()
        return True

    def _apply_connection_effect(self, gem_type):
        """Apply stat boosts based on gem type used in connection"""
        if gem_type == 'rubellite':  # Red + Blue gem
            self.base_color[0] = min(255, self.base_color[0] + 15)  # Increase red (damage)
            self.base_color[2] = min(255, self.base_color[2] + 10)  # Increase blue (defense/mana)
        elif gem_type == 'citrine':  # Red + Green gem
            self.base_color[0] = min(255, self.base_color[0] + 10)  # Increase red (damage)
            self.base_color[1] = min(255, self.base_color[1] + 15)  # Increase green (health/range)
        elif gem_type == 'chrysocolla':  # Blue + Green gem
            self.base_color[2] = min(255, self.base_color[2] + 15)  # Increase blue (defense/mana)
            self.base_color[1] = min(255, self.base_color[1] + 10)  # Increase green (health/range)

    def redraw(self):
        self.image.fill((0, 0, 0, 0))
        pg.draw.circle(self.image, tuple(self.base_color), (20, 20), 18)
        pg.draw.circle(self.image, (51, 51, 51), (20, 20), 20, 3)
        
        # Draw connection points
        for i in range(self.num_points):
            angle = self.connection_points[i]
            x = 20 + int(15 * math.cos(angle))
            y = 20 + int(15 * math.sin(angle))
            pg.draw.circle(self.image, (200, 200, 200), (x, y), 2)
        
        # Draw connections
        for point1_idx, point2_idx in self.connections:
            angle1 = self.connection_points[point1_idx]
            angle2 = self.connection_points[point2_idx]
            
            x1 = 20 + int(15 * math.cos(angle1))
            y1 = 20 + int(15 * math.sin(angle1))
            x2 = 20 + int(15 * math.cos(angle2))
            y2 = 20 + int(15 * math.sin(angle2))
            
            pg.draw.line(self.image, (255, 255, 0), (x1, y1), (x2, y2), 2)
        
        if self.selected:
            pg.draw.circle(self.image, (255, 255, 0), (20, 20), 22, 2)

    def update(self, units_group):
        self.spawn_timer += 1
        if self.spawn_timer % s.COLOR_PAYOUT_INTERVAL == 0:
            color_reward = [random.randint(0, 3), random.randint(0, 3), random.randint(0, 3)]
            self.circle_crafter.add_to_color_pouch(color_reward)
        if self.spawn_timer >= s.SUMMON_INTERVAL and len(self.circle_crafter.fighters) < s.MAX_SUMMONS:
            self.spawn_timer = 0
            y = self.rect.centery
            x = self.rect.centerx
            unit = FighterUnit(x, y, self.base_color, self.direction, units_group, self.circle_crafter.isPlayer, self.circle_crafter)
            units_group.add(unit)
            self.circle_crafter.fighters.add(unit)

    def handle_event(self, event, all_circles):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                for circle in all_circles:
                    circle.selected = False
                    circle.redraw()
                self.circle_crafter.summon_circ = self
                self.selected = True
                self.redraw()
        if self.selected and event.type == pg.KEYDOWN:
            if event.key == pg.K_r and self.circle_crafter.color_pouch[0] >= 3:
                self.base_color[0] = min(255, self.base_color[0] + 3)
                self.circle_crafter.color_pouch[0] -= 3
            if event.key == pg.K_g and self.circle_crafter.color_pouch[1] >= 3:
                self.base_color[1] = min(255, self.base_color[1] + 3)
                self.circle_crafter.color_pouch[1] -= 3
            if event.key == pg.K_b and self.circle_crafter.color_pouch[2] >= 3:
                self.base_color[2] = min(255, self.base_color[2] + 3)
                self.circle_crafter.color_pouch[2] -= 3
            if event.mod & pg.KMOD_SHIFT:
                if event.key == pg.K_r and self.circle_crafter.color_pouch[1] <= 255 and self.base_color[0] > 3:
                    self.base_color[0] = max(0, self.base_color[0] - 3)
                    self.circle_crafter.color_pouch[1] += 1
                if event.key == pg.K_g and self.circle_crafter.color_pouch[2] <= 255 and self.base_color[1] > 3:
                    self.base_color[1] = max(0, self.base_color[1] - 3)
                    self.circle_crafter.color_pouch[2] += 1
                if event.key == pg.K_b and self.circle_crafter.color_pouch[0] <= 255 and self.base_color[2] > 3:
                    self.base_color[2] = max(0, self.base_color[2] - 3)
                    self.circle_crafter.color_pouch[0] += 1
        self.redraw()