import pygame
from settings import *

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, powerup_type="speed_boost"):
        super().__init__()
        self.powerup_type = powerup_type
        self.image = self.create_powerup_surface()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = SCROLL_SPEED
        self.duration = POWERUP_DURATION
        
    def create_powerup_surface(self):
        surface = pygame.Surface((30, 30), pygame.SRCALPHA)
        
        if self.powerup_type == "speed_boost":
            pygame.draw.circle(surface, BLUE, (15, 15), 15)
            # Draw a lightning bolt or arrow
            pygame.draw.polygon(surface, WHITE, [(10, 5), (20, 5), (15, 15), (20, 15), (10, 25), (15, 15), (10, 15)])
        elif self.powerup_type == "high_jump":
            pygame.draw.circle(surface, GREEN, (15, 15), 15)
            # Draw an up arrow
            pygame.draw.polygon(surface, WHITE, [(15, 5), (25, 15), (20, 15), (20, 25), (10, 25), (10, 15), (5, 15)])
        elif self.powerup_type == "slow_motion":
            pygame.draw.circle(surface, PURPLE, (15, 15), 15)
            # Draw a clock
            pygame.draw.circle(surface, WHITE, (15, 15), 10, 2)
            pygame.draw.line(surface, WHITE, (15, 15), (15, 8), 2)
            pygame.draw.line(surface, WHITE, (15, 15), (20, 15), 2)
        
        return surface
    
    def update(self):
        # Move power-up to the left (scrolling effect)
        self.rect.x -= self.speed
        
        # Remove if off-screen
        if self.rect.right < 0:
            self.kill() 