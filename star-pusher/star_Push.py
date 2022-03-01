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

		if mapNeedsRedraw:
			mapSurf = drawMap(mapObj, gameStatObj, levelObj['goals'])
			mapNeedsRedraw =  False
		if cameraUp and cameraOffsety < MAX_CAM_X_PAN:
			cameraOffsety += CAM_MOVE_SPEED
		elif cameraDown and cameraOffsety > -MAX_CAM_X_PAN:
			cameraOffsety -= CAM_MOVE_SPEED
		if cameraLeft and cameraOffsetX < MAX_CAM_Y_PAN:
			cameraOffsetX += CAM_MOVE_SPEED
		elif cameraRight and cameraOffsetX > -MAX_CAM_Y_PAN:
			cameraOffsetX -= CAM_MOVE_SPEED

		# adjust mapSurf;s Rect object based on the camera offset.
		mapSurfRect = mapSurf.get_rect()
		mapSurfRect.center = (HALF_W + cameraOffsetX, HALF_H + cameraOffsety)

		# draw  mapSurf to the to DISPLAYSURF Surface objects.
		DISPLAYSURF.blit(mapSurf, mapSurfRect)

		DISPLAYSURF.blit(levelSurf, levelRect)
		stepSurf = BASCIFONT.render("Steps: %s" % (gameStatObj['stepCounter']), 1, TEXTCOLOR)
		stepRect = stepSurf.get_rect()
		stepRect.bottomleft = (20, WIN_HEIGHT - 10)
		DISPLAYSURF.blit(stepSurf, stepRect)

		if levelIsComplete:
			# is solved, show the "solved!" image until the player has pressed a key.
			solvedRect = IMAGEDICT['solved'].get_rect()
			solvedRect.center(IMAGEDICT['solved'], solvedRect)

			if keyPressed:
				return 'solved'

		pygame.display.update() # draw DISPLAYSURF to the screen.
		FPSCLOCK.tick()

def decorateMap(mapObj, startxy):
	'''
	Makes a copy of the given map object and modifies it.
	here is what is don to it:
	    * walls that are corners are turned into corner pieces.
	    * the outside/inside floor tile distinction is made.
	    * tree/rock decorations are randomly added to the outside tiles.

	returns the deocrated map object.
	'''
	startx, starty = startxy # Syntactic sugar

	# copy the map object so we dont modify the original passed.
	mapObjCopy = copy.deepcopy(mapObj)

	# remove the non-wall characters from the map data.
	for x in range(len(mapObjCopy)):
		for y in range(len(mapObjCopy[0])):
			if mapObjCopy[x][y] in ('$', '.', '@', '+', '*'):
				mapObjCopy[x][y] = ' '

	# flood fill to determine inside/outside floor tiles.
	floorFill(mapObjCopy, startx, starty, ' ', 'o')

	# convert the adjoined walls into corner tiles.
	for x in range(len(mapObjCopy)):
		for y in range(len(mapObjCopy[0])):

			if mapObjCopy[x][y] == "#":
				if (isWall(mapObjCopy, x, y-1) and isWall(mapObjCopy, x+1, y)) or \
				(isWall(mapObjCopy, x+1, y) and isWall(mapObjCopy, x, y+1)) or \
				(isWall(mapObjCopy, x, y+1) and isWall(mapObjCopy, x-1, y)) or \
				(isWall(mapObjCopy, x-1, y) and isWall(mapObjCopy, x, y-1)):
					mapObjCopy[x][y] = 'x'
			elif mapObjCopy[x][y] == ' ' and random.randint(0, 99) < OUTSIDE_DECORATION_PCT:
				mapObjCopy[x][y] = random.choice(list(OUTSIDE_DECOMAPPING.keys()))

	return mapObjCopy

def isBlocked(mapObj, gameStatObj, x, y):
	'''
		Return true if the (x, y) position on the map is 
		block by a wall or star, otherwise return False.
	'''
	if isWall(mapObj, x, y):
		return True
	elif x < 0 or x >= len(mapObj) or y < 0 or y >= len(mapObj[x]):
		return True # x and y aren't actually on the map.
	elif (x, y) in gameStatObj['start']:
		return True # a star is blocking 

	return False

def makeMove(mapObj, gameStatObj, playerMoveTo):
	'''
	given a map and game state object, see if it is possible for the player to make the given move.
	if it is, then change the player's position (and the position of any pushed star). if not, do nothing.

	return True if the player moved, otherwise False.
	'''

	# can the player move in any direction ?
	playerx, playery = gameStatObj['player']

	# this variable is "syntactic sugar". typing "stars" is more readable than typing "gameStatObj"['stars'] in ur code.
	stars = gameStatObj['stars']

	if playerMoveTo == UP:
		xOffset = 0
		yOffset = -1 
	elif playerMoveTo == RIGHT:
		xOffset = 1
		yOffset = 0
	elif playerMoveTo == DOWN:
		xOffset = 0
		yOffset = 1
	elif playerMoveTo == LEFT:
		xOffset = -1
		yOffset = 0
def readLevelsFile(filename):
        assert os.path.exists(filename), 'connot fund the levels file: %s ' % (filename)
        mapFile = open(filename, 'r')
        # each level must end with a blank line
        content = mapFile.readlines() + ['\r\n']
        mapFile.close()

        levels = [] # Will contain a list of level object.
        levelNum = 0
        mapTextLines = [] # contains the lines for a single levels map
        mapObj = [] # the map object made from the data in mapTextLines
        for lineNum in range(len(content)):
                # process each line that was in the level file.
                line = content[lineNum].restrip('r\n')

                if ';' in line:
                        # ignore the ; lines, they are the comment in the levels file.
                        line = line[:line.find(';')]
                if line != '':
                        # this line is part of the map
                        mapTextLines.append(line)
                elif line == '' and len(mapTextLines) > 0:
                        # a blank line indicates the end of the levels map in the file.
                        # convert the text in mapTextLines into a level object
                        # find the longest row in the map
                        maxWidth = -1
                        for i in range(len(mapTextLines)):
                                if len(mapTextLines[i]) > maxWidth:
                                        maxWidth = len(mapTextLines[i])
                        # add spaces to the end of the shorter rows this
                        # ensures the map will be rectangluar
                        for i in range(len(mapTextLines[0])):
                                mapObj.append([])
                        for y in range(maxWidth):
                                mapObj[x].append(mapTextLines[y][x])

                        # loop through the spaces in the map and find the @, ., and $
                        # characters for the starting game state.
                        startx = None # the x and y for the player's starting position
                        starty = None
                        goals = []
                        stars = []



print("star Pusher done: pg~269")
