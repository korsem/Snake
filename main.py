# importing libraries
import pygame
from sys import exit
from pygame.math import Vector2
import time
import random

class FRUIT
    def _init_(self):
        #pozycja startowa
        self.x = 5
        self.y = 5
        self.pos = Vector2(self.x,self.y)

    def draw_fruit(self):
        fruit_rect = pygame_Rect(self.pos.x,self.pos.y, cell_size, cell_size)
        pygame.draw.rect(surface, color, fruit_rect)

#setting up the window
pygame.init()

cell_size = 20
cell_number = 10

screen = pygame.display.set_mode((cell_size * cell_number, cell_number*cell_size))
pygame.display.set_caption("Snake")
screen.fill((150, 00, 73))

#How much frames per seconds
fps = pygame.time.Clock()

#rectange


#main loop
while True:
    for event in pygame.event.get(): #waiting for user input
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    pygame.display.update()
    fps.tick(60)
