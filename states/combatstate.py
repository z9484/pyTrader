from character import *
from fightingcharacter import *
from state import *
import pygame, sys
from pygame.locals import *

BLACK = (0,0,0)
TILESIZE = 32
WHITE = (255, 255, 255)
TIMER = 3000

class CombatState(State):
    def __init__(self, screen, content):
        super(CombatState, self).__init__(screen, content)

        self.player1 = FightingCharacter("Bob")
        self.command = 0
        self.timer = TIMER
        self.isAttacking = False

    def draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.content["@"], (100, 200) )

        timertext = self.content["font1"].render("Time: " + str(self.timer), True, WHITE)
        commandtext = self.content["font1"].render("Selected Command: " + str(self.command), True, WHITE)
        text = self.content["font1"].render("HP: " + str(self.player1.hp), True, WHITE)

        if self.isAttacking:
            atext = self.content["font1"].render("Attack: " + str(self.command), True, WHITE)        
            self.screen.blit(atext, (self.screen.get_rect().centerx, self.screen.get_rect().centery))

        # Create a rectangle
        textRect = text.get_rect()

        # Center the rectangle
        textRect.centerx = self.screen.get_rect().centerx
        textRect.centery = 480 * .9

        self.screen.blit(text, textRect)
        self.screen.blit(commandtext, (640*.1, 480*.1))
        self.screen.blit(timertext, (640*.1, 480*.05))

    def update(self, clock):
        super(CombatState, self).update(clock) 
        for key in self.keys:
            if key == K_ESCAPE: sys.exit(0)
            elif key == K_q: self.first()
            elif key == K_w: self.second()
            elif key == K_e: self.third()
            elif key == K_r: self.fourth()
            elif key == K_d: self.defend()
            elif key == K_BACKSPACE: self.cancel()

        self.updatet(clock.get_time())

    def updatet(self, dt):
        if not self.isAttacking:
            self.timer -= dt
            if self.timer <= 0:
                self.attack()
        
    def attack(self):
        self.isAttacking = True

    def first(self):
        self.command = 1

    def second(self):
        self.command = 2

    def third(self):
        self.command = 3

    def fourth(self):
        self.command = 4

    def cancel(self):
        self.command = 0

    def defend(self):
        self.command = 10

    
