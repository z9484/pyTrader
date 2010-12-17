from character import *
from state import *
from loadmap import *
import pygame, sys
from pygame.locals import *

COOLTIME = 5
BLACK = (0,0,0)
WHITE = (255, 255, 255)
TILESIZE = 32
MAPX = 20
MAPY = 50
OBSTACLES = ["#"]

class GameState(State):
    def __init__(self, screen, content):
        super(GameState, self).__init__(screen, content)

        self.player1 = Character()
        self.cooldown = COOLTIME
        self.dt  = 0
        self.map = loadMap("maps/t1.map")
        self.view = self.findView(self.player1.posX, self.player1.posY)
        self.prevState = pygame.event.get()

    def draw(self):
        self.screen.fill(BLACK)
        for y in xrange(5):
            for x in xrange(5):
                try:
                    self.screen.blit(self.content[self.view[y][x]], (x*TILESIZE, y*TILESIZE) )
                except:
                    print y,x

        self.screen.blit(self.content["@"], (2*TILESIZE, 2*TILESIZE))

        text = self.content["font1"].render("X:" + str(self.player1.posX) + " Y:" + str(self.player1.posY), True, WHITE)   
        self.screen.blit(text, (self.screen.get_rect().centerx, self.screen.get_rect().centery))

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
        
    def check_cool(self):
        if self.cooldown <= 0:
	        self.cooldown = COOLTIME
	        return True
        else:
	        self.cooldown -= self.dt
	        return False

    def keyreleased(self, key):
        super(GameState, self).keyreleased(key) 

    def move(self, direction):
        if self.check_cool():
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
        if key == K_a:
            print "a pressed"

    def findKey(self, key):
        for event in self.prevState:
            if event.key == key:
                return event
       

    def update(self, clock):
        #super(GameState, self).update(clock)
        self.state = []

        for event in pygame.event.get():
            if event.type == QUIT: sys.exit(0)    
            if hasattr(event, 'key'):
                self.state.append(event)

        for keyevent in self.state:
            prevState       
            if prevState.KEYDOWN and keyevent.type == KEYUP:

        """
        

        for event in pygame.event.get():
            if event.type == QUIT: sys.exit(0)    
            if hasattr(event, 'key'):
                if event.type == KEYDOWN: self.keys.append(event.key)
                elif event.type == KEYUP: self.keyreleased(event.key)
        """

        self.dt = clock.get_time()

        for key in self.keys:
            if key == K_ESCAPE or key == K_q: sys.exit(0)
            elif key == K_LEFT: self.move("left")
            elif key == K_RIGHT: self.move("right")
            elif key == K_UP: self.move("up")
            elif key == K_DOWN: self.move("down")
            elif key == K_a: self.letter(K_a)

        self.prevState = self.state
        

    def findView(self, x,y):
        view = []
        for q in xrange(-2,3):
            row = []
            for r in xrange(-2,3):
                if y+q >= MAPY or x+r >= MAPX or y+q < 0 or x+r < 0:
                    row.append("#")
                else:
                    try:
                        row.append(self.map[y+q][x+r])
                    except:
                        print y+q,x+r
            view.append(row)  

        return view        

