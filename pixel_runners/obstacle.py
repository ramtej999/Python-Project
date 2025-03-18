import pygame
import random
import numpy as np
from settings import *

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, obstacle_type="spike"):
        super().__init__()
        self.obstacle_type = obstacle_type
        self.image = self.create_obstacle_surface(width, height)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = SCROLL_SPEED
        
    def create_obstacle_surface(self, width, height):
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        if self.obstacle_type == "spike":
            # Draw a triangle for spikes
            pygame.draw.polygon(surface, RED, [(0, height), (width/2, 0), (width, height)])
        elif self.obstacle_type == "fire":
            # Draw a fire obstacle
            pygame.draw.rect(surface, YELLOW, (0, 0, width, height))
            for i in range(5):
                x = random.randint(0, width-10)
                pygame.draw.circle(surface, RED, (x, 5), 5)
        else:
            # Default obstacle
            pygame.draw.rect(surface, RED, (0, 0, width, height))
            
        return surface
    
    def update(self):
        # Move obstacle to the left (scrolling effect)
        self.rect.x -= self.speed
        
        # Remove if off-screen
        if self.rect.right < 0:
            self.kill()

class MovingObstacle(Obstacle):
    def __init__(self, x, y, width, height, obstacle_type="moving_platform", move_distance=100, move_speed=2, vertical=False):
        super().__init__(x, y, width, height, obstacle_type)
        self.vertical = vertical
        self.move_distance = move_distance
        self.move_speed = move_speed
        self.start_pos = pygame.math.Vector2(x, y)
        self.direction = 1
        self.progress = 0
        
    def update(self):
        # Move obstacle left (scrolling)
        self.rect.x -= SCROLL_SPEED
        
        # Handle vertical or horizontal movement
        if self.vertical:
            self.progress += self.move_speed * self.direction
            if abs(self.progress) > self.move_distance:
                self.direction *= -1
                self.progress = self.move_distance * self.direction
            self.rect.y = self.start_pos.y + self.progress
        else:
            self.progress += self.move_speed * self.direction
            if abs(self.progress) > self.move_distance:
                self.direction *= -1
                self.progress = self.move_distance * self.direction
            self.rect.x = self.start_pos.x - SCROLL_SPEED + self.progress
        
        # Remove if off-screen
        if self.rect.right < 0:
            self.kill() 