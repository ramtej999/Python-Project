# Game settings and constants
import pygame
import os

# Screen settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "Pixel Runners"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Player settings
PLAYER_SPEED = 10
PLAYER_JUMP_POWER = 30
PLAYER_GRAVITY = 0.8
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 80
PLAYER_DASH_POWER = 10
PLAYER_DASH_COOLDOWN = 1000  # milliseconds

# Level settings
GROUND_HEIGHT = 100
PLATFORM_SPEED = 2
SCROLL_SPEED = 3

# Power-up settings
POWERUP_DURATION = 5000  # milliseconds
SPEED_BOOST_MULTIPLIER = 1.5
HIGH_JUMP_MULTIPLIER = 1.3
SLOW_MOTION_FACTOR = 0.5

# Asset paths
ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets")
IMAGE_DIR = os.path.join(ASSET_DIR, "images")
SOUND_DIR = os.path.join(ASSET_DIR, "sounds")

# Character skins
CHARACTER_SKINS = {
    "default": "player_default.png",
    "ninja": "player_ninja.png",
    "robot": "player_robot.png",
    "astronaut": "player_astronaut.png"
}

# Level configurations
LEVELS = [
    {
        "name": "Green Hills",
        "background": "bg_hills.png",
        "platform_density": 0.1,
        "obstacle_density": 0.05,
        "powerup_density": 0.02,
        "scroll_speed": 3,
        "coin_density": 0.5
    },
    {
        "name": "Desert Run",
        "background": "bg_desert.png",
        "platform_density": 0.15,
        "obstacle_density": 0.08,
        "powerup_density": 0.03,
        "scroll_speed": 4,
        "coin_density": 0.5
    },
    {
        "name": "Ice Cave",
        "background": "bg_ice.png",
        "platform_density": 0.2,
        "obstacle_density": 0.1,
        "powerup_density": 0.04,
        "scroll_speed": 5,
        "coin_density": 0.5
    }
] 