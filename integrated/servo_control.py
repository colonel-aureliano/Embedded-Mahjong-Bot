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
    output_value = normalized_input * (output_max - output_min) + output_min

    return output_value


def get_latest_play_value(file_path):
    # Open the log file in read mode
    detected_list = []
    bot_plays_value = ""
    with open(file_path, 'r') as file:
        # Seek to the end of the file
        file.seek(0, 2)
        while True:
            # Continuously monitor for changes in the file
            line = file.readline()
            if line:
                # Parse the line to extract the detected list
                detected_list_match = re.match(r"Detected: (.+)", line)
                if detected_list_match:
                    detected_list = eval(detected_list_match.group(1))
                    print("Detected List:" + str(detected_list))

                # Parse the line to extract the bot plays value
                bot_plays_match = re.match(r"Bot plays (.+)", line)
                if bot_plays_match:
                    bot_plays_value = bot_plays_match.group(1)
                    print("Bot Plays Value:"+ bot_plays_value) 
                if detected_list and bot_plays_value:
                    return detected_list,bot_plays_value
            else:
                # If no new lines are found, wait for a moment before checking again
                time.sleep(0.1)


#================================running===============================
def run_control(rack, played):
    GPIO.setmode(GPIO.BCM) # Sets the pin numbering system to use the physical layout
    # Path to the log file
    log_file_path = "logs/log2.txt"

    pi_hw = pigpio.pi()
    # Set up pin 11 for PWM
    #GPIO.setup(26,GPIO.OUT)  # Sets up pin 11 to an output (instead of an input)
    #p = GPIO.PWM(26, 50)     # Sets up pin 11 as a PWM pin
    #p.start(0)               # Starts running PWM on the pin and sets it to 

    tile_range = (0, 13)
    pointer_range = (10, 4)

    start_time = time.time()


    # Call the function to continuously monitor the log file for the latest play value

    #rack = []

    dc2 = 12
    end_dc = dc2 * 10000

    while True:
        if time.time() - start_time > 5:
                break
        # Move the servo back and forth
        #rack, played = get_latest_play_value(log_file_path)

        tile = rack.index(played)
        #print("tile_played: "+str(tile))
        #tile = int(input("Tile value: "))
        pointer = map_value(tile, tile_range, pointer_range)
        in_dc = int(pointer * 10000)
        #p.ChangeDutyCycle(pointer)     # Changes the pulse width to 3 (so moves the servo)
        pi_hw.hardware_PWM(13, 50, in_dc)
        time.sleep(2)                 # Wait 1 second
    pi_hw.hardware_PWM(13, 50, end_dc)

        # Clean up everything
    pi_hw.stop()
    #p.stop()                 # At the end of the program, stop the PWM
    GPIO.cleanup()           # Resets the GPIO pins back to defaults