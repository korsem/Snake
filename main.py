# importing libraries
import pygame
from sys import exit
from pygame.math import Vector2
from math import floor
import random

class FRUIT:
    def __init__(self):
        # starting position
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x,self.y)

    def draw_fruit(self): # actually fruit is croissant because croissants are yummy
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(snacky, fruit_rect)
    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x,self.y)

class COFFEE: # snake likes coffee snake likes fast snack is even better with coffee
    def __init__(self):
        # starting position of coffee is out of my area
        self.x = cell_number
        self.y = cell_number
        self.pos = Vector2(self.x,self.y)
        # wheter snake goes faaaast
        self.speed = False

    def draw_coffee(self):
        coffee_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(coffee, coffee_rect)
    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x,self.y)

    def drunk(self):
        self.x = cell_number
        self.y = cell_number
        self.pos = Vector2(self.x, self.y)


class SNAKE:
    def __init__(self):
        # snake is stored in a list
        self.body = [Vector2(4, 7), Vector2(3, 7), Vector2(2,7)]
        self.direction = Vector2(1, 0) # default moves to the left
        self.new_block = False # if the new block will be added
        # snake's speed
        self.speed_multiplier = 1 # currently if snakes is faster it doesnt eat
        self.boost_duration = 10000  # 10 seconds in milliseconds
        self.boost_end_time = 0  # time at which the speed boost will end

    def draw_snake(self):
        for elements in self.body:
            snake_rect = pygame.Rect(int(elements.x * cell_size), int(elements.y * cell_size), cell_size, cell_size)
            pygame.draw.rect(screen, (170, 00, 60), snake_rect)
    def move_snake(self):
        if self.new_block == False:
            body_copy = self.body[:-(self.speed_multiplier)] # without the last element
        else: # if the new block will be added
            body_copy = self.body[:] # with the last element because snake has eaten the snack
            self.new_block = False
        body_copy.insert(0, body_copy[0] + self.direction) # snake is moving by the direction

        if(self.speed_multiplier == 2): # but cant change direction after 1 block
            self.body = body_copy[:]
            main_game.check_collision()
            body_copy.insert(0, body_copy[0] + self.direction)

        self.body = body_copy[:]
        screen.fill((180, 215, 70)) # I need to think of a better way to update the screen (without that you can still see the "old" parts of the snake)

    def add_block(self):
        self.new_block = True

    def fast(self):
        if self.speed_multiplier == 1:
            self.speed_multiplier = 2
            boost_start_time = pygame.time.get_ticks()  # record the time when the speed boost starts
            self.boost_end_time = boost_start_time + self.boost_duration
        else:
            self.speed_multiplier = 1
            self.boost_end_time = 0
    def verify_speed(self): # if my snake has speed_multiplier == 2 i want it to get back to normal after certain time (10 seconds)
        if self.speed_multiplier == 2 and pygame.time.get_ticks() >= self.boost_end_time:
            self.fast()


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.boost = COFFEE()
    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
        self.snake.verify_speed()
    def draw_elements(self):
        self.draw_grass()
        self.boost.draw_coffee()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()

            # it draws whether there will be a boost
            draw = random.randint(0, 3) # 33% chance of a boost occuring
            if draw == 0:
                self.boost.randomize()
        elif self.boost.pos == self.snake.body[0]:
            self.boost.drunk()
            self.snake.fast()
    def game_over(self):
        pygame.quit()
        exit()

    def check_fail(self):
        if not (0 <= self.snake.body[0].x < cell_number and 0 <= self.snake.body[0].y < cell_number): # if snake's head hits the walls it is game over
            self.game_over()
        for element in self.snake.body[1:]: # if snake hits itself its game over
            if element == self.snake.body[0]:
                self.game_over()
    def draw_grass(self):
        grass_color = (170, 200, 60)
        for row in range(cell_size):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 == 1:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
    def draw_score(self):
        score_text = ": "+str(len(self.snake.body)-3) # score is the number of snacks snake has eaten
        score_surface = game_font.render(score_text, True, (80, 90, 12))
        score_x = int(cell_size * cell_number - cell_size)
        score_y = int(cell_size * cell_number - cell_size//2)

        score_rect = score_surface.get_rect(center = (score_x, score_y))
        snacky_rect = snacky.get_rect(midright = (score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(snacky_rect.left, snacky_rect.top, snacky_rect.width + score_rect.width + 5, snacky_rect.height + score_rect.height)

        pygame.draw.rect(screen, (165, 208, 80), bg_rect,2)
        screen.blit(score_surface, score_rect)
        screen.blit(snacky,snacky_rect)
        pygame.draw.rect(screen, (80, 90, 12), bg_rect, 2) # frame over the score

# setting up the window
pygame.init()

cell_size = 35
cell_number = 15

screen = pygame.display.set_mode((cell_size * cell_number, cell_number * cell_size))
pygame.display.set_caption("Snake")
screen.fill((180, 215, 70))

# loading my images and scaling them
snacky = pygame.image.load('Graphics/croissant.png').convert_alpha()
snacky = pygame.transform.scale(snacky, (cell_size, cell_size))

coffee = pygame.image.load('Graphics/coffee.png').convert_alpha()
coffee = pygame.transform.scale(coffee, (cell_size, cell_size))

# adding font
game_font = pygame.font.Font(None, floor(cell_size * 0.7)) # None is default font

# How much frames per seconds
fps = pygame.time.Clock()

# fruit
fruit = FRUIT()

#coffee
boost = COFFEE()

# snake
snake = SNAKE()

# intervals of time when snake is moving
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 200) # in miliseconds

main_game = MAIN()

# main loop
while True:
    for event in pygame.event.get(): # waiting for user input
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN: # keyboard control
            if event.key == pygame.K_UP and main_game.snake.direction.y != 1:
                main_game.snake.direction = Vector2(0, -1)
            elif event.key == pygame.K_DOWN and main_game.snake.direction.y != -1:
                main_game.snake.direction = Vector2(0, 1)
            elif event.key == pygame.K_LEFT and main_game.snake.direction.x != 1:
                main_game.snake.direction = Vector2(-1, 0)
            elif event.key == pygame.K_RIGHT and main_game.snake.direction.x != -1:
                main_game.snake.direction = Vector2(1, 0)
    main_game.draw_elements()
    pygame.display.update()
    fps.tick(60)

