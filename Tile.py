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

    def addBarrierToTile( barrier: Barrier ):
        '''
        Add or change tile contents to Barrier (1 tile of the barrier only)
        '''
        self.contents = barrier
        self.symbol = 'X'
        # do checks go here or in the board?
        pass

    def addTreasureToTile( self, treasureValue):
        '''
        Add or change tile contents to Treasure
        '''
        self.contents = Treasure( treasureValue )
        self.symbol = '$'
        # do checks go here or in the board?
        # no treasure if barrier or treasure
        # re-randomize?
        pass

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