from game.settings import game_config


class Player:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 100
        self.attack_strength = 25
        self.defense = 5
        self.weapon = "knife"
        self.gold = 100
        self.items = ["knife"]
        self.small_image_asset = game_config.get_asset_as_image(f"hero_small")
        self.big_image_asset = game_config.get_asset_as_image(f"hero_big")

    def move(self, dx, dy):
        # Check the tilemap to see if the move is onto a wall.
        if game_config.tilemap[self.y + dy][self.x + dx] == game_config.get_asset_map_char("wall"):
            return
        # Update movement
        self.x += dx
        self.y += dy

    def draw(self, screen):
        screen.blit(self.small_image_asset, (self.x * game_config.get_setting("tile_size"), self.y * game_config.get_setting("tile_size")))

    def attack(self, enemy):
        damage = self.attack_strength - (enemy.defense // 2)
        damage = max(1, damage)  # Ensure at least 1 damage is dealt
        enemy.health = max(0, enemy.health - damage)  # Ensure health does not go below 0