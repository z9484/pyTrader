TILESIZE = 32
class Character(object):
    def __init__(self):
        self.posX = 2
        self.posY = 2
        self.credits = 100
        self.food = 0
        self.mineral = 0
        self.equipment = 0
        self.maxcargo = 25


    def moveLeft(self):
	    self.posX -= 1

    def moveRight(self):
	    self.posX += 1

    def moveUp(self):
	    self.posY -= 1

    def moveDown(self):
	    self.posY += 1

    def snap(self):
        print self.posX, self.posY
        self.posX = (self.posX / TILESIZE + 1) * TILESIZE
        
    def viewBalance(self):
        print "Balance:", str(self.credits).rjust(5)
        print "Food:", str(self.food).rjust(8)
        print "Minerals:", str(self.mineral).rjust(4)
        print "Eqipment:", str(self.equipment).rjust(4)
        print "Cargo:", (str(self.findcargo())+"/"+str(self.maxcargo)).rjust(7)
        
    def findcargo(self):
        return self.mineral + self.food + self.equipment

