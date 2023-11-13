import pygame


class Config:

    def __init__(self):
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
                "size": (self._game_settings["tile_size"], self._game_settings["tile_size"])
            },
            "wall": {
                "path": "wall.bmp",
                "map_char": "#",
                "size": (self._game_settings["tile_size"], self._game_settings["tile_size"])
            },
            "exit": {
                "path": "exit.bmp",
                "map_char": "*",
                "size": (self._game_settings["tile_size"], self._game_settings["tile_size"])
            },
            "story": {
                "path": "story.png",
                "size": (self._game_settings["screen_width"], self._game_settings["screen_height"]-400)
            },
            "hero_small": {
                "path": "hero.png",
                "size": (self._game_settings["tile_size"], self._game_settings["tile_size"])
            },
            "hero_big": {
                "path": "hero.png",
                "size": (self._game_settings["tile_size"]*4, self._game_settings["tile_size"]*4)
            },
            "enemy_1_small": {
                "path": "enemy_1.png",
                "size": (self._game_settings["tile_size"], self._game_settings["tile_size"])
            },
            "enemy_1_big": {
                "path": "enemy_1.png",
                "size": (self._game_settings["tile_size"]*4, self._game_settings["tile_size"]*4)
            },
            "enemy_2_small": {
                "path": "enemy_2.png",
                "size": (self._game_settings["tile_size"], self._game_settings["tile_size"])
            },
            "enemy_2_big": {
                "path": "enemy_2.png",
                "size": (self._game_settings["tile_size"]*4, self._game_settings["tile_size"]*4)
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