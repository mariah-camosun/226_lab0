#class Board
from Tile import Tile

class Board:
    def __init__(self, size, numBarriers, numTreasures):
        self.size = size
        self.numBarriers = numBarriers
        self.numTreasures = numTreasures
        self.makeEmptyBoard( size )
        self.makeBarriers( numBarriers )
        self.makeTreasures( numTreasures )

    def __str__(self):
        output = ''
        for row in self.grid:
            for tile in row:
                output += tile.__str__()
            output += "\n"
        return output

    def changeBoard(size, numBarriers, numTreasures):
        pass
        # clear old board
        # init new board: Board(size, numBarriers, numTreasures)

    def validateParams_ForEach (noGivenFuncNames):
        pass
        #if invalid param: "ValueError exception" (too many trips this same error)
        #barriers must be <= 20% of board
        #treasures must be <= 5% of board

    def makeEmptyBoard(self, size):
        # create size x size collection of Tiles; ea empty (initially) '_' representation
        row = [Tile()] * size # shallow copies?
        self.grid = [row] * size # shallow copies of array row?
    
    def makeBarriers( self, numBarriers ):
        # create numBarriers - randomly placed 2x2 block, wraps edges of board, 
        # can overlap (but not completely). 'X' rep
        pass

    def makeTreasures( self, numTreasures ):
        # creates numTreasures - randomly placed, on empty tiles. '$' rep
        pass