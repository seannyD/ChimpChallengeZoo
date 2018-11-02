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

#
# The generic button class
#
class Button(object):
  def __init__(self, rect, colour, enabled=True):
    self.rect    = rect
    self.colour  = colour
    self.enabled = enabled

  def isPressed(self, x, y):
    return self.enabled and self.rect.collidepoint(x, y)

  def draw(self, surface):
    pygame.draw.rect(
        surface,
        self.colour,
        self.rect,
      )

  def do(self):
    print "Implement in subclass"
