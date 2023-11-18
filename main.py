from game.settings import game_config
from game.player import Player
from game.enemy import Enemy
from game.setup import *

import openai
import pygame
import sys
import random


# Temp settings
GENERATE = False

# Setup
openai.api_key = game_config.load_api_key()
pygame.init()




def gpt4(premise):
    response=openai.ChatCompletion.create(
     model="gpt-4",
     messages=[
        {"role": "system", "content": "You are a video game designer."},
        {"role": "user", "content": "Write the text for 3 acts for a video game. Each act should be described in 500 characters or less,  describe the setting, the hero and the villain. The first act should establish the main characters, their relationships, and the world they live in.  The second act should depicts the hero’s attempt to resolve the problem initiated by the first turning point, only to find themselves in ever worsening situations. The third act features the resolution of the story. Return JSON with three values named ‘act1’, ‘act2’, and ‘act3’ that correspond to the three acts. The video game has the following theme'. Theme: "+premise} 
    ]
    )
    return response["choices"][0]["message"]["content"]

txt=gpt4(game_config.theme)
f = open("game_resources/cutscene.txt", "w")
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
    pygame.mixer.music.pause()victory(screen)           
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    # Create an all new theme for the game
    # if GENERATE:
    #     game_config.generate_all_assets()
    # Run the main loop
    game_loop()