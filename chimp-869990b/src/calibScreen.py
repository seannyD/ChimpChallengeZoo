import constants as c
import pygame
from pygame.locals import *

def calibScreen(screen, clock):
  #
  # Base objects
  #
  w, h = screen.get_width(), screen.get_height()


  font_hs = pygame.font.Font(c.NUMBERFONT, 38)
  hs_text_pos = [100,200]
  hs_text_render = font_hs.render("Touch the top left corner to start", True, c.white)
  

  done, quit = False, False
  while done==False and quit==False:
    for event in pygame.event.get():
      quit = (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or (event.type == pygame.QUIT)
      if(event.type == pygame.MOUSEBUTTONUP):
        print "pos",pygame.mouse.get_pos()
        p = pygame.mouse.get_pos()
        done = p[0]<7 & p[1] < 7

    screen.blit(hs_text_render, hs_text_pos)
    clock.tick(c.FPS)
    pygame.display.flip()

  return c.ScreenAction.NEXT if not quit else c.ScreenAction.QUIT