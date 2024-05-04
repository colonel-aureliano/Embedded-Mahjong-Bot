# assume t1 - t9 are 0 - 8
# assume w1 - w9 are 9 - 17
# assume b1 - b9 are 18 - 26
# flowers is 27 - 30
# honors east - white is 31 - 37
# seasons is 38 - 41

# adapted from /JohnnyLiang1018/MahjongAI/master/offline_mahjong/MahjongAgent.py

from collections import defaultdict

class HandPartitioner:

  partition = {}
  efficiency_map = {}
#   num_remain_tile = 70
#   tile_count = [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4]

  def __init__(self):
      pass

  def pair_extract(self,hand):
    remain = []
    x = 0
    while x < (len(hand)-1):
        if (hand[x] == hand[x+1]):
            x+=2
            continue
        remain.append(hand[x])
        x+=1
    if(x<len(hand)):
        remain.append(hand[x])
    return remain 
  
  def tri_extract(self,hand):  
    remain = []
    x = 0
    while x < (len(hand)-2):
        if(hand[x] == hand[x+1] == hand[x+2]):
            x+=3
            continue
        remain.append(hand[x])
        x+=1

    if(x<len(hand)):
        remain.append(hand[x])
    if(x<len(hand)-1):
        remain.append(hand[x+1])

    return remain

  def seq_extract(self,hand,index):
      
      remain = []
      remain.extend(hand[0:index])
      partial_hand = hand[index:]
      index_1_count = 0
      index_2_count = 0
      index_3_count = 0
      index_1_move = 0
      index_2_move = 0
      index_3_move = 0 
      x = 0
      value = partial_hand[0]
      while x < (len(partial_hand)-2):
          
          # print(partial_hand)
          if(index_1_move == 0):
              value = partial_hand[x]
              index_1_count = partial_hand.count(value)
              #print(value)
          
          # no more possible sequences beyong tile 25
          if(value >= 25):
              # print("greater than 15")
              remain.extend(partial_hand[x:])
              return remain
          
          # if three values are within the same type
          if (value // 9 == (value+2) // 9):

              if(index_2_move == 0):
                  index_2_count = partial_hand.count(value+1)
                  #print(value+1)
              if(index_3_move == 0):
                  index_3_count = partial_hand.count(value+2)
                  #print(value+2)

              # print(str(index_1_count) + "," + str(index_2_count) + "," + str(index_3_count))

              # if there are at least one instance of each value
              if (index_1_count >0 and index_2_count >0 and index_3_count>0):

                  # if the numbers of each value are the same
                  if(index_1_count == index_2_count == index_3_count):
                      
                      # loop index advance move sum * 3
                      x += ((index_1_count)*3 + index_1_move + index_2_move + index_3_move)

                      # full reset
                      index_1_count = 0
                      index_2_count = 0
                      index_3_count = 0
                      index_1_move = 0
                      index_2_move= 0
                      index_3_move = 0
                      continue
                  # if the first value is the smallest
                  if (index_1_count <= index_2_count and index_1_count <= index_3_count):
                      
                      
                      
                      # index_2 and index_3 -= index_1, index_2_move and 3_move += index_1
                      index_2_count -= index_1_count
                      index_3_count -= index_1_count
                      index_2_move += index_1_count
                      index_3_move += index_1_count


                      # loop index advance index_1_move + index_1_count
                      if(index_2_count == 0 ):
                          x += (index_1_move+index_1_count+index_2_move)
                          index_1_count = index_3_count
                          index_1_move = index_3_move

                          index_2_count = 0
                          index_2_move = 0
                          index_3_count = 0
                          index_3_move = 0

                          value += 2
                          continue
                      
                      elif(index_3_count == 0 ):
                          
                          remain.extend([(value+1) for i in range(index_2_count)])

                          x += (index_1_move+index_1_count+index_2_move+index_2_count+index_3_move)

                          # full reset
                          index_1_count = 0
                          index_1_move = 0
                          index_2_count = 0
                          index_2_move = 0
                          index_3_count = 0
                          index_3_move = 0

                          continue

                      else:
                          x += (index_1_move+index_1_count)
                          # index_1 = index_2, index_2 = index_3, index_3 = 0
                          index_1_count = index_2_count
                          index_1_move = index_2_move
                          index_2_count = index_3_count
                          index_2_move = index_3_move
                          index_3_count = 0
                          index_3_move = 0
                          value += 1
                          continue
                  
                  elif (index_2_count <= index_1_count and index_2_count <= index_3_count):

                      index_1_count -= index_2_count
                      index_3_count -= index_2_count
                      index_1_move += index_2_count
                      index_3_move += index_2_count
                      
                      remain.extend([value for i in range(index_1_count)])
                      if(index_3_count == 0):
                          x += (index_1_move + index_1_count + index_2_move + index_2_count + index_3_move)

                          # full reset
                          index_1_count = 0
                          index_2_count = 0
                          index_3_count = 0
                          index_1_move = 0 
                          index_2_move = 0
                          index_3_move = 0
                          continue

                      else:
                          x += (index_1_move + index_1_count + index_2_count + index_2_move)
                          index_1_count = index_3_count
                          index_1_move = index_3_move
                          index_2_count = 0
                          index_2_move = 0
                          index_3_count = 0
                          index_3_move = 0
                          value += 2
                          continue
                      
                      
                      
                  elif (index_3_count <= index_1_count and index_3_count <= index_2_count):
                      

                      # remaining 
                      index_1_count -= index_3_count
                      index_2_count -= index_3_count

                      index_1_move += index_3_count
                      index_2_move += index_3_count

                      remain.extend([value for i in range(index_1_count)])
                      remain.extend([(value+1) for i in range(index_2_count)])
                      # move index by the tile 
                      x += (index_1_move+ index_1_count + index_2_move + index_2_count + index_3_count + index_3_move)
                      
                      # full reset
                      index_1_count = 0
                      index_2_count = 0
                      index_3_count = 0
                      index_1_move = 0
                      index_2_move = 0
                      index_3_move = 0 
                      continue
                                


          x += (index_1_count + index_1_move)
          remain.extend([value for i in range(index_1_count)])
          #print("# of index 1 added to remain "+ str(index_1_count))
          index_1_count = index_2_count
          index_1_move = index_2_move
          index_2_count = index_3_count
          index_2_move = index_3_move
          index_3_count = 0
          index_3_move = 0 
          value += 1

      # seq_extract v1.0
      # remain = []
      # remain.extend(hand[0:index])
      # duplicate = []
      # x = index
      # while x < (len(hand)-2):
      #     if(hand[x]//9 == hand[x+2]//9):
      #         while(hand[x] == hand[x+1] or hand[x+1] == hand[x+2]):
      #             if(hand[x] == hand[x+1]):
      #                 hand.count

      #         if(hand[x]+2 == hand[x+1]+1 == hand[x+2]):
      #             x+=3
      #             continue
                  
                  
      #     remain.append(hand[x])
      #     x+=1   
      x += (index_1_move + index_2_move + index_3_move)

      if(x<len(partial_hand)-1):
          remain.append(partial_hand[x+1])
      if(x <= len(partial_hand)-1):
          remain.append(partial_hand[x])
      # print("extract seq:")
      # print(remain)
      return sorted(remain)

  # print tiles that are used in all the possible partitions
  def used_tile(self):
      used_tile_list = {}
      self.efficiency_map = defaultdict(int)
      for key in self.partition:
          for index in self.partition[key]:
              if("middle" in key): 
                  self.efficiency_map[index] +=1
                  self.efficiency_map[index+2] +=1
              elif("two-way" in key):
                  self.efficiency_map[index] +=1
                  self.efficiency_map[index+1] +=1
              else:
                  self.efficiency_map[index] +=1
      print(self.efficiency_map)
      return used_tile_list

  # print tiles that are needed for incomplete sequences 
  def tile_needed(self,input):
      waiting_tile_list = []
      for index in self.partition[input]:
          if("pair" in input or "single" in input):
              # get remaining tile at certain location
              # modify efficiency map value based on remaining tile
              value = self.remaining_tile(index) * 0.1
              self.efficiency_map[str(index)] += value
              waiting_tile_list.append(index)
          if("middle" in input):
              waiting_tile_list.append(index+1)
          if("two-way" in input):
              # can add a condition check to eliminate negative index
              waiting_tile_list.append(index-1)
              waiting_tile_list.append(index+2)
          if("one-way" in input):
              if(index%9==0):
                  waiting_tile_list.append(index+2)
              else:
                  waiting_tile_list.append(index)
      waiting_tile_list.sort()
      return waiting_tile_list

  def partition_dict(self,hand,parti_type):
      return_dict = {}
      if("seq" in parti_type):
          # sequence
          hand_1 = self.seq_extract(hand,0)
          temp_list = self.locate_index(hand,hand_1,True)
          seq_dict = self.inc_seq_extract(hand_1)

          return_dict.setdefault("seq-complete",temp_list)
          return_dict.setdefault("seq-two-way",seq_dict["seq-two-way"])
          return_dict.setdefault("seq-one-way",seq_dict["seq-one-way"])
          return_dict.setdefault("seq-middle",seq_dict["seq-middle"])

          # triplet
          hand_2 = self.tri_extract(hand_1)
          temp_list_2 = self.locate_index(hand_1,hand_2,False)
          return_dict.setdefault("triplet",temp_list_2)

          # pair
          hand_3 = self.pair_extract(hand_2)
          temp_list_3 = self.locate_index(hand_2,hand_3,False)
          return_dict.setdefault("pair",temp_list_3)
          return_dict.setdefault("single",hand_3)

      elif("tri" in parti_type):
          # triplet 
          hand_1 = self.tri_extract(hand)
          temp_list = self.locate_index(hand,hand_1,False)
          return_dict.setdefault("triplet",temp_list)

          # sequence
          hand_2 = self.seq_extract(hand_1,0)
          temp_list_2 = self.locate_index(hand_1,hand_2,True)
          return_dict.setdefault("seq-complete",temp_list_2)

          seq_dict = self.inc_seq_extract(hand_2)
          return_dict.setdefault("seq-two-way",seq_dict["seq-two-way"])
          return_dict.setdefault("seq-one-way",seq_dict["seq-one-way"])
          return_dict.setdefault("seq-middle",seq_dict["seq-middle"])

          # pair
          hand_3 = self.pair_extract(hand_2)
          temp_list_3 = self.locate_index(hand_2,hand_3,False)
          return_dict.setdefault("pair",temp_list_3)
          return_dict.setdefault("single",hand_3)

      else:
          # seven pairs
          hand_1 = self.pair_extract(hand)
          temp_list = self.locate_index(hand,hand_1,False)
          return_dict.setdefault("pair",temp_list)
          return_dict.setdefault("single",hand_1)

      # print(return_dict)
      return return_dict

  def locate_index(self,hand_bef,hand_aft,isSeq):
      return_list = []
      index = 0
      diff = []
      # find the difference
      while index < len(hand_bef):
          value = hand_bef[index]
          count_after = hand_aft.count(value)
          count_before = hand_bef.count(value)
          if(count_after < count_before):
              diff.extend([value for i in range(count_before-count_after)])
              index += count_before
          else:
              index += 1
      
      if(isSeq == False):
          return_list = list(dict.fromkeys(diff))
          return return_list

      # the tile value
      tile = 0
      while tile < 25:
          if (len(diff) == 0):
              break

          num_tile_1 = diff.count(tile)
          if(num_tile_1 == 0):
              tile += 1
              continue
          
          elif(diff.count(tile+1) > 0 and diff.count(tile+2) > 0):
              return_list.append(tile)
              diff.remove(tile)
              diff.remove(tile+1)
              diff.remove(tile+2)

          else:
              tile += 1
      
      return return_list
          
  def inc_seq_extract(self,hand):
      return_dict = {}
      return_dict.setdefault("seq-two-way",[])
      return_dict.setdefault("seq-one-way",[])
      return_dict.setdefault("seq-middle",[])
      x = 0
      while x < 25:
          first_tile = hand.count(x)
          if(first_tile > 0):
              second_tile = 0
              third_tile = 0

              # only valid if the tiles are the same types
              if(x // 9 == (x+1) // 9):
                  second_tile = hand.count(x+1)
              if(x // 9 == (x+2) // 9):
                  third_tile = hand.count(x+2)

              # if there are two consecutive tiles
              if(second_tile > 0):
                  if(x % 9 == 0 or x % 9 == 8):
                      return_dict["seq-one-way"].extend([x]*min(first_tile,second_tile))
                  else:
                      return_dict["seq-two-way"].extend([x]*min(first_tile,second_tile))
                  
                  x += 1

              elif(third_tile > 0):
                  if((x+2) // 9 == (x+3) // 9 and hand.count(x+3) == 0):
                      return_dict["seq-middle"].extend([x]*min(first_tile,third_tile))
                  
                  if(third_tile == 1 and hand.count(x+3) == 0):
                      x += 1
              
          x += 1

      return return_dict