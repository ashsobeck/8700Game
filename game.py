import pygame
import json
from Screens import Screens
from pumpkin import Pumpkin
from snake import Snake

# Init pygame


class Game(object):
    __instance = None
    WIDTH = 960
    HEIGHT = 640
    BLOCK_SIZE = 32

    def __new__(cls, width=960, height=640, block_size=32):
        if Game.__instance is None:
            print('Game Initializing...')
            Game.__instance = object.__new__(cls)
        Game.__instance.width = width
        Game.__instance.height = height
        Game.__instance.block_size = block_size
        return Game.__instance
    
    def run(self):
        pygame.init()
        pygame.font.init()
        
        window = pygame.display.set_mode((self.width, self.height))

        clock = pygame.time.Clock()
        pygame.display.set_caption("Haunted Ghost Snake")
        icon = pygame.image.load("icons/scream.png")
        pygame.display.set_icon(icon)

        #keep track of prev color so we know what pixel color to look for when editing png files
        #keep it in a json file so we can record it from instance to instance
        with open("information.json", "r") as j:
            information = json.load(j)


        #create our snek
        snake = Snake(window, information, self.width,
                      self.height, self.block_size)
        screens = Screens(window, snake, information, self.width, self.height, self.block_size)
        running = True
        snake_alive = True

        SCREEN_UPDATE = pygame.USEREVENT
        timer_set = False
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == SCREEN_UPDATE and snake_alive and screens.game_start:
                    # when the timer goes off then move the snake
                    snake.move_snake()
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and snake.direction != 'right':
                        snake.next_direction = 'left'
                    if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and snake.direction != 'left':
                        snake.next_direction = 'right'
                    if (event.key == pygame.K_UP or event.key == pygame.K_w) and snake.direction != 'down':
                        snake.next_direction = 'up'
                    if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and snake.direction != 'up':
                        snake.next_direction = 'down'
                    if not snake_alive:
                        if event.key == pygame.K_SPACE:
                            #make a new snake
                            snake = Snake(window, information, self.width, self.height,
                                            self.block_size)
                            screens.game_snake = snake
                            snake.update_difficulty(screens.difficulty)
                            screens.game_start = False
                            snake_alive = True
                            timer_set = False

            window.blit(screens.background_image, (0, 0))

            if screens.game_start:
                #draw snek
                snake.draw_snake()

                # will check if the snake has eaten a pumpkin and will create
                # a new pumpkin as well as elongate the snake.
                # will also draw the pumpkins on the screen
                snake.if_eat_pumpkin()

                #check if the snake collides with itself or border
                if snake.if_death():
                    snake_alive = False
                    snake.draw_death()
            else:
                screens.draw_menu()

            #update the display
            pygame.display.update()

            # this means the game operates at 60 fps, just makes the movements smoother and not choppy
            clock.tick(60)

            if screens.game_start and not timer_set:
                pygame.time.set_timer(SCREEN_UPDATE, screens.difficulty)
                timer_set = True

# 32 pixel images. 30 Cells in x direction, 20 cells in Y direction


# set the window size


# set the icon and game name

