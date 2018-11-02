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

from borg import *
import datetime as d

IDLE_TIMEOUT = d.timedelta(seconds=60)

#
# The player class
#
class Player(Borg):

  def __init__(self):
    Borg.__init__(self)

  def reset(self):
    # null values
    self.name, self.age = "", -1
    self.score, self.stats, self.lives = 0, [], 3
    # results
    self.results_track = [1000,650,430,210]
    self.results_buffers = [ResultsBuffer(),ResultsBuffer(),ResultsBuffer(),ResultsBuffer()]
    self.keepActive()
    return self

  # make sure the player is active
  def keepActive(self):
    self.lastActionTime = d.datetime.now()
  def isActive(self):
    return d.datetime.now() < self.lastActionTime + IDLE_TIMEOUT 

  def updateLives(self, dx):
    self.lives += dx
    if self.lives < 0:
      self.lives = 0
  def isAlive(self):
    return self.lives > 0

  def updateScore(self, dx): 
    self.score += dx
    if self.score < 0:
      self.score = 0

class ResultsBuffer:
	def __init__(self,maxResults=1000):
		self.results = []
		self.maxResults = maxResults

	def addResult(self,r):
		if isinstance(r,(int,long,float)):
			self.results.append(r)
		else:
			print "Could not add result"

	def getMean(self):
		numPoints = len(self.results)
		sumPoints = sum(self.results)
		if numPoints==0 or sumPoints==0:
			return 0
		else:
			return sumPoints/float(numPoints)
