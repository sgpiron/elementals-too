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
            "floor": {
                "path": "floor.bmp",
                "size": (self._game_settings["tile_size"], self._game_settings["tile_size"])
            },
            "wall": {
                "path": "wall.bmp",
                "size": (self._game_settings["tile_size"], self._game_settings["tile_size"])
            },
            "exit": {
                "path": "exit.bmp",
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
            "villian_one_small": {
                "path": "villian_one.png",
                "size": (self._game_settings["tile_size"], self._game_settings["tile_size"])
            },
            "villian_one_big": {
                "path": "villian_one.png",
                "size": (self._game_settings["tile_size"]*4, self._game_settings["tile_size"]*4)
            },
            "villian_two_small": {
                "path": "villian_two.png",
                "size": (self._game_settings["tile_size"], self._game_settings["tile_size"])
            },
            "villian_two_big": {
                "path": "villian_two.png",
                "size": (self._game_settings["tile_size"]*4, self._game_settings["tile_size"]*4)
            }
        }

    def load_api_key(self, filename="openai-api.key"):
        with open(filename, "r") as f:
            return f.read().strip()

    def load_map(self, filename="map.txt"):
        with open(f'{self._RESOURCE_PATH}/{filename}', "r") as f:
            return f.readlines()

    def get_setting(self, key):
        return self._game_settings[key]

    def get_asset_path(self, key):
        return f'{self._RESOURCE_PATH}/{self._assets[key]["path"]}'

    def get_asset_shape(self, key):
        return f'{self._RESOURCE_PATH}/{self._assets[key]["shape"]}'

    def get_asset_size(self, key):
        return self._assets[key]["size"]

    def get_asset_as_image(self, key):
        return pygame.transform.scale(pygame.image.load(self.get_asset_path(key)), self.get_asset_size(key))


game_config = Config()