import pygame
from pygame.locals import *
import sys, random, time

pygame.init()

''' ** how the drawing functions work in pygame for different shapes
pygame.draw.polygon(surface, color, pointlist, width)
pygame.draw.line(surface, color, start_point, end_point, width)
pygame.draw.lines(surface, color, closed, pointlist, width)
pygame.draw.circle(surface, color, center_point, radius, width)
pygame.draw.ellipse(surface, color, bounding_rectangle, width)
pygame.draw.rect(surface, color, rectangle_tuple, width)
'''

# global varibales
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5


# colors
BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (129,129,129)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
# another way to do it with the pygame objects method is -->
#color1 = pygame.Color(0,0,0)

# display resolution
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("GAME")
# frames per second
FPS = 60
FramePerSec = pygame.time.Clock()
SCORE = 0

# setting font_small_render
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Gamer OVer", True, BLACK)

backgorund = pygame.image.load('AnimatedStreet.png')

DISPLAYSURF.blit(backgorund, (0,0))

# drawing a simple robot face with shapes
# Assign FPS a value
'''
FPS = 30
FramePerSec = pygame.time.Clock()

# creating the shapes
pygame.draw.line(DISPLAYSURF, BLUE, (150,130), (130, 170))
pygame.draw.line(DISPLAYSURF, BLUE, (150,130), (170, 170))
pygame.draw.line(DISPLAYSURF, GREEN, (130,170), (170, 170))

pygame.draw.circle(DISPLAYSURF, BLACK, (100,50), 30)
pygame.draw.circle(DISPLAYSURF, BLUE, (200,50), 30)

pygame.draw.rect(DISPLAYSURF, RED, (100,200, 100, 50),2)
pygame.draw.rect(DISPLAYSURF, BLACK, (110,260, 80, 5))
'''

# the race game now begins

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('enemy.png')
        self.surf = pygame.Surface((50,80))
        #self.rect = self.surf.get_rect(center = (random.randint(40, SCREEN_WIDTH-40), 0)),SCREEN_HEIGHT)

        self.rect = self.surf.get_rect(center = (random.randint(40,SCREEN_WIDTH-40), 0))

    def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        if (self.rect.bottom > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
            #self.rect.center = (random.randint(30, 370), 0)  #'[  car | car ]'
'''
    def draw(self, surface):
        surface.blit(self.image, self.rect)
'''

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Player.png')
        self.surf = pygame.Surface((40, 75))
        self.rect = self.surf.get_rect(center = (160, 520))
        #self.rect = self.surf.get_rect()

    def move(self):
        pressed_keys =pygame.key.get_pressed()
        '''
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, - +1)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 3)
        '''
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)
    '''
    def draw(self, surface):
        surface.blit(self.image, self.rect)
    '''

# setting up the sprites
P1 = Player()
E1 = Enemy()

# sprites group
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

# adding a new user event
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# game loop
while True:
    # quiting the game (game loop)
    for event in pygame.event.get(): # scans for the events that ocure during the game. the type attr tells us what type it is
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(backgorund, (0,0))
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))

    # movement
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # collision dection
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(0.5)

        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30,250))

        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit

    pygame.display.update()
    FramePerSec.tick(FPS)
