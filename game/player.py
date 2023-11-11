class Player:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 100
        self.attack = 10
        self.defense = 5
        self.weapon = "knife"
        self.gold = 100
        self.items=["knife"]

    def move(self, dx, dy):
        # Check the tilemap to see if the move is onto a wall.
        if tilemap[self.y + dy][self.x + dx] == WALL:
            return
        # Update movement
        self.x += dx
        self.y += dy

    def draw(self, screen):
        #pygame.draw.rect(screen, (255, 0, 0), (self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        screen.blit(HERO_IMG, (self.x * TILE_SIZE, self.y * TILE_SIZE))

    def attack_enemy(self, enemy):
        damage = self.attack - (enemy.defense // 2)
        damage = max(1, damage)  # Ensure at least 1 damage is dealt
        enemy.health = max(0, enemy.health - damage)  # Ensure health does not go below 0
        print(f"Player attacks with {self.weapon} and deals {damage} damage!")