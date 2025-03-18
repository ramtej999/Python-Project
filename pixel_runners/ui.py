import pygame
from settings import *

class UI:
    def __init__(self):
        self.font = pygame.font.SysFont('Arial', 24)
        self.title_font = pygame.font.SysFont('Arial', 48, bold=True)
        self.menu_font = pygame.font.SysFont('Arial', 36)
    
    def draw_player_stats(self, screen, players):
        for i, player in enumerate(players):
            # Player info background
            pygame.draw.rect(screen, BLACK, (20 + i * 400, 20, 350, 100), border_radius=10)
            pygame.draw.rect(screen, WHITE, (20 + i * 400, 20, 350, 100), width=2, border_radius=10)
            
            # Player name and score
            player_text = f"Player {player.player_id}"
            player_color = RED if player.player_id == 1 else BLUE
            player_name = self.font.render(player_text, True, player_color)
            screen.blit(player_name, (30 + i * 400, 30))
            
            # Score
            score_text = f"Score: {player.score}"
            score_surf = self.font.render(score_text, True, WHITE)
            screen.blit(score_surf, (30 + i * 400, 60))
            
            # Coins
            coins_text = f"Coins: {player.coins}"
            coins_surf = self.font.render(coins_text, True, YELLOW)
            screen.blit(coins_surf, (150 + i * 400, 60))
            
            # Checkpoints
            checkpoint_text = f"CP: {player.checkpoints}"
            checkpoint_surf = self.font.render(checkpoint_text, True, GREEN)
            screen.blit(checkpoint_surf, (250 + i * 400, 60))
            
            # Active power-ups
            powerup_y = 90
            for powerup_type in player.active_powerups:
                color = BLUE
                if powerup_type == "high_jump":
                    color = GREEN
                elif powerup_type == "slow_motion":
                    color = PURPLE
                
                powerup_text = f"{powerup_type.replace('_', ' ').title()}"
                powerup_surf = self.font.render(powerup_text, True, color)
                screen.blit(powerup_surf, (30 + i * 400, powerup_y))
                powerup_y += 25
    
    def draw_menu(self, screen, selected_option=0, options=None):
        if options is None:
            options = ["Start Game", "Multiplayer", "Leaderboard", "Quit"]
        
        # Title
        title_surf = self.title_font.render("PIXEL RUNNERS", True, WHITE)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH//2, 150))
        screen.blit(title_surf, title_rect)
        
        # Menu options
        for i, option in enumerate(options):
            color = YELLOW if i == selected_option else WHITE
            option_surf = self.menu_font.render(option, True, color)
            option_rect = option_surf.get_rect(center=(SCREEN_WIDTH//2, 300 + i * 60))
            screen.blit(option_surf, option_rect)
            
            # Draw selection indicator
            if i == selected_option:
                pygame.draw.rect(screen, YELLOW, option_rect.inflate(20, 10), width=3, border_radius=5)
    
    def draw_level_select(self, screen, levels, selected_level=0):
        # Title
        title_surf = self.title_font.render("SELECT LEVEL", True, WHITE)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH//2, 150))
        screen.blit(title_surf, title_rect)
        
        # Level options
        for i, level in enumerate(levels):
            color = YELLOW if i == selected_level else WHITE
            level_surf = self.menu_font.render(level["name"], True, color)
            level_rect = level_surf.get_rect(center=(SCREEN_WIDTH//2, 300 + i * 60))
            screen.blit(level_surf, level_rect)
            
            # Draw selection indicator
            if i == selected_level:
                pygame.draw.rect(screen, YELLOW, level_rect.inflate(20, 10), width=3, border_radius=5)
    
    def draw_game_over(self, screen, players):
        # Background overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        # Game Over text
        game_over_surf = self.title_font.render("GAME OVER", True, WHITE)
        game_over_rect = game_over_surf.get_rect(center=(SCREEN_WIDTH//2, 150))
        screen.blit(game_over_surf, game_over_rect)
        
        # Player scores
        for i, player in enumerate(players):
            player_text = f"Player {player.player_id}: {player.score} points"
            player_color = RED if player.player_id == 1 else BLUE
            player_surf = self.menu_font.render(player_text, True, player_color)
            player_rect = player_surf.get_rect(center=(SCREEN_WIDTH//2, 250 + i * 50))
            screen.blit(player_surf, player_rect)
        
        # Winner announcement for multiplayer
        if len(players) > 1:
            winner = max(players, key=lambda p: p.score)
            winner_text = f"Player {winner.player_id} Wins!"
            winner_color = RED if winner.player_id == 1 else BLUE
            winner_surf = self.menu_font.render(winner_text, True, winner_color)
            winner_rect = winner_surf.get_rect(center=(SCREEN_WIDTH//2, 350))
            screen.blit(winner_surf, winner_rect)
        
        # Continue prompt
        continue_surf = self.font.render("Press SPACE to continue", True, WHITE)
        continue_rect = continue_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 100))
        screen.blit(continue_surf, continue_rect)

    def create_player_surface(self):
        # Create a simple colored rectangle for the player
        surface = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT), pygame.SRCALPHA)
        color = RED if self.player_id == 1 else BLUE
        pygame.draw.rect(surface, color, (0, 0, PLAYER_WIDTH, PLAYER_HEIGHT), border_radius=10)
        return surface