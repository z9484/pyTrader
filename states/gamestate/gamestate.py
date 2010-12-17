from character import *
from state import *
from loadmap import *
import pygame, sys
from pygame.locals import *
from console import *


BLACK = (0,0,0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
TILESIZE = 32
OBSTACLES = ["#"]

class GameState(State):
    def __init__(self, screen, content):
        super(GameState, self).__init__(screen, content)

        self.player1 = Character()

        self.map = loadMap("maps/t2.map")
        self.mapX = len(self.map[0])
        self.mapY = len(self.map)
        self.view = self.findView(self.player1.posX, self.player1.posY)
        self.buffer = ""
        self.history = ["","",""]
        self.console = Console()

    def draw(self):
        self.screen.fill(BLACK)
        for y in xrange(5):
            for x in xrange(5):
                try:
                    self.screen.blit(self.content[self.view[y][x]], (x*TILESIZE, y*TILESIZE) )
                except:
                    print "bad terrain at", y,x

        self.screen.blit(self.content["@"], (2*TILESIZE, 2*TILESIZE))

        text = self.content["font1"].render("X:" + str(self.player1.posX) + " Y:" + str(self.player1.posY), True, WHITE)   
        self.screen.blit(text, (self.screen.get_rect().centerx, self.screen.get_rect().centery))
        
        text = self.content["font1"].render(self.buffer, True, WHITE)  
        self.screen.blit(text, (self.screen.get_rect().centerx, self.screen.get_rect().centery+150))

        for i in xrange(len(self.history)):
            text = self.content["font1"].render(self.history[i], True, BLUE)  
            self.screen.blit(text, (self.screen.get_rect().centerx, self.screen.get_rect().centery+90+20*i))


 
    def update(self, clock):
        super(GameState, self).update(clock)

        for key in self.keysDown:
            self.keyHandler(key)

        for i in xrange(len(self.keys)):
            if self.check_cool(i):
                self.keyHandler(self.keys[i][0])
            
    def player_left(self):
        if self.view[2][1] not in OBSTACLES:
            self.player1.moveLeft()

    def player_right(self):
        if self.view[2][3] not in OBSTACLES:
            self.player1.moveRight()

    def player_up(self):
        if self.view[1][2] not in OBSTACLES:
            self.player1.moveUp()

    def player_down(self):
        if self.view[3][2] not in OBSTACLES:
            self.player1.moveDown()

    def keyreleased(self, key):
        super(GameState, self).keyreleased(key) 

    def move(self, direction):
        #if self.check_cool():
        if direction == "up":
            self.player_up()
        elif direction == "down":
            self.player_down()
        elif direction == "left":
            self.player_left()
        elif direction == "right":
            self.player_right()
        self.view = self.findView(self.player1.posX, self.player1.posY)

    def letter(self, key):

        #if its a alpha numeric character
        if key > 31 and key < 128: 
            self.buffer += chr(key)
        else:
            print key
        
    def findKey(self, key):
        for event in self.prevState:
            if event.key == key:
                return event
       	        
    def keyHandler(self, key):
        if key == K_ESCAPE: sys.exit(0)
        elif key == K_LEFT: self.move("left")
        elif key == K_RIGHT: self.move("right")
        elif key == K_UP: self.move("up")
        elif key == K_DOWN: self.move("down")
        elif key == K_KP0: self.letter(K_0)
        elif key == K_KP1: self.letter(K_1)
        elif key == K_KP2: self.letter(K_2)
        elif key == K_KP3: self.letter(K_3)
        elif key == K_KP4: self.letter(K_4)
        elif key == K_KP5: self.letter(K_5)
        elif key == K_KP6: self.letter(K_6)
        elif key == K_KP7: self.letter(K_7)
        elif key == K_KP8: self.letter(K_8)
        elif key == K_KP9: self.letter(K_9)
        elif key == K_RETURN or key == K_KP_ENTER: self.enter()
        elif key == K_BACKSPACE: self.backspace()
        elif key == K_SPACE: self.letter(key)
        else: self.letter(key)

    def enter(self):
        #self.console.execute(self.buffer)
        self.history.append(self.buffer)
        self.history.pop(0)
        self.buffer = ""

    def backspace(self):
        self.buffer = self.buffer[:-1]
        
    def findView(self, x,y):
        view = []
        for q in xrange(-2,3):
            row = []
            for r in xrange(-2,3):
                if y+q >= self.mapY or x+r >= self.mapX or y+q < 0 or x+r < 0:
                    row.append("#")
                else:
                    try:
                        row.append(self.map[y+q][x+r])
                    except:
                        print y+q,x+r
            view.append(row)  

        return view        

