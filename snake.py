import pygame

class Snake():
    def __init__(self, window, width=960, height=640, block_size=32):

        self.window = window
        self.width = width
        self.height = height
        self.block_size = block_size

        # keep track of all the snake parts
        #.set_alpha allows us to edit the transparency of our snake parts of a scale of 0-255
        #255 being opaque and 0 being fully transparent. This is responsible for calling it a "ghost" snake
        self.head_up = pygame.image.load("icons/Snake/Snake_Head_Up.png").convert()
        self.head_up.set_alpha(150)
        self.head_down = pygame.image.load("icons/Snake/Snake_Head_Down.png").convert()
        self.head_down.set_alpha(150)
        self.head_right = pygame.image.load("icons/Snake/Snake_Head_Right.png").convert()
        self.head_right.set_alpha(150)
        self.head_left = pygame.image.load("icons/Snake/Snake_Head_Left.png").convert()
        self.head_left.set_alpha(150)

        self.body_hori = pygame.image.load("icons/Snake/Snake_Body_Hori.png").convert()
        self.body_hori.set_alpha(150)
        self.body_vert = pygame.image.load("icons/Snake/Snake_Body_Vert.png").convert()
        self.body_vert.set_alpha(150)

        self.tail_right = pygame.image.load("icons/Snake/Snake_Tail_R.png").convert()
        self.tail_right.set_alpha(150)
        self.tail_left = pygame.image.load("icons/Snake/Snake_Tail_L.png").convert()
        self.tail_left.set_alpha(150)
        self.tail_down = pygame.image.load("icons/Snake/Snake_Tail_D.png").convert()
        self.tail_down.set_alpha(150)
        self.tail_up = pygame.image.load("icons/Snake/Snake_Tail_U.png").convert()
        self.tail_up.set_alpha(150)

        self.body_tr = pygame.image.load("icons/Snake/Snake_Corner_TR.png").convert()
        self.body_tr.set_alpha(150)
        self.body_tl = pygame.image.load("icons/Snake/Snake_Corner_TL.png").convert()
        self.body_tl.set_alpha(150)
        self.body_br = pygame.image.load("icons/Snake/Snake_Corner_BR.png").convert()
        self.body_br.set_alpha(150)
        self.body_bl = pygame.image.load("icons/Snake/Snake_Corner_BL.png").convert()
        self.body_bl.set_alpha(150)

        self.direction = 'right'
        self.next_direction = 'right'
        # the body keeps track of the positon of each body part
        # for simplicity we will keep track of what cell its in
        self.body = [[15, 10], [14, 10], [13, 10], [12, 10], [11, 10], [10, 10], [9, 10]]
        # this will hold the rectangles of each block. Used in collision detection
        self.rect = [pygame.Rect(l[0] * self.block_size, l[1] * self.block_size, self.block_size, self.block_size) for l in self.body]
        self.new_body = False
        
    def draw_snake(self):
        self.update_head()
        self.update_tail()

        for index, block in enumerate(self.body):
            x = block[0] * self.block_size
            y = block[1] * self.block_size
            # create rectangle around block object. This is for collisions
            rect = pygame.Rect(x, y, self.block_size, self.block_size)
            self.rect[index] = rect

            #if its the front of the snake show the head
            if index == 0:
                self.window.blit(self.head, rect)
            #if at the end then show the tail
            elif index == self.body.__len__() - 1:
                self.window.blit(self.tail, rect)
            else:
                #if it's in the middle then get the 2 blocks on either side
                prev_block = self.subtract_positions(self.body[index + 1], block)
                next_block = self.subtract_positions(self.body[index - 1], block)

                # body orientations: if the prev and next block are on same plane
                if prev_block[0] == next_block[0]:
                    self.window.blit(self.body_vert, rect)
                elif prev_block[1] == next_block[1]:
                    self.window.blit(self.body_hori, rect)
                else:
                    # corners
                    if prev_block[0] == -1 and next_block[1] == -1 or \
                       prev_block[1] == -1 and next_block[0] == -1:
                        self.window.blit(self.body_tl, rect)
                    elif prev_block[0] == -1 and next_block[1] == 1 or \
                         prev_block[1] == 1 and next_block[0] == -1:
                        self.window.blit(self.body_bl, rect)
                    elif prev_block[0] == 1 and next_block[1] == -1 or \
                         prev_block[1] == -1 and next_block[0] == 1:
                        self.window.blit(self.body_tr, rect)
                    elif prev_block[0] == 1 and next_block[1] == 1 or \
                         prev_block[1] == 1 and next_block[0] == 1:
                        self.window.blit(self.body_br, rect)

    def move_snake(self):
        # get every element except the last one since it dissappears
        if self.new_body:
            copy = self.body
        else:
            copy = self.body[:-1]
        front = self.body[0]
        self.direction = self.next_direction
        # Checks if its at a border then dont move the snake
        if (front[0] != 0 and self.direction == 'left') or (
                front[0] != 29 and self.direction == 'right') or (
                front[1] != 0 and self.direction == 'up') or (
                front[1] != 19 and self.direction == 'down'):
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
            if self.new_body:
                body_pos = self.body[0]
                #add a rect for the new block we added in the beginning of the snake
                self.rect.insert(0, pygame.Rect(body_pos[0] * self.block_size, 
                                                body_pos[1] * self.block_size, 
                                                self.block_size, self.block_size))
                self.new_body = False
        else:
            print("DEAD YOU HAVE DIED WOW YOU SUCK")

    #update the head to be a certain image based on direction
    def update_head(self):
        if self.direction == 'right':
            self.head = self.head_right
        elif self.direction == 'left':
            self.head = self.head_left
        elif self.direction == 'up':
            self.head = self.head_up
        elif self.direction == 'down':
            self.head = self.head_down
        else:
            self.head = self.head_right

    #update the tail to be a certain image based on direction
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

    #subtract the positions of 2 snake body parts
    def subtract_positions(self, first_list: list, second_list: list) -> list:
        final_position = []
        # zip allows us to iterate over bost lists at the same time
        for a, b in zip(first_list, second_list):
            final_position.append(a - b)
        return final_position

    #returns true if the head of the snake (rect[0]) collides with any part of the rest of the snake
    def if_collision(self):
        if True in [self.rect[0].colliderect(rect) for rect in self.rect[1:]]:
            print ("STOP HITTING YOURSELF")
            return True
        else:
            return False

    #since the image png's have been update, we need to update each self variable with the new image
    def update_snake_color(self):
        self.head_up = pygame.image.load("icons/Snake/Snake_Head_Up.png").convert()
        self.head_up.set_alpha(150)
        self.head_down = pygame.image.load("icons/Snake/Snake_Head_Down.png").convert()
        self.head_down.set_alpha(150)
        self.head_right = pygame.image.load("icons/Snake/Snake_Head_Right.png").convert()
        self.head_right.set_alpha(150)
        self.head_left = pygame.image.load("icons/Snake/Snake_Head_Left.png").convert()
        self.head_left.set_alpha(150)

        self.body_hori = pygame.image.load("icons/Snake/Snake_Body_Hori.png").convert()
        self.body_hori.set_alpha(150)
        self.body_vert = pygame.image.load("icons/Snake/Snake_Body_Vert.png").convert()
        self.body_vert.set_alpha(150)

        self.tail_right = pygame.image.load("icons/Snake/Snake_Tail_R.png").convert()
        self.tail_right.set_alpha(150)
        self.tail_left = pygame.image.load("icons/Snake/Snake_Tail_L.png").convert()
        self.tail_left.set_alpha(150)
        self.tail_down = pygame.image.load("icons/Snake/Snake_Tail_D.png").convert()
        self.tail_down.set_alpha(150)
        self.tail_up = pygame.image.load("icons/Snake/Snake_Tail_U.png").convert()
        self.tail_up.set_alpha(150)

        self.body_tr = pygame.image.load("icons/Snake/Snake_Corner_TR.png").convert()
        self.body_tr.set_alpha(150)
        self.body_tl = pygame.image.load("icons/Snake/Snake_Corner_TL.png").convert()
        self.body_tl.set_alpha(150)
        self.body_br = pygame.image.load("icons/Snake/Snake_Corner_BR.png").convert()
        self.body_br.set_alpha(150)
        self.body_bl = pygame.image.load("icons/Snake/Snake_Corner_BL.png").convert()
        self.body_bl.set_alpha(150)