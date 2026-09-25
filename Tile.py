from Barrier import Barrier
from Treasure import Treasure
from Player import Player

class Tile:
#keeps track of own contents
    def __init__(self):
        self.contents = None 

    # def __init__(self, xcoord: int, ycoord: int):
    #     self.contents="empty"
    #     self.xcoord=xcoord
    #     self.ycoord=ycoord

    def __str__(self):
        '''
        Display the Contents of the tile.
        (OR IF storing only the string, the self.contents)

        :return self.contents.name: the 'name' of the contents item
        '''
        return f'{self.symbol}'

    # def changeTile( content: enumOrClass? ):
    #     ''' 
    #     Change or add new contents to the tile

    #     :param content: the 'class or enum' of the contents item to add
    #     '''
    #     self.contents=content

    def clearTile():
        '''
        Empty the Contents of the tile
        '''
        self.contents = None
        self.symbol = '_'

    def addBarrierToTile( barrier: Barrier ):
        '''
        Add or change tile contents to Barrier
        '''
        self.contents = barrier
        self.symbol = 'X'
        # do checks go here or in the board?
        # if self.contents (before) == barrier.topLeft then do not place
        # re-randomize?
        pass

    def addTreasureToTile( treasure: Treasure):
        '''
        Add or change tile contents to Treasure
        '''
        self.contents = treasure
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