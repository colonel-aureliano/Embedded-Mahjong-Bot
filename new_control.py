# [names] is the list of all current tiles
# [name] is the current tile being played

# Set up libraries and overall settings
import RPi.GPIO as GPIO  # Imports the standard Raspberry Pi GPIO library
import time   # Imports sleep (aka wait or pause) into the program
import re
import pigpio

#================================helper functions===============================
def map_value(input_value, input_range, output_range):
    input_min, input_max = input_range
    output_min, output_max = output_range

    # Normalize the input value
    normalized_input = (input_value - input_min) / (input_max - input_min)

    # Map the normalized input value to the output range
    result = normalized_input * (output_max - output_min) + output_min
    output_value = round(result, 2)

    return output_value

#================================running===============================

GPIO.setmode(GPIO.BCM) # Sets the pin numbering system to use the physical layout
# Path to the log file
pi_hw = pigpio.pi()
#pi_hw.set_mode(13, pigpio.OUTPUT)

# Set up pin 11 for PWM
#GPIO.setup(26,GPIO.OUT)  # Sets up pin 11 to an output (instead of an input)
#p = GPIO.PWM(26, 50)     # Sets up pin 11 as a PWM pin
#p.start(0)               # Starts running PWM on the pin and sets it to 

tile_range = (0, 13)
pointer_range = (10, 5)

start_time = time.time()


dc2 = 3
end_dc = dc2 * 10000

# Call the function to continuously monitor the log file for the latest play value

#rack = []

#pointer = 0
while True:
    if time.time() - start_time > 30:
            break

    tile = int(input("Tile value: "))
    pointer = map_value(tile, tile_range, pointer_range)
    in_dc = int(pointer * 10000)
    #p.ChangeDutyCycle(pointer)     # Changes the pulse width to 3 (so moves the servo)
    #time.sleep(3)                 # Wait 1 second
    #p.ChangeDutyCycle(3) #go back to initial position
    pi_hw.hardware_PWM(13, 50, in_dc)
    print("hello")
    #time.sleep(1)
    #pi_hw.hardware_PWM(13, 0, end_dc)
    time.sleep(2)
    print("bye")

        # Clean up everything
pi_hw.stop()
#p.stop()                 # At the end of the program, stop the PWM
GPIO.cleanup()           # Resets the GPIO pins back to defaults