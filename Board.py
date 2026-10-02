import random
from Tile import Tile
from typing import TYPE_CHECKING
from Player import Player

class Board:
# TODO
# [ ] fix functions that pass in unneccessary variables (eg. Boardsize)

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
        self.tileCount = 0
        print(f"to make: {size}*{size}, {numBarriers} barriers, {numTreasures} treasures")
        self.makeEmptyBoard()
        self.makeBarriers( numBarriers )
        self.makeTreasures( numTreasures )
        # For now, treating as single entry for simplicity
        # self.players = []
        # self.players.append( self.makeNewPlayer() ) 
        self.players = [self.makeNewPlayer()]

    def __str__(self)->str:
        '''
        returns a sting representing the current state of the board

        :return: str, current board state
        '''
        output = "\n"
        for row in self.grid:
            for tile in row:
                output += tile.__str__()
                output += "  "
            output += "\n"
        output += "\nnum treasures remaining: " + (str)(self.treasureCount) + "\n"
        self.reportPlayerScores()
        return output

# init functions
    def makeEmptyBoard(self):
        '''
        make an empty board of size x size tiles
        sets tile count to size**2, clears treasure and barrier counts
        '''
        # create size x size collection of Tiles; ea empty (initially)
        size = self.getBoardSize()
        self.grid = []
        try:
            self.validateSize( size )
        except TypeError:
            print( "size = ", size, " is not an integer")
        except ValueError:
            print( f"size must be an integer in [1-30]; entered size is {size}" )
        else:
            self.setTileCount( size*size )
            self.setTreasureCount( 0 )
            self.setBarrierCount( 0 )

            for item in range( size ):
                self.grid.append( [ Tile() for _ in range (size) ] )

    def makeBarriers( self, numBarriers: int )->bool:
        '''
        generate board barriers

        :param numBarriers: number of barrier blocks to make
        :return: bool isValid
        '''
        boardSize = self.getBoardSize()
        try: 
            self.validateBarrierCount(numBarriers)
        except ValueError:
            maxBlocks = (boardSize*boardSize)*.2/4
            if numBarriers <= 0:
                print( "must have at least 1 barrier block, and no more than ", maxBlocks)
            else: 
                print(f"{numBarriers} is too many barriers for board size, at current size, generate no more than ", maxBlocks)
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

        # NOTE realized I can eliminate this parameter wherever it is used
        :param boardSize: int, size of board
        '''
        while(True):
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

    def makeTreasures( self, numTreasures: int )->bool:
        '''
        generate board treasures

        :param numTreasures: number of treasures to make
        :return: bool isValid
        '''
        boardSize = self.getBoardSize()               
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
                self.makeOneTreasure()

    def makeOneTreasure( self )->None:
        '''
        create 1 treasure at a random position
        includes check for previous tile contents and increments treasureCount on success
        '''
        boardSize = self.getBoardSize()
        while(True):
            x = random.randint(0, boardSize-1)
            y = random.randint(0, boardSize-1)
            treasureTile = self.getCoordContents(x,y)
            isDuplicate = treasureTile.setTreasureTile( 1 )
            if ( not isDuplicate ):
                break

        #once successfull treasure, add 1 to treasureCount
        self.setTreasureCount( self.get_treasure_count() + 1 )

    def makeNewPlayer( self )->Player:
        '''
        creates a new player and places it on a random empty tile

        :return: Player, the new player
        '''
        '''
        creates a new player and places it on a random empty tile

        :return: Player, the new player
        '''
        while True:
            tile, column, row = self.randomizePosition()
            if tile.getTileContents() == None:
                # place new player instance into contents
                newPlayer = tile.setTileContents( Player( column, row, self ) )
                return newPlayer

# Setters and Getters
    def getBoard( self )->list[list[Tile]]:
        '''
        returns the 2D array of board tiles

        :return: 2D array of tiles 
        '''
        return self.grid
    # no set_board() - instead, makeEmptyBoard()

    def getBoardSize( self )->int:
        '''
        get the number of tiles per side of the board
        Note: no setter, as changing would require re-generating the board

        :return: int, number of tiles per side
        '''
        return self.size    
    # no set_board_size() - only done at init

    def getCoordContents( self, column: int, row: int )->Tile:
        '''
        returns tile for a specific 2D array position[row][column]

        :param row: index of row in board array
        :param column: index of tile in row array
        :return: Tile
        '''
        if self.checkOnBoard( column,row ):
            return self.getBoard()[row][column]
    # no set_coord_contents() - only done at init

    def getPlayers( self )->list[Player]:
        '''
        returns all current players as a list

        :return: list[Player], list of all current players
        '''
        output = "Current players: "
        for player in self.players:
            output += (str)(player)
            output += ','
        print(output)
        return self.players
    #no set_players() - instead, makeNewPlayer()

    def getTileCount( self )->int:
        '''
        get number of tiles on the board

        :return: number of tiles in the board
        '''        
        return self.tileCount
    def setTileCount( self, count: int )->None:
        '''
        set tileCount to value count

        :param count: number of tiles in the board
        '''
        self.tileCount = count

    def get_treasure_count( self )->int:
        '''
        get number of treasures on the board

        :return: number of treasures on the board
        ''' 
        return self.treasureCount
    def setTreasureCount( self, count: int )->None:
        '''
        set treasureCount to value count

        :param count: number of treasures on the board
        '''
        self.treasureCount = count

    def getBarrierCount( self )->int:
        '''
        get number of barrier blocks on the board

        :return: number of barrier blocks on the board
        '''         
        return self.barrierCount
    def setBarrierCount( self, count: int )->None:
        '''
        set barrierCount to value count

        :param count: number of barrier blocks (not tiles) on the board
        '''        
        self.barrierCount = count

# expanded setters
    def decrement_treasure_count( self ):
        self.treasureCount -= 1

    def randomizePosition(self):
        '''
        get a random board position and return tile, if any

        :return: tile instance: Tile, x-coordinate: int, y-coordinate: int
        '''
        boardSize = self.getBoardSize()
        column = random.randint(0, boardSize-1)
        row = random.randint(0, boardSize-1)
        prevTile = self.getCoordContents( column, row )
        return prevTile, column, row

    def placeInRandomEmpty( self, itemToPlace ):
        '''
        Places an item in a random empty tile. Loops until successfully placed.

        :param itemToPlace: item to place into the game Tile. Acceptable classes: Player, Barrier, Treasure
        Places an item in a random empty tile. Loops until successfully placed.

        :param itemToPlace: item to place into the game Tile. Acceptable classes: Player, Barrier, Treasure
        '''
        while True:
            tile, _, _ = self.randomizePosition()
            if tile.getTileContents() == None:
                tile.setTileContents( itemToPlace )
                break

# Validation and checks
    def validateSize(self, size: int)->bool:
        '''
        Validates size parameter for the game board is an integer > 0 and <= 30
        Validates size parameter for the game board is an integer > 0 and <= 30

        :param size: int between [1,30], size of each side of the board (board is size x size)
        :return: bool, isValid
        :return: bool, isValid
        '''
        if not isinstance(size, int):
            raise TypeError
        elif ( not( 0 < size <= 30) ):
            raise ValueError
        else:
            return True
        
    def validateBarrierCount (self, numBarriers: int)->bool:
        '''
        Validates numBarriers parameter is an integer > 0, and
        Does not occupy > 20% of the board

        :param numBarriers: int > 0 and < 20% of board, number of barrier blocks to make
        :return: bool, isValid
        :return: bool, isValid
        '''
        if not isinstance(numBarriers, int ):
            raise TypeError            
        elif ( numBarriers <= 0 ):
            raise ValueError
        # barriers must be <= 20% of board; each barrier takes (up to) 4 tiles
        elif ( numBarriers*4 > ( self.getTileCount() * .2 ) ):
            raise ValueError
        else:
            return True

    def validateTreasureCount (self, numTreasures: int)->bool:
        '''
        Validates numTreasures parameter is an integer > 0, and
        Does not occupy > 5% of the board

        :param numTreasures: int > 0 and < 5% of board, number of treasures to make
        :return: bool, isValid
        :return: bool, isValid
        '''
        if not isinstance(numTreasures, int ):
            raise TypeError
        elif ( numTreasures <= 0 ):
            raise ValueError
        # treasures must be <= 5% of board
        elif ( numTreasures > self.getTileCount() * .05 ):
            raise ValueError
        else:
            return True

    def checkOnBoard( self, column, row )->bool:
        '''
        checks if coordinates are within the gameboard


        :return: bool, isOnGameboard
        '''
        if ( 0 <= column < self.getBoardSize() and 0 <= row < self.getBoardSize() ):
            return True        
        else:
            return False

# Utility
    def reportPlayerScores(self):
        '''
        prints out the current player scores for all players
        '''
        '''
        prints out the current player scores for all players
        '''
        players = self.getPlayers()
        for player in players:
            print(f"player {player.get_name()}: score: {player.get_score()}")