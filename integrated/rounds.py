from camera_onnx_infer import Infer
import json
from player.Player import Player
import gpio_interface
import tft_display
import servo_control
from time import sleep

prediction_path = "integrated/predictions.json"
generate_predicted_image = False

# Takes a picture and feed all detected tiles to player
# Returns player's decision
def play_round(infer : Infer, player : Player, tile_mapping : dict[str, int], reverse_tile_mapping, counter: int) -> int:

  player.reset_hand()
  unsorted_pred = infer.shoot_detect_to_json(prediction_path, generate_predicted_image)

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

  if(len(tiles) < 14):
    return -1, None, None
    # for _ in range(14-len(tiles)):
    #   print("Add missing tile: ")
    #   name = input()
    #   names.append(name)
    #   tiles.append(tile_mapping[name])

  for tile in tiles:
    player.add_tile(tile)
    
  tile = player.play_tile()
  if (tile == -2): return tile, None, None
  name = reverse_tile_mapping[tile]
  rack = names

  return tile, name, rack

#####################################################

def rounds_factored(infer, player, gpio_input_only: bool, button_next: bool = False):
  with open("integrated/player_tile_mapping.json") as f:
    tile_mapping = json.load(f)
  
  reverse_tile_mapping = {v: k for k, v in tile_mapping.items()}
  counter = 1

  tft = tft_display.screen_object()
  prompt_ready = "Player ready?"
  prompt_quit = "button 27: do quit"
  prompt_playing = "Playing..."
  prompt_won = "Bot won!"

  while(not gpio_interface.do_quit):
    prompt_round = f"Round {counter}"
    
    prompt_buttons = f"Button 23: affirm ready; {prompt_quit}"

    print(f"################### {prompt_round} ###################")
    print(f"{prompt_ready} Press enter to confirm.")

    tft_display.display_up_to_three_texts(tft, prompt_ready, prompt_round, prompt_buttons)

    if (gpio_input_only): gpio_interface.player_ready()
    else: input()
    
    print(prompt_playing)
    tft_display.display_up_to_three_texts(tft, prompt_playing)

    played_tile, name, tile_rack = play_round(infer, player, tile_mapping, reverse_tile_mapping, counter)
    if (played_tile == -2):
      # won
      print(prompt_won)
      tft_display.display_up_to_three_texts(tft, prompt_won, None, "Button 17: confirm")
      if (gpio_input_only): gpio_interface.confirm_won()
      else: sleep(4)
      break
    elif (played_tile == -1):
      print("Number of tiles wrong. Retry.")
      tft_display.display_up_to_three_texts(tft, "Retry", "Number of tiles wrong.")
      sleep(5)
      continue
    counter += 1
 
    sleep_time = 0
    prompt_played = f"Bot plays {name}"
    if button_next:
      prompt_next = "Button 17: start next round"
      wait_on_button = True
    else:
      sleep_time = 5
      prompt_next = f"{sleep_time} seconds till next round"
      wait_on_button = False
    
    print(prompt_played)
    index_of_played = tile_rack.index(name)
    if index_of_played < 7:
      prompt_which_played = f'{index_of_played+1}th from right'
    else:
      prompt_which_played = f'{14-index_of_played}th from left'
      
    tft_display.display_up_to_three_texts(tft, prompt_played, prompt_which_played, prompt_next)

    servo_control.run_control(index_of_played)

    if (gpio_input_only): 
      print(prompt_next)
      gpio_interface.go_to_next_round(wait_on_button, sleep_time)
    else:
      print("Press enter to continue.")
      input()
  
  return True


#####################################################


def rounds(infer, player, gpio_input_only: bool, button_next: bool = False):
  """
  Executes the rounds of the game using GPIO interface.
  Displays status to PiTFT.

  Args:
    infer: The inference model used for making predictions.
    player: The player object representing the bot.

  Returns:
    bool: True if the game rounds were executed successfully.

  """

  return rounds_factored(infer, player, gpio_input_only, button_next)
