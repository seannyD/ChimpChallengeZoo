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

import random, os
import pygame
from pygame.locals import *

import constants as c

from shapes import *
from math import *

from makePlot import *
from resultsThings import *
from textrect import *

def rotatePoint(offset, origin, angle):
        sinT = sin(radians(angle))
        cosT = cos(radians(angle))
        return (origin[0] + (cosT * (offset[0] - origin[0]) - sinT * (offset[1] - origin[1])),
                      origin[1] + (sinT * (offset[0] - origin[0]) + cosT * (offset[1] - origin[1])))
    
def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image
    
def animateLeaf(image,originPos,screen,maxAngle=10,timing=1000):

	t = pygame.time.get_ticks()
	tx = cos(((t/float(timing)) % timing)) * maxAngle
	image_rect = image.get_rect()
	image_new_pos = rotatePoint(originPos, (800,700), tx)
	image = rot_center(image,tx)
	screen.blit(image,image_new_pos)


def updateResultsGraph():
	#means = readResults('results/sampleOutput.txt')
	
	correct =  getResultsData("results/keyRounds.csv",['latency','correct'])
#	print "correct",correct
	player = Player()
	sorted = [[int(x[1]) for x in correct if int(x[0]) == y] for y in player.results_track]
#	print "sorted",sorted
	means = []
	for x in sorted:
		if len(x) > 0 and sum(x) > 0:
			means.append(100* sum(x)/float(len(x)))
		else:
			means.append(0)
#	print "means",means
	makeMyGraph(means,otherLabel="Humans")


def updateHighScores():
	highS = getResultsData("results/highscores.csv",['score','name'])
	print highS
	highS = [[int(x[0]),x[1]] for x in highS]
	highS.sort()
	highS.reverse()
	print "High Scores"
	#hs_text = "NAME  SCORE\n"
	hs_text = ""
	for x in highS[:c.number_of_highscores]:
		#print x[1],x[0]
		hs_text += str(x[1])+":  "+str(x[0])+"\n"
	return hs_text[:-1]




#
# The idle screen
#
def idleScreen(screen, clock):
  #
  # Base objects
  #
  w, h = screen.get_width(), screen.get_height()

  player = Player().reset()


#  for i in range(1008):
#    pygame.mouse.set_pos(i,0)
#  for i in range(754):
#    pygame.mouse.set_pos(1008,i)
  
  # header
  font = pygame.font.Font(c.HEADERFONT, 86)
  header_text = font.render("The Chimp Challenge", True, c.header_col)
  header_text_rect = header_text.get_rect()
  header_text_pos = \
    [ w/2 - header_text_rect.width/2
    , 50
    ]
  header_border_rect = \
    [ header_text_pos[0] - 3*c.border_width  # x
    , header_text_pos[1] - 3*c.border_width  # y
    , header_text_rect.width  + 6*c.border_width  # w
    , header_text_rect.height + 6*c.border_width  # h
    ]

  # The chimp TODO: resize to screen resolution
  chimp = pygame.image.load("images/chimp.png")
  chimp_rect = chimp.get_rect()
  chimp_pos  = \
    [ 0
    , 120
    ]
    
  leafL = pygame.image.load("images/Leaf1L_b.png")
  leafL_pos = [-300,-200]
  leafL2 = pygame.image.load("images/Leaf2LDark_b.png")
  leafL2_pos = [-200,-300]
  
  leafR = pygame.image.load("images/Leaf1R_b.png")
  leafR_pos = [1000,300]
  leafR2 = pygame.image.load("images/Leaf1RDark_b.png")
  leafR2_pos = [900,200]

  # resultsGraph
  updateResultsGraph()
  results_graph = pygame.image.load("results/myGraph.png")
  results_graph_pos = (80,430)
  results_graph_border_rect = Rect(results_graph_pos[0]-30,results_graph_pos[1]-30,600,350)
  # results Graph header
  font2 = pygame.font.Font(c.HEADERFONT, 46)
  r_header_text = font2.render("Current Results", True, c.light_green)
  r_header_text_rect = r_header_text.get_rect()
  r_header_text_pos = (results_graph_border_rect.left - 20,results_graph_border_rect.top-r_header_text_rect.h)
  r_header_text_border = Rect(r_header_text_pos[0]-20,r_header_text_pos[1]-20,r_header_text_rect.w+40,r_header_text_rect.h+40)

  # high score table
  hs_text = updateHighScores()
  font_hs = pygame.font.Font(c.NUMBERFONT, 38)
  hs_text_pos = [700,results_graph_pos[1]-10]
  hs_rect = Rect(hs_text_pos[0],hs_text_pos[1],400,(font_hs.get_linesize()*c.number_of_highscores+1))
  hs = render_textrect(hs_text, font_hs, hs_rect, c.foreground_col, c.light_green, justification=0)

  hs_border_rect = Rect(hs_rect[0]-20,hs_rect[1]-20,hs_rect[2]+40,hs_rect[3]+40)
  hs_header_text = font2.render("High Scores", True, c.light_green)
  hs_header_text_rect = hs_header_text.get_rect()
  hs_header_text_pos = (hs_border_rect.left - 20,r_header_text_pos[1])
  hs_header_text_border = Rect(hs_header_text_pos[0]-20,hs_header_text_pos[1]-20,hs_header_text_rect.w+40,hs_header_text_rect.h+40)

 # touch the screen sign
  touch_the_screen = font2.render("Touch the screen to play!", True, c.light_green)
  touch_the_screen_rect = touch_the_screen.get_rect()
#  touch_the_screen_pos = [(w/2) - touch_the_screen_rect.w/2,h-touch_the_screen_rect.h-50]
  touch_the_screen_pos = [results_graph_pos[0],hs_rect.bottom-touch_the_screen_rect.h]
  touch_the_screen_border = Rect(touch_the_screen_pos[0]-20,touch_the_screen_pos[1]-20,touch_the_screen_rect.w+40,touch_the_screen_rect.h+40)

  done, quit = False, False
  while done==False and quit==False:
    #
    # Event processing
    #
    for event in pygame.event.get():
      quit = (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or (event.type == pygame.QUIT)
      done = (event.type == pygame.MOUSEBUTTONUP)

    #
    # Drawing
    #

    # background
    screen.fill(c.background_col)
    # leaves
    animateLeaf(leafL2,leafL2_pos,screen,maxAngle=1,timing=1000)
    animateLeaf(leafL,leafL_pos,screen,maxAngle=2,timing=900)

    # header
    RoundedRect(screen, c.border_col, c.border_fill_col, header_border_rect, c.border_width, c.border_round)
    screen.blit(header_text, header_text_pos)

    # chimp
    screen.blit(chimp, chimp_pos)
    
    # graph
    RoundedRect(screen, c.dark_green, c.dark_green, r_header_text_border, c.border_width, c.border_round)
    screen.blit(r_header_text, r_header_text_pos)
    RoundedRect(screen, c.border_col, c.white, results_graph_border_rect, c.border_width, c.border_round)
    screen.blit(results_graph, results_graph_pos)

    # highscores
    RoundedRect(screen, c.dark_green, c.dark_green, hs_header_text_border, c.border_width, c.border_round)
    screen.blit(hs_header_text, hs_header_text_pos)
    RoundedRect(screen, c.border_col, c.light_green, hs_border_rect, c.border_width, c.border_round)
    screen.blit(hs, hs_text_pos)
    
    RoundedRect(screen,c.light_green,c.dark_green,touch_the_screen_border,c.border_width,c.border_round)
    screen.blit(touch_the_screen,touch_the_screen_pos)

    clock.tick(c.FPS)
    pygame.display.flip()

  # Transition to next screen
  return c.ScreenAction.NEXT if not quit else c.ScreenAction.QUIT
