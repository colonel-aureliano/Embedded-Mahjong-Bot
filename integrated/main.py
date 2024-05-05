from camera_onnx_infer import Infer
import json
from player.Player import Player

def play_round(infer : Infer, player : Player, mapping : dict[str, int]):
  prediction_path = "integrated/predictions.json"
  infer.shoot_detect_to_json(prediction_path, True)

  # read predictions.json
  with open(prediction_path) as f:
    predictions = json.load(f)

  names = []
  tiles = []
  for prediction in predictions:
    name = prediction['class_name']
    names.append(name)
    tiles.append(mapping[name])

  if(len(tiles) != 14):
    print(names)
    for i in range(14-len(tiles)):
      name = input("Add missing tile: ")
      names.append(name)
      tiles.append(mapping[name])

  for tile in tiles:
    player.add_tile(tile)
    
  tile = player.play_tile()
  print(tile)

def main():
  infer = Infer()
  player = Player()
  
  # read player_tile_mapping.json
  with open("integrated/player_tile_mapping.json") as f:
    mapping = json.load(f)

  play_round(infer, player, mapping)

main()