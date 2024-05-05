from camera_onnx_infer import Infer
import json
from player.Player import Player

def play_round(infer : Infer, player : Player, tile_mapping : dict[str, int], generate_image = False):
  prediction_path = "integrated/predictions.json"
  infer.shoot_detect_to_json(prediction_path, generate_image)

  # read predictions.json
  with open(prediction_path) as f:
    predictions = json.load(f)

  reverse_tile_mapping = {v: k for k, v in tile_mapping.items()}

  names = []
  tiles = []
  for prediction in predictions:
    name = prediction['class_name']
    names.append(name)
    tiles.append(tile_mapping[name])

  if(len(tiles) != 14):
    print(names)
    for _ in range(14-len(tiles)):
      name = input("Add missing tile: ")
      names.append(name)
      tiles.append(tile_mapping[name])

  for tile in tiles:
    player.add_tile(tile)
    
  tile = player.play_tile()
  name = reverse_tile_mapping[tile]
  print(name)

def main():
  infer = Infer()
  player = Player()
  
  # read player_tile_mapping.json
  with open("integrated/player_tile_mapping.json") as f:
    mapping = json.load(f)

  generate_image = False

  play_round(infer, player, mapping, generate_image)

main()