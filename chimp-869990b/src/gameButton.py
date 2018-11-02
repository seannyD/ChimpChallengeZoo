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

import pygame
from pygame.locals import *

import constants as c
from button import *

#
# The 14 segment LED display polygons
#
LED = [ [(25.0, 0.0), (115.0, 0.0), (125.0, 10.0), (115.0, 20.0), (25.0, 20.0), (15.0, 10.0), (25.0, 0.0)]
      , [(0.0, 90.0), (0.0, 20.0), (10.0, 10.0), (20.0, 20.0), (20.0, 90.0), (10.0, 100.0), (0.0, 90.0)]
      , [(30.0, 25.0), (55.0, 75.0), (55.0, 85.0), (50.0, 85.0), (25.0, 40.0), (25.0, 25.0), (30.0, 25.0)]
      , [(60.0, 85.0), (60.0, 25.0), (80.0, 25.0), (80.0, 85.0), (70.0, 95.0), (60.0, 85.0)]
      , [(110.0, 25.0), (85.0, 75.0), (85.0, 85.0), (90.0, 85.0), (115.0, 40.0), (115.0, 25.0), (110.0, 25.0)]
      , [(120.0, 90.0), (120.0, 20.0), (130.0, 10.0), (140.0, 20.0), (140.0, 90.0), (130.0, 100.0), (120.0, 90.0)]
      , [(25.0, 90.0), (55.0, 90.0), (65.0, 100.0), (55.0, 110.0), (25.0, 110.0), (15.0, 100.0), (25.0, 90.0)]
      , [(85.0, 90.0), (110.0, 90.0), (120.0, 100.0), (110.0, 110.0), (85.0, 110.0), (75.0, 100.0), (85.0, 90.0)]
      , [(0.0, 180.0), (0.0, 110.0), (10.0, 100.0), (20.0, 110.0), (20.0, 180.0), (10.0, 190.0), (0.0, 180.0)]
      , [(30.0, 175.0), (55.0, 125.0), (55.0, 115.0), (50.0, 115.0), (25.0, 160.0), (25.0, 175.0), (30.0, 175.0)]
      , [(60.0, 175.0), (60.0, 110.0), (70.0, 100.0), (80.0, 110.0), (80.0, 175.0), (60.0, 175.0)]
      , [(110.0, 175.0), (85.0, 125.0), (85.0, 115.0), (90.0, 115.0), (115.0, 160.0), (115.0, 175.0), (110.0, 175.0)]
      , [(120.0, 180.0), (120.0, 110.0), (130.0, 100.0), (140.0, 110.0), (140.0, 180.0), (130.0, 190.0), (120.0, 180.0)]
      , [(25.0, 180.0), (115.0, 180.0), (125.0, 190.0), (115.0, 200.0), (25.0, 200.0), (15.0, 190.0), (25.0, 180.0)]
      ]

def boundingRect(paths):
  rect = Rect(9999, 9999, 0, 0)
  for p in paths:
    for (x, y) in p:
      if x < rect.x: rect.x = x
      if y < rect.y: rect.y = y
      if x > rect.w: rect.w = x
      if y > rect.h: rect.h = y
  rect.w, rect.h = rect.w - rect.x, rect.h - rect.y
  return rect

# the bounds of the LED
LED_RECT = boundingRect(LED)

# The live segments of the LED display for numerals
LED_NUM = [ [0, 1, 5, 8, 12, 13]
          , [4, 5, 12]
          , [0, 5, 7, 6, 8, 13]
          , [0, 5, 7, 12, 13]
          , [1, 6, 7, 5, 12]
          , [0, 1, 6, 7, 12, 13]
          , [0, 1, 8, 13, 12, 7, 6]
          , [0, 5, 12]
          , [0, 1, 8, 13, 12, 5, 6, 7]
          , [13, 12, 5, 0, 1, 6, 7]
          ]

# The live segments of the LED display for symbols
LED_SYM = [ [0, 1, 5, 8, 12, 13] # NB: this is just 0
          , [1, 6, 8]
          , [1, 8, 13, 12, 7, 10]
          , [1, 0, 5, 12, 13]
          , [5, 6, 7, 8, 10]
          , [0, 3, 6, 7, 10, 13]
          , [5, 1, 8, 13, 12, 4, 2]
          , [13, 5, 12]
          , [1, 8, 13, 12, 5, 9, 11, 3]
          , [0, 5, 12, 13, 9, 2, 7]
          ]
#
# The game button class
#
# TODO make this use the LED display
class GameButton(Button):
  def __init__(self, rect, gridpos, colour, value,
      visible=False, mask=False, enabled=False, symbols=False):
    Button.__init__(self, rect, colour, enabled)
    self.gridpos = gridpos
    self.value   = value
    self.visible = visible
    self.mask    = mask
    self.symbols = symbols
    #
    # LED path data
    #
    # scale and centre figure
    # this is some embarrassingly inefficient code
    self.paths = []
    paths = LED_SYM[value] if symbols else LED_NUM[value]
    sX, sY = float(rect.w)/LED_RECT.w, float(rect.h)/LED_RECT.h
    scale = sX if sX < sY else sY
    scale *= 0.9 # make it a bit smaller than the button rect
    for i in paths:
      p = [(x*scale + rect.x ,y*scale + rect.y) for (x, y) in LED[i]]
      self.paths.append(p)
    # centre symbol in button rect
    symRect = boundingRect(self.paths)
    dx = (self.rect.w - symRect.w)/2. - (symRect.x - self.rect.x)
    dy = (self.rect.h - symRect.h)/2. - (symRect.y - self.rect.y)
    for i in range(len(self.paths)):
      self.paths[i] = [(x+dx, y+dy) for (x, y) in self.paths[i]]
 
  def changeColour(self, colour):
    self.colour = colour

  def draw(self, surface):
    if (self.visible):
      # if masked, draw the rect
      if (self.mask):
        Button.draw(self, surface)
      # else draw the value
      else: 
        for p in self.paths:
          pygame.draw.polygon(surface, self.colour, p)

  def getValue(self):
    return self.value

  def do(self):
    self.visible, self.enabled = False, False
