import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Board import Board
    from Tile import Tile
    from Treasure import Treasure    

class Player:
# Requirements
# [~] 'name' string ( renamed .num to .name; function names left alone )
#       [ ] auto-set, first = 1, increments for ea new player
#       [ ] should probably rename the get/set etc from number to name (not technically a req't)
# [x] row and column coordinates ( renamed xCoord to row, yCoord to column; function names left alone)
# [x] score
# [ ] ValueError if negative
#       [ ] row, column
#       [ ] score
# [ ] ValueError if outside the board boundary
#       [ ] row, column
# [ ] add_score() methd: param: score to be added to existing score
# [ ] get_score() methd: returns curr score
# [ ] move() methd: takes direction 'UDLR' to change player location
#       [ ] if move direction is not possible, nothing should happen
#       [ ] ValueError thrown if direction is invalid
#               [ ] not one of 4 options
#               [ ] if not *possible* but a valid UDLR, no ValueError, just nothing, CONFIRM
# [ ] __str__() methd:

# ~~~ ~~~ while in the 'main, repeatedly' section, look more like move rules ~~~ ~~~
#       [ ] if given tile contains treasure, 
#               [ ] replace treasure with blank
#               [ ] add 1 to the Player's score
#       [ ] if the player would move into a barrier or off the board, do not move

# ~~~ Part C ~~~ 
# general/copy to all [ ] copy reqts to ea class
# [ ] add detailed header comments to ALL methods 
# [ ] make sure ALL instance variables of classes not accessed directly by outside code
# [ ] abv re-perspective. This class does NOT directly access any outside instance variables
#          - eg. bad: board.player.row += 1
#          - instead: board.move('D'), which will in turn call self.player.move('D')

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
        self.incrementPlayerCount()
        self.name = self.getTotalPlayerCount()
        self.symbol = (str)(self.name)
        self.score = 0
        self.row = x
        self.column = y
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

    # Instance Variables: (name, symbol, score, row, column, gameBoard)
    def getPlayerNumber(self):
        return self.name
    # no setPlayerNumber() - only done at init

    def getPlayerSymbol(self):
        return self.symbol
    # no setPlayerSymbol() - only done at init

    def get_score( self ):
        return self.score
    def set_score( self, score ):
        self.score = score

    def get_coords( self ):
        return self.row, self.column
    def set_coords( self, x, y):
        self.row = x
        self.column = y

    def get_board( self ):
        return self.gameBoard
    # no set_board() - only done at init

# Modification of Setters
    @classmethod
    def incrementPlayerCount( cls ):
        cls.playerCount += 1
     
    def add_score( self, addScore ):
        self.score += addScore
        return self.score

# Validation
# [ ] ValueError if negative
#       [ ] row, column
#       [ ] score
# [ ] ValueError if outside the board boundary
#       [ ] row, column
# [ ] ValueError thrown if move() direction is invalid

    def validateDirection( self, direction ):
        if ( direction == "U" or direction == "D" or direction == "L" or direction == "R" ):
            return True
        else:
            raise ValueError

    def validateCoords( self, row:int, column:int)->bool:
        '''
        validates that coordinates (row and column) are both within the valid range (above 0, less than board size)

        :return: bool, isValid for BOTH row and column coordinates
        '''
        boardSize = self.get_board().getBoardSize()
        if ( 0 <= row < boardSize and 0 <= column < boardSize ):
            return True
        else: 
            raise ValueError
        
    # def checkOnBoard( self, x, y )->bool:

# Move
    def getMoveDirection( self ):
        while True:
            direction = input(f"Move player {self.getPlayerSymbol()}: \nEnter a direction (U-up D-down L-left R-right) to move: ")
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
        try:
            areCoordsValid = self.validateCoords( x2, y2 )
        except ValueError as details:
            print(f"Coordinates [{x2},{y2}] are outside the game board")
            return
        
        if ( not self.validateCoords( x2, y2 ) ):
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
                treasure = targetTile.getTileContents()
                treasure.collectTreasure( board, targetTile, self )
            # else empty is only alternative (unspecified), 
            # no movement blocks then Given ALREADY PREVIOUSLY checked in bounds into
            # all successful move intos use the following code hence outside the if block
            targetTile.addPlayerToTile( self )
            self.set_coords( x2, y2 )
            oldTile.clearTile()

