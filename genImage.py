from game.settings import game_config
from game.player import Player
from game.enemy import Enemy
from game.setup import *
import title_screen

import openai
import pygame
import sys
import random
import requests

# Temp settings
GENERATE = False

# Setup
openai.api_key = game_config.load_api_key()
THEME="Cold war spy movie set in Moscow"
THEME="1970s New York's Little Italy Mob"
PROMPT = THEME+" villan character in the style of a 90s video game"
response = openai.Image.create(
        prompt=PROMPT,
        n=1,
        size="256x256",
    )

img_url = response["data"][0]["url"]

response = requests.get(img_url)
if response.status_code:
        fp = open('villan.png', 'wb')
        fp.write(response.content)
        fp.close()
