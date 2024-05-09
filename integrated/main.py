from camera_onnx_infer import Infer
import rounds
from player.Player import Player
import sys
from datetime import datetime

def main():
  infer = Infer()
  player = Player()
  end = rounds.rounds_gpio(infer, player)
  # end = rounds.rounds_command_line(infer, player)
  if (end):
    print("Bye!")
  else:
    print("Game ended unexpectedly.")

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

  # Redirect stdout to log file
  sys.stdout = Logger(f"logs/{current_time}_log.txt")

  # Now all print statements will be redirected to log.txt
  print(f"Mahjong Bot Run Log; ran at {current_time}")

  main()