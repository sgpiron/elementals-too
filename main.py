from distutils.command.sdist import sdist
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
pygame.init()

def genHeroImage():
    PROMPT =  game_config.theme+" hero character cinematic style"
    print(PROMPT)
    response = openai.Image.create(
        prompt=PROMPT,
        n=1,
        size="256x256",
    )

    img_url = response["data"][0]["url"]

    response = requests.get(img_url)
    if response.status_code:
        fp = open('game_resources/3/hero.png', 'wb')
        fp.write(response.content)
        fp.close()


def genVillainImages():
    PROMPT =  game_config.theme+" villain character cinematic style"

    response = openai.Image.create(
        prompt=PROMPT,
        n=5,
        size="256x256",
    )
 
    
    #yes this should be a loop, looked this up, need to convert the response payload into a dict (perhaps using JSON). Too Lazy to do. :)  

    img_url = response["data"][0]["url"]

    rp = requests.get(img_url)
    if rp.status_code:
        fp = open('game_resources/3/villain'+str(0)+'.png', 'wb')
        fp.write(rp.content)
        fp.close()
    
    img_url = response["data"][1]["url"]

    rp = requests.get(img_url)
    if rp.status_code:
        fp = open('game_resources/3/villain'+str(1)+'.png', 'wb')
        fp.write(rp.content)
        fp.close()

    img_url = response["data"][2]["url"]

    rp = requests.get(img_url)
    if rp.status_code:
        fp = open('game_resources/3/villain'+str(2)+'.png', 'wb')
        fp.write(rp.content)
        fp.close()

def scaleImages():
    TILE_SIZE=game_config._game_settings["tile_size"]
    print(TILE_SIZE)
    print(game_config.get_asset_path("hero_small"))
    HERO_IMG = pygame.image.load(game_config.get_asset_path("hero_small"))
    game_config._assets["hero_big"]["path"] = pygame.transform.scale(HERO_IMG,(TILE_SIZE*4, TILE_SIZE*4))
    print(game_config.get_asset_path("hero_big"))
    '''VILLAN_IMG = pygame.image.load('game_resources/enemy_1.png')
    VILLAN_IMG_BIG = pygame.transform.scale(VILLAN_IMG,(TILE_SIZE*4, TILE_SIZE*4))
    VILLAN_IMG = pygame.transform.scale(VILLAN_IMG,(TILE_SIZE, TILE_SIZE))
    VILLAN_IMG2 = pygame.image.load('game_resources/villan2.png')
    VILLAN_IMG_BIG2 = pygame.transform.scale(VILLAN_IMG2,(TILE_SIZE*4, TILE_SIZE*4))
    VILLAN_IMG2 = pygame.transform.scale(VILLAN_IMG2,(TILE_SIZE, TILE_SIZE))'''

def gpt4(premise):
    response=openai.ChatCompletion.create(
     model="gpt-4",
     messages=[
        {"role": "system", "content": "You are a video game designer."},
        {"role": "user", "content": "Write the text for 3 acts for a video game. Each act should be described in 500 characters or less,  describe the setting, the hero and the villain. The first act should establish the main characters, their relationships, and the world they live in.  The second act should depicts the hero’s attempt to resolve the problem initiated by the first turning point, only to find themselves in ever worsening situations. The third act features the resolution of the story. Return JSON with three values named ‘act1’, ‘act2’, and ‘act3’ that correspond to the three acts. The video game has the following theme'. Theme: "+premise} 
    ]
    )
    return response["choices"][0]["message"]["content"]

def genStory():
    txt=gpt4(game_config.theme)
    f = open("game_resources/cutscene.json", "w")
    f.write(txt)
    f.close()

# Game loop
def game_loop():
    # Setup the story screen
    screen = pygame.display.set_mode((game_config.get_setting("screen_width"), game_config.get_setting("screen_height")))
    pygame.display.set_caption(game_config.get_setting("screen_caption"))
    clock = pygame.time.Clock()

    # Display the story on the screen
    
    for act in ['act1','act2','act3']:

        
        game_config.tilemap=game_config.load_map("")

        # Setup the game screen
        screen = pygame.display.set_mode((game_config.get_setting("screen_width"), game_config.get_setting("screen_height")))
        pygame.display.set_caption(game_config.get_setting("screen_caption"))
        clock = pygame.time.Clock()

        display_story(screen,act)    

        # Setup the characters
        player = Player(1, 1)
        #enemies = [Enemy(1, 5, 'chase', 1), Enemy(8, 5, 'chase', 2)]
        enemies=[]
        for n in range(0,random.randint(2,6)):
            enemies.append(Enemy(random.randint(1,10),random.randint(2,10),'chase',random.randint(1,2)))
        # Event loop

        pygame.mixer.init()  # Initialize the mixer module.
        pygame.mixer.music.load('./game_resources/bg_music.mp3')
        pygame.mixer.music.play(-1,0.0)  

        while True:
            # Handle events
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

            # Draw the screen
            screen.fill((0, 0, 0))
            draw_map(screen)
            player.draw(screen)

            # Check if the enemied have caught the player
            for enemy in enemies:
                if enemy.x == player.x and enemy.y == player.y:
                    screen.blit(enemy.big_image_asset, (game_config.get_setting("screen_width") - 180, game_config.get_setting("screen_height") - 240))
                    display_stats(
                        screen, 
                        enemy, 
                        (game_config.get_setting("screen_width") - 300, game_config.get_setting("screen_height")),
                        (game_config.get_setting("screen_width") - 180, game_config.get_setting("screen_height") - 240)
                    )
                    outcome = battle(player, enemy)
                    if outcome == 0:
                        enemies.remove(enemy)
                    elif outcome == 1:
                        print("ya dead!")
                        screen = pygame.display.set_mode((game_config.get_setting("screen_width"), game_config.get_setting("screen_height")))
                        pygame.display.set_caption(game_config.get_setting("screen_caption"))
                        pygame.mixer.music.pause()
                        gameover(screen)   
            
            # Display the player stats
            display_stats(screen, player, (200, game_config.get_setting("screen_height")), (0, game_config.get_setting("screen_height") - 240))

            # Draw the enemies
            for enemy in enemies:
                enemy.draw(screen)

            # Exit if player is on the exit tile
            if game_config.tilemap[player.y][player.x] == game_config.get_asset_map_char("exit"):
                #next level:
                
                pygame.mixer.music.pause()
                pygame.mixer.init()  # Initialize the mixer module.
                sound1 = pygame.mixer.Sound('./game_resources/exit.mp3')
                sound1.play()  
                break
                

            pygame.display.flip()
            clock.tick(60)
    screen = pygame.display.set_mode((game_config.get_setting("screen_width"), game_config.get_setting("screen_height")))
    pygame.display.set_caption(game_config.get_setting("screen_caption"))
    pygame.mixer.music.pause()
    victory(screen)           
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    # Create an all new theme for the game
    # if GENERATE:
    #     game_config.generate_all_assets()
    # Run the main loop
    
    prompt=title_screen.intro()
    print("loop")
    print(prompt)
    game_config.theme=prompt
    if prompt=="'Yakuza world in Tokyo's Kabukicho district'":
        game_config._assets["cutscene"]["path"]="0/cutscene.json"
        print(game_config._assets["cutscene"]["path"])
    elif prompt=="'Cold war spy movie set in Moscow'":
        game_config._assets["cutscene"]["path"]="1/cutscene.json"
        print(game_config._assets["cutscene"]["path"])
        game_config.theme="1980s Cold war spy movie set in eastern europe"
        #genHeroImage()
        #genVillainImages() 
        game_config._assets["hero_small"]["path"]="1/hero.png"
        game_config._assets["enemy_1_small"]["path"]="1/villain0.png"
        game_config._assets["enemy_2_small"]["path"]="1/villain1.png"
        game_config._assets["hero_big"]["path"]="1/hero.png"
        game_config._assets["enemy_1_big"]["path"]="1/villain0.png"
        game_config._assets["enemy_2_big"]["path"]="1/villain1.png"
    elif prompt=="'Gritty Mafia world in 1970s New York City'":
        game_config._assets["cutscene"]["path"]="2/cutscene.json"
        print(game_config._assets["cutscene"]["path"])  
        #game_config.theme="1970s New York italian gangster"
        #genHeroImage() 
        #genVillainImages() 
        game_config._assets["hero_small"]["path"]="2/hero.png"
        game_config._assets["enemy_1_small"]["path"]="2/villain0.png"
        game_config._assets["enemy_2_small"]["path"]="2/villain1.png"
        game_config._assets["hero_big"]["path"]="2/hero.png"
        game_config._assets["enemy_1_big"]["path"]="2/villain0.png"
        game_config._assets["enemy_2_big"]["path"]="2/villain1.png"
        #scaleImages()
    else:
        genStory()
        genHeroImage() 
        genVillainImages() 
        game_config._assets["hero_small"]["path"]="3/hero.png"
        game_config._assets["enemy_1_small"]["path"]="3/villain0.png"
        game_config._assets["enemy_2_small"]["path"]="3/villain1.png"
        game_config._assets["hero_big"]["path"]="3/hero.png"
        game_config._assets["enemy_1_big"]["path"]="3/villain0.png"
        game_config._assets["enemy_2_big"]["path"]="3/villain1.png"
    #getStory()
    game_loop()