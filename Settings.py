from xmlrpc.client import Boolean
import pygame
import json

class Settings_Screen:
    def __init__(self, window, json_information: json, snake_colors: dict, snake_color_list: list, width=960, height=640, block_size=32):

        self.window = window
        self.width = width
        self.height = height
        self.block_size = block_size
        self.information = json_information
        self.snake_colors = snake_colors
        self.snake_colors_list = snake_color_list

        self.button_width = int(self.width/6)
        self.button_height = int(self.button_width/4)
        self.image_width = int(self.width/4)
        self.image_height = int(self.image_width/3)
        # will have a list of the images with 4 components
        # [image surface (image.jpg), scaled down image, image rect (used for mouse click and placement), boolean (is this the background image)]
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
        self.background_button = pygame.image.load("icons/Buttons/Background.png").convert()
        self.snake_color_button = pygame.image.load("icons/Buttons/Snake_Color.png").convert()

        self.current_snake_color = self.information["prev_color"]
        self.mouse_clicked = False

        # keep a list of the image names
        self.image_names = [self.spider_webs_image, self.boards_image, self.forest_image, 
                            self.cemetary_moon_image,self.cemetary_pump_image, self.cemetary_image, 
                            self.moon_image, self.witch_image, self.scarecrow_image]
        self.init_background_images()
        self.background_image = pygame.transform.scale(self.image_list[self.information["background_image_index"]][0], (self.width, self.height))
        #set image background to true in the image list
        self.image_list[self.information["background_image_index"]][3] = True


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

    #check if a button was clicked in the settings page
    # returns two booleans, the first one is if we go back to home page
    # second boolean is if we should update snake color
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
                    with open("information.json", "w") as j_file:
                        self.information['background_image_index'] = index
                        json.dump(self.information, j_file, indent=2)
                    self.mouse_clicked = True
                    return False, False

        if self.arrow_rect.collidepoint(m_pos):
            if pygame.mouse.get_pressed()[0] and not self.mouse_clicked:
                self.background_switcher = False
                self.home = True
                self.mouse_clicked = True
                return True, False

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
                with open("information.json", "w") as j_file:
                    self.information['prev_color'] = self.current_snake_color
                    json.dump(self.information, j_file, indent=2)
                return False, True

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
                with open("information.json", "w") as j_file:
                    self.information['prev_color'] = self.current_snake_color
                    json.dump(self.information, j_file, indent=2)
                return False, True
                
        
        if not pygame.mouse.get_pressed()[0]:
            self.mouse_clicked = False
        
        return False, False

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

        self.background_button = pygame.transform.scale(self.background_button, (self.button_width, self.button_height))
        self.snake_color_button = pygame.transform.scale(self.snake_color_button, (self.button_width, self.button_height))