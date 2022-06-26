'''
Require assets:
cat.png
find at: http://invpy.com/cat.png
'''


import pygame, sys
from pygame.locals import *

pygame.init()

FPS = 30 # frames per second settings
fpsClock = pygame.time.Clock()

# set up the window
DISPLAYSURF = pygame.display.set_mode((400, 300), 0, 32)
pygame.display.set_caption("Animation")

WHITE = (255, 255, 255)
catImg = pygame.image.load('./assets/images/cat.png')
catx = 10
caty = 10
direction = 'right'

while True: # the main game loop
    





print("Hello world, debugging done!!")