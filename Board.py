#class Board
from Tile import Tile
import random

class Board:
    def __init__(self, size, numBarriers, numTreasures):
        self.size = size
        self.numBarriers = numBarriers
        self.numTreasures = numTreasures
        self.makeEmptyBoard( size )
        self.makeBarriers( numBarriers, size )
        self.makeTreasures( numTreasures, size )

    def __str__(self):
        output = ''
        for row in self.grid:
            for tile in row:
                output += tile.__str__()
                output += "  "
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
        self.grid = []
        for item in range( size ):
            self.grid.append( [ Tile() for _ in range (size) ] )
    
    def makeBarriers( self, numBarriers, BoardSize ):
        self.makeOneBarrier( BoardSize )

    def makeOneBarrier( self, BoardSize ):
        x = random.randint(0, BoardSize-1)
        y = random.randint(0, BoardSize-1)
        self.grid[y][x].addBarrierToTile( True )        
        self.grid[y+1][x].addBarrierToTile( False )        
        self.grid[y][x+1].addBarrierToTile( False )        
        self.grid[y+1][x+1].addBarrierToTile( False )
        # create numBarriers - randomly placed 2x2 block, wraps edges of board, 
        # can overlap (but not completely). 'X' rep

    def makeTreasures( self, numTreasures, BoardSize ):
        self.makeOneTreasure( BoardSize )

    def makeOneTreasure( self, BoardSize ):
        x = random.randint(0, BoardSize-1)
        y = random.randint(0, BoardSize-1)
        self.grid[y][x].addTreasureToTile( 10 )
        # creates numTreasures - randomly placed, on empty tiles. '$' rep