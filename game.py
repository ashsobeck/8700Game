import pygame
import json
import random
from Screens import Screens
from pumpkin import Pumpkin
from snake import Snake
from blocker import Blocker
from blocker_structures import *


# Init pygame


class Game(object):
    __instance = None
    width = 960
    height = 640
    block_size = 32
    blockers = 10

    # this makes our singleton
    def __new__(cls, width=960, height=640, block_size=32, blockers=10):
        if Game.__instance is None:
            print('Game Initializing...')
            Game.__instance = object.__new__(cls)
        Game.__instance.width = width
        Game.__instance.height = height
        Game.__instance.block_size = block_size
        Game.__instance.blockers = blockers
        return Game.__instance

    def generate_nums_not_in_snake(self, snake_body):
        cells_x = self.width/self.block_size
        cells_y = self.height/self.block_size
        x, y = random.randint(0, cells_x - 1), random.randint(0, cells_y - 1)

        while [x, y] in snake_body:
            x, y = random.randint(0, cells_x - 1), random.randint(0, cells_y - 1)

        return (x, y)

    def make_blockers(self, window, snake_body):
        b = Blocker(window, snake_body, self.width, self.height, self.block_size)
        # creates random amounts of rows, columns and diagonals
        col_len = random.randint(1, 5)
        row_len = random.randint(1, 5)
        diag_len = random.randint(1, 5)
        blocker_list = []
        for i in range(col_len):
            col_x, col_y = self.generate_nums_not_in_snake(snake_body)
            blocker_list.extend(make_col(col_x, col_y, col_len, b))
        for i in range(row_len):
            row_x, row_y = self.generate_nums_not_in_snake(snake_body)
            blocker_list.extend(make_row(row_x, row_y, row_len, b))
        for i in range(diag_len):
            diag_x, diag_y = self.generate_nums_not_in_snake(snake_body)
            blocker_list.extend(make_diagonal(diag_x, diag_y, diag_len, b))

        print(blocker_list)
        return blocker_list

    def get_blocker_coord(self, blocker_list: list[Blocker]):
        coord_list = [blocker.position for blocker in blocker_list]
        for index, pos in enumerate(coord_list):
            pos[0] = int(pos[0] / self.block_size)
            pos[1] = int(pos[1] / self.block_size)
            coord_list[index] = pos

        return coord_list

    def run(self):
        pygame.init()
        pygame.font.init()

        window = pygame.display.set_mode((self.width, self.height))

        clock = pygame.time.Clock()
        pygame.display.set_caption("Haunted Ghost Snake")
        icon = pygame.image.load("icons/scream.png")
        pygame.display.set_icon(icon)

        # keep track of prev color so we know what pixel color to look for
        # when editing png files
        # keep it in a json file so we can record it from instance to instance
        with open("information.json", "r") as j:
            information = json.load(j)

        # create our snek
        snake = Snake(window, self.width,
                      self.height, self.block_size)
        screens = Screens(window, snake, information, self.width, self.height, self.block_size)
        running = True
        snake_alive = True
        blockers = self.make_blockers(window, snake.body) 
        blocker_coord = self.get_blocker_coord(blockers)
        pumpkin_list = [Pumpkin(window)]
        pumpkin_list[0].random_pos(snake.body, screens.levels_class.current_level_coord)
        selected_level = screens.levels_class.selected_level
        snake.level_highscore = information['level_highscores'][selected_level][str(snake.difficulty)]
    
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
                            # make a new snake
                            snake = Snake(window, self.width,
                                          self.height, self.block_size)
                            screens.game_snake = snake
                            snake.update_difficulty(screens.difficulty)
                            screens.game_start = False
                            snake_alive = True
                            timer_set = False
                            blockers = self.make_blockers(window, snake.body)
                            blocker_coord = self.get_blocker_coord(blockers)
                            pumpkin_list = [Pumpkin(window)]
                            if random:
                                pumpkin_list[0].random_pos(snake.body, blocker_coord)
                            else:
                                pumpkin_list[0].random_pos(snake.body, screens.levels_class.current_level_coord)

            window.blit(screens.background_image, (0, 0))
            is_random_level = screens.levels_class.random_level
            if screens.game_start:
                if is_random_level:
                    for block in blockers:
                        block.draw()
                else:
                    screens.levels_class.draw_level()
                # draw snek
                snake.draw_snake()

                # will check if the snake has eaten a pumpkin and will create
                # a new pumpkin as well as elongate the snake.
                # will also draw the pumpkins on the screen
                pump_list_copy = pumpkin_list
                # for each pumpkin
                for pump in pumpkin_list:
                    pump.draw()
                    # pumpking checks if it has collided with the snake
                    create_new, destroy = pump.if_collision(snake.rect)
                    # clone the pumpkin and randomly place it on the map
                    if create_new:
                        snake.new_body = True
                        snake.score += 1
                        p = pump.clone()
                        if is_random_level:
                            p.random_pos(snake.body, blocker_coord)
                        else:
                            p.random_pos(snake.body, screens.levels_class.current_level_coord)
                        # add the new pumpking to the list
                        pump_list_copy.append(p)
                        # update the score of he difficulty and level in the json file
                        if is_random_level:
                            snake.level_highscore = information['random_highscore'][str(snake.difficulty)]
                            if snake.score > snake.level_highscore:
                                with open("information.json", "w") as j_file:
                                    information['random_highscore'][str(snake.difficulty)] = snake.score
                                    snake.level_highscore = snake.score
                                    json.dump(information, j_file, indent=4)
                        else:
                            snake.level_highscore = information['level_highscores'][selected_level][str(snake.difficulty)]
                            if snake.score > snake.level_highscore:
                                with open("information.json", "w") as j_file:
                                    information['level_highscores'][selected_level][str(snake.difficulty)] = snake.score
                                    snake.level_highscore = snake.score
                                    json.dump(information, j_file, indent=4)
                # if the eaten pumpkin has gone through the whole snake, remove from list
                    if destroy:
                        # removes specific class instance from list
                        pump_list_copy.remove(pump)
                # reset pumpkin list
                pumpkin_list = pump_list_copy

                # check if the snake collides with itself or border
                if is_random_level:
                    if snake.if_death(blocker.rect for blocker in blockers):
                        snake_alive = False
                        snake.draw_death()
                else:
                    if snake.if_death(screens.levels_class.current_level_rect):
                        snake_alive = False
                        snake.draw_death()
            else:
                screens.draw_menu()
                if is_random_level:
                    if selected_level != -1:
                        #if the user has changed the level, change the random position of the first pump
                        pumpkin_list[0].random_pos(snake.body, screens.levels_class.current_level_coord)
                        selected_level = screens.levels_class.selected_level
                    snake.level_highscore = information['random_highscore'][str(snake.difficulty)]
                else:
                    if selected_level != screens.levels_class.selected_level:
                        # if the user has changed the level, change the random position of the first pump
                        pumpkin_list[0].random_pos(snake.body, screens.levels_class.current_level_coord)
                        selected_level = screens.levels_class.selected_level
                    # if the user changed difficulty, set highscore for that difficulty
                    snake.level_highscore = information['level_highscores'][selected_level][str(snake.difficulty)]

            # update the display
            pygame.display.update()

            # this means the game operates at 60 fps, just makes the movements
            # smoother and not choppy
            clock.tick(60)

            if screens.game_start and not timer_set:
                pygame.time.set_timer(SCREEN_UPDATE, screens.difficulty)
                timer_set = True

# 32 pixel images. 30 Cells in x direction, 20 cells in Y direction


# set the window size


# set the icon and game name
