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
PLAYERHEIGHT = 15
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
TIMEOFFSET = 300

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
        self.image = self.setImage()
        self.rect = self.image.get_rect()
        self.name = 'enemy'
        self.vectorx = 1
        self.moveNumber = 0
        self.moveTime = MOVETIME
        self.timeOffset = row * TIMEOFFSET
        self.timer = pygame.time.get_ticks() - self.timeOffset


    def update(self, keys, currentTime):
        if currentTime - self.timer > self.moveTime:
            if self.moveNumber < 6:
                self.rect.x += MOVEX * self.vectorx
                self.moveNumber += 1
            elif self.moveNumber >= 6:
                self.vectorx *= -1
                self.moveNumber = 0
                self.rect.y += MOVEY
                self.moveTime -= 100
            self.timer = currentTime


    def setImage(self):
        if self.row == 0:
            image = pygame.image.load('alien1.png')
        elif self.row == 1:
            image = pygame.image.load('alien2.png')
        elif self.row == 2:
            image = pygame.image.load('alien3.png')
        else:
            image = pygame.image.load('alien1.png')
        image.convert_alpha()
        image = pygame.transform.scale(image, (self.width, self.height))

        return image



class Text(object):
    def __init__(self, font, size, message, color, rect, surface):
        self.font = pygame.font.Font(font, size)
        self.message = message
        self.surface = self.font.render(self.message, True, color)
        self.rect = self.surface.get_rect()
        self.setRect(rect)

    def setRect(self, rect):
        self.rect.centerx, self.rect.centery = rect.centerx, rect.centery - 5


    def draw(self, surface):
        surface.blit(self.surface, self.rect)



class App(object):
    
    def __init__(self):
        pygame.init()
        self.displaySurf, self.displayRect = self.makeScreen()
        self.gameStart = True
        self.needToMakeEnemies = True
        
        self.introMessage1 = Text('orena.ttf', 25,
                                 'Welcome to Space Invaders!',
                                 GREEN, self.displayRect,
                                 self.displaySurf)
        self.introMessage2 = Text('orena.ttf', 20,
                                  'Press Any Key to Continue',
                                  GREEN, self.displayRect,
                                  self.displaySurf)
        self.introMessage2.rect.top = self.introMessage1.rect.bottom + 5
        
        self.player = self.makePlayer()
        self.bullets = pygame.sprite.Group()
        self.allSprites = pygame.sprite.Group(self.player)
        self.keys = pygame.key.get_pressed()
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.enemyMoves = 0


        
    

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
        enemies = pygame.sprite.Group()
        
        for row in range(ARRAYHEIGHT):
            for column in range(ARRAYWIDTH):
                enemy = Enemy(row, column)
                enemy.rect.x = XMARGIN + (column * (ENEMYWIDTH + ENEMYGAP))
                enemy.rect.y = YMARGIN + (row * (ENEMYHEIGHT + ENEMYGAP))
                enemies.add(enemy)

        return enemies



    def checkInput(self):
        for event in pygame.event.get():
            self.keys = pygame.key.get_pressed()
            if event.type == QUIT:
                self.terminate()

            elif event.type == KEYDOWN:
                if event.key == K_SPACE and len(self.bullets) == 0:
                    bullet = Bullet(self.player.rect)
                    self.bullets.add(bullet)
                    self.allSprites.add(bullet)
                elif event.key == K_ESCAPE:
                    self.terminate()


    def gameStartInput(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.terminate()
            elif event.type == KEYUP:
                self.gameStart = False

        


    def checkCollisions(self):
        pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
        
                

    def terminate(self):
        pygame.quit()
        sys.exit()


    def mainLoop(self):
        while True:
            if self.gameStart:
                self.displaySurf.fill(BGCOLOR)
                self.introMessage1.draw(self.displaySurf)
                self.introMessage2.draw(self.displaySurf)
                self.gameStartInput()
                pygame.display.update()
                
            else:
                if self.needToMakeEnemies:
                    self.enemies = self.makeEnemies()
                    self.allSprites.add(self.enemies)
                    self.needToMakeEnemies = False
                else:    
                    currentTime = pygame.time.get_ticks()
                    self.displaySurf.fill(BGCOLOR)
                    self.checkInput()
                    self.allSprites.update(self.keys, currentTime)
                    self.checkCollisions()
                    self.allSprites.draw(self.displaySurf)
                    pygame.display.update()
                    self.clock.tick(self.fps)
            
            
    


if __name__ == '__main__':
    app = App()
    app.mainLoop()
