#class Board
class Board:
    # assuming these are supposed to be class variables
    # param size
    # param numBarriers
    # param numTreasures
    size = '' #class variables
    numBarriers = ''
    numTreasures = ''

    def __init__(self):
        self.value = 10 #instance variable

    def changeBoard(size, numBarriers, numTreasures):
        Board.size = size
        Board.numBarriers = numBarriers
        Board.numTreasures = numTreasures

    #validate params (no given funcNames)
        #if invalid param: "ValueError exception" (too many trips this same error)
        #barriers must be <= 20% of board
        #treasures must be <= 5% of board

    def makeBoard():
        Board.makeEmptyBoard()
        Board.makeBarriers()
        Board.makeTreasures()

    def makeEmptyBoard():
        # create size x size collection of Tiles; ea empty (initially) '_' representation
        # Board.size x Board.size
        print('')
    
    def makeBarriers():
        # create numBarriers - randomly placed 2x2 block, wraps edges of board, can overlap (but not completely). 'X' rep
        # Board.numBarriers
        print('')

    def makeTreasures():
        # creates numTreasures - randomly placed, on empty tiles. '$' rep
        # Board.numTreasures
        print('')