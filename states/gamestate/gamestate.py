from character import *
from state import *
from loadmap import *
import pygame, sys
from pygame.locals import *
#from console import *
from point import *
from states.gamestate.outpost import *
import cPickle as pickle

BLACK = (0,0,0)
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)
TILESIZE = 32
MAXTEXT = 30
OBSTACLES = ["#"]
COMMODITY = {0:"none", 1:"food", 2:"mineral", 3:"equipment"}

class GameState(State):
    def __init__(self, screen, content):
        super(GameState, self).__init__(screen, content)

        
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

        
        
        text = self.content["font1"].render(self.buffer, True, WHITE)  
        self.screen.blit(text, (self.screen.get_rect().centerx, self.screen.get_rect().centery+150))

        for i in xrange(len(self.history)):
            text = self.content["font1"].render(self.history[i], True, GRAY)  
            self.screen.blit(text, (self.screen.get_rect().centerx, self.screen.get_rect().centery+90+20*i))

        text = self.content["font1"].render("X:" + str(self.player1.posX) + " Y:" + str(self.player1.posY), True, WHITE)   
        self.screen.blit(text, (self.screen.get_rect().centerx-150, self.screen.get_rect().centery-240))
        
        text = self.content["font1"].render("Credits: " + str(self.player1.credits).rjust(8), True, WHITE)  
        self.screen.blit(text, (self.screen.get_rect().centerx-150, self.screen.get_rect().centery-225))
        text = self.content["font1"].render("Food: " + str(self.player1.food).rjust(13), True, WHITE)  
        self.screen.blit(text, (self.screen.get_rect().centerx-150, self.screen.get_rect().centery-210))
        text = self.content["font1"].render("Minerals: " + str(self.player1.mineral).rjust(8), True, WHITE)  
        self.screen.blit(text, (self.screen.get_rect().centerx-150, self.screen.get_rect().centery-195))
        text = self.content["font1"].render("Equipment: " + str(self.player1.equipment).rjust(4), True, WHITE)  
        self.screen.blit(text, (self.screen.get_rect().centerx-150, self.screen.get_rect().centery-180))
        text = self.content["font1"].render("Cargo: " + (str(self.player1.findcargo())+"/"+str(self.player1.maxcargo)).rjust(10), True, WHITE)  
        self.screen.blit(text, (self.screen.get_rect().centerx-150, self.screen.get_rect().centery-165))


        if self.inTown:
            text = self.content["font1"].render("Outpost: ", True, WHITE)  
            self.screen.blit(text, (self.screen.get_rect().centerx, self.screen.get_rect().centery-240))
            text = self.content["font1"].render("Type: " + self.outpost.type, True, WHITE)  
            self.screen.blit(text, (self.screen.get_rect().centerx, self.screen.get_rect().centery-225))
            text = self.content["font1"].render("Food: " + str(self.outpost.food.current) + "/" + str(self.outpost.food.capacity) + " at " + str(self.outpost.food.getSellPrice()) + "/" + str(self.outpost.food.getBuyPrice()), True, WHITE)  
            self.screen.blit(text, (self.screen.get_rect().centerx, self.screen.get_rect().centery-210))
            text = self.content["font1"].render("Minerals: " + str(self.outpost.mineral.current) + "/" + str(self.outpost.mineral.capacity) + " at " + str(self.outpost.mineral.getSellPrice()) + "/" + str(self.outpost.mineral.getBuyPrice()), True, WHITE)  
            self.screen.blit(text, (self.screen.get_rect().centerx, self.screen.get_rect().centery-195))
            text = self.content["font1"].render("Equipment: " + str(self.outpost.equipment.current) + "/" + str(self.outpost.equipment.capacity) + " at " + str(self.outpost.equipment.getSellPrice()) + "/" + str(self.outpost.equipment.getBuyPrice()), True, WHITE)  
            self.screen.blit(text, (self.screen.get_rect().centerx, self.screen.get_rect().centery-180))
        
 
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
        #if its a alpha numeric character
        if key > 31 and key < 128 and len(self.buffer) < MAXTEXT:
            self.buffer += chr(key)
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
        self.dispMessage(self.buffer)
        raw = self.buffer.strip()
        
        if self.currentCommand == -1:
            if raw == "g":
                if (self.player1.posX, self.player1.posY) in self.outposts:
                    self.outpost = self.outposts[(self.player1.posX, self.player1.posY)]
                    self.inTown = True
                    self.dispMessage("Welcome to the Outpost")
                    self.currentCommand = 0
                else:
                    print "no"
                    
        elif self.currentCommand == 0:
            if raw == "b":
                self.currentCommand = 1
                self.dispMessage("What would you like to buy?")
            elif raw == "s":
                self.currentCommand = 3
                self.dispMessage("What would you like to sell?")
            elif raw == "q" or raw == "exit":
                self.dispMessage("Goodbye")
                self.inTown = False
                self.outpost = None
                self.currentCommand = -1
                
        elif self.currentCommand == 1:
            if raw == "f":
                self.dispMessage("How much food?")
                self.currentCommand = 2
                self.currentCommodity =  1                  
            elif raw ==  "m":
                self.dispMessage("How many minerals?")
                self.currentCommand = 2
                self.currentCommodity =  2             
            elif raw == "e":
                self.dispMessage("How much equipment?")
                self.currentCommand = 2
                self.currentCommodity = 3
            elif raw == "q" or raw == "exit":
                self.dispMessage("Goodbye")
                self.currentCommand = 0
            else:
                self.dispMessage("Invalid choice.")
        elif self.currentCommand == 2:
            if raw == "q" or raw == "exit":
                self.dispMessage("Goodbye")
                self.currentCommand = 0
            self.buy(COMMODITY[self.currentCommodity], raw)
        elif self.currentCommand == 3:
            if raw == "f":
                self.dispMessage("How much food?")
                self.currentCommand = 4
                self.currentCommodity =  1                  
            elif raw ==  "m":
                self.dispMessage("How many minerals?")
                self.currentCommand = 4
                self.currentCommodity =  2             
            elif raw == "e":
                self.dispMessage("How much equipment?")
                self.currentCommand = 4
                self.currentCommodity = 3
            elif raw == "q" or raw == "exit":
                self.dispMessage("Goodbye")
                self.currentCommand = 0
            else:
                self.dispMessage("Invalid choice.")
        elif self.currentCommand == 4:
            if raw == "q" or raw == "exit":
                self.dispMessage("Goodbye")
                self.currentCommand = 0
            self.sell(COMMODITY[self.currentCommodity], raw)
            
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
            self.currentCommand = 1
            self.dispMessage("What would you like to buy?")
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
            self.currentCommand = 3
            self.dispMessage("What would you like to Sell?")
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
        try:
            with open("player.dat", 'r') as file: 
                storage = pickle.load(file)
                self.player1 = storage
        except:
            print "Creating new player"
            self.player1 = Character()
            
        try:
            with open("outposts.dat", 'r') as file: 
                storage = pickle.load(file)
                self.outposts = storage
        except:
            print "Loading outpost data"
            self.outposts = {(24,9): Outpost(Point(24,9), "Mine",
                 Commodity("Food", 1.05, 2600, 1300, 1),
                 Commodity("Mineral", 0.9, 7000, 3500, 1),
                 Commodity("Equipment", 1.15, 3500, 1750, 1)
                 ),
                 (45,45): Outpost(Point(45,45), "City",
                 Commodity("Food", 1.15, 6800, 3400, 1),
                 Commodity("Mineral", 1.1, 4300, 2150,  1),
                 Commodity("Equipment", 1.1, 4300, 2150,  1)
                 ),
                 (47,28): Outpost(Point(47,28), "City",
                 Commodity("Food", 1.15, 7400, 3700, 1),
                 Commodity("Mineral", 1.1, 4600, 2300,  1),
                 Commodity("Equipment", 1.1, 4600, 2300,  1)
                 ),
                 (10,3): Outpost(Point(10,3), "Mine",
                 Commodity("Food", 1.05, 3300, 1650, 1),
                 Commodity("Mineral", 0.9, 8800, 4400,  1),
                 Commodity("Equipment", 1.15, 4400, 2200,  1)
                 ),
                 (12,12): Outpost(Point(12,12), "Farm",
                 Commodity("Food", 0.9, 6400, 3200, 1),
                 Commodity("Mineral", 1, 1600, 800,  1),
                 Commodity("Equipment", 1.1, 3200, 1600,  1)
                 ),
                 (25,35): Outpost(Point(25,35), "Factory",
                 Commodity("Food", 1.05, 3300, 1650, 1),
                 Commodity("Mineral", 1.15, 6600, 3300,  1),
                 Commodity("Equipment", 0.9, 8800, 4400,  1)
                 ),
                 (2,39): Outpost(Point(2,39), "Farm",
                 Commodity("Food", 0.9, 5000, 2500, 1),
                 Commodity("Mineral", 1, 1300, 650,  1),
                 Commodity("Equipment", 1.1, 2500, 1250,  1)
                 ),
                 (14,38): Outpost(Point(14,38), "Farm",
                 Commodity("Food", 0.9, 8800, 4400, 1),
                 Commodity("Mineral", 1, 2200, 1100,  1),
                 Commodity("Equipment", 1.1, 4400, 2200,  1)
                 ),
                 (37,50): Outpost(Point(37,50), "Factory",
                 Commodity("Food", 1.05, 3200, 1600, 1),
                 Commodity("Mineral", 1.15, 6300, 3150,  1),
                 Commodity("Equipment", 0.9, 8400, 4200,  1)
                 ),
                 (42,22): Outpost(Point(42,22), "Mine",
                 Commodity("Food", 1.05, 3700, 1850, 1),
                 Commodity("Mineral", 0.9, 9800, 4900,  1),
                 Commodity("Equipment", 1.15, 4900, 2450,  1)
                 ),
                 (7,29): Outpost(Point(7,29), "Farm",
                 Commodity("Food", 0.9, 9800, 4900, 1),
                 Commodity("Mineral", 1, 2500, 1250,  1),
                 Commodity("Equipment", 1.1, 4900, 2450,  1)
                 ),
                 (25,2): Outpost(Point(25,2), "Factory",
                 Commodity("Food", 1.05, 2700, 1350, 1),
                 Commodity("Mineral", 1.15, 5400, 2750,  1),
                 Commodity("Equipment", 0.9, 7200, 3600,  1)
                 ),
                 (5,22): Outpost(Point(5,22), "Mine",
                 Commodity("Food", 1.05, 900, 450, 1),
                 Commodity("Mineral", 0.9, 2400, 1200,  1),
                 Commodity("Equipment", 1.15, 1200, 600,  1)
                 ),
                 (38,50): Outpost(Point(38,50), "Farm",
                 Commodity("Food", 0.9, 2800, 1400, 1),
                 Commodity("Mineral", 1, 700, 350,  1),
                 Commodity("Equipment", 1.1, 1400, 700,  1)
                 ),
                 (5,46): Outpost(Point(5,46), "Factory",
                 Commodity("Food", 1.05, 3500, 1750, 1),
                 Commodity("Mineral", 1.15, 6900, 3450,  1),
                 Commodity("Equipment", 0.9, 9200, 4600,  1)
                 ),
                 (11,33): Outpost(Point(11,33), "City",
                 Commodity("Food", 1.15, 2800, 1400, 1),
                 Commodity("Mineral", 1.1, 1800, 900,  1),
                 Commodity("Equipment", 1.1, 1800, 900,  1)
                 ),
                 (15,7): Outpost(Point(15,7), "Factory",
                 Commodity("Food", 1.05, 3500, 1750, 1),
                 Commodity("Mineral", 1.15, 7100, 3550,  1),
                 Commodity("Equipment", 0.9, 9400, 4700,  1)
                 ),
                 (42,35): Outpost(Point(42,35), "Farm",
                 Commodity("Food", 0.9, 9200, 4600, 1),
                 Commodity("Mineral", 1, 2300, 1150,  1),
                 Commodity("Equipment", 1.1, 4600, 2300,  1)
                 ),
                 (6,9): Outpost(Point(6,9), "Farm",
                 Commodity("Food", 0.9, 8200, 4100, 1),
                 Commodity("Mineral", 1, 2100, 1050,  1),
                 Commodity("Equipment", 1.1, 4100, 2050,  1)
                 ),
                 (23,17): Outpost(Point(23,17), "Farm",
                 Commodity("Food", 0.9, 10000, 5000, 1),
                 Commodity("Mineral", 1, 2500, 1250,  1),
                 Commodity("Equipment", 1.1, 5000, 2500,  1)
                 ),
                 (41,41): Outpost(Point(41,41), "Factory",
                 Commodity("Food", 1.05, 3500, 1750, 1),
                 Commodity("Mineral", 1.15, 6900, 3450,  1),
                 Commodity("Equipment", 0.9, 9200, 4600,  1)
                 ),
                 (12,23): Outpost(Point(12,23), "Factory",
                 Commodity("Food", 1.05, 3500, 1750, 1),
                 Commodity("Mineral", 1.15, 6900, 3450,  1),
                 Commodity("Equipment", 0.9, 9200, 4600,  1)
                 ),
                 (20,13): Outpost(Point(20,13), "Farm",
                 Commodity("Food", 0.9, 2800, 1400, 1),
                 Commodity("Mineral", 1, 700, 350,  1),
                 Commodity("Equipment", 1.1, 1400, 700,  1)
                 ),
                 (10,7): Outpost(Point(10,7), "Mine",
                 Commodity("Food", 1.05, 3800, 1900, 1),
                 Commodity("Mineral", 0.9, 10000, 5000,  1),
                 Commodity("Equipment", 1.15, 5000, 2500,  1)
                 ),
                 (44,43): Outpost(Point(44,43), "Mine",
                 Commodity("Food", 1.05, 3400, 1700, 1),
                 Commodity("Mineral", 0.9, 9000, 4500,  1),
                 Commodity("Equipment", 1.15, 4500, 2250,  1)
                 )				 
                 }
            
    def exit(self):
        storage = self.player1
        with open("player.dat", 'w') as file: 
            pickle.dump(storage, file)
            
        storage = self.outposts
        with open("outposts.dat", 'w') as file: 
            pickle.dump(storage, file)
            
            
        sys.exit(0)
        
        
