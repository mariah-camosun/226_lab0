from Barrier import Barrier
from Treasure import Treasure
from Player import Player

class Tile:
#keeps track of own contents
    def __init__(self):
        self.contents = None
        self.symbol = '_'

    def __str__(self):
        '''
        Display the Contents of the tile.
        :return tile symbol: self.symbol of the instance
        '''
        return f'{self.symbol}'

    def clearTile():
        '''
        Empty the Contents of the tile
        '''
        self.contents = None
        self.symbol = '_'

    def addBarrierToTile( self, isOrigin ):
        '''
        Add or change tile contents to Barrier (1 tile of the barrier only)
        Inclues checks for previous tile contents
        '''
        if (isOrigin==True):
            if (self.contents != None):
                if (self.contents.isOrigin==True):
                    print("duplicate barrier")
                    return True
                else:
                    self.contents = Barrier( isOrigin )
                    self.symbol = self.contents.symbol
                    return False
            else:
                self.contents = Barrier( isOrigin )
                self.symbol = self.contents.symbol
                return False
        elif (self.contents == None):
            self.contents = Barrier( isOrigin )
            self.symbol = self.contents.symbol
            return False
        else:
            return False

    def addTreasureToTile( self, treasureValue):
        '''
        Add or change tile contents to Treasure
        Includes checks for previous tile contents
        '''
        if ( self.contents == None ):
            self.contents = Treasure( treasureValue )
            self.symbol = '$'
            return False
        else:
            return True
        # do checks go here or in the board?
        # no treasure if barrier or treasure
        # re-randomize?

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