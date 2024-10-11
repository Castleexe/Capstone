import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join #importing these to load sprites dynamically
pygame.init()

pygame.display.set_caption("Platformer") #setting window name

BG_COLOR = (255, 255, 255)
WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYER_VEL = 5 #player speed

window = pygame.display.set_mode((WIDTH, HEIGHT))

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

if __name__ == "__main__":
    main(window) #this line makes it so that only call the main func only when we call it directly 