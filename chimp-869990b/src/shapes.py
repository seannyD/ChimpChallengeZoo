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
from math import sqrt

#
# Draw a rounded rect
# 
def RoundedRect(surface,BorderColor,FillColor,(posx,posy,dimensionx,dimensiony),width,roundedness):
  for x in xrange(roundedness,0-1,-1):
    y = sqrt((roundedness**2)-(x**2))
    rect = (posx+(roundedness-x),
            posy+(roundedness-y),
            dimensionx-(2*(roundedness-x)),
            dimensiony-(2*(roundedness-y)))
    pygame.draw.rect(surface,BorderColor,rect,0)
  for x in xrange(roundedness-width,0-1,-1):
    y = sqrt(((roundedness-width)**2)-(x**2))
    rect = (posx+(roundedness-x),
            posy+(roundedness-y),
            dimensionx-(2*(roundedness-x)),
            dimensiony-(2*(roundedness-y)))
    pygame.draw.rect(surface,FillColor,rect,0)
