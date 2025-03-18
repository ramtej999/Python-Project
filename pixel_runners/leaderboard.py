import pygame
import json
import os
from settings import *

class Leaderboard:
    def __init__(self):
        self.scores = []
        self.font = pygame.font.SysFont('Arial', 24)
        self.title_font = pygame.font.SysFont('Arial', 48, bold=True)
        self.file_path = "leaderboard.json"
        self.load_scores()
    
    def load_scores(self):
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r') as file:
                    self.scores = json.load(file)
                    # Sort scores in descending order
                    self.scores.sort(key=lambda x: x["score"], reverse=True)
        except Exception as e:
            print(f"Error loading leaderboard: {e}")
            self.scores = []
    
    def save_scores(self):
        try:
            with open(self.file_path, 'w') as file:
                json.dump(self.scores, file)
        except Exception as e:
            print(f"Error saving leaderboard: {e}")
    
    def add_score(self, player_name, score, level_name):
        # Add new score
        new_score = {
            "player_name": player_name,
            "score": score,
            "level": level_name,
            "date": pygame.time.get_ticks()  # Simple timestamp
        }
        
        self.scores.append(new_score)
        
        # Keep only top 10 scores
        self.scores.sort(key=lambda x: x["score"], reverse=True)
        self.scores = self.scores[:10]
        
        # Save updated scores
        self.save_scores()
    
    def draw(self, screen):
        # Background
        pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH//4, 100, SCREEN_WIDTH//2, SCREEN_HEIGHT - 200), border_radius=10)
        pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH//4, 100, SCREEN_WIDTH//2, SCREEN_HEIGHT - 200), width=2, border_radius=10)
        
        # Title
        title_surf = self.title_font.render("LEADERBOARD", True, WHITE)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH//2, 150))
        screen.blit(title_surf, title_rect)
        
        # Headers
        header_y = 200
        rank_header = self.font.render("Rank", True, YELLOW)
        screen.blit(rank_header, (SCREEN_WIDTH//4 + 30, header_y))
        
        name_header = self.font.render("Player", True, YELLOW)
        screen.blit(name_header, (SCREEN_WIDTH//4 + 100, header_y))
        
        score_header = self.font.render("Score", True, YELLOW)
        screen.blit(score_header, (SCREEN_WIDTH//4 + 250, header_y))
        
        level_header = self.font.render("Level", True, YELLOW)
        screen.blit(level_header, (SCREEN_WIDTH//4 + 350, header_y))
        
        # Draw line under headers
        pygame.draw.line(screen, WHITE, 
                         (SCREEN_WIDTH//4 + 20, header_y + 30), 
                         (SCREEN_WIDTH//4 + SCREEN_WIDTH//2 - 20, header_y + 30), 2)
        
        # Scores
        if not self.scores:
            no_scores = self.font.render("No scores yet!", True, WHITE)
            no_scores_rect = no_scores.get_rect(center=(SCREEN_WIDTH//2, 300))
            screen.blit(no_scores, no_scores_rect)
        else:
            for i, score_data in enumerate(self.scores):
                y_pos = 250 + i * 40
                
                # Rank
                rank_text = f"{i+1}."
                rank_surf = self.font.render(rank_text, True, WHITE)
                screen.blit(rank_surf, (SCREEN_WIDTH//4 + 30, y_pos))
                
                # Player name
                name_surf = self.font.render(score_data["player_name"], True, WHITE)
                screen.blit(name_surf, (SCREEN_WIDTH//4 + 100, y_pos))
                
                # Score
                score_surf = self.font.render(str(score_data["score"]), True, WHITE)
                screen.blit(score_surf, (SCREEN_WIDTH//4 + 250, y_pos))
                
                # Level
                level_surf = self.font.render(score_data["level"], True, WHITE)
                screen.blit(level_surf, (SCREEN_WIDTH//4 + 350, y_pos))
        
        # Back instruction
        back_text = self.font.render("Press ESC to return to menu", True, WHITE)
        back_rect = back_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 120))
        screen.blit(back_text, back_rect) 