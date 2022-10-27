import pygame

BLOCK_SIZE = 32


class Snake():
    def __init__(self, screen, width, height):

        self.screen = screen
        # keep track of all the snake parts
        self.head_up = pygame.image.load("icons/Snake_Head_Up.png")
        self.head_down = pygame.image.load("icons/Snake_Head_Down.png")
        self.head_right = pygame.image.load("icons/Snake_Head_Right.png")
        self.head_left = pygame.image.load("icons/Snake_Head_Left.png")

        self.body_hori = pygame.image.load("icons/Snake_Body_Hori.png")
        self.body_vert = pygame.image.load("icons/Snake_Body_Vert.png")

        self.tail_right = pygame.image.load("icons/Snake_Tail_R.png")
        self.tail_left = pygame.image.load("icons/Snake_Tail_L.png")
        self.tail_down = pygame.image.load("icons/Snake_Tail_D.png")
        self.tail_up = pygame.image.load("icons/Snake_Tail_U.png")

        self.body_tr = pygame.image.load("icons/Snake_Corner_TR.png")
        self.body_tl = pygame.image.load("icons/Snake_Corner_TL.png")
        self.body_br = pygame.image.load("icons/Snake_Corner_BR.png")
        self.body_bl = pygame.image.load("icons/Snake_Corner_BL.png")

        self.direction = 'right'
        # the body keeps track of the positon of each body part
        # for simplicity we will keep track of what cell its in
        self.body = [[15, 10], [14, 10], [13, 10], [12, 10]]
        self.width = width
        self.height = height

    def draw_snake(self):
        self.update_head()
        self.update_tail()

        for index, block in enumerate(self.body):
            x = block[0] * BLOCK_SIZE
            y = block[1] * BLOCK_SIZE
            # create rectangle around block object. This is for collisions
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)

            if index == 0:
                self.screen.blit(self.head, rect)
            elif index == self.body.__len__() - 1:
                self.screen.blit(self.tail, rect)
            else:
                prev_block = self.subtract_positions(
                    self.body[index + 1], block)
                next_block = self.subtract_positions(
                    self.body[index - 1], block)

                # body positions
                if prev_block[0] == next_block[0]:
                    self.screen.blit(self.body_vert, rect)
                elif prev_block[1] == next_block[1]:
                    self.screen.blit(self.body_hori, rect)
                else:
                    # corners
                    if prev_block[0] == -1 and next_block[1] == -1 or prev_block[1] == -1 and next_block[0] == -1:
                        self.screen.blit(self.body_tl, rect)
                    elif prev_block[0] == -1 and next_block[1] == 1 or prev_block[1] == 1 and next_block[0] == -1:
                        self.screen.blit(self.body_bl, rect)
                    elif prev_block[0] == 1 and next_block[1] == -1 or prev_block[1] == -1 and next_block[0] == 1:
                        self.screen.blit(self.body_tr, rect)
                    elif prev_block[0] == 1 and next_block[1] == 1 or prev_block[1] == 1 and next_block[0] == 1:
                        self.screen.blit(self.body_br, rect)

    def update_head(self):
        if self.direction == 'right':
            self.head = self.head_right
        elif self.direction == 'left':
            self.head = self.head_left
        elif self.direction == 'up':
            self.head = self.head_up
        else:
            self.head = self.head_down

    def update_tail(self):
        # take the cell values of the block beside the tail minues the tail
        tail = self.subtract_positions(self.body[-2], self.body[-1])
        if tail[0] == 1:
            self.tail = self.tail_right
        elif tail[0] == -1:
            self.tail = self.tail_left
        elif tail[1] == -1:
            self.tail = self.tail_up
        else:
            self.tail = self.tail_down

    def subtract_positions(self, first_list: list, second_list: list) -> list:
        final_position = []
        # zip allows us to iterate over bost lists at the same time
        for a, b in zip(first_list, second_list):
            final_position.append(a - b)
        return final_position

    def move_snake(self):
        # get every element except the last one since it dissappears
        copy = self.body[:-1]
        front = self.body[0]
        if self.direction == 'left':
            # move head one block to left in x direction
            copy.insert(0, [front[0] - 1, front[1]])
        elif self.direction == 'right':
            # move head one block to right in x direction
            copy.insert(0, [front[0] + 1, front[1]])
        elif self.direction == 'down':
            # move head one block down in y direction
            copy.insert(0, [front[0], front[1] + 1])
        else:
            # move head one block down in y direction
            copy.insert(0, [front[0], front[1] - 1])
        self.body = copy
