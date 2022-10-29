import pygame
import random
from snake import Snake


class Pumpkin():
    def __init__(self, window, snake: Snake, width=960, height=640, block_size=32):

        #make the first pumpkin fully opaque
        self.image = pygame.image.load("icons/Pumpkin.png").convert()
        self.image.set_alpha(255)

        self.window = window
        #it keeps track of our snek so it knows when it has collided
        #since there can be multiple pumpkins at once, it's easier for it to keep track
        self.snake = snake
        self.width = width
        self.height = height
        self.block_size = block_size

        #will be true with pumpkin has collided with head of the snake
        self.eaten = False
        #will be set to true briefly when its needed to create new pumpking
        self.create_new = False
        # will be true when pumpkin has gone through body of the snake
        self.destroy = False

        #create a random position for the pumpkin
        self.position = self.random_pos()

    def draw(self):
        x = self.position[0] * self.block_size
        y = self.position[1] * self.block_size
        self.rect = pygame.Rect(x, y, self.block_size, self.block_size)
        self.window.blit(self.image, self.rect)

    def if_collision(self):
        if not self.eaten:
            #if it has collided with head of the snake
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
        pump = Pumpkin(self.window, self.snake, self.width, self.height, self.block_size)
        return pump

    def random_pos(self):
        cells_x = self.width/self.block_size
        cells_y = self.height/self.block_size
        x, y = random.randint(0, cells_x - 1), random.randint(0, cells_y - 1)
        # generate random numbers until it's not in the snake if it appears
        while [x, y] in self.snake.body:
            x, y = random.randint(0, cells_x - 1), random.randint(0, cells_y - 1)

        return [x, y]
