from character import *
from constants import *
from state import *
import pygame, sys
from pygame.locals import *
from states.gamestate.gamestate import *
import cPickle as pickle
import socket

class LoginState(State):
    def __init__(self, screen, content):
        super(LoginState, self).__init__(screen, content)

        self.current = 0
        self.playername = ""
        self.password = ""
        self.error = False
        
        try:
            self.channel = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
            self.channel.connect((HOST, PORT))
        except:
            print "Server is offline"
            self.exit()      
        
    def insert(self, game):
        self.game = game
        
    def draw(self):
        self.screen.fill(BLACK)

        text = self.content["font1"].render("Welcome to PyTrader", True, WHITE)  
        self.screen.blit(text, (self.screen.get_rect().centerx-60, self.screen.get_rect().centery-160))

        text = self.content["font1"].render("Player Name:", True, WHITE)  
        self.screen.blit(text, (self.screen.get_rect().centerx-120, self.screen.get_rect().centery-75))

        text = self.content["font1"].render("Password:", True, WHITE)  
        self.screen.blit(text, (self.screen.get_rect().centerx-120, self.screen.get_rect().centery-60))
        
        text = self.content["font1"].render(self.playername, True, WHITE)  
        self.screen.blit(text, (self.screen.get_rect().centerx-30, self.screen.get_rect().centery-75))

        text = self.content["font1"].render(self.password, True, WHITE)  
        self.screen.blit(text, (self.screen.get_rect().centerx-30, self.screen.get_rect().centery-60))

        text = self.content["font1"].render("\\", True, WHITE)  
        if self.current == 0:
            self.screen.blit(text, (self.screen.get_rect().centerx-36, self.screen.get_rect().centery-75))
        else:
            self.screen.blit(text, (self.screen.get_rect().centerx-36, self.screen.get_rect().centery-60))

        if self.error:
            text = self.content["font1"].render("Incorrect player name or password", True, WHITE)  
            self.screen.blit(text, (self.screen.get_rect().centerx-30, self.screen.get_rect().centery+100))
        
        
    def update(self, clock):
        super(LoginState, self).update(clock)

        for key in self.keysDown:
            self.keyHandler(key)

        for i in xrange(len(self.keys)):
            if self.check_cool(i):
                self.keyHandler(self.keys[i][0])

    def letter(self, key):
        sbuffer = ""
        shift = False
        for i in xrange(len(self.keys)):
            if self.keys[i][0] == K_LSHIFT or self.keys[i][0] == K_RSHIFT or self.keys[i][0] == K_CAPSLOCK:
                shift = True
                break
        #if its a alpha numeric character    
        if (key > 31 and key < 47) or (key > 60 and key < 128):
            if shift:        
                sbuffer = chr(key).upper()
            else:
                sbuffer = chr(key)
       
        elif key > 46 and key < 60:
            if not shift:
                sbuffer = chr(key)
            else:
                if key == K_1:
                    character = chr(K_EXCLAIM) 
                elif key == K_2:
                    character = chr(K_AT)
                elif key == K_3:
                    character = chr(K_HASH)
                elif key == K_4:
                    character = chr(K_DOLLAR)
                elif key == K_5:
                    character = chr(37)
                elif key == K_6:
                    character = chr(K_CARET)
                elif key == K_7:
                    character = chr(K_AMPERSAND)
                elif key == K_8:
                    character = chr(K_ASTERISK)
                elif key == K_9:
                    character = chr(K_LEFTPAREN)
                elif key == K_0:
                    character = chr(K_RIGHTPAREN)
                elif key == K_SLASH:
                    character = chr(K_QUESTION)
                elif key == K_SEMICOLON:
                    character = chr(K_COLON)
                else:
                    character = chr(key)
                sbuffer = character

        if self.current == 0:
            self.playername += sbuffer
        elif self.current == 1:
            self.password += sbuffer
       	        
    def keyHandler(self, key):
        if key == K_ESCAPE: self.exit()
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
        if self.current == 0:
            self.current = 1
        elif self.current == 1:
            self.submit()

        
    def backspace(self):
        if self.current == 0:
            self.playername = self.playername[:-1]
        elif self.current == 1:
            self.password = self.password[:-1]
    
    def submit(self):
        self.channel.send(pickle.dumps((self.playername,self.password)))
        packet = self.channel.recv(25) #Authentication status
        print packet
        if packet == "1":
            player = pickle.loads(self.channel.recv(1024))
            print player
        else:
            #Invalid Information
            self.current = 0
            self.error = True
        # self.exit()
        self.game.gamestate = [GameState(self.screen, self.content, self.game, self.channel, player)]
        
    def load(self):
        try:
            with open("player.dat", 'r') as file: 
                storage = pickle.load(file)
                self.player1 = storage
        except:
            print "Creating new player"
            self.player1 = Character("Z9484")
            
        try:
            with open("outposts.dat", 'r') as file: 
                storage = pickle.load(file)
                self.outposts = storage
        except:
            print "Loading outpost data"
            self.outposts = {(24,9): Outpost(1, Point(24,9), "Mine",
                 Commodity("Food", 1.05, 2600, 1300, 1),
                 Commodity("Mineral", 0.9, 7000, 3500, 1),
                 Commodity("Equipment", 1.15, 3500, 1750, 1)
                 ),
                 (45,45): Outpost(2, Point(45,45), "City",
                 Commodity("Food", 1.15, 6800, 3400, 1),
                 Commodity("Mineral", 1.1, 4300, 2150,  1),
                 Commodity("Equipment", 1.1, 4300, 2150,  1)
                 ),
                 (47,28): Outpost(3, Point(47,28), "City",
                 Commodity("Food", 1.15, 7400, 3700, 1),
                 Commodity("Mineral", 1.1, 4600, 2300,  1),
                 Commodity("Equipment", 1.1, 4600, 2300,  1)
                 ),
                 (10,3): Outpost(4, Point(10,3), "Mine",
                 Commodity("Food", 1.05, 3300, 1650, 1),
                 Commodity("Mineral", 0.9, 8800, 4400,  1),
                 Commodity("Equipment", 1.15, 4400, 2200,  1)
                 ),
                 (12,12): Outpost(5, Point(12,12), "Farm",
                 Commodity("Food", 0.9, 6400, 3200, 1),
                 Commodity("Mineral", 1, 1600, 800,  1),
                 Commodity("Equipment", 1.1, 3200, 1600,  1)
                 ),
                 (25,35): Outpost(6, Point(25,35), "Factory",
                 Commodity("Food", 1.05, 3300, 1650, 1),
                 Commodity("Mineral", 1.15, 6600, 3300,  1),
                 Commodity("Equipment", 0.9, 8800, 4400,  1)
                 ),
                 (2,39): Outpost(7, Point(2,39), "Farm",
                 Commodity("Food", 0.9, 5000, 2500, 1),
                 Commodity("Mineral", 1, 1300, 650,  1),
                 Commodity("Equipment", 1.1, 2500, 1250,  1)
                 ),
                 (14,38): Outpost(8, Point(14,38), "Farm",
                 Commodity("Food", 0.9, 8800, 4400, 1),
                 Commodity("Mineral", 1, 2200, 1100,  1),
                 Commodity("Equipment", 1.1, 4400, 2200,  1)
                 ),
                 (37,50): Outpost(9, Point(37,50), "Factory",
                 Commodity("Food", 1.05, 3200, 1600, 1),
                 Commodity("Mineral", 1.15, 6300, 3150,  1),
                 Commodity("Equipment", 0.9, 8400, 4200,  1)
                 ),
                 (42,22): Outpost(10, Point(42,22), "Mine",
                 Commodity("Food", 1.05, 3700, 1850, 1),
                 Commodity("Mineral", 0.9, 9800, 4900,  1),
                 Commodity("Equipment", 1.15, 4900, 2450,  1)
                 ),
                 (7,29): Outpost(11, Point(7,29), "Farm",
                 Commodity("Food", 0.9, 9800, 4900, 1),
                 Commodity("Mineral", 1, 2500, 1250,  1),
                 Commodity("Equipment", 1.1, 4900, 2450,  1)
                 ),
                 (25,2): Outpost(12, Point(25,2), "Factory",
                 Commodity("Food", 1.05, 2700, 1350, 1),
                 Commodity("Mineral", 1.15, 5400, 2750,  1),
                 Commodity("Equipment", 0.9, 7200, 3600,  1)
                 ),
                 (5,22): Outpost(13, Point(5,22), "Mine",
                 Commodity("Food", 1.05, 900, 450, 1),
                 Commodity("Mineral", 0.9, 2400, 1200,  1),
                 Commodity("Equipment", 1.15, 1200, 600,  1)
                 ),
                 (38,50): Outpost(14, Point(38,50), "Farm",
                 Commodity("Food", 0.9, 2800, 1400, 1),
                 Commodity("Mineral", 1, 700, 350,  1),
                 Commodity("Equipment", 1.1, 1400, 700,  1)
                 ),
                 (5,46): Outpost(15, Point(5,46), "Factory",
                 Commodity("Food", 1.05, 3500, 1750, 1),
                 Commodity("Mineral", 1.15, 6900, 3450,  1),
                 Commodity("Equipment", 0.9, 9200, 4600,  1)
                 ),
                 (11,33): Outpost(16, Point(11,33), "City",
                 Commodity("Food", 1.15, 2800, 1400, 1),
                 Commodity("Mineral", 1.1, 1800, 900,  1),
                 Commodity("Equipment", 1.1, 1800, 900,  1)
                 ),
                 (15,7): Outpost(17, Point(15,7), "Factory",
                 Commodity("Food", 1.05, 3500, 1750, 1),
                 Commodity("Mineral", 1.15, 7100, 3550,  1),
                 Commodity("Equipment", 0.9, 9400, 4700,  1)
                 ),
                 (42,35): Outpost(18, Point(42,35), "Farm",
                 Commodity("Food", 0.9, 9200, 4600, 1),
                 Commodity("Mineral", 1, 2300, 1150,  1),
                 Commodity("Equipment", 1.1, 4600, 2300,  1)
                 ),
                 (6,9): Outpost(19, Point(6,9), "Farm",
                 Commodity("Food", 0.9, 8200, 4100, 1),
                 Commodity("Mineral", 1, 2100, 1050,  1),
                 Commodity("Equipment", 1.1, 4100, 2050,  1)
                 ),
                 (23,17): Outpost(20, Point(23,17), "Farm",
                 Commodity("Food", 0.9, 10000, 5000, 1),
                 Commodity("Mineral", 1, 2500, 1250,  1),
                 Commodity("Equipment", 1.1, 5000, 2500,  1)
                 ),
                 (41,41): Outpost(21, Point(41,41), "Factory",
                 Commodity("Food", 1.05, 3500, 1750, 1),
                 Commodity("Mineral", 1.15, 6900, 3450,  1),
                 Commodity("Equipment", 0.9, 9200, 4600,  1)
                 ),
                 (12,23): Outpost(22, Point(12,23), "Factory",
                 Commodity("Food", 1.05, 3500, 1750, 1),
                 Commodity("Mineral", 1.15, 6900, 3450,  1),
                 Commodity("Equipment", 0.9, 9200, 4600,  1)
                 ),
                 (20,13): Outpost(23, Point(20,13), "Farm",
                 Commodity("Food", 0.9, 2800, 1400, 1),
                 Commodity("Mineral", 1, 700, 350,  1),
                 Commodity("Equipment", 1.1, 1400, 700,  1)
                 ),
                 (10,7): Outpost(24, Point(10,7), "Mine",
                 Commodity("Food", 1.05, 3800, 1900, 1),
                 Commodity("Mineral", 0.9, 10000, 5000,  1),
                 Commodity("Equipment", 1.15, 5000, 2500,  1)
                 ),
                 (44,43): Outpost(25, Point(44,43), "Mine",
                 Commodity("Food", 1.05, 3400, 1700, 1),
                 Commodity("Mineral", 0.9, 9000, 4500,  1),
                 Commodity("Equipment", 1.15, 4500, 2250,  1)
                 )				 
                 }

    def exit(self):
        # self.channel.close()
        sys.exit(0)
        
        
