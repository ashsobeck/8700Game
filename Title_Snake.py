import pygame

from pumpkin import Pumpkin


#class just for drawing the snake on the home screen
class Title_Snake():
    def __init__(self, window, width=960, height=640, block_size=32):

        self.window = window
        self.width = width
        self.height = height
        self.block_size = block_size

        # keep track of all the snake parts
        #.set_alpha allows us to edit the transparency of our snake parts of a scale of 0-255
        #255 being opaque and 0 being fully transparent. This is responsible for calling it a "ghost" snake
        self.head_up = pygame.image.load("icons/Snake_Head_Up.png").convert()
        self.head_up.set_alpha(150)
        self.head_up = pygame.transform.scale(self.head_up, (self.block_size, self.block_size))
        self.head_down = pygame.image.load("icons/Snake_Head_Down.png").convert()
        self.head_down.set_alpha(150)
        self.head_down = pygame.transform.scale(self.head_down, (self.block_size, self.block_size))
        self.head_right = pygame.image.load("icons/Snake_Head_Right.png").convert()
        self.head_right.set_alpha(150)
        self.head_right = pygame.transform.scale(self.head_right, (self.block_size, self.block_size))
        self.head_left = pygame.image.load("icons/Snake_Head_Left.png").convert()
        self.head_left.set_alpha(150)
        self.head_left = pygame.transform.scale(self.head_left, (self.block_size, self.block_size))

        self.body_hori = pygame.image.load("icons/Snake_Body_Hori.png").convert()
        self.body_hori.set_alpha(150)
        self.body_hori = pygame.transform.scale(self.body_hori, (self.block_size, self.block_size))
        self.body_vert = pygame.image.load("icons/Snake_Body_Vert.png").convert()
        self.body_vert.set_alpha(150)
        self.body_vert = pygame.transform.scale(self.body_vert, (self.block_size, self.block_size))

        self.tail_right = pygame.image.load("icons/Snake_Tail_R.png").convert()
        self.tail_right.set_alpha(150)
        self.tail_right = pygame.transform.scale(self.tail_right, (self.block_size, self.block_size))
        self.tail_left = pygame.image.load("icons/Snake_Tail_L.png").convert()
        self.tail_left.set_alpha(150)
        self.tail_left = pygame.transform.scale(self.tail_left, (self.block_size, self.block_size))
        self.tail_down = pygame.image.load("icons/Snake_Tail_D.png").convert()
        self.tail_down.set_alpha(150)
        self.tail_down = pygame.transform.scale(self.tail_down, (self.block_size, self.block_size))
        self.tail_up = pygame.image.load("icons/Snake_Tail_U.png").convert()
        self.tail_up.set_alpha(150)
        self.tail_up = pygame.transform.scale(self.tail_up, (self.block_size, self.block_size))

        self.body_tr = pygame.image.load("icons/Snake_Corner_TR.png").convert()
        self.body_tr.set_alpha(150)
        self.body_tr = pygame.transform.scale(self.body_tr, (self.block_size, self.block_size))
        self.body_tl = pygame.image.load("icons/Snake_Corner_TL.png").convert()
        self.body_tl.set_alpha(150)
        self.body_tl = pygame.transform.scale(self.body_tl, (self.block_size, self.block_size))
        self.body_br = pygame.image.load("icons/Snake_Corner_BR.png").convert()
        self.body_br.set_alpha(150)
        self.body_br = pygame.transform.scale(self.body_br, (self.block_size, self.block_size))
        self.body_bl = pygame.image.load("icons/Snake_Corner_BL.png").convert()
        self.body_bl.set_alpha(150)
        self.body_bl = pygame.transform.scale(self.body_bl, (self.block_size, self.block_size))

        self.pumpkin = pygame.image.load("icons/Pumpkin.png").convert()
        self.pumpkin.set_alpha(255)
        self.pumpkin = pygame.transform.scale(self.pumpkin, (self.block_size, self.block_size))


        self.cells_x = int(self.width/self.block_size)
        self.cells_y = int(self.height/self.block_size)
        #body from head down
        #using cells to try an be dynamic in case the width and height of the screen change
        self.body = []
        self.make_body()
        self.direction= 'left'

    def draw_snake(self):

        for index, block in enumerate(self.body):
            x = block[0] * self.block_size
            y = block[1] * self.block_size
            # create rectangle around block object. This is for collisions

            #if its the front of the snake show the head
            if index == 0:
                self.window.blit(self.pumpkin, (x, y))
            elif index == 1:
                self.window.blit(self.head_right, (x, y))
            #if at the end then show the tail
            elif index == self.body.__len__() - 1:
                self.window.blit(self.tail_up, (x, y))
            else:
                #if it's in the middle then get the 2 blocks on either side
                prev_block = self.subtract_positions(self.body[index + 1], block)
                next_block = self.subtract_positions(self.body[index - 1], block)

                # body orientations: if the prev and next block are on same plane
                if prev_block[0] == next_block[0]:
                    self.window.blit(self.body_vert, (x, y))
                elif prev_block[1] == next_block[1]:
                    self.window.blit(self.body_hori, (x, y))
                else:
                    # corners
                    if prev_block[0] == -1 and next_block[1] == -1 or \
                       prev_block[1] == -1 and next_block[0] == -1:
                        self.window.blit(self.body_tl, (x, y))
                    elif prev_block[0] == -1 and next_block[1] == 1 or \
                         prev_block[1] == 1 and next_block[0] == -1:
                        self.window.blit(self.body_bl, (x, y))
                    elif prev_block[0] == 1 and next_block[1] == -1 or \
                         prev_block[1] == -1 and next_block[0] == 1:
                        self.window.blit(self.body_tr, (x, y))
                    elif prev_block[0] == 1 and next_block[1] == 1 or \
                         prev_block[1] == 1 and next_block[0] == 1:
                        self.window.blit(self.body_br, (x, y))

    #subtract the positions of 2 snake body parts
    def subtract_positions(self, first_list: list, second_list: list) -> list:
        final_position = []
        # zip allows us to iterate over bost lists at the same time
        for a, b in zip(first_list, second_list):
            final_position.append(a - b)
        return final_position

    #make the body of the snake on the start and other screens, using cells to be dynamic
    #the body is a list of lists of blocks. Each block is a piece of the snake
    #to add to the body of the snake all you have to do is add a cell [x,y] to the body list
    def make_body(self):
        
        #insert tail, won't be on screen
        self.body.insert(0, [int(self.cells_x * 2/3), self.cells_y])

        for x in range(int(self.cells_x * 2/3), 0, -1):
            self.body.insert(0, [x, self.cells_y - 1])

        for y in range(self.cells_y - 1, 0, -1):
            self.body.insert(0, [0, y])

        for x in range(self.cells_x):
            self.body.insert(0, [x, 0])

        for y in range(int(self.cells_y * 1/2) - 1):
            self.body.insert(0, [self.cells_x - 1, y + 1])

        for x in range(self.cells_x - 1, int(self.cells_x * 1/2), -1):
            self.body.insert(0, [x, int(self.cells_y * 1/2)])
        
        for y in range(int(self.cells_y * 1/2) - 1, int(self.cells_y * 1/2) - 3, -1):
            self.body.insert(0, [int(self.cells_x * 1/2) + 1, y])

        for x in range(int(self.cells_x * 1/2) +  2, int(self.cells_x * 1/2) + 6):
            self.body.insert(0, [x, int(self.cells_y * 1/2) - 2])
