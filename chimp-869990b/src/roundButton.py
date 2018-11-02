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
import math
import constants as c

#
# The generic round button class
#
class RoundButton(object):
  def __init__(self, x, y, r,
      border     = 0.1,
      border_col = (100,100,100),
      bg_col     = (200,200,200),
      enabled    = True
    ):
    self.x, self.y, self.r = x, y, r
    self.border     = border
    self.border_col = border_col
    self.bg_col     = bg_col
    self.enabled    = True
    font = pygame.font.Font(c.HEADERFONT, 52)
    self.go = font.render("GO", True, c.white)
    self.go_pos = [self.x-(self.go.get_rect().w/2),self.y-(self.go.get_rect().h/2)]
  def draw(self, surface):
    # border
    pygame.draw.circle(surface, self.border_col,
        (self.x, self.y), self.r,)
    pygame.draw.circle(surface, self.bg_col,
        (self.x, self.y), (self.r - self.border),)
    surface.blit(self.go,self.go_pos)


  def isPressed(self, x, y):
    return pow((x - self.x), 2) + pow((y - self.y), 2) < pow(self.r, 2)

  def do(self):
    print "Implement in subclass"
