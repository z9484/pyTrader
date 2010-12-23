import pygame, sys
from pygame.locals import *

from character import *
from states.gamestate.gamestate import *
from states.combatstate import *
from point import *
from states.gamestate.outpost import *

FRAMES_PER_SECOND = 30


class Game(object):
    def __init__(self):
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("BattleSim")
        self.clock = pygame.time.Clock()

        ## Load Content ##
        player = pygame.image.load('gfx/ninja.png')
        ground = pygame.image.load('gfx/grass.bmp')
        wall = pygame.image.load('gfx/gmtn.bmp')

        pygame.font.init()
        font = pygame.font.Font(None, 20)

        self.tiles = {}
        self.tiles["@"] = player
        self.tiles["_"] = ground
        self.tiles["#"] = wall
        self.tiles["font1"] = font

        self.gamestate = GameState(self.screen, self.tiles)
        #self.gamestate = CombatState(self.screen, self.tiles)
        tt = Outpost(Point(24,9), "Mine",
                 Commodity("Food", 1.05, 2600, 1300, 1),
                 Commodity("Mineral", 0.9, 7000, 3500, 1),
                 Commodity("Equipment", 1.15, 3500, 1750, 1)
                 )


    def update(self):
        # USER INPUT
        self.clock.tick(FRAMES_PER_SECOND)
        self.gamestate.update(self.clock)    
        
    def draw(self):
        self.gamestate.draw()
        pygame.display.flip()

    def run(self):

        while 1:
            self.update()
            self.draw()


game = Game()
game.run()
