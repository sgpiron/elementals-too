from game.settings import game_config

import textwrap
import openai
import pygame


def generate_assets():
    pass

def load_map():
    pass

def generate_text(messages):
    return openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )["choices"][0]["message"]["content"]

def display_story(screen, theme):
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

