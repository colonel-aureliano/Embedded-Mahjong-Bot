import RPi.GPIO as GPIO
import os
import tft_display
import main
from time import sleep
import threading

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

def player_ready(accept_command_line_enter=True):
  # do_return = False
  do_return = threading.Event()
  
  def gpio():
    # global do_return
    while(True):
      input_state = GPIO.input(23)
      if input_state == False:
        # do_return = True
        do_return.set()
        return

  def cmd_line():
    # global do_return
    input()
    do_return.set()
    # do_return = True
    return

  if (accept_command_line_enter):
    thread1 = threading.Thread(target=gpio)
    thread2 = threading.Thread(target=cmd_line)

    # Start the threads
    thread1.start()
    thread2.start()

    # while (not do_return):
    #   sleep(1)
    do_return.wait()
    thread1.kill()
    thread2.kill()
    return True
  else:
    gpio()
    return True

def go_to_next_round(wait_on_button=True, sleep_time=4, accept_command_line_enter=True):
  do_return = False

  def gpio():
    global do_return
    if wait_on_button:
      while(True):
        input_state = GPIO.input(17)
        if input_state == False:
          do_return = True
    else:
      sleep(sleep_time)
    return

  def cmd_line():
    global do_return
    input()
    do_return = True
    return

  if (accept_command_line_enter):
    thread1 = threading.Thread(target=gpio)
    thread2 = threading.Thread(target=cmd_line)

    # Start the threads
    thread1.start()
    thread2.start()

    while (not do_return):
      continue
    thread1.terminate()
    thread2.terminate()
    return True
  else:
    gpio()
    return True