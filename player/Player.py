# assume t1 - t9 are 0 - 8
# assume w1 - w9 are 9 - 17
# assume b1 - b9 are 18 - 26
# flowers is 27 - 30
# honors east - white is 31 - 37
# seasons is 38 - 41

from .HandPartitioner import HandPartitioner

class Player:
  partitioner : HandPartitioner = None
  current_hand : list[int] = []
  bamboo_indices = range(0, 9)
  character_indices = range(9, 18)
  dot_indices = range(18, 27)
  flower_indices = range(27, 31)
  honor_indices = range(31, 38)
  season_indices = range(38, 42)
  suit_name_index_mapping_dict = {
    'bamboo': 0,
    'character': 1,
    'dot': 2,
    'honor': [3,4],
    0: 'bamboo',
    1: 'character',
    2: 'dot',
    3: 'honor',
    4: 'honor'
  }

  def __init__(self):
    self.partitioner = HandPartitioner()
    self.current_hand = []
  
  def add_tile(self, tile: int):
    if (len(self.current_hand) >= 14):
      raise Exception("Hand is already full")
    self.current_hand.append(tile)
  
  def reset_hand(self):
    self.current_hand = []

  # Decides on a tile to play
  # Remove the tile from its own hand and return it
  def play_tile(self) -> int:
    if (len(self.current_hand) < 14):
      raise Exception("Hand is not full")
    if (len(self.current_hand) > 14):
      raise Exception("Hand is overfull")
    tile = self.__decision()
    if (tile == -2): return tile
    self.current_hand.remove(tile)
    return tile

  def __jinzhang_on_suite(self, tiles_out_there: list[int], hand: list[int]) -> dict[str, int]:

    bamboo_character_dot_honors_jinzhang_dict = {
      'bamboo': 0,
      'character': 0,
      'dot': 0,
      'honor': 0
    }

    def __jinzhang_for_suit(suit: int, jinzhang_count: int):
      if (suit == 0): bamboo_character_dot_honors_jinzhang_dict['bamboo'] += jinzhang_count
      elif (suit == 1): bamboo_character_dot_honors_jinzhang_dict['character'] += jinzhang_count
      elif (suit == 2): bamboo_character_dot_honors_jinzhang_dict['dot'] += jinzhang_count
      else: bamboo_character_dot_honors_jinzhang_dict['honor'] += jinzhang_count

    for tile in set(hand):
      jinzhang_count : int = 0
      suit : int = tile // 9                    # 0 for bamboo, 1 for character, 2 for dot, 3 or 4 for honors
      jinzhang_count += tiles_out_there[tile]   # the tile itself can form a couplet/triplet/quadruplet with itself
      __jinzhang_for_suit(suit, jinzhang_count)
    
    patterns : dict = self.partitioner.find_patterns(self.current_hand)
    for key, tile_list in patterns.items():
      if (key == 'seq-complete'):
        for tile in tile_list:
          suit : int = tile // 9
          if (tile % 9 == 0): 
            # one way seqs
            __jinzhang_for_suit(suit, tiles_out_there[tile+3])
          elif (tile % 9 == 6):
            # one way seqs
            __jinzhang_for_suit(suit, tiles_out_there[tile-1])
          else:
            # two way seqs
            __jinzhang_for_suit(suit, tiles_out_there[tile-1] + tiles_out_there[tile+3])
      elif (key == 'seq-two-way'):
        for tile in tile_list:
          suit : int = tile // 9
          __jinzhang_for_suit(suit, tiles_out_there[tile-1] + tiles_out_there[tile+2])
      elif (key == 'seq-one-way'):
        for tile in tile_list:
          suit : int = tile // 9
          if (tile % 9 == 0): 
            # one way seqs
            __jinzhang_for_suit(suit, tiles_out_there[tile+2])
          elif (tile % 9 == 7):
            # one way seqs
            __jinzhang_for_suit(suit, tiles_out_there[tile-1])
      elif (key == 'seq-middle'):
        for tile in tile_list:
          suit : int = tile // 9
          __jinzhang_for_suit(suit, tiles_out_there[tile+1])
      elif (key == 'single'):
        for tile in tile_list:
          suit : int = tile // 9
          if suit not in self.suit_name_index_mapping_dict['honor']:
            __jinzhang_for_suit(suit, (tiles_out_there[tile-1] + tiles_out_there[tile+1]) // 2)
          # supporting JinZhang that form incomplete sequences, i.e. 7 turning into 7,8 or 6,7
      else:
        continue

    return bamboo_character_dot_honors_jinzhang_dict

  def in_same_suit(self, tile1: int, tile2: int) -> bool:
    return tile1 // 9 == tile2 // 9    

  def __jinzhang(self, hand: list[int], tiles_out_there) -> dict[int, int]:
    # assuming len(hand) <= 14, no flowers or seasons
    # calculate the number of "JinZhang" for each tile in hand
    # "JinZhang" is the number of tiles that can be paired with any tile in hand/{tile}
    # To be "paired" means to form a sequence or triplet or couplet
    # E.g. Hand [10, 10, 10, 11, 11, 11, 12, 12, 12, 13, 13, 13, 33, 31], tile 10
    # Removing tile 10 from hand, we have [10, 10, 11, 11, 11, 12, 12, 12, 13, 13, 13, 31, 33]
    # JinZhang = 8 kinds (9, 10, 11, 12, 13, 14, 31, 33)
    # But since there are only 4 cards of each kind, given current hand
    # Real JinZhang = 4 + 1 + 1 + 1 + 1 + 4 + 3 + 3 = 18
    
    # first consider JinZhang for each suit, assuming JinZhang is calculated for a tile in another suit
    bamboo_character_dot_honors_jinzhang_dict = self.__jinzhang_on_suite(tiles_out_there, hand)

    jinzhang = {}

    for tile in set(hand):
      suit : int = tile // 9                  # 0 for bamboo, 1 for character, 2 for dot, 3 or 4 for honors
      jinzhang_count_on_other_suits : int = 0
      # # accumulate all values in bamboo_character_dot_honors_jinzhang_dict not belonging to the suit
      # for key, value in bamboo_character_dot_honors_jinzhang_dict.items():
      #   if (key == 'bamboo' and suit != 0):
      #     jinzhang_count_on_other_suits += value
      #   elif (key == 'character' and suit != 1):
      #     jinzhang_count_on_other_suits += value
      #   elif (key == 'dot' and suit != 2):
      #     jinzhang_count_on_other_suits += value
      #   elif (key == 'honor' and suit != 3 and suit != 4):
      #     jinzhang_count_on_other_suits += value
      #   else:
      #     continue
      
      # print(jinzhang_count_on_other_suits)

      # then calculate JinZhang for the same suit with respect to only the current tile
      # number of tiles out there the same as itself
      jinzhang[tile] = jinzhang_count_on_other_suits + tiles_out_there[tile]
      if (suit in self.suit_name_index_mapping_dict['honor']): 
        continue

      if (self.in_same_suit(tile-1, tile)):
        jinzhang[tile] += tiles_out_there[tile-1]      # number of tiles out there adjacent to itself
        if (tile - 1 in hand and self.in_same_suit(tile-2, tile-1)):
          jinzhang[tile] += tiles_out_there[tile-2]     # number of tiles out there 2 tiles away from itself
      if (self.in_same_suit(tile+1, tile)):
        jinzhang[tile] += tiles_out_there[tile+1]
        if (tile + 1 in hand and self.in_same_suit(tile+2, tile+1)):
          jinzhang[tile] += tiles_out_there[tile+2]
      
      # # then calculate JinZhang for the same suit minus current tile
      # new_hand = hand.copy()
      # new_hand.remove(tile)
      # new_hand = [x for x in new_hand if x // 9 == suit]
      # # add them together
      # jinzhang[tile] = jinzhang_count_on_other_suits + self.__jinzhang_on_suite(tiles_out_there, new_hand)[self.suit_name_index_mapping_dict[suit]]
    
    return jinzhang


  # Assuming flowers and seasons do not contribute to winning hand.
  def __decision(self) -> int:
    # decide on which tile to play from a hand of 14 tiles
    # E.g. Hand [10, 10, 10, 11, 11, 11, 12, 12, 12, 13, 13, 13, 31, 33]
    # patterns : dict = self.partitioner.find_patterns(self.current_hand)
    # {'seq-complete': [10, 10, 10], 'seq-two-way': [], 'seq-one-way': [], 'seq-middle': [], 'triplet': [13], 'pair': [], 'single': [31, 33]}
    # tri_primary : dict = self.partitioner.find_patterns(self.current_hand, 'tri')
    # {'triplet': [10, 11, 12, 13], 'seq-complete': [], 'seq-two-way': [], 'seq-one-way': [], 'seq-middle': [], 'pair': [], 'single': [31, 33]}

    # Principle: 
    # 0. If any of flowers or seasons found, play it right away
    for tile in self.current_hand:
      if (tile in self.flower_indices or tile in self.season_indices):
        return tile
      
    tiles_out_there = [4] * 42
    for tile in self.current_hand:
      tiles_out_there[tile] -= 1
    
    simulated_hand = self.current_hand.copy()
      
    # 1. Remove tiles that are part of a complete sequence or triplet
    patterns : dict = self.partitioner.find_patterns(simulated_hand)
    # print(patterns)
    # print(tiles_out_there)

    for key, tile_list in patterns.items():
      if key == 'seq-complete':
        for tile in tile_list:
          simulated_hand.remove(tile)
          simulated_hand.remove(tile+1)
          simulated_hand.remove(tile+2)
      elif key == 'triplet':
        for tile in tile_list:
          simulated_hand.remove(tile)
          simulated_hand.remove(tile)
          simulated_hand.remove(tile)
      elif key == 'quadruplet':
        for tile in tile_list:
          simulated_hand.remove(tile)
          simulated_hand.remove(tile)
          simulated_hand.remove(tile)
          simulated_hand.remove(tile)
      else:
        continue
    # print(simulated_hand)
    # print(patterns)
    winning_hand = simulated_hand.copy()
    for key, tile_list in patterns.items():
      if key == 'couplet' and len(tile_list) > 0:
        winning_hand.remove(tile_list[0])
        winning_hand.remove(tile_list[0])
      else:
        continue
    
    if (len(winning_hand) == 0): return -2

    # 2. Calculate for each of the rest of the tiles, the number of "JinZhang"    
    jinzhang_dict : dict[int, int]= self.__jinzhang(simulated_hand, tiles_out_there)

    for key, tile_list in patterns.items():
      if key == 'couplet':
        for tile in tile_list:
          jinzhang_dict[tile] += 8

    # print(sorted(jinzhang_dict.items(), key=lambda x: x[1])) 

    # # 3. Play the tile with max score    
    # # In case of tie, play the one that is not part of a couplet in patterns
    # min_tiles = []
    # min_score = 0
    # for tile, score in jinzhang_dict.items():
    #   if score < min_score:
    #     min_score = score
    #     min_score = [tile]
    #   elif score == min_score:
    #     min_score.append(tile)
    # for tile in min_score:
    #   if tile in patterns['couplet']:
    #     continue
    #   return tile

    # 3. Play the tile with max score
    tile = min(jinzhang_dict, key=jinzhang_dict.get)

    return tile