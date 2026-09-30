from Barrier import Barrier
from Treasure import Treasure
from Player import Player

class Tile:
# Requirements    
# [x] keeps track of own contents

# ~~~ Part C ~~~ 
# general/copy to all [ ] copy reqts to ea class
# [ ] add detailed header comments to ALL methods 
# [ ] make sure ALL instance variables of classes not accessed directly by outside code
# [ ] abv re-perspective. This class does NOT directly access any outside instance variables
#          - eg. bad: board.player.row += 1
#          - instead: board.move('D'), which will in turn call self.player.move('D')
    def __init__(self)->None:
        '''
        initialize a new tile & set contents to empty, symbol to match
        '''
        self.setTileContents( None )
        self.setTileSymbol( '_' )

    def __str__(self)->str:
        '''
        Display the (symbol of) Contents of the tile.
        :return self.symbol: str, symbol for the tile instance
        '''
        return f'{ self.getTileSymbol() }'

# Getters & Setters
    # No Class Variables
    # Instance Variables ( contents, symbol )
    def setTileContents( self, item )->None: #HOW TO HINT? should be one of a list of custom classes
        '''
        set the contents of the tile
        includes subsequent symbol change
        :param item: set to a barrier, treasure, or player instance
        '''
        self.contents = item
        if item != None:
            self.setTileSymbol( item.symbol )
            return item
        else:
            self.setTileSymbol( "_" )
            return item     
        # match type(item):
        #     case Treasure:
        #         self.setTreasureTile( 1 )
        #     case Barrier:
    def getTileContents( self ): #HOW TO HINT? as abv meth'd
        '''
        get the item contained in the tile
        :return: the item in 'self.contents' the barrier, treasure, player instance, or if empty, None
        '''
        return self.contents

    def setTileSymbol(self, symbol: str)->None:
        '''
        set the symbol for the tile
        :param symbol: str, symbol for the tile.
        '''
        self.symbol = symbol
    def getTileSymbol( self )->str:
        '''
        get the symbol for the tile
        :return: str, symbol to display for the tile
        '''
        return self.symbol

# expanded setters
    def clearTile(self)->None:
        '''
        Empty the Contents of the tile & change symbol to empty symbol
        '''
        self.setTileContents( None )
        self.setTileSymbol( '_' )

# Validation and Checks
    def checkTileEmpty(self)->bool:
        if ( self.getTileContents() == None ):
            return True
        else:
            return False

    def checkTileBarrier(self)->tuple[bool, bool]:
        '''
        :return: tuple[ isBarrier, isBarrierOrigin ]
        '''
        contents = self.getTileContents()
        isBarrier = isinstance( contents, Barrier)
        if isBarrier:
            return True, contents.getIsOrigin()
        else:
            return False, False

    def checkTileTreasure(self)->int:
        '''
        :return: value of treasure. Value of 0 is no treasure!
        '''
        contents = self.getTileContents()
        isTreasure = isinstance( contents, Treasure)
        if isTreasure:
            return contents.getValue()
        else:
            return 0

    def setTreasureTile( self, treasureValue: int )->bool:
        '''
        Add or change tile contents to Treasure
        Includes checks for previous tile contents
        :param treasureValue: the point value for the treasure item
        :return: bool, isBlocked - true if tile already full
        '''
        isEmpty = self.checkTileEmpty()
        if ( isEmpty ):
            tTile = Treasure( treasureValue )
            self.setTileContents( tTile )
            self.setTileSymbol( tTile.getSymbol() )
            return False
        else:
            return True

    def setBarrierTile(self, isOrigin: bool )->bool: # this methd needs some cleanup
        '''
        Add or change tile contents to Barrier
        Includes checks for previous tile contents
        :param isOrigin: is this barrier tile the origin of its barrier block
        :return: bool, isDuplicate - true if tile already contains barrier origin
        '''
        bTile = Barrier( isOrigin ) #instanciate barrier
        prevContents = self.getTileContents()
        # rework if statement for less duplication

        if ( isOrigin == True ):
            if ( prevContents != None):
                # barriers are first non-empy generated. 
                # Contents should only be empty or barrier
                if ( prevContents.getIsOrigin() == True ): 
                    # print("duplicate barrier")
                    return True
                else:
                    self.setTileContents( bTile )
                    self.setTileSymbol( bTile.getSymbol() )
                    return False
            else:
                self.setTileContents( bTile )
                self.setTileSymbol( bTile.getSymbol() )
                return False
        elif (self.contents == None):
            self.setTileContents( bTile )
            self.setTileSymbol( bTile.getSymbol() )
            return False
        else:
            return False

    def addPlayerToTile( self, player: Player ): # NOT properly commented yet - player class still WIP
        '''
        Move player into tile (add player to tile component)
        '''
        self.contents = player
        self.symbol = player.num
        # do checks go here or in the board?
        # if tile = barrier, cannot place here
        # if tile = treasure, add points, change contents to player
        # if tile = other player ??? treat like barrier?
        # pass