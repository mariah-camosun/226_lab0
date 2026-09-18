#class Board

#param size
#param numBarriers
#param numTreasures

#validate params (no given funcNames)
    #if invalid param: "ValueError exception" (too many trips this same error)
    #barriers must be <= 20% of board
    #treasures must be <= 5% of board

#create size x size collection of Tiles; ea empty (initially) '_' representation
#create numBarriers - randomly placed 2x2 block, wraps edges of board, can overlap (but not completely). 'X' rep
#creates numTreasures - randomly placed, on empty tiles. '$' rep