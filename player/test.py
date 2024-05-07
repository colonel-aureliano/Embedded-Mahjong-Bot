# assume t1 - t9 are 0 - 8
# assume w1 - w9 are 9 - 17
# assume b1 - b9 are 18 - 26
# flowers is 27 - 30
# honors east - white is 31 - 37
# seasons is 38 - 41

from HandPartitioner import HandPartitioner
from Player import Player

def HandPartitionerTest():   
    # test_hands =[  
    #                 [1, 2,  3,  4,  5,  6,  9,  10, 11, 15, 16, 32, 32, 33],
    #                 [0, 2,  3,  4,  5,  6,  9,  10, 11, 15, 16, 32, 32, 33],
    #                 [1, 1,  2,  2,  3,  3,  5,  5,  6,  6,  10, 10, 12, 12],
    #                 [0, 0,  0,  1,  2,  4,  5,  5,  5,  6,  6,  15, 16, 17],
    #                 [1, 2,  3,  5,  5,  5,  6,  6,  6,  14, 15, 16, 19, 19],
    #                 [0, 3,  4,  8,  10, 10, 15, 18, 19, 20, 20, 31, 32, 33],
    #                 [10,10, 10, 11, 11, 11, 12, 12, 12, 13, 13, 13, 33, 31]
    #             ]
    test_hands =[  
        [1, 3 ,2, 14, 14, 25, 26,26,  32,32,32, 33,33,33],
    ]

    agent = HandPartitioner()    

    for i in test_hands:
       print("Testing Hand {}".format(i))
       result = agent.find_patterns(i)
       print(result)

def PlayerTest():
    test_hand = [0, 0, 1, 3, 9, 14, 16, 17, 24, 25, 26, 31, 31, 32]

    agent = Player()
    for tile in test_hand:
      agent.add_tile(tile)
    
    tile = agent.play_tile()
    print(tile)

# HandPartitionerTest()
PlayerTest()