import pygame
import numpy as np
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, player_id=1):
        super().__init__()
        self.player_id = player_id
        self.skin = "default"
        
        # Load player image
        self.load_images()
        self.image = self.animations["idle"][0]
        self.rect = self.image.get_rect(topleft=(x, y))
        
        # Movement variables
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = PLAYER_SPEED
        self.jump_power = PLAYER_JUMP_POWER
        self.gravity = PLAYER_GRAVITY
        self.on_ground = False
        
        # Animation variables
        self.animation_state = "idle"
        self.frame_index = 0
        self.animation_speed = 0.1
        self.facing_right = True
        
        # Dash variables
        self.can_dash = True
        self.dashing = False
        self.dash_time = 0
        self.dash_cooldown = PLAYER_DASH_COOLDOWN
        self.last_dash = 0
        
        # Power-up variables
        self.active_powerups = {}
        
        # Game variables
        self.score = 0
        self.coins = 0
        self.checkpoints = 0
        
    def load_images(self):
        # In a real game, you'd load actual sprite sheets
        # For this example, we'll create colored rectangles
        self.animations = {
            "idle": [self.create_player_surface()],
            "run": [self.create_player_surface() for _ in range(4)],
            "jump": [self.create_player_surface()],
            "dash": [self.create_player_surface()]
        }
    
    def create_player_surface(self):
        # Create a simple colored rectangle for the player
        surface = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT), pygame.SRCALPHA)
        color = RED if self.player_id == 1 else BLUE
        pygame.draw.rect(surface, color, (0, 0, PLAYER_WIDTH, PLAYER_HEIGHT), border_radius=10)
        return surface
    
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
    
    def jump(self):
        if self.on_ground:
            self.direction.y = -self.jump_power
            self.on_ground = False
            self.animation_state = "jump"
    
    def dash(self):
        current_time = pygame.time.get_ticks()
        if self.can_dash and current_time - self.last_dash >= self.dash_cooldown:
            self.dashing = True
            self.dash_time = current_time
            self.last_dash = current_time
            
            # Apply dash force in the direction player is facing
            dash_direction = 1 if self.facing_right else -1
            self.direction.x = PLAYER_DASH_POWER * dash_direction
            self.animation_state = "dash"
    
    def update_animation(self):
        # Update animation frame
        self.frame_index += self.animation_speed
        
        if self.frame_index >= len(self.animations[self.animation_state]):
            self.frame_index = 0
        
        image = self.animations[self.animation_state][int(self.frame_index)]
        
        # Flip image if facing left
        if self.facing_right:
            self.image = image
        else:
            self.image = pygame.transform.flip(image, True, False)
    
    def update_animation_state(self):
        if self.dashing:
            self.animation_state = "dash"
        elif self.direction.y < 0:
            self.animation_state = "jump"
        elif self.direction.x != 0:
            self.animation_state = "run"
        else:
            self.animation_state = "idle"
    
    def apply_powerup(self, powerup_type, duration):
        self.active_powerups[powerup_type] = {
            "start_time": pygame.time.get_ticks(),
            "duration": duration
        }
        
        # Apply power-up effects
        if powerup_type == "speed_boost":
            self.speed = PLAYER_SPEED * SPEED_BOOST_MULTIPLIER
        elif powerup_type == "high_jump":
            self.jump_power = PLAYER_JUMP_POWER * HIGH_JUMP_MULTIPLIER
    
    def update_powerups(self):
        current_time = pygame.time.get_ticks()
        expired_powerups = []
        
        for powerup_type, data in self.active_powerups.items():
            if current_time - data["start_time"] >= data["duration"]:
                expired_powerups.append(powerup_type)
        
        # Remove expired power-ups and reset their effects
        for powerup_type in expired_powerups:
            del self.active_powerups[powerup_type]
            
            if powerup_type == "speed_boost":
                self.speed = PLAYER_SPEED
            elif powerup_type == "high_jump":
                self.jump_power = PLAYER_JUMP_POWER
    
    def get_input(self):
        keys = pygame.key.get_pressed()
        
        # Player 1 controls
        if self.player_id == 1:
            if keys[pygame.K_a]:
                self.direction.x = -self.speed
                self.facing_right = False
            elif keys[pygame.K_d]:
                self.direction.x = self.speed
                self.facing_right = True
            else:
                self.direction.x = 0
                
            if keys[pygame.K_w]:
                self.jump()
                
            if keys[pygame.K_LSHIFT]:
                self.dash()
        
        # Player 2 controls
        elif self.player_id == 2:
            if keys[pygame.K_LEFT]:
                self.direction.x = -self.speed
                self.facing_right = False
            elif keys[pygame.K_RIGHT]:
                self.direction.x = self.speed
                self.facing_right = True
            else:
                self.direction.x = 0
                
            if keys[pygame.K_UP]:
                self.jump()
                
            if keys[pygame.K_RSHIFT]:
                self.dash()
    
    def update_dash_state(self):
        current_time = pygame.time.get_ticks()
        
        if self.dashing and current_time - self.dash_time >= 200:  # Dash lasts 200ms
            self.dashing = False
            self.direction.x = 0
    
    def update(self, platforms):
        self.get_input()
        self.update_dash_state()
        self.update_powerups()
        
        # Move horizontally
        self.rect.x += self.direction.x
        
        # Check for collisions with platforms
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # Horizontal collision
                if self.direction.x > 0:  # Moving right
                    self.rect.right = platform.rect.left
                elif self.direction.x < 0:  # Moving left
                    self.rect.left = platform.rect.right
        
        # Apply gravity and check for vertical collisions
        self.apply_gravity()
        
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # Vertical collision
                if self.direction.y > 0:  # Falling
                    self.rect.bottom = platform.rect.top
                    self.direction.y = 0
                    self.on_ground = True
                elif self.direction.y < 0:  # Jumping
                    self.rect.top = platform.rect.bottom
                    self.direction.y = 0
        
        # Keep player within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.direction.y = 0
            self.on_ground = True
        
        # Update animation state and frame
        self.update_animation_state()
        self.update_animation() 