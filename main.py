import pygame
import json
from Screens import Screens
from pumpkin import Pumpkin
from snake import Snake

# Init pygame
pygame.init()
pygame.font.init()

# 32 pixel images. 30 Cells in x direction, 20 cells in Y direction
WIDTH = 960
HEIGHT = 640
BLOCK_SIZE = 32

# set the window size
window = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

# set the icon and game name
pygame.display.set_caption("Haunted Ghost Snake")
icon = pygame.image.load("icons/scream.png")
pygame.display.set_icon(icon)

#keep track of prev color so we know what pixel color to look for when editing png files
#keep it in a json file so we can record it from instance to instance
with open("information.json", "r") as j:
    information = json.load(j)


#create our snek
snake = Snake(window, information, WIDTH, HEIGHT, BLOCK_SIZE)
screens = Screens(window, snake, information, WIDTH, HEIGHT, BLOCK_SIZE)
running = True

SCREEN_UPDATE = pygame.USEREVENT
timer_set = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == SCREEN_UPDATE:
            # when the timer goes off then move the snake
            snake.move_snake()
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and snake.direction != 'right':
                snake.next_direction = 'left'
            if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and snake.direction != 'left':
                snake.next_direction = 'right'
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and snake.direction != 'down':
                snake.next_direction = 'up'
            if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and snake.direction != 'up':
                snake.next_direction = 'down'

    window.blit(screens.background_image, (0, 0))

    if screens.game_start:
        #draw snek
        snake.draw_snake()

        # will check if the snake has eaten a pumpkin and will create
        # a new pumpkin as well as elongate the snake.
        # will also draw the pumpkins on the screen
        snake.if_eat_pumpkin()

        #check if the snake collides with itself or border
        if snake.if_death():
            pygame.quit()
    else:
        screens.draw_menu()

    #update the display
    pygame.display.update()

    # this means the game operates at 60 fps, just makes the movements smoother and not choppy
    clock.tick(60)

    if screens.game_start and not timer_set:
        pygame.time.set_timer(SCREEN_UPDATE, screens.difficulty)
        timer_set = True
