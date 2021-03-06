import pygame, sys
from pygame.locals import *
from constants import *

class State(object):
    def __init__(self, screen, content):
        self.screen = screen
        self.content = content
        self.cooldown = COOLTIME
        self.dt  = 0
        self.keys = []

    def update(self, clock):
        self.keysDown = []
        # self.keysUp = []
        self.dt = clock.get_time()
        
        for event in pygame.event.get():
            # if event.type == QUIT: sys.exit(0)    
            if hasattr(event, 'key'):
                # if event.type == KEYDOWN: self.keysDown.append(event.key); self.keys.append([event.key, ICOOLTIME])
                # elif event.type == KEYUP: self.keysUp.append(event.key); self.keyreleased(event.key)
                if event.type == KEYDOWN: self.keysDown.append(event.key); self.keys.append([event.key, ICOOLTIME])
                elif event.type == KEYUP: self.keyreleased(event.key)
            
    def draw(self):
        pass
    
    def keyreleased(self, key):
        for i in xrange(len(self.keys)):
            if self.keys[i][0] == key:
                self.keys.pop(i)
                break

    def check_cool(self, index):
        cool = COOLTIME
        if self.keys[index][0] == K_BACKSPACE:
            cool = 25
            
        if self.keys[index][1] <= 0:
	        self.keys[index][1] = cool
	        return True
        else:
	        self.keys[index][1] -= self.dt
	        return False
