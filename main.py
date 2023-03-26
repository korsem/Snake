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
        pygame.draw.rect(screen, (105, 0, 60), fruit_rect)

class SNAKE:
    def __init__(self):
        # snake is stored in a list
        self.body = [Vector2(5, 7), Vector2(6, 7), Vector2(7,7)]
        self.direction = Vector2(1, 0) # default moves to the left

    def draw_snake(self):
        for elements in self.body:
            snake_rect = pygame.Rect(int(elements.x * cell_size), int(elements.y * cell_size), cell_size, cell_size)
            pygame.draw.rect(screen, (170, 00, 60), snake_rect)
    def move_snake(self):
        body_copy = self.body[:-1] # without the last element
        body_copy.insert(0, body_copy[0] + self.direction) # snake is moving by the direction
        self.body = body_copy[:]


# setting up the window
pygame.init()

cell_size = 20
cell_number = 10

screen = pygame.display.set_mode((cell_size * cell_number, cell_number*cell_size))
pygame.display.set_caption("Snake")
screen.fill((180, 215, 70))

# How much frames per seconds
fps = pygame.time.Clock()

# fruit
fruit = FRUIT()

# snake
snake = SNAKE()

# intervals of time when snake is moving
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 200) # in miliseconds

# main loop
while True:
    for event in pygame.event.get(): # waiting for user input
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == SCREEN_UPDATE:
            snake.move_snake()
        if event.type == pygame.KEYDOWN: # keyboard controll
            if event.key == pygame.K_UP:
                snake.direction = Vector2(0, -1)
            elif event.key == pygame.K_DOWN:
                snake.direction = Vector2(0, 1)
            elif event.key == pygame.K_LEFT:
                snake.direction = Vector2(-1, 0)
            elif event.key == pygame.K_RIGHT:
                snake.direction = Vector2(1, 0)

    fruit.draw_fruit()
    snake.draw_snake()
    pygame.display.update()
    fps.tick(60)
