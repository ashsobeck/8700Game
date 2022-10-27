import pygame


class Snake(pygame.sprite.Sprite):
    def __init__(self, screen, width, height, block_size):
        super().__init__()
        self.snake_up = pygame.image.load("icons/Snake_Head_Up.png")
        self.snake_down = pygame.image.load("icons/Snake_Head_Down.png")
        self.snake_right = pygame.image.load("icons/Snake_Head_Right.png")
        self.snake_left = pygame.image.load("icons/Snake_Head_Left.png")
        self.screen = screen
        self.x = 300
        self.y = 300
        self.width = width
        self.height = height
        self.block_size = block_size
        self.x_change = block_size
        self.y_change = 0
        self.direction = 'right'

    def draw(self):
        self.x += self.x_change
        self.y += self.y_change

        # stop snek from going out of bounds
        if self.x <= 0:
            self.x = 0
        elif self.x >= self.width - self.block_size:
            self.x = self.width - self.block_size
        if self.y <= 0:
            self.y = 0
        elif self.y >= self.height - self.block_size:
            self.y = self.height - self.block_size

        # draw snek orientation based off of head location
        if self.direction == 'left':
            self.screen.blit(self.snake_left, (self.x, self.y))
        elif self.direction == 'right':
            self.screen.blit(self.snake_right, (self.x, self.y))
        elif self.direction == 'down':
            self.screen.blit(self.snake_down, (self.x, self.y))
        else:
            self.screen.blit(self.snake_up, (self.x, self.y))

    def change_direction(self, direction):
        if direction == 'left':
            self.direction = 'left'
            self.x_change = -3
            self.y_change = 0
        elif direction == 'right':
            self.direction = 'right'
            self.x_change = 3
            self.y_change = 0
        elif direction == 'up':
            self.direction = 'up'
            self.x_change = 0
            self.y_change = -3
        else:
            self.direction = 'down'
            self.x_change = 0
            self.y_change = 3
