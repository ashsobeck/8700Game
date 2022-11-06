import pygame
import random


class Blocker():
    def __init__(self, window, snake_body: list[list[int, int]], width=960, height=640, block_size=32):
        # make blocker opaque
        self.image = pygame.image.load("icons/blocker.png").convert()
        self.image.set_alpha(255)

        self.window = window
        self.width = width
        self.height = height
        self.block_size = block_size
        self.snake_body = snake_body

        self.hit = False
        self.position = self.random_pos(self.snake_body)

    def draw(self):
        self.window.blit(self.image, self.rect)

    def clone(self):
        # make a clone
        block = Blocker(self.window, self.snake_body, self.width, self.height, self.block_size)
        return block

    def if_collision(self, snake: list[pygame.Rect]):
        if self.rect.colliderect(snake[0]):
            self.hit = True
            print('NOPE YOU DED')
        return self.hit

    # snake body should be coordinates of the snake
    def random_pos(self, snake_body: list[list[int, int]]):
        cells_x = self.width/self.block_size
        cells_y = self.height/self.block_size
        x, y = random.randint(0, cells_x - 1), random.randint(0, cells_y - 1)
        # generate random numbers until it's not in the snake if it appears
        while [x, y] in snake_body:
            x, y = random.randint(0, cells_x - 1), random.randint(0, cells_y-1)

        x *= self.block_size
        y *= self.block_size
        self.rect = pygame.Rect(x, y, self.block_size, self.block_size)
        return [x,y]
