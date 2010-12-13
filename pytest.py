import pygame, sys
from pygame.locals import *

from character import *
from states.gamestate import *
from states.combatstate import *

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
