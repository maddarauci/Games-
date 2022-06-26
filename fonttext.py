'''
Hello World program using pygame's font functions.
'''

import pygame, sys 
from pygame.locals import *

pygame.init()
DISPLAYSURF = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Hello World!")


# playing sound.
import time
soundObj = pygame.mixer.Sound('./assets/audio/beep1.ogg')
soundObj.play()
time.sleep(1) # wait and let the sound play for 1 second.
soundObj.stop()


WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)


fontObj = pygame.font.Font('freesansbold.ttf', 32)
textSurfaceObj = fontObj.render('Hello World!', True, GREEN, BLUE)
textRectObj = textSurfaceObj.get_rect()
textRectObj.center = (200, 150)

# main game loop 
while True:
    DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()