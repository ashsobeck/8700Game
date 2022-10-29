import pygame
from Screens import Screens
from pumpkin import Pumpkin
from snake import Snake

# Init pygame
pygame.init()

# 32 pixel images. 30 Cells in x direction, 20 cells in Y direction
WIDTH = 960
HEIGHT = 640
BLOCK_SIZE = 32
game_start = False

# set the window size
window = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

# set the icon and game name
pygame.display.set_caption("Haunted Ghost Snake")
icon = pygame.image.load("icons/scream.png")
pygame.display.set_icon(icon)

screens = Screens(window, WIDTH, HEIGHT)
#create our snek
snake = Snake(window, WIDTH, HEIGHT)
pumpkin_list = []
#create our first pumpkin
pumpkin_list.append(Pumpkin(window, snake))
running = True

SCREEN_UPDATE = pygame.USEREVENT
# set a timer to go off every 200 milliseconds


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == SCREEN_UPDATE:
            # when the timer goes off then move the snake
            snake.move_snake()
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and snake.direction != 'right' and game_start:
                snake.next_direction = 'left'
            if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and snake.direction != 'left' and game_start:
                snake.next_direction = 'right'
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and snake.direction != 'down' and game_start:
                snake.next_direction = 'up'
            if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and snake.direction != 'up' and game_start:
                snake.next_direction = 'down'

    window.blit(screens.background_image, (0, 0))
    if game_start:
        snake.draw_snake()
        #check if the snake collides with itself
        snake.if_collision()

        #make a copy before potentially modifying list of pumpkins
        pump_list_copy = pumpkin_list
        #for each pumpkin
        for pump in pumpkin_list:
            pump.draw()
            #pumpking checks if it has collided with the snake head
            create_new, destroy = pump.if_collision()
            #clone the pumpkin and randomly place it on the map
            if create_new:
                p = pump.clone()
                #add the new pumpking to the list
                pump_list_copy.append(p)
            #if the eaten pumpkin has gone through the whole snake, remove from list
            if destroy:
                #removes specific class instance from list
                pump_list_copy.remove(pump)
        #reset pumpkin list
        pumpkin_list = pump_list_copy
    else:
        screens.draw_home_buttons()
        screens.get_difficulty()

    #update the display
    pygame.display.update()

    # this means the game operates at 60 fps, just makes the movements smoother and not choppy
    clock.tick(60)

    if not game_start:
        game_start = screens.start_game()
        if game_start:
            pygame.time.set_timer(SCREEN_UPDATE, screens.difficulty)