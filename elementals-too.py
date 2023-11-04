import pygame
import sys
import requests
import textwrap
import os
import random
import openai


THEME= "Star Trek-like universe"
THEME= "Cold war spy movie set in Moscow"
THEME="alex krizhevsky must defeat the evil feature engineers"
THEME="Angry pumpkins, halloween themed game"
THEME= "Yakuza world in Tokyo's Kabukicho district"

PROMPT = THEME+" in the style of a 90s video game"

f = open("openai-api.key", "r")
key=f.read()
openai.api_key = key.replace("\n","")
response = openai.Image.create(
    prompt=PROMPT,
    n=1,
    size="256x256",
)

img_url = response["data"][0]["url"]

response = requests.get(img_url)
if response.status_code:
    fp = open('greenland_01a.png', 'wb')
    fp.write(response.content)
    fp.close()
    

    
PROMPT = THEME+" hero character in the style of a 90s video game"

response = openai.Image.create(
    prompt=PROMPT,
    n=1,
    size="256x256",
)

img_url = response["data"][0]["url"]

response = requests.get(img_url)
if response.status_code:
    fp = open('hero.png', 'wb')
    fp.write(response.content)
    fp.close()
    

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


# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 40
FIGHT = False

# Colors for different tiles (used as fallback if bitmaps fail)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

# Tile types
WALL = 1
FLOOR = 0
EXIT=-1

# Load tile images (and scale if needed)
FLOOR_IMG = pygame.transform.scale(pygame.image.load('floor.bmp'), (TILE_SIZE, TILE_SIZE))
WALL_IMG = pygame.transform.scale(pygame.image.load('wall.bmp'), (TILE_SIZE, TILE_SIZE))
EXIT_IMG = pygame.transform.scale(pygame.image.load('exit.bmp'), (TILE_SIZE, TILE_SIZE))
STORY_IMG = pygame.image.load('greenland_01a.png')
STORY_IMG = pygame.transform.scale(STORY_IMG, (SCREEN_WIDTH, SCREEN_HEIGHT-400))
HERO_IMG = pygame.image.load('hero.png')
HERO_IMG_BIG = pygame.transform.scale(HERO_IMG,(TILE_SIZE*4, TILE_SIZE*4))
HERO_IMG = pygame.transform.scale(HERO_IMG,(TILE_SIZE, TILE_SIZE))
VILLAN_IMG = pygame.image.load('villan.png')
VILLAN_IMG_BIG = pygame.transform.scale(VILLAN_IMG,(TILE_SIZE*4, TILE_SIZE*4))
VILLAN_IMG = pygame.transform.scale(VILLAN_IMG,(TILE_SIZE, TILE_SIZE))

# Load map from file
def load_map(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    new_tilemap = []
    for line in lines:
        row = []
        for char in line.strip():  # Remove the newline at the end
            if char == '#':
                row.append(WALL)
            elif char == '.':
                row.append(FLOOR)
            elif char == '*':
                row.append(EXIT)    
        new_tilemap.append(row)
    return new_tilemap

tilemap = load_map('path_to_your_map.txt')


tilemap=[]
for i in range(0,9):
     row=[]
     for j in range(0,20):
       row.append(FLOOR)
     tilemap.append(row)

for i in range(0,random.randint(15,30)):
	tilemap[random.randint(0,8)][random.randint(0,19)]=WALL

tilemap[random.randint(0,8)][random.randint(0,19)]=EXIT

def gpt4(premise):
    response=openai.ChatCompletion.create(
     model="gpt-4",
     messages=[
        {"role": "system", "content": "You are a video game designer."},
        {"role": "user", "content": "Write the text for a cut scene for a video game. In 500 characters or less,  describe the setting, the hero and the villan. The video game has the following theme'. Theme: "+premise} 
    ]
    )
    return response["choices"][0]["message"]["content"]


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

player = Player(1, 1)  # Starting position

# Drawing the map using tile images
def draw_map(screen):
    for y, row in enumerate(tilemap):
        for x, tile in enumerate(row):
            if tile == WALL:
                screen.blit(WALL_IMG, (x * TILE_SIZE, y * TILE_SIZE))
            elif tile == FLOOR:
                screen.blit(FLOOR_IMG, (x * TILE_SIZE, y * TILE_SIZE))
            elif tile == EXIT:
                screen.blit(EXIT_IMG, (x * TILE_SIZE, y * TILE_SIZE))


class Enemy:
    def __init__(self, x, y, behavior):
        self.x = x
        self.y = y
        self.behavior = behavior
        self.health = 80
        self.attack = 8
        self.defense = 3
        self.weapon = "knife"
        self.gold = 10
        self.items=["knife"]

    def move_towards(self, target_x, target_y):
        if random.randint(0,3) == 3:
            return
    		
        if target_x > self.x:
            if tilemap[self.y][self.x + 1] == WALL:
            	self.x=self.x
            else:
            	self.x += 1
        elif target_x < self.x:
            if tilemap[self.y][self.x-1] == WALL:
            	self.x=self.x
            else:
	            self.x -= 1

        if target_y > self.y:
            if tilemap[self.y+1][self.x] == WALL:
                self.y=self.y	
            else:
                self.y += 1
        elif target_y < self.y:
            if tilemap[self.y-1][self.x] == WALL:
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
        #pygame.draw.ellipse(screen, color, (self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        screen.blit(VILLAN_IMG, (self.x * TILE_SIZE, self.y * TILE_SIZE))


def display_story(screen):
    txt=gpt4(THEME)
    t=textwrap.fill(txt,70)
    story_text = t.split("\n")
	
    screen.blit(STORY_IMG, (0, 0))
    font = pygame.font.SysFont("nineteenninetyseven11xb", 16)  # Change font as desired

    for idx, line in enumerate(story_text):
        rendered_text = font.render(line, True, (255, 255, 255))
        screen.blit(rendered_text, (20, 300 + idx * 40))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:  # Any key or mouse click
                return


def display_hud(screen, player):
    print("draw hud")
    hud_height = 60
    pygame.draw.rect(screen, GRAY, (0, SCREEN_HEIGHT - hud_height, SCREEN_WIDTH, hud_height))

    font = pygame.font.SysFont("nineteenninetyseven11xb", 16)  # Change font as desired


    health_text = f"Health: {player.health}"
    attack_text = f"Attack: {player.attack}"
    defense_text = f"Defense: {player.defense}"
    weapon_text = f"Weapon: {player.weapon}"
    gold_text = f"Gold: {player.gold}"

    screen.blit(font.render(health_text, True, GRAY), (200, SCREEN_HEIGHT - 200))
    screen.blit(font.render(attack_text, True, GRAY), (200, SCREEN_HEIGHT - 175))
    screen.blit(font.render(defense_text, True, GRAY), (200, SCREEN_HEIGHT - 150))
    screen.blit(font.render(gold_text, True, GRAY), (200, SCREEN_HEIGHT - 125))
    screen.blit(font.render(weapon_text, True, GRAY), (200, SCREEN_HEIGHT - 100))
    screen.blit(HERO_IMG_BIG, (0, SCREEN_HEIGHT - 240))
    #if FIGHT:
    #    screen.blit(VILLAN_IMG_BIG, (SCREEN_WIDTH-240, SCREEN_HEIGHT - 240))  


# Main game loop
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Bitmap Roguelike')
    clock = pygame.time.Clock()

    display_story(screen)
	
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Bitmap Roguelike')
    clock = pygame.time.Clock()
    player = Player(1, 1) 
    enemies = [Enemy(5, 5, 'chase'),Enemy(8, 5, 'chase')]
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move(-1, 0)
                if event.key == pygame.K_RIGHT:
                    player.move(1, 0)
                if event.key == pygame.K_UP:
                    player.move(0, -1)
                if event.key == pygame.K_DOWN:
                    player.move(0, 1)
                for enemy in enemies:
   	                enemy.update(player)    

        screen.fill(BLACK)  # Default color for 'empty' space
        draw_map(screen)
        player.draw(screen)

        for enemy in enemies:
            if enemy.x == player.x and enemy.y==player.y:
                FIGHT=True
                print("fight")
                #display_hud(screen, player)
                #pygame.display.flip()
                font = pygame.font.SysFont("nineteenninetyseven11xb", 16)
                screen.blit(VILLAN_IMG_BIG, (SCREEN_WIDTH-180, SCREEN_HEIGHT - 240))  
                health_text = f"Health: {enemy.health}"
                attack_text = f"Attack: {enemy.attack}"
                defense_text = f"Defense: {enemy.defense}"
                weapon_text = f"Weapon: {enemy.weapon}"
                gold_text = f"Gold: {enemy.gold}"

                screen.blit(font.render(health_text, True, GRAY), (SCREEN_WIDTH-300, SCREEN_HEIGHT - 200))
                screen.blit(font.render(attack_text, True, GRAY), (SCREEN_WIDTH-300, SCREEN_HEIGHT - 175))
                screen.blit(font.render(defense_text, True, GRAY), (SCREEN_WIDTH-300, SCREEN_HEIGHT - 150))
                screen.blit(font.render(gold_text, True, GRAY), (SCREEN_WIDTH-300, SCREEN_HEIGHT - 125))
                screen.blit(font.render(weapon_text, True, GRAY), (SCREEN_WIDTH-300, SCREEN_HEIGHT - 100))

       	display_hud(screen, player)

        for enemy in enemies:
            enemy.draw(screen)
        
     
                 
        if tilemap[player.y][player.x] == EXIT:
              pygame.quit()
              sys.exit()

                     
        pygame.display.flip()

        clock.tick(60)

if __name__ == '__main__':
    main()
