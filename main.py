import pygame

# Init pygame
pygame.init()

WIDTH = 800
HEIGHT = 600

# set the screen size
screen = pygame.display.set_mode((WIDTH, HEIGHT))
background_image = pygame.image.load("icons/spider_webs.jpg")
# fit the image to the game size
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))


# set the icon and game name
pygame.display.set_caption("Haunted Ghost Snake")
icon = pygame.image.load("icons/scream.png")
pygame.display.set_icon(icon)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background_image, (0, 0))
    pygame.display.update()
