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

DEBUG = False

class ScreenAction:
  QUIT = -1
  IDLE = 0
  NEXT = 1

#
# Game constants
#
FPS = 48
rows, columns = 5, 8 # for the main grid
min_number, max_number = 1, 9
game_border_width      = 0.01  # fraction of screen width
start_button_radius    = 0.085 # fraction of screen width

#
# Appearance constants
#
HEADERFONT = "fonts/ot/gunplay rg.otf"
NUMBERFONT = "fonts/tt/DejaVuSansMono.ttf"

# Base Colours
black       = (0,     0,   0)
white       = (255, 255, 255)
red         = (255,   0,   0)
green       = (  0, 255,   0)
blue        = (  0,   0, 255)
light_green = (167, 180,  13) #a7b40d
dark_green  = (  0,  97,  51) #006133

# layout
background_col = black
foreground_col = white
border_col = dark_green
border_fill_col = light_green
border_width = 8
border_round = 24
header_col = dark_green


number_of_highscores = 10

touchMax_x = 1008.0
touchMax_y = 754.0
screen_x = 1280.0
screen_y = 1024.0


def scaleTouchPos((x,y)):
	if DEBUG:
		return (x,y)
	else:
		return ((float(x)/touchMax_x)*screen_x,(float(y)/touchMax_y)*screen_y)
