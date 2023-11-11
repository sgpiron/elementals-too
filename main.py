from game.settings import game_config
from game.player import Player
from game.enemy import Enemy
from game.setup import *

import openai
import pygame


# Temp settings
GENERATE = True
THEME = "Star Trek-like universe"
PROMPT = THEME + " in a cinematic style"

# Setup
openai.api_key = game_config.load_api_key()
pygame.init()

# player = Player(1, 1)
# enemies = [Enemy(5, 5, 'chase',1), Enemy(8, 5, 'chase', 2)]

# Game loop
def game_loop():
    # Setup Screen
    screen = pygame.display.set_mode((game_config.get_setting("screen_width"), game_config.get_setting("screen_height")))
    pygame.display.set_caption(game_config.get_setting("screen_caption"))
    clock = pygame.time.Clock()
    # Display the initial story setup
    display_story(
        screen,
        [
            { "role": "system", "content": "Act as a professional story designer for an indy video game studio." },
            { "role": "system", "content": f"You are working on a rouge-like video game with the theme: {THEME}" },
            { "role": "user", "content": "Write the text for a cut scene in a video game. Specifically, in 500 characters or less, describe the setting, the hero, and the villan." },
        ]
    )


if __name__ == "__main__":
    game_loop()