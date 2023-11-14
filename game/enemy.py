from game.settings import game_config
import random


class Enemy:
    
    def __init__(self, x, y, behavior, creature_type):
        self.x = x
        self.y = y
        self.behavior = behavior
        self.health = 80
        self.attack_strength = 8
        self.defense = 3
        self.weapon = "knife"
        self.gold = 10
        self.items = ["knife"]
        self.creature_type = creature_type
        self.small_image_asset = game_config.get_asset_as_image(f"enemy_{creature_type}_small")
        self.big_image_asset = game_config.get_asset_as_image(f"enemy_{creature_type}_big")

    def move_towards(self, target_x, target_y):
        if random.randint(0,3) == 3:
            return
    		
        if target_x > self.x:
            if game_config.tilemap[self.y][self.x + 1] == game_config.get_asset_map_char("wall"):
            	self.x=self.x
            else:
            	self.x += 1
        elif target_x < self.x:
            if game_config.tilemap[self.y][self.x-1] == game_config.get_asset_map_char("wall"):
            	self.x=self.x
            else:
	            self.x -= 1

        if target_y > self.y:
            if game_config.tilemap[self.y+1][self.x] == game_config.get_asset_map_char("wall"):
                self.y=self.y	
            else:
                self.y += 1
        elif target_y < self.y:
            if game_config.tilemap[self.y-1][self.x] == game_config.get_asset_map_char("wall"):
                self.y=self.y	
            else: 
                self.y -= 1

    def move_away_from(self, target_x, target_y):
        if target_x > self.x:
            self.x -= 1
        if target_y > self.y:
            self.y -= 1
        
    def update(self, player):
        if self.behavior == 'chase':
            self.move_towards(player.x, player.y)
        elif self.behavior == 'flee':
            self.move_away_from(player.x, player.y)

    def draw(self, screen):
        color = (0, 255, 0) if self.behavior == 'chase' else (0, 0, 255)
        screen.blit(self.small_image_asset, (self.x * game_config.get_setting("tile_size"), self.y * game_config.get_setting("tile_size")))
    
    def attack(self, player):
        damage = self.attack_strength - (player.defense // 2)
        damage = max(1, damage)
        player.health = max(0, player.health - damage)