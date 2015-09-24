import os, sys
import time
from math import sin, cos, atan2
import pygame
from pygame.locals import *

DEADZONE = 0.05

class Big:
  
  def __init__(self,player):
    self.rad = 25
    self.pos = [0,0]
    self.vel = [0,0]
    self.acl = [0,0]

class Small:
  
  def __init__(self,big):
    self.rad = 10
    self.pos = [big.pos[0] + big.rad, big.pos[1] + big.rad] # * [cos(big.aim),sin(big.aim)]
    self.vel = [0,0]
    self.acl = [0,0]
    self.out = False

class Player:

  def __init__(self, joy):
    self.joy = joy
    self.big = Big(self)
    self.small = Small(self.big)
    self.aim = 0.0 # radians

  def swap(self):
    if self.small.out:
      tmp = self.small.pos
      self.small.pos = self.big.pos
      self.big.pos = tmp
      self.small.out = False
    else:
      self.small.pos[0] = self.big.pos[0] + int(self.big.rad*cos(self.aim))
      self.small.pos[1] = self.big.pos[1] + int(self.big.rad*sin(self.aim))
      self.small.out = True

  def update(self):
    xaim = 0.0
    yaim = 0.0
    xaim = self.joy.get_axis(0)
    yaim = self.joy.get_axis(1)
    if abs(xaim) < DEADZONE:
      xaim = 0.0
    if abs(yaim) < DEADZONE:
      yaim = 0.0
    self.aim = atan2(yaim,xaim)
    print self.aim

# Main function that is called every frame
# dt is the amount of time since this function was last called
# p is a list of players indexed by joy ID
# w is the windowSurface for the game
def Game_Frame(dt,p,w):
  w.fill((0,0,0))
  for x in p:
    x.update()
    pygame.draw.circle(w, (255,255,255), x.big.pos, x.big.rad, 0)
    if x.small.out:
      pygame.draw.circle(w, (255,255,255), x.small.pos, x.small.rad, 0)
  pygame.display.update()
  for event in pygame.event.get():
    if event.type == QUIT:
      for x in joysticks:
        x.quit()
      pygame.joystick.quit()
      pygame.quit()
      sys.exit()
    else:
      if event.type == JOYBUTTONDOWN:
        print event
        p[event.joy].swap()

# Main code and game loop  

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

pygame.init()
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
for x in joysticks:
  x.init()

windowSurface = pygame.display.set_mode((500,400),0,32)
pygame.display.set_caption("Hello world!")

if(len(joysticks) > 0):
  p1 = Player(joysticks[0]) # TODO: Account for player 2 and more than 1 controller
  plist = [p1]
if(len(joysticks) > 1):
  p2 = Player(joysticks[1])
  plist = [p1,p2]

curtime = time.time()
oldtime = curtime
dt = 0.0

while True:
  curtime = time.time()
  dt = curtime - oldtime
  oldtime = curtime

  Game_Frame(dt,plist,windowSurface)

