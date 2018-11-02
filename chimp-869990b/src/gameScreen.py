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
from player import *
from grid import *
from gameButton import *
from roundButton import *
from resultsThings import *

#
# the game mode
#   specifies the type of stimuli
class Mode:
  numeral = 0
  symbol  = 1

class PhaseType:
  waiting = 0
  display = 1
  input   = 2
  results = 3

#
# The game screen
#
class GameScreen(object):
  def __init__(self, screen, clock, levels, mode):
    #
    # Base objects
    #
    self.screen = screen
    self.clock  = clock
    #pygame.mixer.init()
    # audio [in]correct sounds
    '''
    self.audio = \
      [ pygame.mixer.Sound("audio/Incorrect.ogg")
      , pygame.mixer.Sound("audio/Correct.ogg")
      ]
    '''

    self.mode = mode

    # fonts
    self.font = pygame.font.Font(c.HEADERFONT, 64)
    self.statsfont = pygame.font.Font(c.NUMBERFONT, 64)
 
    #
    # dimensions
    #
    self.w, self.h = screen.get_width(), screen.get_height()
    self.border_w = int(self.w * c.game_border_width)
    self.border_h = int(self.h * c.game_border_width)
    # the symbol guide
    self.symbol_guide_h = self.h*0.15 if mode==Mode.symbol else 0
    # the player stats - render some fake text to get the height
    self.player_stats_h = self.statsfont.render("0", True, c.black).get_rect().h
    # the game buttons
    self.btn_w = int(self.w / c.columns)
    self.btn_h = int((self.h - self.symbol_guide_h - self.player_stats_h) / c.rows)
    self.btn_padding = 0.05 # padding around each button

    self.current_level = 0
    self.levels, self.level = levels, levels[self.current_level]

    self.buttons          = [] # in order
    self.buttons_selected = [] # the order of buttons selected

    self.grid = Grid(c.rows, c.columns)

    # start button
    r = int(c.start_button_radius * self.w)
    self.startButton = RoundButton(
        r + 4*self.border_w,
        self.h - r - 8*self.border_w,
        r,
        self.border_w, c.foreground_col, c.background_col)

    # variables for feedback
    self.feedback_duration = 1000.0  # time to give feedback after each round
    self.feedback_visible = False
    self.feedback_t = 0

    # symbol guide
    self.guideButtons = []
    if mode==Mode.symbol:
      self.createSymbolGuide()

    # player stats
    self.updateLives()
    self.updateScore()

    # set to the start phase to wait for user input
    self.setPhase(PhaseType.waiting)

  def resetGame(self):
    self.current_level = 0
    self.level = self.levels[self.current_level]
    self.feedback_visible = False
    self.feedback_t = 0
    self.buttons          = [] # in order
    self.buttons_selected = [] # the order of buttons selected
    self.setPhase(PhaseType.waiting)
    Player().lives = 3
    self.updateLives()

  def updateLives(self):
    lives = u''
    for i in range(Player().lives): lives += u'\u2764'
    self.livesText = self.statsfont.render(lives, True, c.red)
    self.livesTextRect = self.livesText.get_rect()
    self.livesPos = [self.border_w, self.h - self.livesTextRect.h]

  def updateScore(self):
    self.scoreText = self.statsfont.render(str(Player().score), True, c.white)
    self.scoreTextRect = self.scoreText.get_rect()
    self.scorePos = \
      [ self.w - self.scoreTextRect.w - self.border_w 
      , self.h - self.livesTextRect.h
      ]

  def createSymbolGuide(self):
    w, h = self.w / 9., self.symbol_guide_h
    for i in range(9):
      self.guideButtons.append(GameButton(Rect(i*w,0,w,h), None, c.foreground_col, i+1, visible=True, enabled=False, symbols=True))

  def newButtons(self):
    self.buttons, self.buttons_selected = [], []
    self.grid.shuffle()
    # get a new set of random numbers
    ns = range(c.min_number, c.max_number+1)
    shuffle(ns)
    for i in sorted(ns[:self.level['n']]):
      gridpos = self.grid.itemLocation(i) # (row, column)
      x = (gridpos[1] + self.btn_padding) * self.btn_w
      y = (gridpos[0] + self.btn_padding) * self.btn_h + self.symbol_guide_h
      w = self.btn_w * (1 - 2 * self.btn_padding)
      h = self.btn_h * (1 - 2 * self.btn_padding)
      self.buttons.append(GameButton(Rect(x, y, w, h), gridpos,
        c.foreground_col, i, symbols=self.mode==Mode.symbol))

  def maskButtons(self):
    for b in self.buttons:
      b.mask, b.enabled = True, True
      
  def unmaskButtons(self):
    for b in self.buttons:
      b.visible, b.mask, b.enabled = True, False, False
    
  def colourButtons(self):
    for b in self.buttons:
      correct = self.buttons_selected.index(b.value) == map(GameButton.getValue, self.buttons).index(b.value)
      b.changeColour([c.red,c.green][correct])

  def handleEvents(self):
    for event in pygame.event.get(): # User did something
      self.quit = (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or (event.type == pygame.QUIT)
      if (event.type == pygame.MOUSEBUTTONDOWN):
        Player().keepActive() # make sure the player isn't idle
	touchPos = c.scaleTouchPos(pygame.mouse.get_pos())
#        b = self.checkForButtonPress(pygame.mouse.get_pos())
        b = self.checkForButtonPress(touchPos)
        # if waiting phase, go to display
        if (b and self.phase == PhaseType.waiting):
          self.setPhase(PhaseType.display)
        # if input phase, keep track of buttons selected
        elif (b and self.phase==PhaseType.input):
          self.buttons_selected.append(b.value)
          # if all the buttons have been selected, go to results
          if (len(self.buttons) == len(self.buttons_selected)):
            self.setPhase(PhaseType.results)

  def checkForButtonPress(self, (x, y)):
    # if waiting phase check for the start button
    if (self.phase == PhaseType.waiting):
      return self.startButton if self.startButton.isPressed(x, y) else None
    for b in self.buttons:
      if (b.isPressed(x, y)):
        b.do()
        return b # one button at a time
    return None

  #
  # Drawing
  #
  def drawWaiting(self):
    # Level message
    msg = self.font.render(self.level['msg'], True, c.header_col)
    msg_pos = \
      [ self.w/2 - msg.get_rect().width/2
      , self.h/2 - msg.get_rect().height/2
      ]
    stageText = str(self.level['n'])+" symbols, "+str(self.level['t'])+"ms"
    stageText_r = self.font.render(stageText,True,c.header_col)
    stageText_pos = \
      [ self.w/2 - stageText_r.get_rect().width/2
      , self.h/2 + stageText_r.get_rect().height
      ]

    self.screen.blit(msg, msg_pos)
    self.screen.blit(stageText_r, stageText_pos)

    # start button
    self.startButton.draw(self.screen)

  # draw the game buttons
  def drawButtons(self):
    for b in self.buttons:
      b.draw(self.screen)

  def draw(self):
    # background
    self.screen.fill(c.background_col)

    # player stats (not in training levels)
    if not self.level['type']=='training':
      self.screen.blit(self.livesText, self.livesPos) # lives
      self.screen.blit(self.scoreText, self.scorePos) # score

    # symbol guide
    for b in self.guideButtons:
      b.draw(self.screen)

    if (self.phase == PhaseType.waiting):
      self.drawWaiting()
    elif (self.phase == PhaseType.display or
        self.phase == PhaseType.input):
      self.drawButtons()
    elif (self.phase == PhaseType.results):
      # animate feedback
      correct = self.buttons_selected == map(GameButton.getValue, self.buttons)
      if self.feedback_visible:
    	  ct = (pygame.time.get_ticks() - self.feedback_t +1) / self.feedback_duration
    	  if ct < 1:
	    	  self.drawButtons()
	    	  self.animateFeedback(correct, ct)
    	  else:
	        self.feedback_visible = False
	        self.setPhase(PhaseType.waiting)
      else:          
          self.feedback_t = pygame.time.get_ticks()
          self.unmaskButtons()
          self.colourButtons()
          self.feedback_visible = True
    #pygame.display.flip()
    pygame.display.update()

  def animateFeedback(self,correct,ct):
    # Using Text
    minSize = 10
    maxSize = 400
    text = [u'\u2717',u'\u2713'][correct]
    font = pygame.font.Font(c.NUMBERFONT, int(minSize + ((maxSize-minSize) * ct)))
    f_text = font.render(text, True, [c.red,c.green][correct])
    f_text_rect = f_text.get_rect()
    f_text_rect.center = (self.w/2,self.h/2)
    self.screen.blit(f_text,f_text_rect.topleft)

  def setPhase(self, phase):
    self.phase = phase
    # WAITING phase: start a new level
    if (self.phase == PhaseType.waiting):
      if Player().isAlive():
        self.newButtons()
      else:
        self.endGame()
    # DISPLAY phase: display the numbers
    elif (self.phase == PhaseType.display):
      # make the buttons visible
      for b in self.buttons: b.visible = True
      self.draw()
      # display for t
      pygame.time.delay(self.level['t'])
      # INPUT phase: hide the numbers and wait for input
      self.maskButtons()
      self.phase = PhaseType.input
      self.draw()
    elif (self.phase == PhaseType.results):
      # save results
      self.writeResults()

      btnValues = map(GameButton.getValue, self.buttons)
      correct = self.buttons_selected == btnValues 

      # play [in]correct audio
      #self.audio[correct].play() 

      # Update the score (if not training)
      if not self.level['type']=='training':
        total_correct = 0 
        for (i, j) in zip(self.buttons_selected, btnValues):
          if i==j: total_correct += 1
        score = total_correct * len(btnValues) * 10
        if correct: score *= 2 # 100% correct bonus
        Player().updateScore(score)

      # level up if correct or on training mode
      if correct or self.level['type']=='training':
        self.current_level += 1
        self.level = self.levels[self.current_level]
      # else lose a life
      else:
        Player().updateLives(-1)

      # update the player stats
      self.updateLives()
      self.updateScore()

  def endGame(self):
    saveScore() # save high score
  	# TODO animate end game
    self.done = True

  def writeResults(self):
    latency = self.level['t']
    num_numerals = self.level['n']
    success = int(self.buttons_selected == map(GameButton.getValue, self.buttons))
    roundTime = 1
    grid_positions = [x.gridpos for x in self.buttons]

    saveRound(latency,num_numerals,self.buttons_selected,map(GameButton.getValue, self.buttons),roundTime,grid_positions)

    try:
      player = Player()
      # if this is one of the conditions we're interested in, add to results of player
      if latency in player.results_track and num_numerals==5:
        player.results_buffers[player.results_track.index(latency)].addResult(success)
        saveKeyRound(latency,num_numerals,success)
    except AttributeError: print "Player has not been set."

  def run(self):
    self.done, self.quit = False, False
    while self.done==False and self.quit==False:
      # Event processing
      self.handleEvents()
      self.draw()
      tickFPS = self.clock.tick(c.FPS)
      # check if player is idle
      if not Player().isActive():
        return c.ScreenAction.IDLE

    return c.ScreenAction.NEXT if not self.quit else c.ScreenAction.QUIT
