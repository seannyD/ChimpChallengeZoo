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
from game import *
from math import *

from makePlot import *

from player import *

def rotatePoint(offset, origin, angle):
        sinT = sin(radians(angle))
        cosT = cos(radians(angle))
        return (origin[0] + (cosT * (offset[0] - origin[0]) - sinT * (offset[1] - origin[1])),
                      origin[1] + (sinT * (offset[0] - origin[0]) + cosT * (offset[1] - origin[1])))
    
def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy() # Not compatible with pygame 1.8
#    rot_rect = Rect(orig_rect[0],orig_rect[1],orig_rect[2],orig_rect[3])
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
	player = Player()
	makeMyGraph([x.getMean() for x in player.results_buffers],otherLabel="You")


#
# The idle screen
#
def resultsScreen(screen, clock):
  #
  # Base objects
  #
  w, h = screen.get_width(), screen.get_height()

  # header
  font = pygame.font.Font(c.HEADERFONT, 86)
  header_text = font.render("Game Over", True, c.header_col)
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

  # Score 
  score_title_text = font.render("Your score:", True, c.light_green)
  score_title_rect = score_title_text.get_rect()
  score_title_pos = \
    [ w/2 - score_title_rect.width/2
    , 300
    ]
  score_title_border_rect = [score_title_pos[0]-20,score_title_pos[1]-20,score_title_rect.w+40,score_title_rect.h+40]

  score_text = font.render(str(Player().score),True,c.header_col)
  score_rect = score_text.get_rect()
  score_pos = [800,420]
  score_border_rect = Rect(score_pos[0] -20,score_pos[1]-20,score_rect.w+40,score_rect.h+40)

  #Buttons 
    
  font2 = pygame.font.Font(c.HEADERFONT, 60)
  play_again_text = font2.render("Play Again",True,c.header_col)
  play_again_rect = play_again_text.get_rect()
  play_again_pos = [800,600]
  play_again_border_rect = Rect(play_again_pos[0] -20,play_again_pos[1]-40,play_again_rect.w+40,play_again_rect.h+80)
  
  new_player_text = font2.render("New Player",True,c.header_col)
  new_player_rect = new_player_text.get_rect()
  new_player_pos = [800,750]
  new_player_border_rect = Rect(new_player_pos[0] -20,new_player_pos[1]-40,new_player_rect.w+40,new_player_rect.h+80)
  
  
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
  results_graph_pos = (80,600)
  results_graph_border_rect = Rect(results_graph_pos[0]-30,results_graph_pos[1]-30,600,350)
  # results Graph header
  font2 = pygame.font.Font(c.HEADERFONT, 46)
  r_header_text = font2.render("Results", True, c.light_green)
  r_header_text_rect = r_header_text.get_rect()
  r_header_text_pos = (results_graph_border_rect.left - 20,results_graph_border_rect.top-r_header_text_rect.h)
  r_header_text_border = Rect(r_header_text_pos[0]-20,r_header_text_pos[1]-20,r_header_text_rect.w+40,r_header_text_rect.h+40)
  done, quit = False, False
  while done==False and quit==False:
    #
    # Event processing
    #
    for event in pygame.event.get():
      if event.type==pygame.MOUSEBUTTONDOWN:
        Player().keepActive()
	touchPos = c.scaleTouchPos(pygame.mouse.get_pos())
#        if play_again_border_rect.collidepoint(pygame.mouse.get_pos()):
        if play_again_border_rect.collidepoint(touchPos):
         # game.currentScreen = game.ScreenType.NAME
          done = True
#        elif new_player_border_rect.collidepoint(pygame.mouse.get_pos()):
        elif new_player_border_rect.collidepoint(touchPos):
          done = True
      quit = (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or (event.type == pygame.QUIT)
      #done = (event.type == pygame.MOUSEBUTTONDOWN)

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
    
    # score
    RoundedRect(screen,c.dark_green,c.dark_green,score_title_border_rect,c.border_width,c.border_round)
    screen.blit(score_title_text,score_title_pos)
    RoundedRect(screen,c.dark_green,c.white,score_border_rect,c.border_width,c.border_round)
    screen.blit(score_text,score_pos)
    
    # buttons
    RoundedRect(screen,c.dark_green,c.light_green,play_again_border_rect,c.border_width,c.border_round)
    screen.blit(play_again_text,play_again_pos)
    RoundedRect(screen,c.dark_green,c.light_green,new_player_border_rect,c.border_width,c.border_round)
    screen.blit(new_player_text,new_player_pos)
    
    # graph
    RoundedRect(screen, c.dark_green, c.dark_green, r_header_text_border, c.border_width, c.border_round)
    screen.blit(r_header_text, r_header_text_pos)
    RoundedRect(screen, c.border_col, c.white, results_graph_border_rect, c.border_width, c.border_round)
    screen.blit(results_graph, results_graph_pos)

    #clock.tick(c.FPS)
    pygame.display.flip()

    # check if player is idle
    if not Player().isActive():
      return c.ScreenAction.IDLE

  # Transition to next screen
  return c.ScreenAction.NEXT if not quit else c.ScreenAction.QUIT
