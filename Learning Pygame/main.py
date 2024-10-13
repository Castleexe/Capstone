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

class Player(pygame.sprite.Sprite):
    color = (255, 0, 0)
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left" #what direction player is facing
        self.animation_count = 0 #to reset animation when going left or right
    
    def move(self, dx, dy):
        self.rect.x += dx #displacement x
        self.rect.y += dy #displacement y
    
    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0
    
    def loop(self, fps): #run once every frame
        self.move(self.x_vel, self.y_vel)
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)


def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _,_, width, height = image.get_rect() #_ for values we dont care about
    tiles = []

    for i in range(WIDTH // width + 1): #tells x amount tiles
        for j in range(HEIGHT // height + 1):  #tells y amount tiles
            pos = (i * width, j * height) #pos of top left tile of current tile
            tiles.append(pos)
    return tiles, image

def draw(window, background, bg_img, player):
    for tile in background:
        window.blit(bg_img, tile)

    player.draw(window)

    pygame.display.update()

def main(window):
    clock = pygame.time.Clock()
    background, bg_img = get_background("Green.png")

    player = Player(100,100,50,50)

    run = True
    while(run):
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        draw(window, background, bg_img, player)
    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window) #this line makes it so that only call the main func only when we call it directly 