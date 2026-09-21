#class Board
class Board:
    # assuming these are supposed to be class variables
    # size = '' #class variables
    # numBarriers = ''
    # numTreasures = ''
    # looks like probably not supposed to be class variables

    def __init__(self, size, numBarriers, numTreasures):
        self.size = size
        self.numBarriers = numBarriers
        self.numTreasures = numTreasures        

    def changeBoard(size, numBarriers, numTreasures):
        pass
        # clear old board
        # init new board
        # Board(self, size, numBarriers, numTreasures)
        # doesnt like reassinging to self.value
        # nor the self in the abv Board() call

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