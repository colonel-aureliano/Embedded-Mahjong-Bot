import pygame
import os

WHITE = 255,255,255
BLACK = 0, 0, 0
CENTER = 240,180
TOP = 240, 60
LOWER = 240, 300
os.putenv('SDL_VIDEODRIVER','fbcon') # two environment variables for piTFT display
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV','dummy') # Environment variables for touchscreen
os.putenv('SDL_MOUSEDEV','/dev/null')
os.putenv('DISPLAY','')

font_big = pygame.font.Font(None, 50)
font_small = pygame.font.Font(None, 30)
size = width, height = 320, 240 

def clean_up():
  pygame.quit()

#####################################################

def display_smaller_top(screen, text):
  screen.fill(BLACK)
  text_surface = font_small.render(text, True, WHITE)
  rect = text_surface.get_rect(center=TOP)
  screen.blit(text_surface, rect)
  pygame.display.flip()
  # pygame.display.update()

def display_big_center(screen, text):
  screen.fill(BLACK)
  text_surface = font_big.render(text, True, WHITE)
  rect = text_surface.get_rect(center=CENTER)
  screen.blit(text_surface, rect)
  pygame.display.flip()
  # pygame.display.update()

def display_smaller_lower(screen, text):
  screen.fill(BLACK)
  text_surface = font_big.render(text, True, WHITE)
  rect = text_surface.get_rect(center=LOWER)
  screen.blit(text_surface, rect)
  pygame.display.flip()
  # pygame.display.update()

#####################################################

def screen_object():
  pygame.init()
  return pygame.display.set_mode(size)

def trial(screen):
  screen.fill(BLACK)
  text_surface = font_big.render('Hello World!', True, WHITE)
  rect = text_surface.get_rect(center=CENTER)
  screen.blit(text_surface, rect)
  pygame.display.flip()
  # pygame.display.update()

def main():
  pygame.init()
  # pygame.mouse.set_visible(False)
  screen = pygame.display.set_mode(size) 
  trial(screen)
  pygame.quit()

if __name__ == "__main__":
    main()