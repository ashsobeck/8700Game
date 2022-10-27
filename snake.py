import pygame


class Snake(pygame.sprite.Sprite):
    def __init__(self, screen, width, height, block_size):
        super().__init__()
        self.image = pygame.image.load("icons/pumpkin.png")
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

        if self.x <= 0:
            self.x = 0
        elif self.x >= self.width - self.block_size:
            self.x = self.width - self.block_size
        if self.y <= 0:
            self.y = 0
        elif self.y >= self.height - self.block_size:
            self.y = self.height - self.block_size
        self.screen.blit(self.image, (self.x, self.y))

    def change_direction(self, direction):
        if direction == 'left':
            self.x_change = -3
            self.y_change = 0
        elif direction == 'right':
            self.x_change = 3
            self.y_change = 0
        elif direction == 'up':
            self.x_change = 0
            self.y_change = -3
        else:
            self.x_change = 0
            self.y_change = 3
