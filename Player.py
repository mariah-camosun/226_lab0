import random

class Player:
    playerCount = 0
    # auto-increment name as player number
    # contain coors of player
    # contains player score
    # __str__ methd
    # add_score, get_score methods
    # move methd, takes a dir (UDLR) to chg player location if poss (otherwise ignored)
    # value error on: row, col, score negative; row col outside board
    def __init__(self, x, y):
        self.num = 1 # TO BE auto-incremented, for now this will hold place
        self.symbol = (str)(self.num)
        print(f"player number {self.symbol} created")
        self.score = 0
        self.xCoord = x
        self.yCoord = y
        print(f"player coords: {x}, {y}.")

    def __str__(self):
        return f'{self.symbol}'

    def getPlayerNumber(self):
        return self.num



    def incrementPlayerCount( cls ):
        cls.playerCount += 1

    def getTotalPlayerCount( cls ):
        return cls.playerCount

    def setTotalPlayerCount( cls, count ):
        cls.playerCount = count


    # def makeTreasures( self, numTreasures: int, boardSize: int )->bool:
    #     '''
    #     generate board treasures

    #     :param numTreasures: number of treasures to make
    #     :param boardSize: size of 1 side of the board
    #     :return: bool isValid
    #     '''                    
    #     try: 
    #         self.validateTreasureCount(numTreasures)
    #     except ValueError:
    #         maxBlocks = (boardSize*boardSize)*.05
    #         if numTreasures <= 0:
    #             print( "must have at least 1 treasures, and no more than ", maxBlocks)
    #         else: 
    #             print("Too many treasures for board size, at current size, generate no more than ", maxBlocks)
    #             print("increase board size, or decrease number of treasures")
    #         return False
    #     except TypeError:
    #         print(numTreasures + "is not a number")
    #         return False
    #     else:            
    #         for i in range( numTreasures ):
    #             self.makeOneTreasure( boardSize )

    # def makeOneTreasure( self, boardSize: int )->None:
    #     '''
    #     create 1 treasure at a random position
    #     includes check for previous tile contents and increments treasureCount on success

    #     # NOTE realized I can eleminate boardSize parameter wherever it is used
    #     :param boardsize: int, size of board
    #     '''
    #     while(True):
            
    #         y = random.randint(0, boardSize-1)
    #         treasureTile = self.getCoordContents(x,y)
    #         isDuplicate = treasureTile.setTreasureTile( 10 )
    #         if ( not isDuplicate ):
    #             break

    #     #once successfull treasure, add 1 to treasureCount
    #     self.setTreasureCount( self.getTreasureCount() + 1 )        
    # def setTreasureTile( self, treasureValue: int )->bool:
    #     '''
    #     Add or change tile contents to Treasure
    #     Includes checks for previous tile contents
    #     :param treasureValue: the point value for the treasure item
    #     :return: bool, isBlocked - true if tile already full
    #     '''
    #     if ( self.getTileContents() == None ):
    #         tTile = Treasure( treasureValue )
    #         self.setTileContents( tTile )
    #         self.setTileSymbol( tTile.getSymbol() )
    #         return False
    #     else:
    #         return True
