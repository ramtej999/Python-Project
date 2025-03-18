import pygame
import random
import numpy as np
from settings import *
from player import Player
from obstacle import Obstacle, MovingObstacle
from powerup import PowerUp

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, platform_type="normal"):
        super().__init__()
        self.platform_type = platform_type
        self.image = self.create_platform_surface(width, height)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = SCROLL_SPEED
        
        # For breakable platforms
        self.durability = 3 if platform_type == "breakable" else -1
        
        # For disappearing platforms
        self.visible = True
        self.disappear_timer = 0
        self.blink_interval = 200  # milliseconds
        
    def create_platform_surface(self, width, height):
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        if self.platform_type == "normal":
            pygame.draw.rect(surface, GREEN, (0, 0, width, height))
        elif self.platform_type == "breakable":
            pygame.draw.rect(surface, YELLOW, (0, 0, width, height))
            # Add cracks
            for _ in range(3):
                start_x = random.randint(0, width-20)
                start_y = random.randint(0, height-5)
                end_x = start_x + random.randint(10, 20)
                end_y = start_y + random.randint(3, 5)
                pygame.draw.line(surface, BLACK, (start_x, start_y), (end_x, end_y), 2)
        elif self.platform_type == "disappearing":
            pygame.draw.rect(surface, BLUE, (0, 0, width, height))
            # Add pattern
            for x in range(0, width, 10):
                pygame.draw.line(surface, WHITE, (x, 0), (x, height), 1)
        
        return surface
    
    def update(self):
        # Move platform to the left (scrolling effect)
        self.rect.x -= self.speed
        
        # Handle disappearing platforms
        if self.platform_type == "disappearing":
            current_time = pygame.time.get_ticks()
            if current_time - self.disappear_timer > self.blink_interval:
                self.visible = not self.visible
                self.disappear_timer = current_time
                
                if not self.visible:
                    self.rect.y = SCREEN_HEIGHT + 100  # Move off-screen when invisible
                else:
                    self.rect.y -= SCREEN_HEIGHT + 100  # Move back when visible
        
        # Remove if off-screen
        if self.rect.right < 0:
            self.kill()
    
    def damage(self):
        if self.platform_type == "breakable":
            self.durability -= 1
            if self.durability <= 0:
                self.kill()

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = self.create_coin_surface()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = SCROLL_SPEED
        self.value = 10
        
    def create_coin_surface(self):
        surface = pygame.Surface((30, 30), pygame.SRCALPHA)  # Increase size
        pygame.draw.circle(surface, YELLOW, (15, 15), 15)  # Increase radius
        return surface
    
    def update(self):
        # Move coin to the left (scrolling effect)
        self.rect.x -= self.speed
        
        # Remove if off-screen
        if self.rect.right < 0:
            self.kill()

class Checkpoint(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.activated = False  # Initialize the activated attribute
        self.image = self.create_checkpoint_surface()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = SCROLL_SPEED
        self.value = 50
        
    def create_checkpoint_surface(self):
        surface = pygame.Surface((30, 80), pygame.SRCALPHA)
        # Ensure the color reflects the current state of activated
        color = WHITE if self.activated else GREEN
        pygame.draw.rect(surface, color, (0, 0, 10, 80))
        pygame.draw.polygon(surface, color, [(10, 0), (30, 15), (10, 30)])
        return surface
    
    def activate(self):
        if not self.activated:
            self.activated = True
            self.image = self.create_checkpoint_surface()  # Update the surface when activated
            return True
        return False
    
    def update(self):
        # Move checkpoint to the left (scrolling effect)
        self.rect.x -= self.speed
        
        # Remove if off-screen
        if self.rect.right < 0:
            self.kill()

class Level:
    def __init__(self, level_data):
        self.name = level_data["name"]
        self.background_image = level_data["background"]
        self.platform_density = level_data["platform_density"]
        self.obstacle_density = level_data["obstacle_density"]
        self.powerup_density = level_data["powerup_density"]
        self.scroll_speed = level_data["scroll_speed"]
        self.coin_density = level_data["coin_density"]
        
        # Set global scroll speed
        global SCROLL_SPEED
        SCROLL_SPEED = self.scroll_speed
        
        # Create sprite groups
        self.platforms = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.checkpoints = pygame.sprite.Group()
        
        # Level generation variables
        self.level_length = 10000  # pixels
        self.level_position = 0
        self.last_platform_x = 0
        self.ground_y = SCREEN_HEIGHT - GROUND_HEIGHT
        
        # Initialize background positions for parallax effect
        self.bg_positions = [0, SCREEN_WIDTH]  # Initialize bg_positions
        
        # Create the ground
        self.create_ground()
        
        # Generate initial level elements
        self.generate_level_segment(SCREEN_WIDTH * 2)
        
        # Background for parallax effect
        self.bg_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.bg_image.fill((100, 150, 255))  # Sky blue as fallback
        
        # Create a simple background based on level theme
        if "desert" in self.name.lower():
            self.bg_image.fill((230, 190, 100))  # Sandy color
        elif "ice" in self.name.lower():
            self.bg_image.fill((200, 230, 255))  # Light blue
        else:
            self.bg_image.fill((100, 180, 255))  # Sky blue
        
        # Add simple decorations
        for _ in range(20):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT // 2)
            size = random.randint(5, 15)
            color = (255, 255, 255, 150)  # Semi-transparent white
            pygame.draw.circle(self.bg_image, color, (x, y), size)
    
    def create_ground(self):
        # Create the ground platform
        ground = Platform(0, self.ground_y, SCREEN_WIDTH * 2, GROUND_HEIGHT, "normal")
        self.platforms.add(ground)
        self.last_platform_x = SCREEN_WIDTH * 2
    
    def generate_level_segment(self, width):
        x = self.last_platform_x
        while x < self.last_platform_x + width:
            if random.random() < self.platform_density:
                platform_width = random.randint(100, 300)
                platform_height = random.randint(20, 40)
                platform_y = random.randint(200, self.ground_y - 50)
                platform = Platform(x, platform_y, platform_width, platform_height)
                self.platforms.add(platform)

                # Add coins on the platform
                if random.random() < self.coin_density:  # Adjust coin density
                    for i in range(random.randint(3, 6)):  # Add multiple coins
                        coin_x = x + i * 25 + 10  # Space coins evenly
                        coin_y = platform_y - 30  # Place coins above the platform
                        coin = Coin(coin_x, coin_y)
                        self.coins.add(coin)

                x += platform_width + random.randint(100, 300)
            else:
                x += random.randint(100, 200)
        
        # Add checkpoints every 1000 pixels
        checkpoint_spacing = 1000
        checkpoint_start = (self.last_platform_x // checkpoint_spacing + 1) * checkpoint_spacing
        for x in range(checkpoint_start, self.last_platform_x + width, checkpoint_spacing):
            checkpoint = Checkpoint(x, self.ground_y - 80)
            self.checkpoints.add(checkpoint)
        
        # Add moving obstacles
        for _ in range(int((width / 1000) * self.obstacle_density * 5)):
            obstacle_x = self.last_platform_x + random.randint(0, width)
            obstacle_y = random.randint(100, self.ground_y - 100)
            obstacle_width = random.randint(30, 60)
            obstacle_height = random.randint(20, 40)
            vertical = random.choice([True, False])
            move_distance = random.randint(50, 150)
            move_speed = random.uniform(1, 3)
            
            moving_obstacle = MovingObstacle(
                obstacle_x, obstacle_y, obstacle_width, obstacle_height,
                "moving_platform", move_distance, move_speed, vertical
            )
            self.obstacles.add(moving_obstacle)
        
        self.last_platform_x += width
    
    def update(self, players):
        # Update all sprite groups
        self.platforms.update()
        self.obstacles.update()
        self.powerups.update()
        self.coins.update()
        self.checkpoints.update()
        
        # Generate more level if needed
        if self.last_platform_x - self.level_position < SCREEN_WIDTH * 2:
            self.generate_level_segment(SCREEN_WIDTH)
        
        # Update level position
        self.level_position += SCROLL_SPEED
        
        # Update background for parallax effect
        self.bg_positions[0] -= SCROLL_SPEED * 0.5
        self.bg_positions[1] -= SCROLL_SPEED * 0.5
        
        if self.bg_positions[0] <= -SCREEN_WIDTH:
            self.bg_positions[0] = self.bg_positions[1] + SCREEN_WIDTH
        if self.bg_positions[1] <= -SCREEN_WIDTH:
            self.bg_positions[1] = self.bg_positions[0] + SCREEN_WIDTH
        
        # Check collisions for each player
        for player in players:
            # Check collision with coins
            coin_collisions = pygame.sprite.spritecollide(player, self.coins, True)
            for coin in coin_collisions:
                player.score += coin.value
                player.coins += 1
            
            # Check collision with checkpoints
            checkpoint_collisions = pygame.sprite.spritecollide(player, self.checkpoints, False)
            for checkpoint in checkpoint_collisions:
                if checkpoint.activate():
                    player.score += checkpoint.value
                    player.checkpoints += 1
            
            # Check collision with power-ups
            powerup_collisions = pygame.sprite.spritecollide(player, self.powerups, True)
            for powerup in powerup_collisions:
                player.apply_powerup(powerup.powerup_type, powerup.duration)
            
            # Check collision with obstacles
            obstacle_collisions = pygame.sprite.spritecollide(player, self.obstacles, False)
            if obstacle_collisions:
                # Reset player position (simple collision handling)
                player.rect.x -= 50
                player.score -= 20  # Penalty for hitting obstacles
    
    def draw(self, screen):
        # Draw background with parallax effect
        screen.blit(self.bg_image, (self.bg_positions[0], 0))
        screen.blit(self.bg_image, (self.bg_positions[1], 0))
        
        # Draw all sprite groups
        self.platforms.draw(screen)
        self.obstacles.draw(screen)
        self.powerups.draw(screen)
        self.coins.draw(screen)
        self.checkpoints.draw(screen) 