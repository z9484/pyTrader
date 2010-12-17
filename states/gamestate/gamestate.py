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
        self.buffer = ""

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
        
        text = self.content["font1"].render(self.buffer, True, WHITE)  
        self.screen.blit(text, (self.screen.get_rect().centerx, self.screen.get_rect().centery+50))


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
        self.buffer += chr(key)
        
    def findKey(self, key):
        for event in self.prevState:
            if event.key == key:
                return event
       

    def update(self, clock):
        #super(GameState, self).update(clock)
        self.keysDown = []
        self.keysUp = []
        
        for event in pygame.event.get():
            if event.type == QUIT: sys.exit(0)    
            if hasattr(event, 'key'):
                if event.type == KEYDOWN: self.keysDown.append(event.key)
                elif event.type == KEYUP: self.keysUp.append(event.key)
            
        self.dt = clock.get_time()

        for key in self.keysDown:
            if key == K_ESCAPE: sys.exit(0)
            elif key == K_LEFT: self.move("left")
            elif key == K_RIGHT: self.move("right")
            elif key == K_UP: self.move("up")
            elif key == K_DOWN: self.move("down")
            elif key == K_a: self.letter(key)
            elif key == K_b: self.letter(key)
            elif key == K_c: self.letter(key)
            elif key == K_d: self.letter(key)
            elif key == K_e: self.letter(key)
            elif key == K_f: self.letter(key)
            elif key == K_g: self.letter(key)
            elif key == K_h: self.letter(key)
            elif key == K_i: self.letter(key)
            elif key == K_j: self.letter(key)
            elif key == K_k: self.letter(key)
            elif key == K_l: self.letter(key)
            elif key == K_m: self.letter(key)
            elif key == K_n: self.letter(key)
            elif key == K_o: self.letter(key)
            elif key == K_p: self.letter(key)
            elif key == K_q: self.letter(key)
            elif key == K_r: self.letter(key)
            elif key == K_s: self.letter(key)
            elif key == K_t: self.letter(key)
            elif key == K_u: self.letter(key)
            elif key == K_v: self.letter(key)
            elif key == K_w: self.letter(key)
            elif key == K_x: self.letter(key)
            elif key == K_y: self.letter(key)
            elif key == K_z: self.letter(key)
            elif key == K_0: self.letter(key)
            elif key == K_1: self.letter(key)
            elif key == K_2: self.letter(key)
            elif key == K_3: self.letter(key)
            elif key == K_4: self.letter(key)
            elif key == K_5: self.letter(key)
            elif key == K_6: self.letter(key)
            elif key == K_7: self.letter(key)
            elif key == K_8: self.letter(key)
            elif key == K_9: self.letter(key)
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
            elif key == K_RETURN: self.enter()
            elif key == K_BACKSPACE: self.backspace()
            elif key == K_SPACE: self.letter(key)

    def enter(self):
        print self.buffer
        self.buffer = ""

    def backspace(self):
        self.buffer = self.buffer[:-1]
        
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

