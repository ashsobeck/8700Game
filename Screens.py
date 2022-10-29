import pygame

EASY=350
MEDIUM=200
HARD=100
class Screens:
    def __init__(self, window, width, height):
        self.window = window
        self.width = width
        self.height = height

        self.spider_webs = pygame.image.load("icons/spider_webs.jpg").convert()
        self.spider_webs = pygame.transform.scale(self.spider_webs, (self.width, self.height))

        self.start_button = pygame.image.load("icons/Start.png").convert()
        self.start_button = pygame.transform.scale(self.start_button, (163, 45))
        self.start_rect = self.start_button.get_rect()
        self.start_rect.topleft = (200, 300)
        self.easy_button = pygame.image.load("icons/Easy.png").convert()
        self.easy_button = pygame.transform.scale(self.easy_button, (163, 45))
        self.easy_rect = self.easy_button.get_rect()
        self.easy_rect.topleft = (200, 500)
        self.medium_button = pygame.image.load("icons/Medium.png").convert()
        self.medium_button = pygame.transform.scale(self.medium_button, (163, 45))
        self.medium_rect = self.medium_button.get_rect()
        self.medium_rect.topleft = (400, 500)
        self.hard_button = pygame.image.load("icons/Hard.png").convert()
        self.hard_button = pygame.transform.scale(self.hard_button, (163, 45))
        self.hard_rect = self.hard_button.get_rect()
        self.hard_rect.topleft = (600, 500)

        self.difficulty = MEDIUM
        self.background_image = self.spider_webs

    def draw_home_buttons(self):
        self.easy_button.set_alpha(100)
        self.medium_button.set_alpha(100)
        self.hard_button.set_alpha(100)

        if self.difficulty == EASY: self.easy_button.set_alpha(255)
        elif self.difficulty == MEDIUM: self.medium_button.set_alpha(255)
        elif self.difficulty == HARD: self.hard_button.set_alpha(255)

        self.window.blit(self.start_button, (self.start_rect.x, self.start_rect.y))
        self.window.blit(self.easy_button, (self.easy_rect.x, self.easy_rect.y))
        self.window.blit(self.medium_button, (self.medium_rect.x, self.medium_rect.y))
        self.window.blit(self.hard_button, (self.hard_rect.x, self.hard_rect.y))

    def start_game(self):
        m_pos = pygame.mouse.get_pos()

        if self.start_rect.collidepoint(m_pos):
            if pygame.mouse.get_pressed()[0]:
                return True
        return False

    def get_difficulty(self):
        m_pos = pygame.mouse.get_pos()

        if self.easy_rect.collidepoint(m_pos):
            if pygame.mouse.get_pressed()[0]:
                self.difficulty = EASY
        elif self.medium_rect.collidepoint(m_pos):
            if pygame.mouse.get_pressed()[0]:
                self.difficulty = MEDIUM
        elif self.hard_rect.collidepoint(m_pos):
            if pygame.mouse.get_pressed()[0]:
                self.difficulty = HARD
