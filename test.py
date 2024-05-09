def gpio():
  # Set up libraries and overall settings
  import RPi.GPIO as GPIO  # Imports the standard Raspberry Pi GPIO library
  from time import sleep   # Imports sleep (aka wait or pause) into the program
  GPIO.setmode(GPIO.BCM) # Sets the pin numbering system to use the physical layout

  # Set up pin 11 for PWM
  GPIO.setup(26,GPIO.OUT)  # Sets up pin 11 to an output (instead of an input)
  p = GPIO.PWM(26, 50)     # Sets up pin 11 as a PWM pin
  p.start(0)               # Starts running PWM on the pin and sets it to 0

  # Move the servo back and forth
  p.ChangeDutyCycle(3)     # Changes the pulse width to 3 (so moves the servo)
  sleep(1)                 # Wait 1 second
  p.ChangeDutyCycle(12)    # Changes the pulse width to 12 (so moves the servo)
  sleep(1)

  # Clean up everything
  p.stop()                 # At the end of the program, stop the PWM
  GPIO.cleanup()           # Resets the GPIO pins back to defaults

import servo_control
import tft_display

def servo_test():
    lst = ['w9', 'w2', 'w6', 't3', 's', 't1', 'b7', 'w', 'w9', 'b6', 'w8', 'b6', 't9', 'r']
    while True:

        tile = str(input("Tile: "))
        servo_control.run_control(lst,tile)

def tft_test():
    tft = tft_display.screen_object()
    counter = 0
    prompt_round = f"Round {counter}"
    prompt_ready = "Player ready?"
    prompt_buttons = "Press button 23 to affirm, 27 to quit."

    print(f"################### {prompt_round} ###################")
    print(f"{prompt_ready}")

    if (True):
      tft_display.display_smaller_top(tft, prompt_round)
      tft_display.display_big_center(tft, prompt_ready)
      tft_display.display_smaller_lower(tft, prompt_buttons)

tft_test()