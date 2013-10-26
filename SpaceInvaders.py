##Space Invaders##

import pygame
import sys
from pygame.locals import *

##CONSTANTS##

## COLORS ##

#            R    G    B
GRAY      = (100, 100, 100)
NAVYBLUE  = ( 60,  60, 100)
WHITE     = (255, 255, 255)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
BLUE      = (  0,   0, 255)
YELLOW    = (255, 255,   0)
ORANGE    = (255, 128,   0)
PURPLE    = (255,   0, 255)
CYAN      = (  0, 255, 255)
BLACK     = (  0,   0,   0)
NEARBLACK = ( 19,  15,  48)
COMBLUE   = (233, 232, 255)

## Player Constants ##

PLAYERWIDTH = 50
PLAYERHEIGHT = 35
PLAYERCOLOR = COMBLUE
PLAYER1 = 'Player 1'
PLAYERSPEED = 5
PLAYERCOLOR = GREEN

## Display Constants ##

GAMETITLE = 'Space Invaders!'
DISPLAYWIDTH = 640
DISPLAYHEIGHT = 480
BGCOLOR = NEARBLACK
XMARGIN = 50
YMARGIN = 50

## Bullet Constants ##

BULLETWIDTH = 5
BULLETHEIGHT = 5
BULLETCOLOR = GREEN
BULLETNAME = 'Bullet'
BULLETSPEED = 20

## Enemy Constants ##

ENEMYWIDTH = 30
ENEMYHEIGHT = 30
ENEMYNAME = 'Enemy'
ENEMYGAP = 20
ARRAYWIDTH = 10
ARRAYHEIGHT = 4
MOVETIME = 1000
MOVEX = 10
MOVEY = ENEMYHEIGHT

## Direction Dictionary ##
## This dictionary allows for shooting bullets while moving without ##
## the inputs interupting each other.                               ##

DIRECT_DICT = {pygame.K_LEFT  : (-1),
               pygame.K_RIGHT : (1)}





class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width = PLAYERWIDTH
        self.height = PLAYERHEIGHT
        self.image = pygame.Surface((self.width, self.height))
        self.color = PLAYERCOLOR
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.name = PLAYER1
        self.speed = PLAYERSPEED
        self.vectorx = 0

    
    def update(self, keys, *args):
        for key in DIRECT_DICT:
            if keys[key]:
                self.rect.x += DIRECT_DICT[key] * self.speed
                
        self.checkForSide()


    def checkForSide(self):
        if self.rect.right > DISPLAYWIDTH:
            self.rect.right = DISPLAYWIDTH
            self.vectorx = 0
        elif self.rect.left < 0:
            self.rect.left = 0
            self.vectorx = 0



class Bullet(pygame.sprite.Sprite):
    def __init__(self, playerRect):
        pygame.sprite.Sprite.__init__(self)
        self.width = BULLETWIDTH
        self.height = BULLETHEIGHT
        self.color = BULLETCOLOR
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.centerx = playerRect.centerx
        self.rect.bottom = playerRect.top
        self.name = BULLETNAME
        self.vectory = -1
        self.speed = BULLETSPEED

    def update(self, *args):
        self.rect.y += self.vectory * self.speed

        if self.rect.bottom < 0:
            self.kill()

        

class Enemy(pygame.sprite.Sprite):
    def __init__(self, row, column):
        pygame.sprite.Sprite.__init__(self)
        self.width = ENEMYWIDTH
        self.height = ENEMYHEIGHT
        self.row = row
        self.column = column
        self.color = RED
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.name = ENEMYNAME
        self.vectorx = 1
        self.moveNumber = 0


    def update(self, keys, moveEnemies):
        if moveEnemies:
            if self.moveNumber < 6:
                self.rect.x += MOVEX * self.vectorx
                self.moveNumber += 1
            elif self.moveNumber >= 6:
                self.vectorx *= -1
                self.moveNumber = 0
                self.rect.y += MOVEY
                



class App(object):
    def __init__(self):
        pygame.init()
        self.displaySurf, self.displayRect = self.makeScreen()
        self.player = self.makePlayer()
        self.bullets = pygame.sprite.Group()
        self.enemies = self.makeEnemies()
        self.allSprites = pygame.sprite.Group(self.player, self.enemies)
        self.keys = pygame.key.get_pressed()
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.lastMove = 0
        self.enemyMoves = 0
        self.moveEnemies = False
        self.setTimers()




    def setTimers(self):
        pygame.time.set_timer(USEREVENT + 1, MOVETIME)

        

    def makeScreen(self):
        pygame.display.set_caption(GAMETITLE)
        displaySurf = pygame.display.set_mode((DISPLAYWIDTH, DISPLAYHEIGHT))
        displayRect = displaySurf.get_rect()
        displaySurf.fill(BGCOLOR)
        displaySurf.convert()

        return displaySurf, displayRect



    def makePlayer(self):
        player = Player()
        ##Place the player centerx and five pixels from the bottom
        player.rect.centerx = self.displayRect.centerx
        player.rect.bottom = self.displayRect.bottom - 5

        return player


    def makeEnemies(self):
        enemyGroup = pygame.sprite.Group()
        
        for row in range(ARRAYHEIGHT):
            for column in range(ARRAYWIDTH):
                enemy = Enemy(row, column)
                enemy.rect.x = XMARGIN + (column * (ENEMYWIDTH + ENEMYGAP))
                enemy.rect.y = YMARGIN + (row * (ENEMYHEIGHT + ENEMYGAP))
                enemyGroup.add(enemy)

        return enemyGroup


    def stopMovement(self):
        self.moveEnemies = False



    def checkInput(self):
        for event in pygame.event.get():
            self.keys = pygame.key.get_pressed()
            if event.type == QUIT:
                self.terminate()

            elif event.type == USEREVENT + 1:
                self.moveEnemies = True
                

            elif event.type == KEYDOWN:
                if event.key == K_SPACE and len(self.bullets) == 0:
                    bullet = Bullet(self.player.rect)
                    self.bullets.add(bullet)
                    self.allSprites.add(bullet)

        


    def checkCollisions(self):
        pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
        
                

    def terminate(self):
        pygame.quit()
        sys.exit()


    def mainLoop(self):
        while True:
            self.displaySurf.fill(BGCOLOR)
            self.checkInput()
            self.allSprites.update(self.keys, self.moveEnemies)
            self.stopMovement()
            self.checkCollisions()
            self.allSprites.draw(self.displaySurf)
            pygame.display.update()
            self.clock.tick(self.fps)
            
            
    


if __name__ == '__main__':
    app = App()
    app.mainLoop()
