from game.settings import game_config

import textwrap
import openai
import pygame


def generate_assets():
    [
        { "role": "system", "content": "Act as a professional story designer for an indy video game studio." },
        { "role": "system", "content": f"You are working on a rouge-like video game with the theme: {THEME}" },
        { "role": "user", "content": "Write the text for a cut scene in a video game. Specifically, in 500 characters or less, describe the setting, the hero, and the villan." },
    ]
    pass


def draw_map(screen):
    for y, row in enumerate(game_config.tilemap):
        for x, tile in enumerate(row):
            if tile == game_config.get_asset_map_char("wall"):
                screen.blit(game_config.get_asset_as_image("wall"), (x * game_config.get_setting("tile_size"), y * game_config.get_setting("tile_size")))
            elif tile == game_config.get_asset_map_char("floor"):
                screen.blit(game_config.get_asset_as_image("floor"), (x * game_config.get_setting("tile_size"), y * game_config.get_setting("tile_size")))
            elif tile == game_config.get_asset_map_char("exit"):
                screen.blit(game_config.get_asset_as_image("exit"), (x * game_config.get_setting("tile_size"), y * game_config.get_setting("tile_size")))


def generate_text(messages):
    return openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )["choices"][0]["message"]["content"]


def display_story(screen):
    # Get the story text
    with open(game_config.get_asset_path("cutscene"), "r") as f:
        story_text = f.read()
    story_text = textwrap.fill(story_text, 70)
    story_text = story_text.split("\n")
    # Display the story text
    screen.blit(game_config.get_asset_as_image("story"), (0, 0))
    font = pygame.font.SysFont('nineteenninetyseven11xb', 16)
    for i, line in enumerate(story_text):
        text = font.render(line, True, (255, 255, 255))
        screen.blit(text, (20, 300 + i * 40))
    pygame.display.flip()
    # Setup exit functionality
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        keys = pygame.key.get_pressed()
        if event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
            return


def display_stats(screen, character, text_location, image_location):
    font = pygame.font.SysFont('nineteenninetyseven11xb', 16)
    screen.blit(font.render(f"Health: {character.health}", True, (100, 100, 100)), (text_location[0], text_location[1]-200))
    screen.blit(font.render(f"Attack: {character.attack}", True, (100, 100, 100)), (text_location[0], text_location[1]-175))
    screen.blit(font.render(f"Defense: {character.defense}", True, (100, 100, 100)), (text_location[0], text_location[1]-150))
    screen.blit(font.render(f"Weapon: {character.weapon}", True, (100, 100, 100)), (text_location[0], text_location[1]-125))
    screen.blit(font.render(f"Gold: {character.gold}", True, (100, 100, 100)), (text_location[0], text_location[1]-100))
    screen.blit(character.big_image_asset, image_location)


def battle(player, enemy):
    pass


def handle_event(event, player, enemies):
    pass