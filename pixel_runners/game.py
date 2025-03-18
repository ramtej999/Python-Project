import pygame
import sys
import numpy as np
from settings import *
from player import Player
from level import Level
from ui import UI
from leaderboard import Leaderboard
import os
import random

class Game:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        
        # Game state
        self.running = True
        self.game_state = "menu"  # menu, level_select, playing, game_over, leaderboard
        self.selected_option = 0
        self.selected_level = 0
        self.multiplayer = False
        
        # Game objects
        self.ui = UI()
        self.leaderboard = Leaderboard()
        self.players = []
        self.level = None
        
        # Menu options
        self.menu_options = ["Start Game", "Multiplayer", "Leaderboard", "Quit"]
        
        # Load assets
        self.load_assets()
        self.load_ui_assets()  # Call this method to load UI assets
    
    def load_assets(self):
        # Create directory structure if it doesn't exist
        os.makedirs("assets/images/backgrounds", exist_ok=True)
        os.makedirs("assets/images/characters", exist_ok=True)
        os.makedirs("assets/images/platforms", exist_ok=True)
        os.makedirs("assets/images/powerups", exist_ok=True)
        os.makedirs("assets/images/ui", exist_ok=True)
        os.makedirs("assets/sounds", exist_ok=True)
        
        # Create a simple background
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background.fill((100, 150, 255))  # Sky blue
        
        # Draw some simple clouds
        for _ in range(10):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT // 2)
            radius = random.randint(20, 50)
            pygame.draw.circle(self.background, WHITE, (x, y), radius)
    
    def load_ui_assets(self):
        self.start_button = pygame.image.load(os.path.join("assets", "images", "ui", "start_button.png")).convert_alpha()
        self.quit_button = pygame.image.load(os.path.join("assets", "images", "ui", "quit_button.png")).convert_alpha()
        self.menu_background = pygame.image.load(os.path.join("assets", "images", "ui", "menu_background.png")).convert_alpha()
        self.game_over_screen = pygame.image.load(os.path.join("assets", "images", "ui", "game_over.png")).convert_alpha()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if self.game_state == "menu":
                self.handle_menu_events(event)
            elif self.game_state == "level_select":
                self.handle_level_select_events(event)
            elif self.game_state == "playing":
                self.handle_playing_events(event)
            elif self.game_state == "game_over":
                self.handle_game_over_events(event)
            elif self.game_state == "leaderboard":
                self.handle_leaderboard_events(event)
    
    def handle_menu_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.start_button.get_rect(topleft=(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25)).collidepoint(mouse_pos):
                self.select_menu_option("start")
            elif self.quit_button.get_rect(topleft=(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 35)).collidepoint(mouse_pos):
                self.running = False
    
    def handle_level_select_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_level = (self.selected_level - 1) % len(LEVELS)
            elif event.key == pygame.K_DOWN:
                self.selected_level = (self.selected_level + 1) % len(LEVELS)
            elif event.key == pygame.K_RETURN:
                self.start_game()
            elif event.key == pygame.K_ESCAPE:
                self.game_state = "menu"
    
    def handle_playing_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game_state = "game_over"
    
    def handle_game_over_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Add scores to leaderboard
                for player in self.players:
                    self.leaderboard.add_score(f"Player {player.player_id}", player.score, self.level.name)
                self.game_state = "menu"
    
    def handle_leaderboard_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game_state = "menu"
    
    def select_menu_option(self, option):
        if option == "start":
            self.multiplayer = False
            self.game_state = "level_select"
        elif self.menu_options[self.selected_option] == "Multiplayer":
            self.multiplayer = True
            self.game_state = "level_select"
        elif self.menu_options[self.selected_option] == "Leaderboard":
            self.game_state = "leaderboard"
        elif self.menu_options[self.selected_option] == "Quit":
            self.running = False
    
    def start_game(self):
        # Create level
        self.level = Level(LEVELS[self.selected_level])
        
        # Create players
        self.players = []
        player1 = Player(100, SCREEN_HEIGHT - GROUND_HEIGHT - PLAYER_HEIGHT, 1)
        self.players.append(player1)
        
        if self.multiplayer:
            player2 = Player(200, SCREEN_HEIGHT - GROUND_HEIGHT - PLAYER_HEIGHT, 2)
            self.players.append(player2)
        
        self.game_state = "playing"
    
    def update(self):
        if self.game_state == "playing":
            # Update players
            for player in self.players:
                player.update(self.level.platforms)
            
            # Update level
            self.level.update(self.players)
            
            # Check if game is over (all players reached the end or fell off)
            game_over = True
            for player in self.players:
                if player.rect.right < SCREEN_WIDTH and player.rect.bottom < SCREEN_HEIGHT:
                    game_over = False
            
            if game_over:
                self.game_state = "game_over"
    
    def draw(self):
        self.screen.fill(BLACK)
        
        if self.game_state == "menu":
            self.draw_menu()
        elif self.game_state == "level_select":
            self.draw_level_select()
        elif self.game_state == "playing":
            self.draw_game()
        elif self.game_state == "game_over":
            self.draw_game()
            self.ui.draw_game_over(self.screen, self.players)
        elif self.game_state == "leaderboard":
            self.leaderboard.draw(self.screen)
        
        pygame.display.flip()
    
    def draw_menu(self):
        self.screen.blit(self.menu_background, (0, 0))  # Draw the menu background
        self.screen.blit(self.start_button, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25))  # Center the start button
        self.screen.blit(self.quit_button, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 35))  # Center the quit button
    
    def draw_level_select(self):
        # Draw background
        self.screen.fill((50, 50, 100))
        
        # Draw level options
        self.ui.draw_level_select(self.screen, LEVELS, self.selected_level)
    
    def draw_game(self):
        # Draw level
        self.level.draw(self.screen)
        
        # Draw players
        for player in self.players:
            self.screen.blit(player.image, player.rect)
        
        # Draw UI
        self.ui.draw_player_stats(self.screen, self.players)
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit() 