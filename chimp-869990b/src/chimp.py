#!/usr/bin/python

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

import random, os, sys, getopt
import pygame
from pygame.locals import *

import csv

from constants import *
from game import *

from idleScreen import *
from nameScreen import *
from gameScreen import *
from resultsScreen import *
from resultsThings import *


disp_no = os.getenv('DISPLAY')
if disp_no:
  print "I'm running under X display = {0}".format(disp_no)

#driver = 'x11'
#driver = 'svgalib'
#driver = 'fbd'
#driver = 'fbcon'
#if not os.getenv('SDL_VIDEODRIVER'):
    #os.putenv('SDL_VIDEODRIVER', driver)

def usage():
  print "usage: chimp [-d][-m symbol|numeral]"

def main(argv):

  #
  # Command line arguments
  #
  mode = Mode.numeral # default mode

  try:                                
    opts, args = getopt.getopt(argv, "hdm:", ["help", "debug", "mode="])
  except getopt.GetoptError:
    usage()
    sys.exit(2) 

  for opt, arg in opts:
    if opt in ("-h", "--help"):
      usage()
      sys.exit()
    elif opt in ("-d", "--debug"):
      c.DEBUG = True
    elif opt in ("-m", "--mode"):
      if   arg in ("n", "numeral"):
        mode = Mode.numeral
      elif arg in ("s", "symbol"):
        mode = Mode.symbol
      else:
        print "Error: '"+arg+"' is not a valid mode"
        usage()
        sys.exit()

  #
  # Setup and start the game
  #
  random.seed()
  setUpResultsFiles() # make sure results files are in place
  # start the game
  g = Game(mode)
  g.start()

  pygame.quit() # Be IDLE friendly! 

if __name__ == '__main__': main(sys.argv[1:])
