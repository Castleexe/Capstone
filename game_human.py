import pygame
import random
from enum import Enum
from collections import namedtuple
import time 
import PySimpleGUI as sg

pygame.init()
#font = pygame.font.Font('arial.ttf', 25)
font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    
Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)
GREEN = (141, 173, 2)

BLOCK_SIZE = 20
SPEED = 10


class SnakeGame:
    
    def __init__(self, AIscore=100, timeRemaining=30 ,w=640, h=480):
        self.w = w
        self.h = h
        self.AIscore = AIscore
        self.timeRemaining = timeRemaining * 4
        self.prevTime = time.time()
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        
        # Load images
        self.assets = {
            'apple': pygame.transform.scale(pygame.image.load('assets/apple.png'), (BLOCK_SIZE, BLOCK_SIZE)),
            'head_up': pygame.transform.scale(pygame.image.load('assets/head_up.png'), (BLOCK_SIZE, BLOCK_SIZE)),
            'head_down': pygame.transform.scale(pygame.image.load('assets/head_down.png'), (BLOCK_SIZE, BLOCK_SIZE)),
            'head_left': pygame.transform.scale(pygame.image.load('assets/head_left.png'), (BLOCK_SIZE, BLOCK_SIZE)),
            'head_right': pygame.transform.scale(pygame.image.load('assets/head_right.png'), (BLOCK_SIZE, BLOCK_SIZE)),
            'body_vertical': pygame.transform.scale(pygame.image.load('assets/body_vertical.png'), (BLOCK_SIZE, BLOCK_SIZE)),
            'body_horizontal': pygame.transform.scale(pygame.image.load('assets/body_horizontal.png'), (BLOCK_SIZE, BLOCK_SIZE)),
            'body_topleft': pygame.transform.scale(pygame.image.load('assets/body_topleft.png'), (BLOCK_SIZE, BLOCK_SIZE)),
            'body_topright': pygame.transform.scale(pygame.image.load('assets/body_topright.png'), (BLOCK_SIZE, BLOCK_SIZE)),
            'body_bottomleft': pygame.transform.scale(pygame.image.load('assets/body_bottomleft.png'), (BLOCK_SIZE, BLOCK_SIZE)),
            'body_bottomright': pygame.transform.scale(pygame.image.load('assets/body_bottomright.png'), (BLOCK_SIZE, BLOCK_SIZE)),
            'tail_up': pygame.transform.scale(pygame.image.load('assets/tail_up.png'), (BLOCK_SIZE, BLOCK_SIZE)),
            'tail_down': pygame.transform.scale(pygame.image.load('assets/tail_down.png'), (BLOCK_SIZE, BLOCK_SIZE)),
            'tail_left': pygame.transform.scale(pygame.image.load('assets/tail_left.png'), (BLOCK_SIZE, BLOCK_SIZE)),
            'tail_right': pygame.transform.scale(pygame.image.load('assets/tail_right.png'), (BLOCK_SIZE, BLOCK_SIZE)),
        }
        # init game state
        self.direction = Direction.RIGHT
        
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        
        self.score = 0
        self.food = None
        self._place_food()
        
    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()
        
    def play_step(self, first=False):
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and self.direction is not Direction.RIGHT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_d and self.direction is not Direction.LEFT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_w and self.direction is not Direction.DOWN:
                    self.direction = Direction.UP
                elif event.key == pygame.K_s and self.direction is not Direction.UP:
                    self.direction = Direction.DOWN
       
        # 2. move
        self._move(self.direction) # update the head
        self.snake.insert(0, self.head)

        currentTime = time.time()
        if (currentTime - self.prevTime >= 1):
            self.timeRemaining -= 1
            self.prevTime = time.time()

        # 3. check if game over
        game_over = False
        if self._is_collision() or self.timeRemaining <= 0:
            game_over = True
            return game_over, self.score
            
        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return game_over, self.score

    def _is_collision(self):
        # hits boundary
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        # hits itself
        if self.head in self.snake[1:]:
            return True
        
        return False
        
    def _update_ui(self):
        self.display.fill(GREEN)
        
        # Draw the food
        self.display.blit(self.assets['apple'], pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        # Draw the snake
        for i, pt in enumerate(self.snake):
            if i == 0:  # Head
                if self.direction == Direction.UP:
                    image = self.assets['head_up']
                elif self.direction == Direction.DOWN:
                    image = self.assets['head_down']
                elif self.direction == Direction.LEFT:
                    image = self.assets['head_left']
                else:  # RIGHT
                    image = self.assets['head_right']
            elif i == len(self.snake) - 1:  # Tail
                prev = self.snake[i - 1]
                if pt.y < prev.y:  # Moving up
                    image = self.assets['tail_up']
                elif pt.y > prev.y:  # Moving down
                    image = self.assets['tail_down']
                elif pt.x < prev.x:  # Moving left
                    image = self.assets['tail_left']
                else:  # Moving right
                    image = self.assets['tail_right']
            else:  # Body
                prev = self.snake[i - 1]
                next_pt = self.snake[i + 1]
                if prev.x == next_pt.x:  # Vertical
                    image = self.assets['body_vertical']
                elif prev.y == next_pt.y:  # Horizontal
                    image = self.assets['body_horizontal']
                elif (prev.x < pt.x and next_pt.y < pt.y) or (prev.y < pt.y and next_pt.x < pt.x):  # Top-left corner
                    image = self.assets['body_topleft']
                elif (prev.x > pt.x and next_pt.y < pt.y) or (prev.y < pt.y and next_pt.x > pt.x):  # Top-right corner
                    image = self.assets['body_topright']
                elif (prev.x < pt.x and next_pt.y > pt.y) or (prev.y > pt.y and next_pt.x < pt.x):  # Bottom-left corner
                    image = self.assets['body_bottomleft']
                else:  # Bottom-right corner
                    image = self.assets['body_bottomright']
            self.display.blit(image, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
                
        text = font.render("Score: " + str(self.score), True, WHITE)
        aiScore = font.render("SCORE TO BEAT: " + str(self.AIscore), True, WHITE)
        timeLeft = font.render("Time remaining: " + str(round(self.timeRemaining)) + " Seconds", True, RED)
        
        self.display.blit(text, [0, 0])
        self.display.blit(aiScore, [100, 0])
        self.display.blit(timeLeft, [350, 0])
        pygame.display.flip()
        
    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
            
        self.head = Point(x, y)
            
def playGame(AIscore, timeTaken):
    game = SnakeGame(AIscore, timeTaken)
    first = True
    # game loop
    while True:
        game_over, score = game.play_step()
        if (first):
            timer(3)
        first = False
        if game_over == True:
            showScores(score, AIscore)
            break
        
    print('Final Score', score)

def timer(duration):
    layout = [[sg.Text("", size=(10), justification="center", font=("Helvetica", 48), key="-TIMER-")]]
    window = sg.Window("Countdown Timer", layout, element_justification="center", finalize=True, no_titlebar=True)
    for remaining_time in range(duration, -1, -1):
            window["-TIMER-"].update(f"{remaining_time}")
            window.refresh()
            time.sleep(1)
    window.close()
    
def showScores(humanScore, Aiscore):
    if humanScore > Aiscore:
        sg.popup(f"Your score: {humanScore}, AI score {Aiscore} \nYou Win! ",font=50)
    else: 
        sg.popup(f"Your score: {humanScore}, AI score {Aiscore} \nAi Wins :( ", font=50)

'''
if __name__ == '__main__':
    game = SnakeGame()
    first = True
    # game loop
    while True:
        game_over, score = game.play_step(first)
        if (first):
            sleep(3)
        first = False
        if game_over == True:
            break
        
    print('Final Score', score)
        
        
    pygame.quit()
'''