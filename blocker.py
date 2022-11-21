import pygame
import random


class Blocker():
    def __init__(self, window, snake_body: list[list[int, int]], width=960,
                 height=640, block_size=32, position=[-1, -1]):
        # make blocker opaque
        self.image = pygame.image.load("icons/block.png").convert()
        self.image.set_alpha(255)

        self.window = window
        self.width = width
        self.height = height
        self.block_size = block_size
        self.snake_body = snake_body

        self.hit = False
        self.position = self.random_pos(self.snake_body)
        if -1 not in position:
            self.position = self.get_pos(position)

    def draw(self):
        self.window.blit(self.image, self.rect)

    def clone(self, x=-1, y=-1):
        # make a clone
        if x != -1 and y != -1:
            return Blocker(self.window, self.snake_body, self.width,
                           self.height, self.block_size, [x, y])
        block = Blocker(self.window, self.snake_body, self.width, self.height, self.block_size)
        return block

    def if_collision(self, snake: list[pygame.Rect]):
        if self.rect.colliderect(snake[0]):
            self.hit = True
            print('NOPE YOU DED')
        return self.hit

    def get_pos(self, position: list[int]):
        x, y = position
        x *= self.block_size
        y *= self.block_size

        self.rect = pygame.Rect(x, y, self.block_size, self.block_size)
        return [x, y]

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
        return [x, y]
