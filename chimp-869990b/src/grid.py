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

from random import shuffle

#
# The grid class, 0-indexed
#
class Grid(object):
  def __init__(self, rs, cs):
    self.rs, self.cs = rs, cs
    self.reset()

  def rc2i(self, r, c):
    assert r >= 0 and r < self.rs, 'row index out of range'
    assert c >= 0 and c < self.cs, 'col index out of range'
    return (r * self.cs) + c

  def i2rc(self, i):
    assert i >=0 and i < len(self.d), 'index out of range'
    return i / self.cs, i % self.cs

  def reset(self):
    self.d = [x for x in range(self.rs * self.cs)]

  def shuffle(self):
    shuffle(self.d)

  def getValue(self, r, c):
    return self.d[self.rc2i(r, c)]

  #def setValue(self, r, c, v):
    #self.d[self.rc2i(r, c)] = v

  def itemLocation(self, v):
    assert v >=0 and v < len(self.d), 'value out of range'
    return self.i2rc(self.d.index(v))
