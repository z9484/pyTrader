import pygame, sys
from pygame.locals import *

ICOOLTIME = 500
COOLTIME = 100

class State(object):
    def __init__(self, screen, content):
        self.screen = screen
        self.content = content
        self.cooldown = COOLTIME
        self.dt  = 0
        self.keys = []

    def update(self, clock):
        self.keysDown = []
        self.keysUp = []
        self.dt = clock.get_time()
        
        for event in pygame.event.get():
            if event.type == QUIT: sys.exit(0)    
            if hasattr(event, 'key'):
                if event.type == KEYDOWN: self.keysDown.append(event.key); self.keys.append([event.key, ICOOLTIME])
                elif event.type == KEYUP: self.keysUp.append(event.key); self.keyreleased(event.key)
            
    def draw(self):
        pass
    
    def keyreleased(self, key):
        for i in xrange(len(self.keys)):
            if self.keys[i][0] == key:
                self.keys.pop(i)
                break


    def check_cool(self, index):
        if self.keys[index][1] <= 0:
	        self.keys[index][1] = COOLTIME
	        return True
        else:
	        self.keys[index][1] -= self.dt
	        return False
