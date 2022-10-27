import pygame
from snake import Snake

# Init pygame
pygame.init()

# 32 pixel images. 30 Cells in x direction, 20 cells in Y direction
WIDTH = 960
HEIGHT = 640
BLOCK_SIZE = 32

# set the screen size
screen = pygame.display.set_mode((WIDTH, HEIGHT))
background_image = pygame.image.load("icons/spider_webs.jpg")
# fit the image to the game size
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
clock = pygame.time.Clock()


# set the icon and game name
pygame.display.set_caption("Haunted Ghost Snake")
icon = pygame.image.load("icons/scream.png")
pygame.display.set_icon(icon)

snake = Snake(screen, WIDTH, HEIGHT)
running = True

SCREEN_UPDATE = pygame.USEREVENT
# set a timer to go off every 200 milliseconds
pygame.time.set_timer(SCREEN_UPDATE, 200)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == SCREEN_UPDATE:
            # when the timer goes off then move the snake
            snake.move_snake()
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and snake.direction != 'right':
                snake.direction = 'left'
            if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and snake.direction != 'left':
                snake.direction = 'right'
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and snake.direction != 'down':
                snake.direction = 'up'
            if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and snake.direction != 'up':
                snake.direction = 'down'

    screen.blit(background_image, (0, 0))
    snake.draw_snake()
    pygame.display.update()
    # this means the game operates at 60 fps, just makes the movements smoother and not choppy
    clock.tick(60)
