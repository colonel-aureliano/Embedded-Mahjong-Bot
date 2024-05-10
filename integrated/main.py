from camera_onnx_infer import Infer
import rounds
from player.Player import Player
import sys
import os
import traceback
from datetime import datetime
import gpio_interface

def main():
  infer = Infer()
  player = Player()
  end = rounds.rounds_gpio(infer, player)
  # end = rounds.rounds_command_line(infer, player)
  if (end):
    print("Bye!")
  else:
    print("Game ended unexpectedly.")

def clean_up():
  gpio_interface.clean_up()
  print("Button 27 pressed. Bye!")
  os._exit(0)

#####################################################

class Logger:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass
    
if __name__ == "__main__":
  current_time = datetime.now()
  log_filename = f"logs/{current_time}_log.txt"

  # Redirect stdout to log file
  sys.stdout = Logger(log_filename)

  try:
    # Now all print statements will be redirected to log.txt
    print(f"Mahjong Bot Run Log; ran at {current_time}")
    main()

  except Exception as e:
    print(f"An exception occurred: {e}")
    traceback.print_exc()

    # Delete the log file if an exception is thrown
    try:
        os.remove(log_filename)
        print("Deleted log file due to exception.")
    except Exception as e:
        print(f"Failed to delete log file: {e}")
    
    clean_up()