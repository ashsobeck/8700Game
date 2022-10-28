import pygame
import random
from snake import Snake


class Pumpkin():
    def __init__(self, screen, snake: Snake, width=960, height=640, block_size=32):

        self.image = pygame.image.load("icons/Pumpkin.png").convert()
        self.image.set_alpha(255)
        self.screen = screen
        self.snake = snake
        self.width = width
        self.height = height
        self.block_size = block_size
        self.position = self.random_pos()
        self.eaten = False
        #will eb set to true briefly when its needed to create new pumpking
        self.create_new = False
        self.destroy = False

    def draw(self):
        x = self.position[0] * self.block_size
        y = self.position[1] * self.block_size
        self.rect = pygame.Rect(x, y, self.block_size, self.block_size)
        self.screen.blit(self.image, self.rect)

    def if_collision(self):
        if not self.eaten:
            if self.rect.colliderect(self.snake.rect[0]):
                # add some transparency
                self.image.set_alpha(100)
                print("YES SIR EAT THAT PUMPKIN")
                self.snake.new_body = True
                self.eaten = True
                self.create_new = True
        else:
            #setting this back to false ensure that only 1 pumpkin is created
            self.create_new = False
            #once pumpkin has passed through snake, every collision with snake body will return false
            if not (True in [self.rect.colliderect(rect) for rect in self.snake.rect]):
                self.destroy = True

        return self.create_new, self.destroy

    def clone(self):
        # make a clone
        pump = Pumpkin(self.screen, self.snake, self.width, self.height, self.block_size)
        return pump

    def random_pos(self):
        cells_x = self.width/self.block_size
        cells_y = self.height/self.block_size
        x, y = random.randint(0, cells_x - 1), random.randint(0, cells_y - 1)
        # generate random numbers until it's not in the snake if it appears
        while [x, y] in self.snake.body:
            x, y = random.randint(0, cells_x - 1), random.randint(0, cells_y - 1)

        return [x, y]
