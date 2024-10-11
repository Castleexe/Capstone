import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join #importing these to load sprites dynamically
pygame.init()

pygame.display.set_caption("Platformer") #setting window name

WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYER_VEL = 5 #player speed

window = pygame.display.set_mode((WIDTH, HEIGHT))

def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _,_, width, height = image.get_rect() #_ for values we dont care about
    tiles = []

    for i in range(WIDTH // width + 1): #tells x amount tiles
        for j in range(HEIGHT // height + 1):  #tells y amount tiles
            pos = (i * width, j * height) #pos of top left tile of current tile
            tiles.append(pos)
    return tiles, image

def draw(window, background, bg_img):
    for tile in background:
        window.blit(bg_img, tile)

    pygame.display.update()

def main(window):
    clock = pygame.time.Clock()
    background, bg_img = get_background("Green.png")

    run = True
    while(run):
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        draw(window, background, bg_img)
    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window) #this line makes it so that only call the main func only when we call it directly 