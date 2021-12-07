# Star Pusher (a Sokoban clone) 
# the original work is by Ai Sweigart: al@inventwithpython.com |
# http://inventwithpython.com/pygame


import random, sys, copy, os
from pygame import * 
#from pygame.locals import *

FPS = 30 # frames per secon to update the screen 
WIN_WIDTH = 800 
WIN_HEIGHT = 700
HALF_W = int(WIN_WIDTH / 2)
HALF_H = int(WIN_HEIGHT / 2)

# total width and height of each tile in pixels.
T_WIDTH = 50
TILE_HEIGHT = 85 
TILE_FLOOR_HEIGHT = 45 

CAM_MOVE_SPEED = 5 # how many pixels per frame the camera moves.

# the percentage of outdoor tiles that have additional 
# decoration on them, such as a tree or rock.
OUTSIDE_DECORATION_PCT = 20

BRIGHT_BLUE = (  0, 170, 255)
WHITE       = (255, 255, 255) 
BGCOLOR     = BRIGHT_BLUE
TEXTCOLOR   = WHITE

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'


def main():
	global FPSCLOCK, DISPLAYSURF, IMAGEDICT, TILEMAPPING, OUTSIDE_DECOMAPPING, BASCIFONT, PLAYER_IMAGES, current_Image

	# pygame initialization and basic set up of the global varibles
	pygame.init()
	FPSCLOCK = pygame.time.clock()

	'''
	because the surface object stored in DISPALYSURF wat returned
	from the pygame.display.set_mode() function, tis is the surface object that is
	drawn to the actual computer screen
	when pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
	'''
	DISPALYSURF = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

	pygame.display.set_caption("Star Pusher")
	BASCIFONT = pygame.font.Font("freesansbold.ttf", 18)

	# A global dict value that will contain all the Pygame
	# Surface object returned by pygame.image.load().
	IMAGEDICT = {'uncovered goal': pygame.image.load('RedSelector.png'),
	'covered goal': pygame.image.load('Selector.png'),
	'Star': pygame.image.load('Star.png'),
	'corner': pygame.image.load('Wall Block Tall.png'),
	'wall': pygame.image.load('Wood Block Wall.png'),
	'inside floor': pygame.image.load('Plain Block.png'),
	'outside floor': pygame.image.load('Grass Block.png'),
	'title': pygame.image.load('star_title.png'),
	'solved': pygame.image.load('star_solved.png'),
	'princess': pygame.image.load('princess.png'),
	'boy': pygame.image.load('boy.png'),
	'catgirl': pygame.image.load('catgirl.png'),
	'horngirl': pygame.image.load('horngirl.png'),
	'pinkgirl': pygame.image.load('pinkgirl.png'),
	'rock': pygame.image.load('Rock.png'),
	'short tree': pygame.image.load('Tree_Short.png'),
	'tall tree': pygame.image.load('Tree_Tall.png'),
	'ugly tree': pygame.image.load('Tree_Ugly.png'),
	}

	# these dict values are global, and map the character that appears
	# in the level file to the surface object it represents.
	TILEMAPPING = {
		'x': IMAGEDICT['corner'],
		'#': IMAGEDICT['wall'],
		'o': IMAGEDICT['inside floor'],
		' ': IMAGEDICT['outside floor'],}

	OUTSIDE_DECOMAPPING = {
	'1': IMAGEDICT['rock'],
	'2': IMAGEDICT['short tree'],
	'3': IMAGEDICT['tall tree'],
	'4': IMAGEDICT['ugly tree'],
	}

	# PLAYERIMAGES is a list of all possible characters the player can be.
	# currentImage is the index of the player's current player image.
	currentImage = 0
	PLAYERIMAGES = [IMAGEDICT['princess'],
		IMAGEDICT['boy'],
		IMAGEDICT['catgirl'],
		IMAGEDICT['horngirl'],
		IMAGEDICT['pinkgirl']]
	startSreen() # show the title screen until the user presses a key.

	'''
	Read the levels from the text file. see the readLevelsFile() for 
	details on the format of this file and how to make your own levels.
	'''
	levels = readLevelsFile('starPusherLevels.text')
	currentLevelIndex = 0

	'''
	The main game loop. this loop runs a single level, when the user
	# finishes that level, the next/previous level is loaded.
	'''
	while True: # main loop of the pygame
		# run the level to actually start playing the game:
		result = runLevel (levels, currentImage)

		if result in ('solved', 'next'):
			# go the next level 
			currentLevelIndex += 1
			if currentLevelIndex >= len(levels):
				# if there are no more level, go back to the first one
				currentLevelIndex = 0
		elif result == 'back':
			# back to the previous level 
			currentLevelIndex -=1
			if currentLevelIndex < 0:
				# if there are no previous levels go the last one 
				currentLevelIndex = len(levels)-1
		elif result == 'reset':
			pass # do nothing, loop re-calls runLevel() to reset the level.


def runLevel(levels, levelNum):
	global currentImage 
	levelObj = levels[levelNum]
	mapObj = decorateMap(levelObj['starState'])
	mapNeedsRedraw = True # set to true to call drawMap()
	levelSurf = BASCIFONT.render('Level %s of %s' % (levelObj['levelNum']
		+ 1, totalNumOfLevels), 1, TEXTCOLOR)
	levelRect = levelSurf.get_rect()
	levelRect.bottomleft = (20, WIN_HEIGHT - 35)
	mapWidth = len(mapObj) * TILE_WIDTH
	mapHeight = (len(mapObj[0]) - 1) * (TILE_HEIGHT - TILE_FLOOR_HEIGHT) + TILE_HEIGHT

	MAX_CAM_X_PAN = abs(HALF_H - int(mapHeight / 2)) + TILE_WIDTH
	MAX_CAM_Y_PAN = abs(HALF_W - int(mapWidth / 2)) + TILE_HEIGHT

	levelIsComplete = False
	# track down how much the camera has moved
	cameraOffsetX = 0
	cameraOffsety = 0
	# track if the keys to move the camera re being held down:
	cameraUp = False
	cameraDown = False
	cameraLeft = False
	cameraRight = False

	while True: # main game loop
		# reset these variables:
		playerMoveTo = None 
		keyPressed = False

		for event in pygame.event.get(): # event handling loop
			if event.type == QUIT:
				# player clicked the 'X' at the corner of the win
				terminate()

			elif event.type == KEYDOWN:
				# handle key presses
				keyPressed = True
				if event.key == K_LEFT:
					playerMoveTo = LEFT
				elif event.key == K_RIGHT:
					playerMoveTo = RIGHT
				elif event.key == K_UP:
					playerMoveTo = UP
				elif event.key == K_DOWN:
					playerMoveTo = DOWN
				# set the camera move mode
				elif event.key == K_a:
					cameraLeft = True 
				elif event.key == K_d:
					cameraRight = True
				elif event.key == K_w:
					cameraUp = True
				elif event.key == K_s:
					cameraDown = True

				elif event.key == K_n:
					return 'next'
				elif event.key == K_b:
					return 'back'

				elif event.key == K_ESCAPE:
					terminate() # # ESC key to quite
				elif event.key == K_BACKSPACE:
					return 'reset'

				elif event.key == K_p:
					# change the player image to the next one.
					currentImage += 1
					if currentImage >= len(PLAYERIMAGES):
						# after the last player image, use the first one.
						currentImage = 0
					mapNeedsRedraw = True

			elif event.type == KEYUP:
				# unset the camera move mode.
				if event.key == K_a:
					cameraLeft = False
				elif event.key == K_d:
					cameraRight = False
				elif event.key == K_w:
					cameraUp = False
				elif event.key == K_s:
					cameraDown = False

		if playerMoveTo != None and not levelIsComplete:
			# if the player pushed a key to move, make the move
			# (if possible) and push any stars that are pushable 
			moved = makeMove(mapObj, gameStatObj, playerMoveTo)

			if moved:
				# increment  the step counter 
				gameStatObj['stepCounter'] += 1
				mapNeedsRedraw = True 
			if levelIsComplete(levelObj, gameStatObj):
				# level is solved, we should show the "solved" image.
				levelIsComplete = True 
				keyPressed = False

		DISPALYSURF.fill(BGCOLOR)
		


print("star Pusher done: pg~266")