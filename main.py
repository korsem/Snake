# importing libraries
import pygame
from sys import exit
from pygame.math import Vector2
import time
import random

class FRUIT:
    def __init__(self):
        # pozycja startowa
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x,self.y)

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(snacky, fruit_rect)
    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x,self.y)

class SNAKE:
    def __init__(self):
        # snake is stored in a list
        self.body = [Vector2(4, 7), Vector2(3, 7), Vector2(2,7)]
        self.direction = Vector2(1, 0) # default moves to the left
        self.new_block = False
    def draw_snake(self):
        for elements in self.body:
            snake_rect = pygame.Rect(int(elements.x * cell_size), int(elements.y * cell_size), cell_size, cell_size)
            pygame.draw.rect(screen, (170, 00, 60), snake_rect)
    def move_snake(self):
        if self.new_block == False:
            body_copy = self.body[:-1] # without the last element
        else:
            body_copy = self.body[:] # with the last element because snake has eaten the snack
            self.new_block = False
        body_copy.insert(0, body_copy[0] + self.direction) # snake is moving by the direction
        self.body = body_copy[:]
        screen.fill((180, 215, 70)) # I need to think of a better way to update the screen (without that you can still see the "old" parts of the snake)

    def add_block(self):
        self.new_block = True

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()

    def game_over(self):
        pygame.quit()
        exit()
        print("ups")

    def check_fail(self):
        if not (0 <= self.snake.body[0].x < cell_number and 0 <= self.snake.body[0].y < cell_number): # if snake's head hits the walls its game over
            self.game_over()
        for element in self.snake.body[1:]: # if snake hits itself its game over
            if element == self.snake.body[0]:
                self.game_over()



# setting up the window
pygame.init()

cell_size = 35
cell_number = 15

screen = pygame.display.set_mode((cell_size * cell_number, cell_number * cell_size))
pygame.display.set_caption("Snake")
screen.fill((180, 215, 70))

# loading my image and scaling it
snacky = pygame.image.load('Graphics/croissant.png').convert_alpha()
snacky = pygame.transform.scale(snacky, (cell_size, cell_size))

# How much frames per seconds
fps = pygame.time.Clock()

# fruit
fruit = FRUIT()

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
