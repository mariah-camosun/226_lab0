#class Board
from Tile import Tile
import random

class Board:
    def __init__(self, size: int, numBarriers: int, numTreasures: int)->None:
        '''
        Creates new board

        :param size: number of tiles per side of board
        :param numBarriers: number of barrier blocks to generate (multiple tiles per block)
        :param numTreasures: number of treasures to generate
        '''
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

    def validateSize(self, size: int)->None:
        '''
        Validates size parameter is an integer > 0 and <= 30
        '''
        if not isinstance(size, int):
            raise TypeError
        elif ( 30 < size <= 0 ):
            raise ValueError
        
    def validateBarrierCount (self, numBarriers: int)->None:
        '''
        Validates numBarriers parameter is an integer > 0, and
        Does not occupy > 20% of the board
        '''
        if not isinstance(numBarriers, int ):
            raise TypeError            
        elif ( numBarriers <= 0 ):
            raise ValueError
        # barriers must be <= 20% of board; each barrier takes (up to) 4 tiles
        elif ( numBarriers*4 > ( self.getTileCount() * .2 ) ):
            raise ValueError

    def validateTreasureCount (self, numTreasures: int)->None:
        '''
        Validates numTreasures parameter is an integer > 0, and
        Does not occupy > 5% of the board
        '''
        if not isinstance(numTreasures, int ):
            raise TypeError
        elif ( numTreasures <= 0 ):
            raise ValueError
        # treasures must be <= 5% of board
        if ( numTreasures > self.getTileCount() * .05 ):
            raise ValueError

    def makeEmptyBoard(self, size):
        # create size x size collection of Tiles; ea empty (initially)
        self.grid = []
        try:
            self.validateSize( size )
        except TypeError:
            print( "size = ", size, " is not an integer")
        except ValueError:
            print( "size must be an integer in [1-30]" )
        else:
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

    def makeBarriers( self, numBarriers: int, boardSize: int )->bool:
        '''
        generate board barriers

        :param numBarriers: number of barrier blocks to make
        :param boardSize: size of 1 side of the board
        :return: bool isValid
        '''         
        try: 
            self.validateBarrierCount(numBarriers)
        except ValueError:
            maxBlocks = (boardSize*boardSize)*.2/4
            if numBarriers <= 0:
                print( "must have at least 1 barrier block, and no more than ", maxBlocks)
            else: 
                print("Too many barriers for board size, at current size, generate no more than ", maxBlocks)
                print("increase board size, or decrease number of barriers")
            return False
        except TypeError:
            print(numBarriers + "is not a number")
            return False
        else:            
            for i in range( numBarriers ): 
                self.makeOneBarrier( boardSize )

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


    def makeTreasures( self, numTreasures, boardSize ):
        '''
        generate board treasures

        :param numTreasures: number of treasures to make
        :param boardSize: size of 1 side of the board
        :return: bool isValid
        '''                    
        try: 
            self.validateTreasureCount(numTreasures)
        except ValueError:
            maxBlocks = (boardSize*boardSize)*.05
            if numTreasures <= 0:
                print( "must have at least 1 treasures, and no more than ", maxBlocks)
            else: 
                print("Too many treasures for board size, at current size, generate no more than ", maxBlocks)
                print("increase board size, or decrease number of treasures")
            return False
        except TypeError:
            print(numTreasures + "is not a number")
            return False
        else:            
            for i in range( numTreasures ):
                self.makeOneTreasure( boardSize )

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