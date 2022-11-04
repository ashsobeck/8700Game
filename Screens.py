import json
import pygame
import numpy as np
from PIL import Image
import os
from Levels import Levels
from Settings import Settings_Screen
from Title_Snake import Title_Snake
from snake import Snake

EASY = 350
MEDIUM = 200
HARD = 100


class Screens:
    def __init__(self, window, game_snake: Snake, information: json, width=960, height=640, block_size=32):
        self.window = window
        self.width = width
        self.height = height
        self.block_size = block_size
        self.game_start = False
        self.information = information

        # create dummy snake. This is so we can use the images for our background
        self.title_snake = Title_Snake(self.window, self.width, self.height, self.block_size * 2)
        self.game_snake = game_snake

        self.button_width = int(self.width/6)
        self.button_height = int(self.button_width/4)

        self.start_button = pygame.image.load("icons/Buttons/Start.png").convert()
        self.easy_button = pygame.image.load("icons/Buttons/Easy.png").convert()
        self.medium_button = pygame.image.load("icons/Buttons/Medium.png").convert()
        self.hard_button = pygame.image.load("icons/Buttons/Hard.png").convert()
        self.settings_button = pygame.image.load("icons/Buttons/Settings.png").convert()
        self.levels_button = pygame.image.load("icons/Buttons/Levels.png").convert()
        self.init_home_buttons()

        self.difficulty = self.information['difficulty']
        self.game_snake.update_difficulty(self.difficulty)

        # Colors come from information.json. Add Colors in that file for the snake
        self.snake_colors = self.information['colors']
        self.snake_colors_list = list(self.snake_colors.keys())

        self.home = True
        self.settings = False
        self.levels = False
        self.mouse_clicked = False
        self.settings_page = Settings_Screen(self.window, self.information, self.snake_colors, self.snake_colors_list,
                                             self.width, self.height, self.block_size)
        self.levels_page = Levels(self.window, self.width, self.height, self.block_size, self.information)
        # get the background image from the image list saved in the image_list
        self.background_image = pygame.transform.scale(self.settings_page.image_list[self.information["background_image_index"]][0], (self.width, self.height))

    def draw_menu(self):
        self.title_snake.draw_snake()
        if self.home:
            self.draw_home_buttons()
            self.get_click_home()
        elif self.settings:
            self.settings_page.draw_settings_selection()
            go_home, update_snake = self.settings_page.get_click_settings()
            self.background_image = self.settings_page.background_image
            if go_home:
                self.home = True
                self.settings = False
            if update_snake:
                self.update_snake_color()
                self.game_snake.update_snake_color()
                self.title_snake.update_snake_color()
        elif self.levels:
            self.levels_page.draw_levels_screen(self.background_image)
            self.levels = self.levels_page.get_click()
            if not self.levels:
                self.home = True

    def draw_home_buttons(self):
        self.easy_button.set_alpha(100)
        self.medium_button.set_alpha(100)
        self.hard_button.set_alpha(100)
        self.settings_button.set_alpha(255)
        self.levels_button.set_alpha(255)

        if self.difficulty == EASY: self.easy_button.set_alpha(255)
        elif self.difficulty == MEDIUM: self.medium_button.set_alpha(255)
        elif self.difficulty == HARD: self.hard_button.set_alpha(255)

        self.window.blit(self.start_button, self.start_rect)
        self.window.blit(self.levels_button, self.levels_rect)
        self.window.blit(self.easy_button, self.easy_rect)
        self.window.blit(self.medium_button, self.medium_rect)
        self.window.blit(self.hard_button, self.hard_rect)
        self.window.blit(self.settings_button, self.settings_rect)

    def get_click_home(self):
        m_pos = pygame.mouse.get_pos()

        if self.start_rect.collidepoint(m_pos):
            if pygame.mouse.get_pressed()[0] and not self.mouse_clicked:
                self.game_start = True
                self.mouse_clicked = True

        if self.easy_rect.collidepoint(m_pos):
            if pygame.mouse.get_pressed()[0] and not self.mouse_clicked:
                self.difficulty = EASY
                self.mouse_clicked = True
                with open("information.json", "w") as j_file:
                    self.information['difficulty'] = EASY
                    json.dump(self.information, j_file, indent=2)
                self.game_snake.update_difficulty(self.difficulty)

        elif self.medium_rect.collidepoint(m_pos):
            if pygame.mouse.get_pressed()[0] and not self.mouse_clicked:
                self.difficulty = MEDIUM
                self.mouse_clicked = True
                with open("information.json", "w") as j_file:
                    self.information['difficulty'] = MEDIUM
                    json.dump(self.information, j_file, indent=2)
                self.game_snake.update_difficulty(self.difficulty)

        elif self.hard_rect.collidepoint(m_pos):
            if pygame.mouse.get_pressed()[0] and not self.mouse_clicked:
                self.difficulty = HARD
                self.mouse_clicked = True
                with open("information.json", "w") as j_file:
                    self.information['difficulty'] = HARD
                    json.dump(self.information, j_file, indent=2)
                self.game_snake.update_difficulty(self.difficulty)

        if self.settings_rect.collidepoint(m_pos):
            if pygame.mouse.get_pressed()[0] and not self.mouse_clicked:
                self.settings = True
                self.home = False
                self.mouse_clicked = True
                # this is so the mouse won't stay click when we switch to the settings page
                self.settings_page.mouse_clicked = True

        if self.levels_rect.collidepoint(m_pos):
            if pygame.mouse.get_pressed()[0] and not self.mouse_clicked:
                self.levels = True
                self.home = False
                self.mouse_clicked = True
                # this is so the mouse won't stay click when we switch to the levels page
                self.levels_page.mouse_clicked = True

        if pygame.mouse.get_pressed()[0] is False:
            self.mouse_clicked = False
        

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

        self.levels_button = pygame.transform.scale(self.levels_button, (self.button_width, self.button_height))
        self.levels_rect = self.levels_button.get_rect(topleft=(self.width/5, self.height/2 + self.button_height))

    def update_snake_color(self):
        #loop through ever snake png and change the color
        icon_dir = 'icons/Snake/'
        for images in os.listdir(icon_dir):
            if images.endswith('.png'):

                name = icon_dir + str(images)
                im = Image.open(name)
                data = np.array(im)
                hex_prev = self.snake_colors[self.settings_page.previous_snake_color]['hex']
                prev_color = list(int(hex_prev[i:i+2], 16) for i in (0, 2, 4))

                hex_new = self.snake_colors[self.settings_page.current_snake_color]['hex']
                new_color = list(int(hex_new[i:i+2], 16) for i in (0, 2, 4))

                # orig color values
                r1 = prev_color[0]
                g1 = prev_color[1]
                b1 = prev_color[2]

                #new color vlaues
                r2 = new_color[0]
                g2 = new_color[1]
                b2 = new_color[2]

                # get the current rgb values from the image
                red, green, blue = data[:,:,0], data[:,:,1], data[:,:,2]
                #mask the values with the previous colors (match them)
                mask = (red == r1) & (green == g1) & (blue == b1)
                #apply the mask with the new colors (replace old with new)
                data[:,:,:3][mask] = [r2, g2, b2]

                im = Image.fromarray(data)
                im.save(name)
