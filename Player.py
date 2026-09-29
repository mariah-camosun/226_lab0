import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Board import Board
    

class Player:
    playerCount = 0
    # [ ] auto-increment name as player number
    # [x] contain coors of player
    # [~] contains player score
    # [x] __str__ methd
    # [x] add_score method, 
    # [x] get_score methods
    # [ ] move methd, takes a dir (UDLR) to chg player location if poss (otherwise ignored)
    # [ ] value error on: row, col, score negative; row col outside board
    def __init__(self, x, y, gameBoard):
        self.num = 1 # TO BE auto-incremented, for now this will hold place
        self.symbol = (str)(self.num)
        print(f"player number {self.symbol} created")
        self.score = 0
        self.xCoord = x
        self.yCoord = y
        print(f"player coords: {x}, {y}.")
        self.gameBoard = gameBoard
        type(self).incrementPlayerCount()

    def __str__(self):
        return f'{self.symbol}'

# Getters & Setters
    # Class variables: (player count)
    @classmethod
    def incrementPlayerCount( cls ):
        cls.playerCount += 1

    @classmethod
    def getTotalPlayerCount( cls ):
        return cls.playerCount

    @classmethod
    def setTotalPlayerCount( cls, count ):
        cls.playerCount = count

    # 
    def getPlayerNumber(self):
        return self.num

    def get_score( self ):
        return self.score
    
    def add_score( self, addScore ):
        score = self.get_score()
        score += addScore
        return score

    def get_coords( self ):
        return self.xCoord, self.yCoord

    def get_board( self ):
        return self.gameBoard
    
    def move( self ): # direction not a param, as includes user prompt
        from Treasure import Treasure
        direction = input("Enter a direction (U-up D-down L-left R-right) to move")
        direction = direction.upper()
        isValid = self.validateDirection( direction )
        if isValid==True:
            board = self.get_board()
            x,y = self.get_coords()
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
            prevTile = board.getCoordContents( x,y )
            targetTile = board.getCoordContents( x2,y2 )
            targetContents = targetTile.getTileContents()
            if ( targetContents == None ):
                targetTile.addPlayerToTile( self )
                prevTile.clearTile()
            elif ( isinstance(targetContents, Treasure) ):
                treasureValue = targetContents.getValue()
                self.add_score( treasureValue )
                targetTile.addPlayerToTile( self )
                prevTile.clearTile()
            # print(board)

    def validateDirection( self, direction ):
        if not isinstance( direction, str ):
            raise TypeError
        elif ( direction == "U" or direction == "D" or direction == "L" or direction == "R" ):
            return True
        else:
            raise ValueError