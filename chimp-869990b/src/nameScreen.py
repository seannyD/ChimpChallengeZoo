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
  
  -------------------------
  
  This part implements a touch keyboard.
  a Keyboard includes one or more KeyboardKey and a KeyboardInput (text input field)
  Each KeyboardKey is a rounded rectangle with some text.
  A mouse press event is passed to the keyboard, which searches its keys to see if 
  one contains the mouse position.
  If a KeyboardKey does contain the mouse position, it calls its command.
  The command is set when initialising the KeyboardKey
  A LetterKeyCommand will send the text of the KeyboardKey to the Keyboard's input buffer
  A GoKeyCommand handles the game logic
  
  ## TO DO:  
  Background graphics, animation
  player_name and palyer_age should be variables in the main chimp.py
  (see final statements of this file)
  
'''

import random, os
import pygame
from pygame.locals import *

import constants as c
from shapes import *

from player import *

###########################
# Constants for this screen

input_border_col = c.dark_green
input_fill_col = c.white

key_w = 94 #button width
key_h = 97

upper_top = 782  #when the screen is actually full size
upper_top = 350
mid_top = upper_top + key_h
lower_top = mid_top + key_h

upper_left = 109
mid_left = 142
lower_left = 189

num_left = (1280/2) - ((3*key_w)/2) # for number keyboard

upperRowKeys = ['Q','W','E','R','T','Y','U','I','O','P']
midRowKeys = ['A','S','D','F','G','H','J','K','L','.']
lowerRowKeys = ['Z','X','C','V','B','N','M']

delete_key_text = "DELETE"

input_top = 250
input_width = 400
input_height = 100
name_input_limit = 3

infoText_width = 500

# END OF CONSTANTS
#############################




class GoKeyCommand:
	# This command is triggered when it's time to go to the next screen
	def __init__(self,keyboard):
		self.keyboard = keyboard
	def do(self):
		# the first time this is called, the player has just enterd their name:
		# display age input
		if self.keyboard.layout=="QWERTY":
			print "Player ID:",''.join(self.keyboard.buffer)
			# save name to keyboard saved_data:
			self.keyboard.saved_data.append(''.join(self.keyboard.buffer))
			self.keyboard.resetKeyboard(input_limit=2,minimum_letters_for_go=1,layout="NUM")
			self.keyboard.setInfoText("How old are you?")
		# the second time this is called, the player has entered their age, and they're ready to start
		elif self.keyboard.layout=="NUM":
			print "Player age:",''.join(self.keyboard.buffer)
			# save name to keyboard saved_data:
			self.keyboard.saved_data.append(''.join(self.keyboard.buffer))			
			print "NEXT SCREEN!"
			# GO TO NEXT SCREEN
			self.keyboard.keyboard_done = True


class Keyboard:
	"""Creates a touch keyboard with delete button, and go button
	Layout can be QWERTY or NUM
	"""
	
	def __init__(self,screen,font,input_limit,minimum_letters_for_go=None,layout="QWERTY",infoText=""):
		# for the game logic
		self.keyboard_done = False
		
		self.screen = screen
		self.font = font
		self.buffer = []  # buffer to store current input
		self.saved_data = []  # set of saved inputs
		self.limit= input_limit  # maximum number of characters in input

		# list of keys in keyboard
		self.keys = []

		if minimum_letters_for_go <> None:
			self.minGo = minimum_letters_for_go
			if self.limit < self.minGo:
				self.minGo = self.limit
		else:
			self.minGo = self.limit

		self.layout=layout
		if self.layout=="QWERTY":
			self.QWERTY_layout()
		elif self.layout=="NUM":
			self.Num_layout()
			
		# text input field
		input_left = (self.screen.get_width()/2) - (input_width/2)
		input_rect = Rect(input_left,input_top,input_width,input_height)
		self.input = KeyboardInput(input_rect,self.font,self)
		
		# button for going to next screen
		self.goButton = False # is go button visible and active?
		self.goButtonKey = KeyboardKey(self,input_left+input_width+20,input_top,100,input_height,"GO!",self.font,GoKeyCommand(self))
		
		self.infoText = infoText
		infoText_left = (self.screen.get_width()/2) - (infoText_width/2)
		self.infoText_rect = Rect(infoText_left, input_top - input_height -20,infoText_width,input_height)
		

		
	def addKey(self,k):
		self.keys = self.keys + [k]
		
	def removeAllKeys(self):
		self.keys = []
		
	def resetKeyboard(self,input_limit=None,minimum_letters_for_go=None,layout=None):
		self.buffer = []

		self.removeAllKeys()
		self.goButton = False
		self.input.draw(self.screen)
		
		if input_limit <> None:
			self.limit = input_limit			
		if minimum_letters_for_go <> None:
			self.minGo = minimum_letters_for_go
			if self.limit < self.minGo:
				self.minGo = self.limit
		if layout <> None:
			self.layout = layout
		
		if self.layout=="QWERTY":
			self.QWERTY_layout()
		elif self.layout=="NUM":
			self.Num_layout()
		self.input.setText([])
	
	def setInfoText(self,t):
		self.infoText  = t

		
	def QWERTY_layout(self):
	
		"""Lay out the keyboard on the screen"""
		#upper row
		for x in [(upperRowKeys,upper_left,upper_top),(midRowKeys,mid_left,mid_top),(lowerRowKeys,lower_left,lower_top)]:
			key_list = x[0]
			key_left = x[1]
			key_top = x[2]
			for i in range(len(key_list)):
				l = key_left + (i * key_w)
				t = key_top
				keyLetter = key_list[i]
				self.addKey(KeyboardKey(self,l,t,key_w,key_h,keyLetter,self.font,LetterKeyCommand(self,keyLetter)))
			
		# delete key
		l = lower_left + (len(lowerRowKeys) * key_w)
		t = lower_top
		self.addKey(KeyboardKey(self,l,t,key_w*2,key_h,delete_key_text,self.font,LetterKeyCommand(self,delete_key_text)))

	def Num_layout(self):
		for (key_list,key_left,key_top) in [(['1','2','3'],num_left,upper_top),(['4','5','6'],num_left,mid_top),(['7','8','9'],num_left,lower_top),(['0'],num_left+key_w,lower_top+key_h)]:
			for i in range(len(key_list)):
				l = key_left + (i * key_w)
				t = key_top
				keyLetter = key_list[i]
				self.addKey(KeyboardKey(self,l,t,key_w,key_h,keyLetter,self.font,LetterKeyCommand(self,keyLetter)))


		# delete key
		l = lower_left + (len(lowerRowKeys) * key_w)
		t = lower_top
		self.addKey(KeyboardKey(self,l,t,key_w*2,key_h,delete_key_text,self.font,LetterKeyCommand(self,delete_key_text)))
		
	
	
	def enterLetter(self,letter):
		""" User Presses key"""
		#print ">",letter
		if letter == delete_key_text:
			print "delete key pressed",buffer
			self.buffer = self.buffer[:-1]
		else:
			if len(self.buffer)<self.limit:
				self.buffer.append(letter)
		self.input.setText(self.buffer)
		
		# check to see if go button should appear
		self.goButton = len(self.buffer)>=self.minGo
	
	def draw(self):
		# keys
		for k in self.keys:
			k.draw(self.screen)
		# text input
		self.input.draw(self.screen)
		# go button
		if self.goButton:
			self.goButtonKey.draw(self.screen)	
		#info text
		if len(self.infoText) > 0:
			RoundedRect(self.screen, input_border_col, c.light_green, self.infoText_rect, c.border_width, c.border_round)
			iText = self.font.render(self.infoText, True, c.header_col)
			iText_rect = iText.get_rect()
			self.screen.blit(iText, [self.infoText_rect.centerx-(iText_rect.w/2),self.infoText_rect.centery-(iText_rect.h/2)])
	
	def handleMouseDown(self,pos):
		
		# Check go button
		if self.goButton:
			self.goButtonKey.handleMouseDown(pos)		

		# check all keys
		t = True
		i = 0
		while t and i < len(self.keys):
			t = not self.keys[i].handleMouseDown(pos)
			i += 1
		
	def resetKeyColours(self):
		for k in self.keys:
			if k.key_fill_col != k.default_fill_col:
				k.key_fill_col = k.default_fill_col
				k.draw(self.screen)
		self.goButtonKey.key_fill_col = self.goButtonKey.default_fill_col
		self.goButtonKey.draw(self.screen)

class KeyboardInput:
	""" Text input that's linked to the keyboard """

	def __init__(self,rect,font,keyboard):
		self.keyboard = keyboard
		self.rect = rect
		self.font = font
		self.setText([])
		
	def setText(self,t):
		self.text = ''.join(t)
		if len(self.text) >= self.keyboard.limit:
			self.text = self.text[:self.keyboard.limit]
		self.text = ''.join(t+['_ ' for x in range((self.keyboard.limit) - len(t))])	 

	
	def draw(self,surface):
		RoundedRect(surface, input_border_col, input_fill_col, self.rect, c.border_width, c.border_round)
		keyText = self.font.render(self.text, True, c.header_col)
		keyText_rect = keyText.get_rect()
		surface.blit(keyText, [self.rect.centerx-(keyText_rect.w/2),self.rect.centery-(keyText_rect.h/2)])


class LetterKeyCommand:
	""" Triggered when a letter button is pressed """
	def __init__(self,keyboard,letter):
		self.keyboard = keyboard
		self.letter = letter
	def do(self):
		self.keyboard.enterLetter(self.letter)

		
#Button class
class KeyboardKey:
	"""Button class based on the command pattern.
	"""
	
	def __init__(self,keyboard,rect,letter,font,command):
		self.__init__(keyboard,rect.top,rect.left,rect.w,rect.h,letter,font,command)
	
	def __init__(self, keyboard, x, y, w, h, letter,font,command,fill_col=c.light_green):
		self.rect = Rect(x, y, w, h)
		self.letter = letter
		self.font = font
		self.keyboard = keyboard
		self.command = command
		self.key_fill_col = fill_col
		self.default_fill_col = fill_col
		
	def handleMouseDown(self, pos):
		if self.rect.collidepoint(pos):
			self.key_fill_col = c.white
			self.command.do()
			return True
		else:
			return False
				
	def draw(self, surface):
		# draw key
		
		RoundedRect(surface, c.border_col, self.key_fill_col, self.rect, c.border_width, c.border_round)
		keyText = self.font.render(self.letter, True, c.header_col)
#			surface.blit(keyText, [self.rect.left,self.rect.top])
		keyText_rect = keyText.get_rect()
		surface.blit(keyText, [self.rect.centerx-(keyText_rect.w/2),self.rect.centery-(keyText_rect.h/2)])
#			pygame.draw.rect(
#				surface,
#				(100,100,100), #gray
#				self.rect,
#				)

#
# The enter your name screen
#
def nameScreen(screen, clock):
  #
  # Base objects
  #
  w, h = screen.get_width(), screen.get_height()

  # header
  font = pygame.font.Font(c.HEADERFONT, 36)
  header_text = font.render("The Chimp Challenge", True, c.header_col)
  header_text_rect = header_text.get_rect()
  header_text_pos = \
    [ w/2 - header_text_rect.width/2
    , h/4 - header_text_rect.height/2
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
    , 50
    ]

	# Keyboard:
  keyFont = pygame.font.Font(c.HEADERFONT, 42)
  keyboard = Keyboard(screen,keyFont,name_input_limit,infoText='Choose your player ID!')

  done, quit = False, False

  pygame.time.set_timer(USEREVENT+1, 100)
  # the player
  p = Player().reset()
  while done==False and quit==False:
    #
    # Event processing
    #
    for event in pygame.event.get():
      quit = (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or (event.type == pygame.QUIT)
      done = keyboard.keyboard_done
      if event.type == MOUSEBUTTONDOWN:
        p.keepActive() # the player is active
	touchPos = c.scaleTouchPos(pygame.mouse.get_pos())
        keyboard.handleMouseDown(touchPos)
      if event.type == USEREVENT+1:
        keyboard.resetKeyColours()

    #
    # Drawing
    #
    screen.fill(c.background_col) # background
    screen.blit(chimp, chimp_pos) # chimp
    keyboard.draw()               # keyboard

    # header
    # RoundedRect(screen, c.border_col, c.border_fill_col, header_border_rect, c.border_width, c.border_round)
   # screen.blit(header_text, header_text_pos)

    clock.tick(c.FPS)
    pygame.display.flip()

    #
    # Transition to next screen
    #
    if done:
      p.name = keyboard.saved_data[0]
      p.age  = keyboard.saved_data[1]

    # check if player is idle
    if not p.isActive():
      return c.ScreenAction.IDLE

  return c.ScreenAction.NEXT if not quit else c.ScreenAction.QUIT
