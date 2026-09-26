from Barrier import Barrier
from Treasure import Treasure
from Player import Player

class Tile:
#keeps track of own contents
    def __init__(self):
        self.setTileContents( None )
        self.setTileSymbol( '_' )

    def __str__(self):
        '''
        Display the (symbol of) Contents of the tile.
        :return tile symbol: self.symbol of the instance
        '''
        return f'{ self.getTileSymbol() }'

    def setTileContents( self, item ):
        self.contents = item

    def getTileContents( self ):
        return self.contents

    def setTileSymbol(self, symbol):
        self.symbol = symbol

    def getTileSymbol( self ):
        return self.symbol

    def clearTile(self):
        '''
        Empty the Contents of the tile & change symbol to empty symbol
        '''
        self.setTileContents( None )
        self.setTileSymbol( '_' )

    def setTreasureTile( self, treasureValue: int )->bool:
        '''
        Add or change tile contents to Treasure
        Includes checks for previous tile contents
        :return: bool, isDuplicate
        '''
        if ( self.getTileContents() == None ):
            tTile = Treasure( treasureValue )
            self.setTileContents( tTile )
            self.setTileSymbol( tTile.getSymbol() )
            return False
        else:
            return True

    def setBarrierTile(self, isOrigin: bool ):
        '''
        Add or change tile contents to Barrier
        Includes checks for previous tile contents
        :return: bool, isDuplicate
        '''
        bTile = Barrier( isOrigin )
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

    def addPlayerToTile( player: Player ):
        '''
        Move player into tile (add player to tile component)
        '''
        self.contents = player
        self.symbol = player.number
        # do checks go here or in the board?
        # if tile = barrier, cannot place here
        # if tile = treasure, add points, change contents to player
        # if tile = other player ??? treat like barrier?
        pass