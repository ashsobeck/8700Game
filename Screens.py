import pygame
from Title_Snake import Title_Snake

EASY=350
MEDIUM=200
HARD=100
class Screens:
    def __init__(self, window, width=960, height=640, block_size=32):
        self.window = window
        self.width = width
        self.height = height
        self.block_size = block_size
        self.game_start = False

        self.button_width = int(self.width/6)
        self.button_height = int(self.button_width/4)
        self.image_width = int(self.width/4)
        self.image_height = int(self.image_width/3)

        # will have a list of the images with three components
        # [image surface (image.jpg), image rect (used for mouse click and placement), boolean (is this the background image)]
        # is initialized automatically
        self.image_list = []

        self.spider_webs_image = pygame.image.load("icons/Backgrounds/Spider_webs.jpg").convert()
        self.boards_image = pygame.image.load("icons/Backgrounds/Boards.jpg").convert()
        self.forest_image = pygame.image.load("icons/Backgrounds/Forest.jpg").convert()
        self.cemetary_moon_image = pygame.image.load("icons/Backgrounds/Cemetary_moon.jpg").convert()
        self.cemetary_pump_image = pygame.image.load("icons/Backgrounds/Cemetary_Pumpkins.jpg").convert()
        self.cemetary_image = pygame.image.load("icons/Backgrounds/Cemetary.jpg").convert()
        self.moon_image = pygame.image.load("icons/Backgrounds/Moon.jpg").convert()
        self.witch_image = pygame.image.load("icons/Backgrounds/Witch.jpg").convert()
        self.scarecrow_image = pygame.image.load("icons/Backgrounds/Scarecrow.jpg").convert()
        self.arrow = pygame.image.load("icons/Arrow.png").convert()

        # keep a list of the image names
        self.image_names = [self.spider_webs_image, self.boards_image, self.forest_image, 
                            self.cemetary_moon_image,self.cemetary_pump_image, self.cemetary_image, 
                            self.moon_image, self.witch_image, self.scarecrow_image]
        self.init_background_images()

        self.start_button = pygame.image.load("icons/Buttons/Start.png").convert()
        self.easy_button = pygame.image.load("icons/Buttons/Easy.png").convert()
        self.medium_button = pygame.image.load("icons/Buttons/Medium.png").convert()
        self.hard_button = pygame.image.load("icons/Buttons/Hard.png").convert()
        self.background_button = pygame.image.load("icons/Buttons/Background.png").convert()
        
        self.init_home_buttons()

        self.difficulty = MEDIUM

        self.home = True
        self.background_switcher = False
        self.mouse_clicked = False
        self.background_image = pygame.transform.scale(self.spider_webs_image, (self.width, self.height))
    
    def draw_screen(self):
        self.draw_snake()
        if self.home:
            self.draw_home_buttons()
            self.get_click_home()
            self.start_game()
        elif self.background_switcher:
            self.draw_background_selection()
            self.get_click_background()

    def draw_home_buttons(self):
        self.easy_button.set_alpha(100)
        self.medium_button.set_alpha(100)
        self.hard_button.set_alpha(100)
        self.background_button.set_alpha(255)

        if self.difficulty == EASY: self.easy_button.set_alpha(255)
        elif self.difficulty == MEDIUM: self.medium_button.set_alpha(255)
        elif self.difficulty == HARD: self.hard_button.set_alpha(255)

        self.window.blit(self.start_button, (self.start_rect.x, self.start_rect.y))
        self.window.blit(self.easy_button, (self.easy_rect.x, self.easy_rect.y))
        self.window.blit(self.medium_button, (self.medium_rect.x, self.medium_rect.y))
        self.window.blit(self.hard_button, (self.hard_rect.x, self.hard_rect.y))
        self.window.blit(self.background_button, (self.background_rect.x, self.background_rect.y))

    def start_game(self):
        m_pos = pygame.mouse.get_pos()

        if self.start_rect.collidepoint(m_pos):
            if pygame.mouse.get_pressed()[0] and not self.mouse_clicked:
                self.game_start = True
                self.mouse_clicked = True

    def get_click_home(self):
        m_pos = pygame.mouse.get_pos()

        if self.easy_rect.collidepoint(m_pos):
            if pygame.mouse.get_pressed()[0] and not self.mouse_clicked:
                self.difficulty = EASY
                self.mouse_clicked = True
        elif self.medium_rect.collidepoint(m_pos):
            if pygame.mouse.get_pressed()[0] and not self.mouse_clicked:
                self.difficulty = MEDIUM
                self.mouse_clicked = True
        elif self.hard_rect.collidepoint(m_pos):
            if pygame.mouse.get_pressed()[0] and not self.mouse_clicked:
                self.difficulty = HARD
                self.mouse_clicked = True

        if self.background_rect.collidepoint(m_pos):
            if pygame.mouse.get_pressed()[0] and not self.mouse_clicked:
                self.background_switcher = True
                self.home = False
                self.mouse_clicked = True

        if pygame.mouse.get_pressed()[0] == False:
            self.mouse_clicked = False

    def get_click_background(self):
        m_pos = pygame.mouse.get_pos()

        for index, image in enumerate(self.image_list):
            rect = image[2]
            if rect.collidepoint(m_pos):
                if pygame.mouse.get_pressed()[0] and not self.mouse_clicked:
                    #set all the images to false showing
                    for im in self.image_list: im[3] = False 
                    #make current image true
                    self.image_list[index][3] = True
                    self.background_image = pygame.transform.scale(image[0], (self.width, self.height))
                    self.mouse_clicked = True

        if self.arrow_rect.collidepoint(m_pos):
            if pygame.mouse.get_pressed()[0] and not self.mouse_clicked:
                self.background_switcher = False
                self.home = True
                self.mouse_clicked = True
        
        if not pygame.mouse.get_pressed()[0]:
            self.mouse_clicked = False

    def draw_snake(self):
        #create dummy snake. This is so we can use the images for our background
        snake = Title_Snake(self.window, self.width, self.height, self.block_size * 2)
        snake.draw_snake()

    def draw_background_selection(self):

        self.window.blit(self.arrow, self.arrow_rect)
        for image in self.image_list:
            im = image[1]
            im_rect = image[2]
            is_selected = image[3]
            im.set_alpha(75) if is_selected == True else im.set_alpha(200)
            self.window.blit(im, im_rect)

    def init_home_buttons(self):
        self.start_button = pygame.transform.scale(self.start_button, (self.button_width, self.button_height))
        self.start_rect = self.start_button.get_rect()
        self.start_rect.topleft = (self.width/5, self.height/3)

        self.easy_button = pygame.transform.scale(self.easy_button, (self.button_width, self.button_height))
        self.easy_rect = self.easy_button.get_rect()
        self.easy_rect.topleft = (self.width/5, self.height * (2/3))

        self.medium_button = pygame.transform.scale(self.medium_button, (self.button_width, self.button_height))
        self.medium_rect = self.medium_button.get_rect()
        self.medium_rect.topleft = (self.width/5 + self.button_width, self.height * (2/3))

        self.hard_button = pygame.transform.scale(self.hard_button, (self.button_width, self.button_height))
        self.hard_rect = self.hard_button.get_rect()
        self.hard_rect.topleft = (self.width/5 + self.button_width * 2, self.height * (2/3))

        self.background_button = pygame.transform.scale(self.background_button, (self.button_width, self.button_height))
        self.background_rect = self.background_button.get_rect()
        self.background_rect.topleft = (self.width/5, self.height * (1/2))

    def init_background_images(self):
        im_wid = int(self.width/10)
        im_height = int(self.height/3)

        self.arrow = pygame.transform.scale(self.arrow, (self.block_size * 2, self.block_size * 2))
        self.arrow_rect = self.arrow.get_rect()
        self.arrow_rect.topleft = (im_wid, im_height - self.image_height - 20)
        self.arrow.set_alpha(200)

        for index, image in enumerate(self.image_names):

            im_small = pygame.transform.scale(image, (self.image_width, self.image_height))
            im_rect = im_small.get_rect()
            row = int(index/3)
            col = (index % 3)
            im_rect.topleft = (im_wid + col * (self.image_width + 20), im_height + row * (self.image_height + 20))
            self.image_list.append([image, im_small, im_rect, False])

        #set first image to be the background
        self.image_list[0][3] = True
 