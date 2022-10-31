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
pumpkin_list = []
#create our first pumpkin
pumpkin_list.append(Pumpkin(window, snake))
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
        snake.draw_snake()
        #check if the snake collides with itself
        if snake.if_collision():
            pygame.quit()

        #make a copy before potentially modifying list of pumpkins
        pump_list_copy = pumpkin_list
        #for each pumpkin
        for pump in pumpkin_list:
            pump.draw()
            #pumpking checks if it has collided with the snake head
            create_new, destroy = pump.if_collision()
            #clone the pumpkin and randomly place it on the map
            if create_new:
                snake.score = snake.score + 1
                p = pump.clone()
                #add the new pumpking to the list
                pump_list_copy.append(p)
                #update the score of he difficulty and level in the json file
                high_score = information['level_highscores'][snake.current_level - 1][str(snake.difficulty)]
                if snake.score > high_score:
                    with open("information.json", "w") as j_file:
                        information['level_highscores'][snake.current_level - 1][str(snake.difficulty)] = snake.score
                        json.dump(information, j_file, indent=2)
        #if the eaten pumpkin has gone through the whole snake, remove from list
            if destroy:
                #removes specific class instance from list
                pump_list_copy.remove(pump)
        #reset pumpkin list
        pumpkin_list = pump_list_copy
    else:
        screens.draw_screen()

    #update the display
    pygame.display.update()

    # this means the game operates at 60 fps, just makes the movements smoother and not choppy
    clock.tick(60)

    if screens.game_start and not timer_set:
        pygame.time.set_timer(SCREEN_UPDATE, screens.difficulty)
        timer_set = True
