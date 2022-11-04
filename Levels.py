from numpy import block
import pygame

class Levels:

    def __init__(self, window, width, height, block_size, information: dict):

        self.window = window
        self.width = width
        self.height = height
        self.block_size = block_size
        self.block_image = pygame.image.load("icons/block.png").convert()
        self.back_arrow = pygame.image.load("icons/Left_Arrow.png").convert()
        self.back_arrow.set_alpha(255)
        self.back_arrow_rect = self.back_arrow.get_rect(topleft=(2*self.block_size, 2*self.block_size))


        self.mouse_clicked = False


    def draw_levels_screen(self, background):
        self.window.blit(background, (0,0))
        self.window.blit(self.back_arrow, self.back_arrow_rect)

    # Screens will be calling this function. If it returns True (default) then
    # it will stay on the levels page. If it returns false (back button clicked)
    # then screens will display the home page
    def get_click(self):
        m_pos = pygame.mouse.get_pos()

        if self.back_arrow_rect.collidepoint(m_pos):
            if pygame.mouse.get_pressed()[0] and not self.mouse_clicked:
                self.mouse_clicked = True
                return False

        if pygame.mouse.get_pressed()[0] is False:
            self.mouse_clicked = False

        return True