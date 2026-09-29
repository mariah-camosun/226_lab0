#class Board
from Tile import Tile
from Player import Player
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
        self.makeNewPlayer()

    def __str__(self)->str:
        '''
        returns a sting representing the current state of the board

        :return: str, current board state
        '''
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

        :param size: int between [1,30], size of each side of the board (board is size x size)
        '''
        if not isinstance(size, int):
            raise TypeError
        elif ( 30 < size <= 0 ):
            raise ValueError
        
    def validateBarrierCount (self, numBarriers: int)->None:
        '''
        Validates numBarriers parameter is an integer > 0, and
        Does not occupy > 20% of the board

        :param numBarriers: int > 0 and < 20% of board, number of barrier blocks to make
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

        :param numTreasures: int > 0 and < 5% of board, number of treasures to make
        '''
        if not isinstance(numTreasures, int ):
            raise TypeError
        elif ( numTreasures <= 0 ):
            raise ValueError
        # treasures must be <= 5% of board
        if ( numTreasures > self.getTileCount() * .05 ):
            raise ValueError

    def makeEmptyBoard(self, size):
        '''
        make an empty board of size x size tiles
        sets tile count to size**2, clears treasure and barrier counts

        :param size: int > 0 and < 30 that is the number of tiles per side of board
        '''
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

    def getBoard( self )->list[list[Tile]]:
        '''
        returns the 2D array of board tiles

        :return: 2D array of tiles 
        '''
        return self.grid
    
    def getCoordContents( self, x: int, y: int )->Tile:
        '''
        returns tile for a specific 2D array position[y][x]

        :param y: index of row in board array
        :param x: index of tile in row array
        :return: Tile
        '''
        return self.getBoard()[y][x]

    def setTileCount( self, count: int )->None:
        '''
        set tileCount to value count

        :param count: number of tiles in the board
        '''
        self.tileCount = count

    def decrementTreasureCount( self ):
        self.treasureCount -= 1
    
    def setTreasureCount( self, count: int )->None:
        '''
        set treasureCount to value count

        :param count: number of treasures on the board
        '''
        self.treasureCount = count

    def setBarrierCount( self, count: int )->None:
        '''
        set barrierCount to value count

        :param count: number of barrier blocks (not tiles) on the board
        '''        
        self.barrierCount = count

    def getBoardSize( self )->int:
        '''
        get the number of tiles per side of the board
        Note: no setter, as changing would require re-generating the board

        :return: int, number of tiles per side
        '''
        return self.size

    def getTileCount( self )->int:
        '''
        get number of tiles on the board

        :return: number of tiles in the board
        '''        
        return self.tileCount

    def getTreasureCount( self )->int:
        '''
        get number of treasures on the board

        :return: number of treasures on the board
        ''' 
        return self.treasureCount
    
    def getBarrierCount( self )->int:
        '''
        get number of barrier blocks on the board

        :return: number of barrier blocks on the board
        '''         
        return self.barrierCount

    def randomizePosition(self):
        '''
        get a random board position and return tile, if any

        :return: tile instance: Tile, x-coordinate: int, y-coordinate: int
        '''
        #if tile occupied, re-roll
        #if tile@ x, y = empty, return Tur
        # if tile@x,y != empty, return False
        boardSize = self.getBoardSize()
        x = random.randint(0, boardSize-1)
        y = random.randint(0, boardSize-1)
        prevTile = self.getCoordContents( x, y )
        return prevTile, x, y

    def placeInRandomEmpty( self, itemToPlace ):
        '''
        loops until successfully placed in empty tile
        '''
        while True:
            tile, _, _ = self.randomizePosition()
            if tile.getTileContents() == None:
                tile.setTileContents( itemToPlace )
                # place item into contents
                break

            
    # def placeBarrierOrigin( self, tileContents, itemToPlace):
    #     if tileContents == None:
    #         # place
    #     elif tileContents.isOrigin == False:
    #         # place
    #     else: 
    #         reroll

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

    def makeOneBarrier( self, boardSize: int )->None:
        '''
        create 1 'block' of barriers (2x2 tiles) at a random position
        includes check for complete overlap and increments barrierCound on success

        # NOTE realized I can eleminate this parameter wherever it is used
        :param boardsize: int, size of board
        '''
        while(True):
            # x = random.randint(0, boardSize-1)
            # y = random.randint(0, boardSize-1)
            # originTile = self.getCoordContents(x,y)
            originTile, x, y = self.randomizePosition()
            isDuplicate = originTile.setBarrierTile( True )
            if ( not isDuplicate ):
                break

        #once successfull barrier origin, add 1 to barrierCount
        self.setBarrierCount( self.getBarrierCount()+1 )

        # if barrier would overflow an edge, wrap overflow barrier tiles (set coord value = 0)
        if ( x+1 == boardSize ):
            x2 = 0
        else:
            x2 = x+1
        if ( y+1 == boardSize ):
            y2 = 0
        else:
            y2 = y+1

        # add remaining barrier tiles of the 2x2 barrier
        self.getCoordContents(x2,y).setBarrierTile( False )        
        self.getCoordContents(x2,y2).setBarrierTile( False )        
        self.getCoordContents(x,y2).setBarrierTile( False )        

    def makeTreasures( self, numTreasures: int, boardSize: int )->bool:
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

    def makeOneTreasure( self, boardSize: int )->None:
        '''
        create 1 treasure at a random position
        includes check for previous tile contents and increments treasureCount on success

        # NOTE realized I can eleminate boardSize parameter wherever it is used
        :param boardsize: int, size of board
        '''
        while(True):
            x = random.randint(0, boardSize-1)
            y = random.randint(0, boardSize-1)
            treasureTile = self.getCoordContents(x,y)
            isDuplicate = treasureTile.setTreasureTile( 10 )
            if ( not isDuplicate ):
                break

        #once successfull treasure, add 1 to treasureCount
        self.setTreasureCount( self.getTreasureCount() + 1 )

    def makeNewPlayer( self )->Player:
        while True:
            tile, x, y = self.randomizePosition()
            if tile.getTileContents() == None:
                newPlayer = tile.setTileContents( Player( x, y ) )
                # place item into contents
                break


    def collectTreasure( self, tile:Tile, player:Player ):
        tileContents = tile.getTileContents()
        self.addToPlayerScore( tileContents.getValue() )
        tile.clearTile()
        self.decrementTreasureCount()
        print(f"remaining treasures: {self.getTreasureCount()}")
        print(f"player{player.getPlayerNumber()} score: {player.getPlayerScore()}")
        tile.addPlayerToTile( player )
        # print(board)