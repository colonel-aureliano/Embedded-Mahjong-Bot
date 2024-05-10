import pygame
# import pigame
from pygame.locals import *
import os
from time import sleep

WHITE = 255,255,255
BLACK = 0, 0, 0
CENTER = 160,120
TOP = 160, 60
LOWER = 160, 200
os.putenv('SDL_VIDEODRIVER','fbcon') # two environment variables for piTFT display
os.putenv('SDL_FBDEV', '/dev/fb0')
os.putenv('SDL_MOUSEDRV','dummy') # Environment variables for touchscreen
os.putenv('SDL_MOUSEDEV','/dev/null')
os.putenv('DISPLAY','')

size = width, height = 320, 240 

pygame.init()
pygame.mouse.set_visible(False)
font_big = pygame.font.Font(None, 50)
font_small = pygame.font.Font(None, 30)
font_real_small = pygame.font.Font(None, 20)

def clean_up():
  pygame.quit()

def display_up_to_three_texts(screen, text1, text2=None, text3=None):
  screen.fill(BLACK)
  display_big_center(screen, text1)
  if text2 != None:
    display_smaller_top(screen, text2)
  if text3 != None:
    display_smaller_lower(screen, text3)
  pygame.display.flip()

#####################################################

def display_smaller_top(screen, text):
  # screen.fill(BLACK)
  text_surface = font_small.render(text, True, WHITE)
  rect = text_surface.get_rect(center=TOP)
  screen.blit(text_surface, rect)
  # pygame.display.flip()

def display_big_center(screen, text):
  # screen.fill(BLACK)
  text_surface = font_big.render(text, True, WHITE)
  rect = text_surface.get_rect(center=CENTER)
  screen.blit(text_surface, rect)
  # pygame.display.flip()

def display_smaller_lower(screen, text):
  # screen.fill(BLACK)
  text_surface = font_real_small.render(text, True, WHITE)
  rect = text_surface.get_rect(center=LOWER)
  screen.blit(text_surface, rect)
  # pygame.display.flip()

#####################################################

def screen_object():
  lcd = pygame.display.set_mode(size)
  return lcd

def trial(screen):
  screen.fill(BLACK)
  text_surface = font_big.render('Hello World!', True, WHITE)
  rect = text_surface.get_rect(center=CENTER)
  screen.blit(text_surface, rect)
  pygame.display.flip()
  sleep(10)

def main():
  screen = pygame.display.set_mode(size) 
  trial(screen)
  clean_up()

if __name__ == "__main__":
    main()