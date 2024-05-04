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
        [1, 3 , 14, 14, 25, 26,26,  32,32,32,33,33,33],
    ]

    agent = HandPartitioner()
    for i in test_hands:
        print("Testing Hand {}".format(i))
        print("Seq Part {}".format(agent.partition_dict(i,'seq')))
        print("Tri Part {}".format(agent.partition_dict(i,'tri')))

def PlayerTest():
    # test_hand = [1, 2, 3, 9, 14, 14, 25, 26, 26, 32, 32, 32 ,33, 33]
    test_hand = [1, 2, 3, 9, 10, 11, 25, 26, 26, 32, 32, 32 ,33, 33]

    agent = Player()
    for tile in test_hand:
      agent.add_tile(tile)
    
    tile = agent.play_tile()
    print(tile)

# HandPartitionerTest()
PlayerTest()