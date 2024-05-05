from camera_onnx_infer import Infer
import json
from player.Player import Player

def play_round(infer : Infer, player : Player, mapping : dict[str, int]):
  infer.shoot_detect_to_json("integrated/predictions.json")

  # read predictions.json
  with open("integrated/predictions.json") as f:
    predictions = json.load(f)

  tiles = []
  for prediction in predictions:
    name = prediction['class_name']
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