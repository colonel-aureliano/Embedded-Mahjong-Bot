from camera_onnx_infer import Infer
import json
from player.Player import Player
import sys
from datetime import datetime

prediction_path = "integrated/predictions.json"
generate_image = False

# Takes a picture and feed all detected tiles to player
# Returns player's decision
def play_round(infer : Infer, player : Player, tile_mapping : dict[str, int], reverse_tile_mapping, counter: int) -> int:

  player.reset_hand()
  infer.shoot_detect_to_json(prediction_path, generate_image)

  # read predictions.json
  with open(prediction_path) as f:
    predictions = json.load(f)

  names = []
  tiles = []
  for prediction in predictions:
    name = prediction['class_name']
    names.append(name)
    tiles.append(tile_mapping[name])
  
  print(f"Detected: {names}")

  if(len(tiles) != 14):
    for _ in range(14-len(tiles)):
      name = input("Add missing tile: ")
      names.append(name)
      tiles.append(tile_mapping[name])

  for tile in tiles:
    player.add_tile(tile)
    
  tile = player.play_tile()
  name = reverse_tile_mapping[tile]
  return tile, name

def main():
  infer = Infer()
  player = Player()
  
  with open("integrated/player_tile_mapping.json") as f:
    tile_mapping = json.load(f)
  
  reverse_tile_mapping = {v: k for k, v in tile_mapping.items()}
  counter = 1

  while(True):
    print(f"################### Round {counter} ###################")
    print("Player ready? (type q to quit)")
    command = input()
    if (command == 'q'): break
    print("Playing in process.")
    played_tile, name = play_round(infer, player, tile_mapping, reverse_tile_mapping, counter)
    counter += 1
    print(f"Bot plays {name}")

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

current_time = datetime.now()

# Redirect stdout to log file
sys.stdout = Logger(f"logs/{current_time}_log.txt")

# Now all print statements will be redirected to log.txt
print(f"Mahjong Bot Run Log; ran at {current_time}")

main()