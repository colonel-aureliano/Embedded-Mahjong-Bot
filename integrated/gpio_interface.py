import RPi.GPIO as GPIO
import os
import tft_display
import main
from time import sleep

GPIO.setmode(GPIO.BCM) 
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

do_quit = False

def clean_up():
  # immediate end below
  tft_display.clean_up()
  GPIO.cleanup()

def GPIO27_callback(channel): 
  global do_quit
  do_quit = True
  print("Button 27 pressed. Bye!")
  main.clean_up()

GPIO.add_event_detect(27, GPIO.FALLING, callback=GPIO27_callback, bouncetime=300) 

def player_ready():
  while(True):
    input_state = GPIO.input(23)
    if input_state == False:
      return True

def go_to_next_round(wait_on_button=True, sleep_time=4):
  if wait_on_button:
    while(True):
      input_state = GPIO.input(17)
      if input_state == False:
        break
  else:
    sleep(sleep_time)

  return True

def confirm_won():
  while(True):
    input_state = GPIO.input(17)
    if input_state == False:
      return True