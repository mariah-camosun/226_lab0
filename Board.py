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
        output += "\n num tiles: " + (str)(self.tileCount) + " num barriers: " + (str)(self.barrierCount) + " num treasures: " + (str)(self.treasureCount) + "\n"
        return output

    def changeBoard(size, numBarriers, numTreasures):
        pass
        # clear old board
        # init new board: Board(size, numBarriers, numTreasures)

    def validateSize(self, size):
        if not isinstance(size, int):
            raise TypeError
        
    def validateBarrierCount (self, numBarriers):
        if not isinstance(numBarriers, int ):
            raise TypeError            
        # barriers must be <= 20% of board; each barrier takes (up to) 4 tiles
        if ( numBarriers*4 > ( self.getTileCount() * .2 ) ):
            raise ValueError

    def validateTreasureCount (self, numTreasures):
        if not isinstance(numTreasures, int ):
            raise TypeError
        # treasures must be <= 5% of board
        if ( numTreasures > self.getTileCount() * .05 ):
            raise ValueError

    def makeEmptyBoard(self, size):
        # create size x size collection of Tiles; ea empty (initially)
        self.grid = []
        # self.validateSize( size )
        self.setTileCount( size*size )
        self.setTreasureCount( 0 )
        self.setBarrierCount( 0 )

        for item in range( size ):
            self.grid.append( [ Tile() for _ in range (size) ] )

    def getBoard( self ):
        return self.grid
    def getCoordContents( self, x: int, y: int )->Tile:
        return self.getBoard()[y][x]

    def setTileCount( self, count ):
        self.tileCount = count
    def setTreasureCount( self, count ):
        self.treasureCount = count
    def setBarrierCount( self, count ):
        self.barrierCount = count

    def getTileCount( self ):
        return self.tileCount
    def getTreasureCount( self ):
        return self.treasureCount
    def getBarrierCount( self ):
        return self.barrierCount

    def makeBarriers( self, numBarriers, BoardSize ):
        try: 
            self.validateBarrierCount(numBarriers)
        except ValueError:
            print("Too many barriers for board size")
            print("increase board size, or decrease number of barriers")
            return False
        except TypeError:
            print(numBarriers + "is not a number")
            return False
        else:            
            for i in range( numBarriers ): 
                self.makeOneBarrier( BoardSize )

    def makeOneBarrier( self, BoardSize ):
        # if barrier would completely overlap another barrier, re-generate coords
        # create numBarriers - randomly placed 2x2 block, wraps edges of board, 
        # can overlap (but not completely). 'X' rep
        while(True):
            x = random.randint(0, BoardSize-1)
            y = random.randint(0, BoardSize-1)
            originTile = self.getCoordContents(x,y)
            isDuplicate = originTile.setBarrierTile( True )
            if ( not isDuplicate ):
                break

        #once successfull barrier origin, add 1 to barrierCount
        self.setBarrierCount( self.getBarrierCount()+1 )

        # if barrier would overflow an edge, wrap overflow barrier tiles (set coord value = 0)
        if ( x+1 == BoardSize ):
            x2 = 0
        else:
            x2 = x+1
        if ( y+1 == BoardSize ):
            y2 = 0
        else:
            y2 = y+1

        # add remaining barrier tiles of the 2x2 barrier
        self.getCoordContents(x2,y).setBarrierTile( False )        
        self.getCoordContents(x2,y2).setBarrierTile( False )        
        self.getCoordContents(x,y2).setBarrierTile( False )        


    def makeTreasures( self, numTreasures, BoardSize ):
        try: 
            self.validateTreasureCount(numTreasures)
        except ValueError:
            print("Too many treasures for board size")
            print("increase board size, or decrease number of treasures")
            return False
        except TypeError:
            print(numTreasures + "is not a number")
            return False
        else:            
            for i in range( numTreasures ):
                self.makeOneTreasure( BoardSize )

    def makeOneTreasure( self, BoardSize ):
        # creates numTreasures - randomly placed, on empty tiles. '$' rep
        while(True):
            x = random.randint(0, BoardSize-1)
            y = random.randint(0, BoardSize-1)
            treasureTile = self.getCoordContents(x,y)
            isDuplicate = treasureTile.setTreasureTile( 10 )
            if ( not isDuplicate ):
                break

        #once successfull treasure, add 1 to treasureCount
        self.setTreasureCount( self.getTreasureCount() + 1 )