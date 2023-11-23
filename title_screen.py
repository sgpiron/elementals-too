import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game with Options and Text Input")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
BLUE = (0,0,255)

# Define fonts
#font = pygame.font.Font(None, 32)
font = pygame.font.SysFont("nineteenninetyseven11xb", 16)

# Define the predefined options
options = ["Prompt> 'Yakuza world in Tokyo's Kabukicho district'", "Prompt> 'Cold war spy movie set in Moscow'", "Prompt> 'Gitty Mafia world in 1970s New York City'"]
option_rects = []

# Define text input variables
text = "Enter your own prompt: "
input_active = True
input_box = pygame.Rect(5, 150 + 40 *4, 140, 32)
text_color = WHITE

# Generate rectangles for options
for index, option in enumerate(options):
    option_rects.append(pygame.Rect(5, 150 + 40 * index, 635, 30))


def draw_options():
    for index, rect in enumerate(option_rects):
        pygame.draw.rect(screen, BLUE, rect,2)
        option_text = font.render(options[index], True, WHITE)
        screen.blit(option_text, (rect.x + 5, rect.y + 5))


def draw_text_input():
    
    pygame.draw.rect(screen, GREY, input_box, 2)
    txt_surf = font.render(text, True, text_color)
    screen.blit(txt_surf, (input_box.x + 5, input_box.y + 5))
    input_box.w = max(200, txt_surf.get_width() + 10)


def intro():
    global text, input_active
    input_active=True
    # Main loop
    running = True
    text=""
    while running:
        screen.fill(BLACK)
        screen.blit(pygame.image.load('game_resources/title.png'),(0,0))
        draw_options()
        draw_text_input()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    input_active = not input_active
                else:
                    for rect in option_rects:
                        if rect.collidepoint(event.pos):
                            print(f"You clicked {options[option_rects.index(rect)]}!")
                            return options[option_rects.index(rect)][8:]

    
            elif event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        print(f"Entered text: {text}")
                        return text
                        text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        pygame.display.flip()

#intro()

#pygame.quit()
#sys.exit()