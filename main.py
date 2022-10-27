import pygame
from snake import Snake

# Init pygame
pygame.init()

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


s = Snake(screen, WIDTH, HEIGHT, BLOCK_SIZE)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                s.change_direction('left')
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                s.change_direction('right')
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                s.change_direction('up')
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                s.change_direction('down')

    screen.blit(background_image, (0, 0))
    s.draw()
    # this means the game operates at 60 fps, just makes the movements smoother and not choppy
    clock.tick(60)
    pygame.display.update()
