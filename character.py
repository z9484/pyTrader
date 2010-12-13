TILESIZE = 32
class Character(object):
    def __init__(self):
	    self.posX = 2
	    self.posY = 2

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

