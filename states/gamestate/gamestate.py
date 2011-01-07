from character import *
from constants import *
from state import *
from loadmap import *
import pygame, sys
from pygame.locals import *
from point import *
from states.gamestate.outpost import *
import cPickle as pickle
from timer import *

OBSTACLES = ["#"]
COMMODITY = {0:"none", 1:"food", 2:"mineral", 3:"equipment"}

class GameState(State):
    def __init__(self, screen, content, game, channel, player):
        super(GameState, self).__init__(screen, content)

        self.game = game
        self.channel = channel
        self.player1 = player
        self.load()
        
        self.map = loadMap("maps/t1.map")
        self.mapX = len(self.map[0])
        self.mapY = len(self.map)
        self.view = self.findView(self.player1.posX, self.player1.posY)
        self.buffer = ""
        self.history = ["","",""]
        self.currentCommand = -1
        self.currentCommodity = 0
        self.inTown = False
        self.updateTimer = Timer(UPDATECOOL)
        #print pygame.game.gamestate
        
        #self.console = Console()
        
                 
        self.outpost = None 
                 
    def insert(self, game):
        self.game = game
		
    def draw(self):
        self.screen.fill(BLACK)
        for y in xrange(5):
            for x in xrange(5):
                try:
                    self.screen.blit(self.content[self.view[y][x]], (x*TILESIZE, y*TILESIZE) )
                except:
                    pass
                    #print "bad terrain at", y,x

        self.screen.blit(self.content["@"], (2*TILESIZE, 2*TILESIZE))

        if self.currentCommand == 10:
            text = self.content["font1"].render("\\", True, WHITE)  
            self.screen.blit(text, (self.screen.get_rect().centerx-6, self.screen.get_rect().centery+150))
        
        
        text = self.content["font1"].render(self.buffer, True, WHITE)  
        self.screen.blit(text, (self.screen.get_rect().centerx, self.screen.get_rect().centery+150))

        for i in xrange(len(self.history)):
            text = self.content["font1"].render(self.history[i], True, GRAY)  
            self.screen.blit(text, (self.screen.get_rect().centerx, self.screen.get_rect().centery+90+20*i))

        xoffset = -150
        yoffset = -135
        toffset = -15
        i = 6
        
        text = self.content["font1"].render("Name: " + self.player1.name.rjust(8), True, WHITE)  
        self.screen.blit(text, (self.screen.get_rect().centerx + xoffset, self.screen.get_rect().centery + yoffset + toffset * i))
        i -= 1
        text = self.content["font1"].render("X:" + str(self.player1.posX) + " Y:" + str(self.player1.posY), True, WHITE)   
        self.screen.blit(text, (self.screen.get_rect().centerx + xoffset, self.screen.get_rect().centery + yoffset + toffset * i))
        i -= 1
        text = self.content["font1"].render("Credits: " + str(self.player1.credits).rjust(8), True, WHITE)  
        self.screen.blit(text, (self.screen.get_rect().centerx + xoffset, self.screen.get_rect().centery + yoffset + toffset * i))
        i -= 1
        text = self.content["font1"].render("Food: " + str(self.player1.food).rjust(13), True, WHITE)  
        self.screen.blit(text, (self.screen.get_rect().centerx + xoffset, self.screen.get_rect().centery + yoffset + toffset * i))
        i -= 1
        text = self.content["font1"].render("Minerals: " + str(self.player1.mineral).rjust(8), True, WHITE)  
        self.screen.blit(text, (self.screen.get_rect().centerx + xoffset, self.screen.get_rect().centery + yoffset + toffset * i))
        i -= 1
        text = self.content["font1"].render("Equipment: " + str(self.player1.equipment).rjust(4), True, WHITE)  
        self.screen.blit(text, (self.screen.get_rect().centerx + xoffset, self.screen.get_rect().centery + yoffset + toffset * i))
        i -= 1
        text = self.content["font1"].render("Cargo: " + (str(self.player1.findcargo())+"/"+str(self.player1.maxcargo)).rjust(10), True, WHITE)  
        self.screen.blit(text, (self.screen.get_rect().centerx + xoffset, self.screen.get_rect().centery + yoffset + toffset * i))


        if self.inTown:
            xoffset = 0
            yoffset = -135
            toffset = -15
            i = 6
            text = self.content["font1"].render("Outpost: " + str(self.outpost.no), True, WHITE)  
            self.screen.blit(text, (self.screen.get_rect().centerx + xoffset, self.screen.get_rect().centery + yoffset + toffset * i))
            i -= 1
            text = self.content["font1"].render("Type: " + self.outpost.type, True, WHITE)
            self.screen.blit(text, (self.screen.get_rect().centerx + xoffset, self.screen.get_rect().centery + yoffset + toffset * i))
            i -= 1
            text = self.content["font1"].render("Food: " + str(self.outpost.food.current) + "/" + str(self.outpost.food.capacity) + " at " + str(self.outpost.food.getSellPrice()) + "/" + str(self.outpost.food.getBuyPrice()), True, WHITE)  
            self.screen.blit(text, (self.screen.get_rect().centerx + xoffset, self.screen.get_rect().centery + yoffset + toffset * i))
            i -= 1
            text = self.content["font1"].render("Minerals: " + str(self.outpost.mineral.current) + "/" + str(self.outpost.mineral.capacity) + " at " + str(self.outpost.mineral.getSellPrice()) + "/" + str(self.outpost.mineral.getBuyPrice()), True, WHITE)  
            self.screen.blit(text, (self.screen.get_rect().centerx + xoffset, self.screen.get_rect().centery + yoffset + toffset * i))
            i -= 1
            text = self.content["font1"].render("Equipment: " + str(self.outpost.equipment.current) + "/" + str(self.outpost.equipment.capacity) + " at " + str(self.outpost.equipment.getSellPrice()) + "/" + str(self.outpost.equipment.getBuyPrice()), True, WHITE)  
            self.screen.blit(text, (self.screen.get_rect().centerx + xoffset, self.screen.get_rect().centery + yoffset + toffset * i))
        
 
    def update(self, clock):
        super(GameState, self).update(clock)

        for key in self.keysDown:
            self.keyHandler(key)

        for i in xrange(len(self.keys)):
            if self.check_cool(i):
                self.keyHandler(self.keys[i][0])
                
        if self.updateTimer.check(self.dt):
            if not self.inTown:
                self.sendUpdate()
            else:
                if self.currentCommand != 2 and self.currentCommand != 4:
                    self.bUpdate()
                pass
                
        
            
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
        if not self.inTown:
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
        if self.currentCommand != -1:
            shift = False
            for i in xrange(len(self.keys)):
                if self.keys[i][0] == K_LSHIFT or self.keys[i][0] == K_RSHIFT or self.keys[i][0] == K_CAPSLOCK:
                    shift = True
                    break
            #if its a alpha numeric character    
            if (key > 31 and key < 47) or (key > 60 and key < 128) and len(self.buffer) < MAXTEXT:
                if shift:        
                    self.buffer += chr(key).upper()
                else:
                    self.buffer += chr(key)
           
            elif key > 46 and key < 60:
                if not shift:
                    self.buffer += chr(key)
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
                    self.buffer += character
            else:
                print key
                
    def findKey(self, key):
        for event in self.prevState:
            if event.key == key:
                return event
       	        
    def keyHandler(self, key):
        if key == K_ESCAPE: self.exit()
        elif key == K_LEFT: self.move("left")
        elif key == K_RIGHT: self.move("right")
        elif key == K_UP: self.move("up")
        elif key == K_DOWN: self.move("down")
        elif key == K_g: self.cmd_g()
        elif key == K_b: self.cmd_b()
        elif key == K_s: self.cmd_s()
        elif key == K_q: self.cmd_q()
        elif key == K_f: self.cmd_f()
        elif key == K_m: self.cmd_m()
        elif key == K_e: self.cmd_e()
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

    def cmd_g(self):
        if self.currentCommand == -1:
            if (self.player1.posX, self.player1.posY) in self.outposts:
                self.outpost = self.outposts[(self.player1.posX, self.player1.posY)]
                self.inTown = True
                self.dispMessage("Welcome to the Outpost")
                self.currentCommand = 0
            else:
                self.dispMessage("There is nothing here to enter.")
        else:
            self.letter(K_g)
                    
    def cmd_b(self): 
        if self.currentCommand == 0:
            self.currentCommand = 1
            self.dispMessage("What would you like to buy?")
        else:
            self.letter(K_b)

    def cmd_s(self): 
        if self.currentCommand == 0:
            self.currentCommand = 3
            self.dispMessage("What would you like to sell?")
        else:
            self.letter(K_s)

    def cmd_f(self): 
        if self.currentCommand == 1:
            price = self.outpost.food.getSellPrice()
            amt = self.player1.findmaxBuy(price)
            if amt > self.outpost.food.bleft():
                amt = self.outpost.food.bleft()
            self.dispMessage("How much food? " + str(amt) + " for " + str(amt * price))
            self.currentCommand = 2
            self.currentCommodity =  1
        elif self.currentCommand == 3:
            amt = self.player1.food
            if self.outpost.food.current + amt > self.outpost.food.capacity:
                amt = self.outpost.food.capacity
            self.dispMessage("How much food? " + str(amt) + " for " + str(amt * self.outpost.food.getBuyPrice()))
            self.currentCommand = 4
            self.currentCommodity =  1           
        else:
            self.letter(K_f)

    def cmd_m(self): 
        if self.currentCommand == 1:
            price = self.outpost.mineral.getSellPrice()
            amt = self.player1.findmaxBuy(price)
            if amt > self.outpost.mineral.bleft():
                amt = self.outpost.mineral.bleft()
            self.dispMessage("How many minerals? " + str(amt) + " for " + str(amt * price))
            self.currentCommand = 2
            self.currentCommodity =  2 
        elif self.currentCommand == 3:
            amt = self.player1.mineral
            if self.outpost.mineral.current + amt > self.outpost.mineral.capacity:
                amt = self.outpost.mineral.capacity
            self.dispMessage("How many minerals? " + str(amt) +" for " + str(amt * self.outpost.mineral.getBuyPrice()))
            self.currentCommand = 4
            self.currentCommodity =  2                 
        else:
            self.letter(K_m)

    def cmd_e(self): 
        if self.currentCommand == 1:
            price = self.outpost.equipment.getSellPrice()
            amt = self.player1.findmaxBuy(price)
            if amt > self.outpost.equipment.bleft():
                amt = self.outpost.equipment.bleft()
            self.dispMessage("How much equipment? " + str(amt) + " for " + str(amt * price))
            self.currentCommand = 2
            self.currentCommodity = 3
        elif self.currentCommand == 3:
            amt = self.player1.equipment
            if self.outpost.equipment.current + amt > self.outpost.equipment.capacity:
                amt = self.outpost.equipment.capacity
            self.dispMessage("How much equipment? " + str(amt) +" for " + str(amt * self.outpost.equipment.getBuyPrice()))
            self.currentCommand = 4
            self.currentCommodity = 3
        else:
            self.letter(K_e)

    def cmd_q(self): 
        if self.currentCommand == 0:
            self.dispMessage("Goodbye")
            self.inTown = False
            self.outpost = None
            self.currentCommand = -1
        elif self.currentCommand > 0 and self.currentCommand < 5:
            self.dispMessage("Base Menu")
            self.currentCommand = 0
        else:
            self.letter(K_q)     
                   
    def enter(self):
        #self.console.execute(self.buffer)
        self.dispMessage(self.buffer)
        raw = self.buffer.strip()

        if self.currentCommand == -1:
            self.currentCommand = 10
        elif self.currentCommand == 2:
            if raw == "a":
                commodity = eval("self.outpost." + COMMODITY[self.currentCommodity])
                price = commodity.getSellPrice()
                amt = self.player1.findmaxBuy(price)
                if amt > commodity.bleft():
                    amt = commodity.bleft()
                self.buy(COMMODITY[self.currentCommodity], str(amt))
            else:    
                self.buy(COMMODITY[self.currentCommodity], raw)
        elif self.currentCommand == 4:
            if raw == "a":
                commodity = eval("self.outpost." + COMMODITY[self.currentCommodity])
                amt = eval("self.player1." + COMMODITY[self.currentCommodity])
                if commodity.current + amt > commodity.capacity:
                    amt = commodity.capacity
                self.sell(COMMODITY[self.currentCommodity], str(amt))
            else:
                self.sell(COMMODITY[self.currentCommodity], raw)
        elif self.currentCommand == 10:
            if raw == "":
                self.currentCommand = -1
            
        self.buffer = ""

    def buy(self, commodity, raw):
        price = eval("self.outpost." + commodity + ".getSellPrice()")
        try:
            amt = int(raw)
            # print amt
            if (self.player1.credits - (amt * price) < 0) or (self.player1.findcargo() + amt > self.player1.maxcargo):
                raise BalanceError
            if not self.outpost.isValid(commodity, -amt):
                raise Error
                
            self.player1.credits -= (amt * price)
            self.outpost.buy(commodity, -amt)
            exec("self.player1." + commodity + " += amt")
            self.dispMessage("Bought " + raw + " " + commodity + "@ " + str(price))
            self.currentCommand = 0
            # self.sendbuy()
            self.channel.send(pickle.dumps( (("b", self.outpost.no, commodity, amt, price), ) ) )
        except:
            self.dispMessage("Invalid amount")

    def sell(self, commodity, raw):
        price = eval("self.outpost." + commodity + ".getBuyPrice()")
        try:
            amt = int(raw)
            # print amt
            if amt > eval("self.player1." + commodity):
                raise BalanceError
            if not self.outpost.isValid(commodity, amt):
                raise Error
                
            self.player1.credits += (amt * price)
            self.outpost.buy(commodity, amt)
            exec("self.player1." + commodity + " -= amt")
            self.dispMessage("Sold " + raw + " " + commodity + "@ " + str(price))
            self.currentCommand = 0
            self.channel.send(pickle.dumps( (("s", self.outpost.no, commodity, amt, price), ) ) )
        except:
            self.dispMessage("Invalid amount")
            
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
        
    
    def dispMessage(self, msg):
        self.history.append(msg)
        self.history.pop(0)

    def load(self):
        size = pickle.loads(self.channel.recv(128))
        self.channel.send("1")
        outposts = pickle.loads(self.channel.recv(size))
        # print outposts
        self.outposts = {}
        types = {1: "Farm", 2: "Mine", 3: "Factory", 4:"City"}
        frate = {1: 0.9, 2: 1.05, 3: 1.05, 4: 1.15}
        mrate = {1: 1, 2: 0.9, 3: 1.15, 4: 1.1}
        erate = {1: 1.1, 2: 1.15, 3: 0.9, 4: 1.1}
        
        for row in outposts:
            # print row
            self.outposts[(row[1], row[2])] = Outpost(row[0], Point(row[1], row[2]), types[row[3]],
            Commodity("Food", frate[row[3]], row[4], row[5], 1),
            Commodity("Mineral", mrate[row[3]], row[6], row[7], 1),
            Commodity("Equipment", erate[row[3]], row[8], row[9], 1)
            )
        
        # print self.outposts
        
        '''
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
            '''
    def daily(self):
        for key in self.outposts:
            self.outposts[key].dailyAdj()
        self.dispMessage("A new day has dawned")
        
    def sendUpdate(self):
        self.channel.send(pickle.dumps( (("m", self.player1.posX, self.player1.posY), ) ) )
    
    def bUpdate(self):
        self.channel.send(pickle.dumps( (("o", [self.outpost.no]), ) ) )
        self.outpost.update(pickle.loads(self.channel.recv(1024)))
        
    def exit(self):
        '''
        storage = self.player1
        with open("player.dat", 'w') as file: 
            pickle.dump(storage, file)
            
        storage = self.outposts
        with open("outposts.dat", 'w') as file: 
            pickle.dump(storage, file)
        '''
        self.sendUpdate()        
        self.channel.close()
        sys.exit(0)
        
        
