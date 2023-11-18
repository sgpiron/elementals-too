# Player class
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

        self.x += dx
        self.y += dy

    def draw(self, screen):
        #pygame.draw.rect(screen, (255, 0, 0), (self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        screen.blit(HERO_IMG, (self.x * TILE_SIZE, self.y * TILE_SIZE))