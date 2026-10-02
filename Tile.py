from Barrier import Barrier
from Treasure import Treasure
from Player import Player

class Tile:
    
    def __init__(self)->None:
        '''
        Initialize a new tile & set contents to empty, symbol to match
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
            self.setTileSymbol( item.get_symbol() )
            return item
        else:
            self.setTileSymbol( "_" )
            return item     
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
    def clear_tile(self)->None:
        '''
        Empty the Contents of the tile & change symbol to empty symbol
        '''
        self.setTileContents( None )
        self.setTileSymbol( '_' )

# Validation and Checks
    def checkTileEmpty(self)->bool:
        '''
        check if the tile is empty

        :return: bool, isEmpty
        '''
        if ( self.getTileContents() == None ):
            return True
        else:
            return False

    def checkTileBarrier(self)->tuple[bool, bool]:
        '''
        check if the tile contains a barrier, and if it is the origin of the barrier block

        :return: tuple[ isBarrier, isBarrierOrigin ]
        '''
        contents = self.getTileContents()
        isBarrier = isinstance( contents, Barrier)
        if isBarrier:
            return True, contents.get_is_origin()
        else:
            return False, False

    def checkTileTreasure(self)->int:
        '''
        Find the value of a treasure. Returns 0 if no treasure.
        
        :return: value of treasure. Value of 0 is no treasure!
        '''
        contents = self.getTileContents()
        isTreasure = isinstance( contents, Treasure)
        if isTreasure:
            return contents.get_value()
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
            self.setTileSymbol( tTile.get_symbol() )
            return False
        else:
            return True

    def setBarrierTile(self, is_origin: bool )->bool: # this methd needs some cleanup
        '''
        Add or change tile contents to Barrier
        Includes checks for previous tile contents

        :param is_origin: is this barrier tile the origin of its barrier block
        :return: bool, isDuplicate - true if tile already contains barrier origin
        '''
        bTile = Barrier( is_origin ) #instanciate barrier
        prevContents = self.getTileContents()

        if ( is_origin == True ) and ( prevContents != None) and ( prevContents.get_is_origin() == True ): 
            # barriers are first non-empy generated. 
            # Contents should only be empty or barrier
            return True
        elif ( is_origin == False ) and ( prevContents != None):
            return False
        else:
            self.setTileContents( bTile )
            self.setTileSymbol( bTile.get_symbol() )
            return False

    def addPlayerToTile( self, player: Player )->None: # NOT properly commented yet - player class still WIP
        '''
        Move player into tile (add player to tile component)

        :param player: Player, the player being moved
        '''
        self.contents = player
        self.symbol = player.get_name()