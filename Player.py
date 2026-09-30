import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Board import Board
    from Tile import Tile
    from Treasure import Treasure    

class Player:
    playerCount = 0
    # [ ] auto-increment name as player number
    # [x] contain coors of player
    # [~] contains player score
    # [x] __str__ methd
    # [x] add_score method, 
    # [x] get_score methods
    # [~] move methd, takes a dir (UDLR) to chg player location if poss (otherwise ignored)
    #       [~] fix: collect treasure properly
    # [ ] value error on: row, col, score negative; row col outside board
    def __init__(self, x, y, gameBoard):
        self.num = 1 # TO BE auto-incremented, for now this will hold place
        self.symbol = (str)(self.num)
        self.score = 0
        self.xCoord = x
        self.yCoord = y
        self.gameBoard = gameBoard
        type(self).incrementPlayerCount()

    def __str__(self):
        return f'{self.symbol}'

# Getters & Setters
    # Class variables: (player count)
    @classmethod
    def getTotalPlayerCount( cls ):
        return cls.playerCount
    @classmethod
    def setTotalPlayerCount( cls, count ):
        cls.playerCount = count

    # Instance Variables: (num, symbol, score, xCoord, yCoord, gameBoard)
    def getPlayerNumber(self):
        return self.num
    # no setPlayerNumber() - only done at init

    def getPlayerSymbol(self):
        return self.symbol
    # no setPlayerSymbol() - only done at init

    def get_score( self ):
        return self.score
    def set_score( self, score ):
        self.score = score

    def get_coords( self ):
        return self.xCoord, self.yCoord
    def set_coords( self, x, y):
        self.xCoord = x
        self.yCoord = y

    def get_board( self ):
        return self.gameBoard
    # no set_board() - only done at init

# Modification of Setters
    @classmethod
    def incrementPlayerCount( cls ):
        cls.playerCount += 1
     
    def add_score( self, addScore ):
        score = self.get_score()
        score += addScore
        return score

# Validation
    def validateDirection( self, direction ):
        if not isinstance( direction, str ):
            raise TypeError
        elif ( direction == "U" or direction == "D" or direction == "L" or direction == "R" ):
            return True
        else:
            raise ValueError

# Move
    def getMoveDirection( self ):
        while True:
            direction = input("Enter a direction (U-up D-down L-left R-right) to move: ")
            direction = direction.upper()
            print(f"direction value entered: {direction}")

            try:
                isValid = self.validateDirection( direction )
            except TypeError as details:
                print(f"{direction} is not a string, must enter one of U, D, L, R") # will also accept lower case
            except ValueError as details:
                print(f"{direction} is not a valid option. Choose one of: U, D, L, R") # will also accept lower case
            else:
                return direction

    def move( self ): # direction not a param, as includes user prompt
        direction = self.getMoveDirection() # direction moving

        board = self.get_board()
        x,y = self.get_coords() # coordinates of initial position
        oldTile = board.getCoordContents( x,y ) # initial position tile

        match direction:
            case "D":
                x2 = x
                y2 = y + 1
            case "U":
                x2 = x
                y2 = y - 1
            case "L":
                x2 = x - 1
                y2 = y
            case "R":
                x2 = x + 1
                y2 = y

        # if x2 or y2 are outside the gameboard bounds, return, otherwise continue checking
        if ( not board.checkOnBoard( x2, y2 ) ):
            return
        else:
            targetTile = board.getCoordContents( x2,y2 ) # tile to move to
            isBarrier, _ = targetTile.checkTileBarrier()
            isTreasure = targetTile.checkTileTreasure()
            if isBarrier: 
            # or targetTile.checkTilePlayer(): #Second check doesnt actually exist yet
                print(f"entered tile is barrier or player: {targetTile.getTileContents()}")
                return
            elif ( isTreasure ): # 0 evals to false, 
                # Board.collectTreasure()
                treasure = targetTile.getTileContents()
                treasure.collectTreasure( board, targetTile, self )
                # treasureValue = targetTile.getTileContents().getValue()
                # self.add_score( treasureValue )
            # else empty is only alternative (unspecified), 
            # no movement blocks then Given ALREADY PREVIOUSLY checked in bounds into
            # all successful move intos use the following code hence outside the if block
            targetTile.addPlayerToTile( self )
            self.set_coords( x2, y2 )
            oldTile.clearTile()

