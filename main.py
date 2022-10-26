import pygame

# Init pygame
pygame.init()

WIDTH = 800
HEIGHT = 600
IMG_SIZE = 32

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

playerImg = pygame.image.load("icons/pumpkin.png")
HeadX = 400
HeadY = 500
HeadX_change = 0
HeadY_change = 0


def player(HeadX, HeadY):
    screen.blit(playerImg, (HeadX, HeadY))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                HeadX_change = -3
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                HeadX_change = 3
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                HeadY_change = -3
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                HeadY_change = 3

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                HeadX_change = 0
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                HeadX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                HeadY_change = 0
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                HeadY_change = 0

    screen.blit(background_image, (0, 0))

    HeadX += HeadX_change
    HeadY += HeadY_change
    if HeadX <= 0:
        HeadX = 0
    elif HeadX >= WIDTH - IMG_SIZE:
        HeadX = WIDTH - IMG_SIZE
    if HeadY <= 0:
        HeadY = 0
    elif HeadY >= HEIGHT - IMG_SIZE:
        HeadY = HEIGHT - IMG_SIZE
    player(HeadX, HeadY)
    # this means the game operates at 60 fps, just makes the movements smoother and not choppy
    clock.tick(60)
    pygame.display.update()
