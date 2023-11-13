from game.settings import game_config
from game.player import Player
from game.enemy import Enemy
from game.setup import *

import openai
import pygame
import sys


# Temp settings
GENERATE = True
THEME = "Star Trek-like universe"
PROMPT = THEME + " in a cinematic style"

# Setup
openai.api_key = game_config.load_api_key()
pygame.init()

# Game loop
def game_loop():
    # Setup the story screen
    screen = pygame.display.set_mode((game_config.get_setting("screen_width"), game_config.get_setting("screen_height")))
    pygame.display.set_caption(game_config.get_setting("screen_caption"))
    clock = pygame.time.Clock()

    # Display the story on the screen
    display_story(screen)

    # Setup the game screen
    screen = pygame.display.set_mode((game_config.get_setting("screen_width"), game_config.get_setting("screen_height")))
    pygame.display.set_caption(game_config.get_setting("screen_caption"))
    clock = pygame.time.Clock()

    # Setup the characters
    player = Player(1, 1)
    enemies = [Enemy(1, 5, 'chase', 1), Enemy(8, 5, 'chase', 2)]

    # Event loop
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move(-1, 0)
                if event.key == pygame.K_RIGHT:
                    player.move(1, 0)
                if event.key == pygame.K_UP:
                    player.move(0, -1)
                if event.key == pygame.K_DOWN:
                    player.move(0, 1)
                for enemy in enemies:
   	                enemy.update(player)

        # Draw the screen
        screen.fill((0, 0, 0))
        draw_map(screen)
        player.draw(screen)

        # Check if the enemied have caught the player
        for enemy in enemies:
            if enemy.x == player.x and enemy.y == player.y:
                screen.blit(enemy.big_image_asset, (game_config.get_setting("screen_width") - 180, game_config.get_setting("screen_height") - 240))
                display_stats(
                    screen, 
                    enemy, 
                    (game_config.get_setting("screen_width") - 300, game_config.get_setting("screen_height")),
                    (game_config.get_setting("screen_width") - 180, game_config.get_setting("screen_height") - 240)
                )
                outcome = battle(player, enemy)
                if outcome == 0:
                    enemies.remove(enemy)
        
        # Display the player stats
        display_stats(screen, player, (200, game_config.get_setting("screen_height")), (0, game_config.get_setting("screen_height") - 240))

        # Draw the enemies
        for enemy in enemies:
            enemy.draw(screen)

        # Exit if player is on the exit tile
        if game_config.tilemap[player.y][player.x] == game_config.get_asset_map_char("exit"):
            pygame.quit()
            sys.exit()

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    game_loop()