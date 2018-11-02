'''
  This file is part of The Chimp Challenge.
  Copyright (C) 2012, Justin Quillinan <justin@justinq.net>
                      Sean Roberts, <s.g.roberts@sms.ed.ac.uk>

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import sys

import constants as c

from idleScreen import *
from nameScreen import *
from gameScreen import *
from resultsScreen import *
from resultsThings import *
from calibScreen import *

from Xlib import X, display

class ScreenType:
  IDLE    = 0
  NAME    = 1
  GAME    = 2
  RESULTS = 3
  MAX     = 3 # final screen type

#
# The main game class to control the levels, etc
#
class Game(object):
  def __init__(self, mode):
    self.mode = mode
    # load the levels
    self.levelData = []
    with open("levels.csv",'rb') as f:
      for row in csv.DictReader(f, quotechar='\"'):
        row['n'], row['t'] = int(row['n']), int(row['t'])
        self.levelData.append(row) 
    # setup pygame
    pygame.init()
    self.screen = pygame.display.set_mode()
    self.clock  = pygame.time.Clock()
    pygame.mouse.set_visible(c.DEBUG)
    pygame.display.set_caption("Chimp Challenge")
    # handle the calibration issue
    if c.DEBUG:
      pygame.mouse.set_pos(0,0)
  def switchMode(self,mode):
    self.mode = mode

  def start(self):
    Player().reset()
    gameScreen = GameScreen(self.screen, self.clock, self.levelData, self.mode)
    #currentScreen = ScreenType.IDLE if not c.DEBUG else ScreenType.GAME
    currentScreen = ScreenType.IDLE

    calib = calibScreen(self.screen,self.clock)
    if calib == c.ScreenAction.QUIT:
      sys.exit(2)
    while True:
      #
      # present the current screen
      #
      if   (currentScreen == ScreenType.IDLE):
        action = idleScreen(self.screen, self.clock)
      elif (currentScreen == ScreenType.NAME):
        action = nameScreen(self.screen, self.clock)
      elif (currentScreen == ScreenType.GAME):
	gameScreen.resetGame()
        action = gameScreen.run()
      elif (currentScreen == ScreenType.RESULTS):
        action = resultsScreen(self.screen, self.clock)
      else:
        print "Invalid screen type: ", currentScreen
        sys.exit(2)

      #
      # Determine next screen
      #
      if (action == c.ScreenAction.QUIT):
        break
      elif (action == c.ScreenAction.IDLE):
        currentScreen = ScreenType.IDLE
      elif (action == c.ScreenAction.NEXT):
        currentScreen = currentScreen + 1 if currentScreen < ScreenType.MAX else ScreenType.IDLE
      else:
        print "Invalid screen action: ", action
        sys.exit(2)
