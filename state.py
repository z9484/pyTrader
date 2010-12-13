import pygame, sys
from pygame.locals import *

class State(object):
    def __init__(self, screen, content):
        self.screen = screen
        self.content = content
        self.keys = []

    def update(self, clock):
        for event in pygame.event.get():
            if event.type == QUIT: sys.exit(0)    
            if hasattr(event, 'key'):
                if event.type == KEYDOWN: self.keys.append(event.key)
                elif event.type == KEYUP: self.keyreleased(event.key)

    def draw(self):
        pass
    
    def keyreleased(self, key):
        self.keys.remove(key)
