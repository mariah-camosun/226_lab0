from Barrier import Barrier
from Treasure import Treasure
from Player import Player

class Tile:
    
    def __init__(self)->None:
        '''
        Initialize a new tile & set contents to empty, symbol to match
        '''
        self.set_contents( None )
        self.set_symbol( '_' )

    def __str__(self)->str:
        '''
        Display the (symbol of) Contents of the tile.

        :return self.symbol: str, symbol for the tile instance
        '''
        return f'{ self.get_symbol() }'

# Getters & Setters
    # No Class Variables
    # Instance Variables ( contents, symbol )
    def set_contents( self, item )->None: #HOW TO HINT? should be one of a list of custom classes
        '''
        set the contents of the tile
        includes subsequent symbol change

        :param item: set to a barrier, treasure, or player instance
        '''
        self.contents = item
        if item != None:
            self.set_symbol( item.get_symbol() )
            return item
        else:
            self.set_symbol( "_" )
            return item     
    def get_contents( self ): #HOW TO HINT? as abv meth'd
        '''
        get the item contained in the tile

        :return: the item in 'self.contents' the barrier, treasure, player instance, or if empty, None
        '''
        return self.contents

    def set_symbol(self, symbol: str)->None:
        '''
        set the symbol for the tile

        :param symbol: str, symbol for the tile.
        '''
        self.symbol = symbol
    def get_symbol( self )->str:
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
        self.set_contents( None )
        self.set_symbol( '_' )

# Validation and Checks
    def check_empty(self)->bool:
        '''
        check if the tile is empty

        :return: bool, is_empty
        '''
        if ( self.get_contents() == None ):
            return True
        else:
            return False

    def check_if_barrier(self)->tuple[bool, bool]:
        '''
        check if the tile contains a barrier, and if it is the origin of the barrier block

        :return: tuple[ is_barrier, is_barrier_origin ]
        '''
        contents = self.get_contents()
        is_barrier = isinstance( contents, Barrier)
        if is_barrier:
            return True, contents.get_is_origin()
        else:
            return False, False

    def check_is_treasure(self)->int:
        '''
        Find the value of a treasure. Returns 0 if no treasure.
        
        :return: value of treasure. Value of 0 is no treasure!
        '''
        contents = self.get_contents()
        is_treasure = isinstance( contents, Treasure)
        if is_treasure:
            return contents.get_value()
        else:
            return 0

    def set_to_treasure( self, treasure_value: int )->bool:
        '''
        Add or change tile contents to Treasure
        Includes checks for previous tile contents

        :param treasure_value: the point value for the treasure item
        :return: bool, isBlocked - true if tile already full
        '''
        is_empty = self.check_empty()
        if ( is_empty ):
            t_tile = Treasure( treasure_value )
            self.set_contents( t_tile )
            self.set_symbol( t_tile.get_symbol() )
            return False
        else:
            return True

    def set_to_barrier(self, is_origin: bool )->bool: # this methd needs some cleanup
        '''
        Add or change tile contents to Barrier
        Includes checks for previous tile contents

        :param is_origin: is this barrier tile the origin of its barrier block
        :return: bool, isDuplicate - true if tile already contains barrier origin
        '''
        b_tile = Barrier( is_origin ) #instanciate barrier
        prev_contents = self.get_contents()

        if ( is_origin == True ) and isinstance(prev_contents, Barrier) and ( prev_contents.get_is_origin() == True ): 
            # barriers are first non-empy generated. 
            # Contents should only be empty or barrier
            return True
        elif ( is_origin == False ) and ( prev_contents != None):
            return False
        else:
            self.set_contents( b_tile )
            self.set_symbol( b_tile.get_symbol() )
            return False

    def set_to_player( self, player: Player )->None: # NOT properly commented yet - player class still WIP
        '''
        Move player into tile (add player to tile component)

        :param player: Player, the player being moved
        '''
        self.contents = player
        self.symbol = player.get_name()