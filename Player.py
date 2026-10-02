from __future__ import annotations
import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Board import Board
    from Tile import Tile
    from Treasure import Treasure    

class Player:
# TODO
# [ ] should probably rename the get/set etc from number to name (not technically a req't)

    playerCount = 0

    def __init__(self, column:int, row:int, gameBoard)->None:
        '''
        create a new Player instance

        :param column: int, the x-position of the player
        :param row: int, the y-position of the player
        :param gameBoard: the gameboard the player is on
        '''
        self.incrementPlayerCount()
        self.name = self.getTotalPlayerCount()
        self.symbol = (str)(self.name)
        self.score = 0
        self.row = row
        self.column = column
        self.gameBoard = gameBoard
        # type(self).incrementPlayerCount()

    def __str__(self)->str:
        '''
        returns the symbol (number) for the player instance

        :return: str, player symbol (number)
        '''
        return f'{self.symbol}'

# Getters & Setters
    # Class variables: (player count)
    @classmethod
    def getTotalPlayerCount( cls )->int:
        '''
        returns the total number of players

        :return: int, number of players
        '''
        return cls.playerCount
    @classmethod
    def setTotalPlayerCount( cls, count:int )->None:
        '''
        sets the player count to the number passed in

        :param count: int, number of current players
        '''
        cls.playerCount = count

    # Instance Variables: (name, symbol, score, column, row, gameBoard)
    def getPlayerNumber(self)->int:
        '''
        returns the name of this player instance

        :return: str, player name
        '''
        return self.name
    # no setPlayerNumber() - only done at init

    def getPlayerSymbol(self)->str:
        '''
        returns the symbol of this player's instance

        :return: str, player symbol
        '''
        return self.symbol
    # no setPlayerSymbol() - only done at init
    def getSymbol(self)->str: # temporarily have both until all refs fixed
        '''
        returns the symbol of this player's instance

        :return: str, player symbol
        '''        
        return self.symbol

    def get_score( self )->int:
        '''
        returns the current score for this player instance

        :return: int, player score
        '''        
        return self.score
    def set_score( self, score:int ):
        '''
        changes this player's score to the number passed in

        :param score: int, new player score        
        '''
        self.score = score

    def get_coords( self )->tuple[int, int]:
        '''
        returns the current gameboard coordinates of this player

        :return: tupple[int, int], column coordiante, row coordinate
        '''
        return self.column, self.row
    def set_coords( self, column:int, row:int)->None:
        '''
        sets the values for player coordinates to the given column and row

        :param column: int, x-position of player
        :param row: int, y-position of player
        '''
        self.column = column
        self.row = row

    def get_board( self )->list[list[Tile]]:
        '''
        returns the gameboard the player is on

        :return: list[list[Tile]], the gameboard containing the player
        '''
        return self.gameBoard
    # no set_board() - only done at init

# Extended Setters
    @classmethod
    def incrementPlayerCount( cls )->None:
        '''
        icreases the player count by 1
        '''        
        cls.playerCount += 1
     
    def add_score( self, addScore:int )->int:
        '''
        adds addScore to this player's score and returns updated score

        :param addScore: int, points to add to player score
        :return: int, player score after update
        '''
        self.score += addScore
        return self.score

# Validation
    def validateDirection( self, direction: str )->bool:
        '''
        validates the entered string is allowed

        :param direction: str, direction to move the player in
        :return: bool, isValid
        '''
        if ( direction == "U" or direction == "D" or direction == "L" or direction == "R" ):
            return True
        else:
            raise ValueError

    def validateCoords( self, row:int, column:int)->bool:
        '''
        validates that coordinates (row and column) are both within the valid range (>= 0, < board size)

        :return: bool, isValid for BOTH row and column coordinates
        '''
        boardSize = self.get_board().getBoardSize()
        if ( 0 <= row < boardSize and 0 <= column < boardSize ):
            return True
        else: 
            raise ValueError

# Move
    def getMoveDirection( self )->str:
        '''
        Prompt user for direction to move in and check for validity

        :return: str, direction to move
        '''
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

    def move( self )->None: # direction not a param, as includes user prompt
        '''
        Move the current player instance. Includes prompting and validation.
        Checks contents of target tile, and moves or not as appropriate.
        '''
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