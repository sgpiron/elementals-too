import requests
import openai
import pygame


class Config:

    def __init__(self):
        self.theme = "Yakuza world in Tokyo's Kabukicho district"
        self._RESOURCE_PATH = "game_resources"
        self._game_settings = {
            "screen_width": 800,
            "screen_height": 600,
            "screen_caption": "The Game",
            "tile_size": 40,
        }
        self._assets = {
            "cutscene": {
                "path": "cutscene.txt"
            },
            "map": {
                "path": "map.txt"
            },
            "floor": {
                "path": "floor.bmp",
                "map_char": ".",
                "size": (self._game_settings["tile_size"], self._game_settings["tile_size"]),
                "generation_size": "",
                "file_type": "bmp",
                "prompt": ""
            },
            "wall": {
                "path": "wall.bmp",
                "map_char": "#",
                "size": (self._game_settings["tile_size"], self._game_settings["tile_size"]),
                "generation_size": "",
                "file_type": "bmp",
                "prompt": ""
            },
            "exit": {
                "path": "exit.bmp",
                "map_char": "*",
                "size": (self._game_settings["tile_size"], self._game_settings["tile_size"]),
                "generation_size": "",
                "file_type": "bmp",
                "prompt": ""
            },
            "story": {
                "path": "story.png",
                "size": (self._game_settings["screen_width"], self._game_settings["screen_height"]-400),
                "generation_size": "256x256",
                "file_type": "png",
                "prompt": ""
            },
            "hero_small": {
                "path": "hero.png",
                "size": (self._game_settings["tile_size"], self._game_settings["tile_size"]),
                "generation_size": "256x256",
                "file_type": "png",
                "prompt": ""
            },
            "hero_big": {
                "path": "hero.png",
                "size": (self._game_settings["tile_size"]*4, self._game_settings["tile_size"]*4),
                "generation_size": "",
                "file_type": "png",
                "prompt": ""
            },
            "enemy_1_small": {
                "path": "enemy_1.png",
                "size": (self._game_settings["tile_size"], self._game_settings["tile_size"]),
                "generation_size": "256x256",
                "file_type": "png",
                "prompt": ""
            },
            "enemy_1_big": {
                "path": "enemy_1.png",
                "size": (self._game_settings["tile_size"]*4, self._game_settings["tile_size"]*4),
                "generation_size": "",
                "file_type": "png",
                "prompt": ""
            },
            "enemy_2_small": {
                "path": "enemy_2.png",
                "size": (self._game_settings["tile_size"], self._game_settings["tile_size"]),
                "generation_size": "256x256",
                "file_type": "png",
                "prompt": ""
            },
            "enemy_2_big": {
                "path": "enemy_2.png",
                "size": (self._game_settings["tile_size"]*4, self._game_settings["tile_size"]*4),
                "generation_size": "",
                "file_type": "png",
                "prompt": ""
            }
        }
        self.tilemap = self.load_map(self.get_asset_path("map"))

    def load_api_key(self, filename="openai-api.key"):
        with open(filename, "r") as f:
            return f.read().strip()

    def load_map(self, filename):
        with open(filename, "r") as f:
            lines = f.readlines()
        tilemap = []
        for line in lines:
            row = []
            for char in line.strip():
                row.append(char)
            tilemap.append(row)
        return tilemap
    
    def _call_image_generation(self, asset_name, asset_information):
        url = openai.Image.create(
            prompt=asset_information["prompt"],
            n=1,
            size=asset_information["size"]
        )["data"][0]["url"]
        response = requests.get(url)
        if response.status_code == 200:
            with open(self.get_asset_path(asset_name), "wb") as f:
                f.wrtie(response.content)
        else:
            raise RuntimeError(response)
    
    def generate_all_assets(self):
        for asset in self._assets:
            if "size" in self._assets[asset]:
                self._call_image_generation(asset, self._assets[asset])

    def get_setting(self, key):
        return self._game_settings[key]

    def get_asset_path(self, key):
        return f'{self._RESOURCE_PATH}/{self._assets[key]["path"]}'

    def get_asset_shape(self, key):
        return f'{self._RESOURCE_PATH}/{self._assets[key]["shape"]}'

    def get_asset_size(self, key):
        return self._assets[key]["size"]

    def get_asset_map_char(self, key):
        return self._assets[key]["map_char"]

    def get_asset_as_image(self, key):
        return pygame.transform.scale(pygame.image.load(self.get_asset_path(key)), self.get_asset_size(key))


game_config = Config()