import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join #importing these to load sprites dynamically
pygame.init()

pygame.display.setcaption("Platformer") #setting window name

BGCOLOR = (255, 255, 255)
WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYERVEL = 5 #player speed

window = pygame.display.setmode((WIDTH, HEIGHT))

def main(window):
    clock = pygame.time.Clock()

    run = True
    while(run):
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
    pygame.quit()
    quit()

if __name == "__main":
    main(window) #this line makes it so that only call the main func only when we call it directly