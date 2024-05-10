from camera_onnx_infer import Infer
import json
from player.Player import Player
import gpio_interface
import tft_display
import servo_control

prediction_path = "integrated/predictions.json"
generate_predicted_image = False

# Takes a picture and feed all detected tiles to player
# Returns player's decision
def play_round(infer : Infer, player : Player, tile_mapping : dict[str, int], reverse_tile_mapping, counter: int) -> int:

  player.reset_hand()
  infer.shoot_detect_to_json(prediction_path, generate_predicted_image)

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
  rack = names
  return tile, name, rack

#####################################################

def rounds_factored(infer, player, gpio_and_tft: bool):
  with open("integrated/player_tile_mapping.json") as f:
    tile_mapping = json.load(f)
  
  reverse_tile_mapping = {v: k for k, v in tile_mapping.items()}
  counter = 1

  tft = tft_display.screen_object()

  while(not gpio_interface.do_quit):
    prompt_round = f"Round {counter}"
    prompt_ready = "Player ready?"
    prompt_buttons = "Button 23: affirm ready; button 27: do quit"

    print(f"################### {prompt_round} ###################")
    print(f"{prompt_ready}")

    if (gpio_and_tft):
      # tft_display.display_smaller_top(tft, prompt_round)
      # tft_display.display_big_center(tft, prompt_ready)
      # tft_display.display_smaller_lower(tft, prompt_buttons)
      tft_display.display_up_to_three_texts(tft, prompt_ready, prompt_round, prompt_buttons)

    if (gpio_and_tft): gpio_interface.player_ready()
    else: input()
    prompt_playing = "Playing in process."

    print(prompt_playing)
    if (gpio_and_tft): 
      tft_display.display_up_to_three_texts(tft, prompt_playing)

    played_tile, name, tile_rack = play_round(infer, player, tile_mapping, reverse_tile_mapping, counter)
    counter += 1

    # name = 'w7'
    # tile_rack = ['g', 'b5', 't4', 'e', 'b1', 't4', 'b2', 'b', 'w1', 't7', 't1', 'w7', 'e', 'b3']

    prompt_played = f"Bot plays {name}"
    prompt_next = "Button 17: start next round; button 27: do quit"

    # servo_control.run_control(tile_rack, name)

    print(prompt_played)

    if (gpio_and_tft): 
      print(prompt_next)
      # tft_display.display_big_center(tft, prompt_played)
      # tft_display.display_smaller_lower(tft, prompt_next)
      tft_display.display_up_to_three_texts(tft, prompt_played, None, prompt_next)
      gpio_interface.go_to_next_round()
    else:
      print("Press enter to continue.")
      input()
  
  return True


#####################################################


def rounds_gpio(infer, player):
  """
  Executes the rounds of the game using GPIO interface.
  Displays status to PiTFT.

  Args:
    infer: The inference model used for making predictions.
    player: The player object representing the bot.

  Returns:
    bool: True if the game rounds were executed successfully.

  """

  return rounds_factored(infer, player, True)


def rounds_command_line(infer, player):
  """
  Executes the command line interface for playing rounds of the game.

  Args:
    infer: The inference model used for making decisions.
    player: The player object representing the human player.

  Returns:
    bool: True if the function executes successfully.

  """
  return rounds_factored(infer, player, False)

#   with open("integrated/player_tile_mapping.json") as f:
#     tile_mapping = json.load(f)
  
#   reverse_tile_mapping = {v: k for k, v in tile_mapping.items()}
#   counter = 1

#   while(True):
#     print(f"################### Round {counter} ###################")
#     print("Player ready? (type q to quit)")
#     command = input()
#     if (command == 'q'): break
#     print("Playing in process.")
#     played_tile, name = play_round(infer, player, tile_mapping, reverse_tile_mapping, counter)
#     counter += 1
#     print(f"Bot plays {name}")
  
#   return True