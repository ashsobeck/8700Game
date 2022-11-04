import pygame

class Levels:

    def __init__(self, window, width, height, block_size, information: dict):

        self.window = window
        self.width = width
        self.height = height
        self.block_size = block_size
        self.cells_x = self.width/self.block_size
        self.cells_y = self.height/self.block_size
        self.rect_width = int(self.block_size * 4)
        self.rect_height = int(self.block_size * 2)

        self.block_image = pygame.image.load("icons/block.png").convert()
        self.block_image.set_alpha(200)
        self.back_arrow = pygame.image.load("icons/Left_Arrow.png").convert()
        self.back_arrow.set_alpha(255)
        self.button = pygame.image.load("icons/Buttons/spooky.jpeg").convert()
        self.button.set_alpha(255)
        self.back_arrow_rect = self.back_arrow.get_rect(topleft=(2*self.block_size, 2*self.block_size))

        #list containing all the levels
        self.levels = []
        self.init_levels()
       
       #get the amount of levels and set the first one
        self.level_count = len(self.levels)
        self.selected_level = 0

        #will contain the rectangles for all the levels in levels screen
        self.level_select_rects = []
        self.init_level_rect()

        #this will hold the rect for the current selected levels
        #will change for every level change
        #create a rect for each coordinate in the current selected level
        self.current_level_rect = [pygame.Rect(l[0] * self.block_size, l[1] * self.block_size, 
                                   self.block_size, self.block_size) for l in self.levels[self.selected_level]]
        self.current_level_coord = self.levels[self.selected_level]

        self.mouse_clicked = False


    def draw_levels_screen(self, background):
        self.window.blit(background, (0,0))
        self.window.blit(self.back_arrow, self.back_arrow_rect)
        self.button = pygame.transform.scale(self.button, (self.rect_width, self.rect_height))
        font = pygame.font.SysFont('Arial', 25, bold=True)
        #text_rect = text.get_rect(center=(self.width/2, 5*self.height/6))
        for index, rect in enumerate(self.level_select_rects):
            
            color = (255,255,255) if index == self.selected_level else (0,0,0)
                
            text = font.render("Level " + str(index), False, color)
            text_rect = text.get_rect(center=(rect.centerx, rect.centery))
            self.window.blit(self.button, rect)
            self.window.blit(text, text_rect)

    def draw_level(self):
        for block_rect in self.current_level_rect:
            self.window.blit(self.block_image, block_rect)

    # Screens will be calling this function. If it returns True (default) then
    # it will stay on the levels page. If it returns false (back button clicked)
    # then screens will display the home page
    def get_click(self):
        m_pos = pygame.mouse.get_pos()

        if self.back_arrow_rect.collidepoint(m_pos):
            if pygame.mouse.get_pressed()[0] and not self.mouse_clicked:
                self.mouse_clicked = True
                return False

        level_click = [rect.collidepoint(m_pos) for rect in self.level_select_rects]
        if True in level_click:
            if pygame.mouse.get_pressed()[0] and not self.mouse_clicked:
                index = level_click.index(True)
                self.selected_level = index
                self.mouse_clicked = True
                #create a rect for each coordinate in the current selected level
                self.current_level_rect = [pygame.Rect(l[0] * self.block_size, l[1] * self.block_size, 
                                           self.block_size, self.block_size) for l in self.levels[self.selected_level]]
                self.current_level_coord = self.levels[self.selected_level]


        if pygame.mouse.get_pressed()[0] is False:
            self.mouse_clicked = False

        return True

    

    def init_level_rect(self):
        left_row = int(self.width/6)
        left_col = int(self.height/4)

        for i in range(self.level_count):
            row = int(i / 4)
            col = int(i % 4)

            #position is the topleft of the rectangle
            self.level_select_rects.append(pygame.Rect(left_row + col * (self.rect_width + 20), 
                                                       left_col + row * (self.rect_height + 20), 
                                                       self.rect_width, self.rect_height))


    def init_levels(self):
        
        #Level 0. Empty with no walls
        self.levels.append([])

        #Level 1. 2 Horizontal lines
        level = []
        start_col = int(self.cells_x/10)
        end_col = int(9*self.cells_x/10)
        height_1 = int(self.cells_y/6)
        height_2 = height_1 * 5
        top_line = [x for x in range(start_col, end_col)]
        for l in top_line:
            level.append([l, height_1])
        bottom_line = [x for x in range(start_col, end_col)]
        for l in bottom_line:
            level.append([l, height_2])
        self.levels.append(level)

        # TODO
        # Level 3
        level = []


        