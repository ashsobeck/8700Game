import json
import pygame
import numpy as np
from PIL import Image
import os
from Title_Snake import Title_Snake

EASY=350
MEDIUM=200
HARD=100
class Screens:
    def __init__(self, window, game_snake, width=960, height=640, block_size=32):
        self.window = window
        self.width = width
        self.height = height
        self.block_size = block_size
        self.game_start = False

        #create dummy snake. This is so we can use the images for our background
        self.title_snake = Title_Snake(self.window, self.width, self.height, self.block_size * 2)
        self.game_snake = game_snake

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
        self.arrow = pygame.image.load("icons/Left_Arrow.png").convert()
        self.color_left_arrow = pygame.image.load("icons/Left_Arrow.png").convert()
        self.color_right_arrow = pygame.image.load("icons/Right_Arrow.png").convert()

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
        self.settings_button = pygame.image.load("icons/Buttons/Settings.png").convert()
        self.snake_color_button = pygame.image.load("icons/Buttons/Snake_Color.png").convert()
        self.init_home_buttons()

        self.difficulty = MEDIUM

        #keep track of prev color so we know what pixel color to look for when editing png files
        #keep it in a json file so we can record it from instance to instance
        with open("icons/Snake/snake.json", "r") as j:
            self.previous_snake_color = json.load(j)['prev_color']
        
        self.current_snake_color = "WHITE"
        # ADD COLORS HERE WITH RGB VALUES. THEN ADD COLOR NAME TO LIST BELOW
        self.snake_colors = {
                             "WHITE": {"color": "WHITE", "r": 255, "g": 255, "b": 255},
                             "RED": {"color": "RED", "r": 255, "g": 0, "b": 0},
                             "GREEN": {"color": "GREEN", "r": 0, "g": 255, "b": 0},
                             "BLUE": {"color": "BLUE", "r": 0, "g": 0, "b": 255}
                            }
        self.snake_colors_list = ["WHITE", "RED", "GREEN", "BLUE"]

        self.home = True
        self.background_switcher = False
        self.mouse_clicked = False
        self.background_image = pygame.transform.scale(self.spider_webs_image, (self.width, self.height))
    
    def draw_screen(self):
        #revert snake color back to white if it was left changed
        self.update_snake_color()
        self.game_snake.update_snake_color()
        self.title_snake.update_snake_color()
        self.title_snake.draw_snake()
        if self.home:
            self.draw_home_buttons()
            self.get_click_home()
            self.start_game()
        elif self.background_switcher:
            self.draw_settings_selection()
            self.get_click_settings()

    def draw_home_buttons(self):
        self.easy_button.set_alpha(100)
        self.medium_button.set_alpha(100)
        self.hard_button.set_alpha(100)
        self.settings_button.set_alpha(255)

        if self.difficulty == EASY: self.easy_button.set_alpha(255)
        elif self.difficulty == MEDIUM: self.medium_button.set_alpha(255)
        elif self.difficulty == HARD: self.hard_button.set_alpha(255)

        self.window.blit(self.start_button, self.start_rect)
        self.window.blit(self.easy_button, self.easy_rect)
        self.window.blit(self.medium_button, self.medium_rect)
        self.window.blit(self.hard_button, self.hard_rect)
        self.window.blit(self.settings_button, self.settings_rect)

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

        if self.settings_rect.collidepoint(m_pos):
            if pygame.mouse.get_pressed()[0] and not self.mouse_clicked:
                self.background_switcher = True
                self.home = False
                self.mouse_clicked = True

        if pygame.mouse.get_pressed()[0] == False:
            self.mouse_clicked = False

    #check if a button was clicked in the settings page
    def get_click_settings(self):
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

        if self.left_arrow_rect.collidepoint(m_pos):
            if pygame.mouse.get_pressed()[0] and not self.mouse_clicked:
                self.previous_snake_color = self.current_snake_color
                index = self.snake_colors_list.index(self.current_snake_color)
                length = len(self.snake_colors_list)
                if index == 0:
                    self.current_snake_color = self.snake_colors_list[length - 1]
                else:
                    self.current_snake_color = self.snake_colors_list[index - 1]
                self.mouse_clicked = True
                with open("icons/Snake/snake.json", "w") as j_file:
                    json.dump({"prev_color": self.current_snake_color}, j_file)
                self.update_snake_color()
                self.game_snake.update_snake_color()
                self.title_snake.update_snake_color()

        if self.right_arrow_rect.collidepoint(m_pos):
            if pygame.mouse.get_pressed()[0] and not self.mouse_clicked:
                self.previous_snake_color = self.current_snake_color
                index = self.snake_colors_list.index(self.current_snake_color)
                length = len(self.snake_colors_list)
                if index == length - 1:
                    self.current_snake_color = self.snake_colors_list[0]
                else:
                    self.current_snake_color = self.snake_colors_list[index + 1]
                self.mouse_clicked = True
                with open("icons/Snake/snake.json", "w") as j_file:
                    json.dump({"prev_color": self.current_snake_color}, j_file)
                self.update_snake_color()
                self.game_snake.update_snake_color()
                self.title_snake.update_snake_color()
        
        if not pygame.mouse.get_pressed()[0]:
            self.mouse_clicked = False

    def draw_settings_selection(self):

        #draw back arrow
        self.window.blit(self.arrow, self.arrow_rect)
        #draw images
        for image in self.image_list:
            im = image[1]
            im_rect = image[2]
            is_selected = image[3]
            im.set_alpha(75) if is_selected == True else im.set_alpha(200)
            self.window.blit(im, im_rect)

        #draw color on bottom
        color = self.snake_colors[self.current_snake_color]
        my_font = pygame.font.SysFont('Comic Sans MS', 50, bold=True)
        text = my_font.render(color["color"], False, (color["r"], color["g"], color["b"]))
        text_rect = text.get_rect(center=(self.width/2, self.height - self.height/6))

        #place color arrows coordinates
        self.left_arrow_rect = self.color_left_arrow.get_rect(center=(self.width/3, self.height - self.height/6))
        self.right_arrow_rect = self.color_right_arrow.get_rect(center=(2*self.width/3, self.height - self.height/6))
        self.color_left_arrow.set_alpha(200)
        self.color_right_arrow.set_alpha(200)

        #place labels coordinates
        background_rect = self.background_button.get_rect(center=(self.width/2, self.arrow_rect.centery))
        snake_color_rect = self.snake_color_button.get_rect(center=(self.width/2, text_rect.centery - 50))

        self.window.blit(text, text_rect)
        self.window.blit(self.background_button, background_rect)
        self.window.blit(self.snake_color_button, snake_color_rect)
        self.window.blit(self.color_left_arrow, self.left_arrow_rect)
        self.window.blit(self.color_right_arrow, self.right_arrow_rect)
        

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

        self.settings_button = pygame.transform.scale(self.settings_button, (self.button_width, self.button_height))
        self.settings_rect = self.settings_button.get_rect()
        self.settings_rect.topleft = (self.width/5, self.height * (1/2))

        self.background_button = pygame.transform.scale(self.background_button, (self.button_width, self.button_height))
        self.snake_color_button = pygame.transform.scale(self.snake_color_button, (self.button_width, self.button_height))

    def init_background_images(self):
        im_wid = int(self.width/10)
        im_height = int(self.height/4)

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

    def update_snake_color(self):
        #loop through ever snake png and change the color
        dir = 'icons/Snake/'
        for images in os.listdir(dir):
            if images.endswith('.png'):

                name = dir + str(images)
                im = Image.open(name)
                data = np.array(im)

                # orig color values
                r1 = self.snake_colors[self.previous_snake_color]["r"]
                g1 = self.snake_colors[self.previous_snake_color]["g"]
                b1 = self.snake_colors[self.previous_snake_color]["b"]

                #new color vlaues
                r2 = self.snake_colors[self.current_snake_color]["r"]
                g2 = self.snake_colors[self.current_snake_color]["g"]
                b2 = self.snake_colors[self.current_snake_color]["b"]

                # get the current rgb values from the image
                red, green, blue = data[:,:,0], data[:,:,1], data[:,:,2]
                #mask the values with the previous colors (match them)
                mask = (red == r1) & (green == g1) & (blue == b1)
                #apply the mask with the new colors (replace old with new)
                data[:,:,:3][mask] = [r2, g2, b2]

                im = Image.fromarray(data)
                im.save(name)
 