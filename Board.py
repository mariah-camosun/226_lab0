import random
from Tile import Tile
from typing import TYPE_CHECKING
from Player import Player

class Board:
# TODO
# [ ] fix functions that pass in unneccessary variables (eg. board_size)

    def __init__(self, size: int, barrier_number: int, treasure_number: int)->None:
        '''
        Creates new board

        :param size: number of tiles per side of board
        :param barrier_number: number of barrier blocks to generate (multiple tiles per block)
        :param treasure_number: number of treasures to generate
        '''
        self.size = size
        self.barrier_number = barrier_number
        self.treasure_number = treasure_number
        self.tile_count = 0
        print(f"to make: {size}*{size}, {barrier_number} barriers, {treasure_number} treasures")
        self.make_empty_board( size )
        self.make_barriers( barrier_number )
        self.make_treasures( treasure_number )
        # For now, treating as single entry for simplicity
        # self.players = []
        # self.players.append( self.make_new_player() ) 
        self.players = [self.make_new_player()]

    def __str__(self)->str:
        '''
        returns a sting representing the current state of the board

        :return: str, current board state
        '''
        output = "\n"
        for row in self.grid:
            for tile in row:
                output += tile.__str__()
                output += "  "
            output += "\n"
        output += "\nnum treasures remaining: " + (str)(self.treasure_count) + "\n"
        self.report_player_scores()
        return output

# init functions
    def make_empty_board(self, size):
        '''
        make an empty board of size x size tiles
        sets tile count to size**2, clears treasure and barrier counts
        '''
        # create size x size collection of Tiles; ea empty (initially)
        try:
            self.validate_size( size )
        except TypeError:
            raise
        except ValueError:
            raise
        else:
            self.size = size
            self.grid = []
            self.set_tile_count( size*size )
            self.set_treasure_count( 0 )
            self.set_barrier_count( 0 )

            for item in range( size ):
                self.grid.append( [ Tile() for _ in range (size) ] )

    def make_barriers( self, barrier_number: int )->None:
        '''
        generate board barriers

        :param barrier_number: number of barrier blocks to make
        :return: bool is_valid
        '''
        board_size = self.get_size()
        try: 
            self.validate_barrier_number(barrier_number)
        except ValueError:
            # max_blocks = (board_size*board_size)*.2/4
            # if barrier_number <= 0:
            #     print( "must have at least 1 barrier block, and no more than ", max_blocks)
            # else: 
            #     print(f"{barrier_number} is too many barriers for board size, at current size, generate no more than ", max_blocks)
            #     print("increase board size, or decrease number of barriers")
            raise
        except TypeError:
            # print(barrier_number + "is not a number")
            raise
        else:            
            for i in range( barrier_number ): 
                self.make_one_barrier( board_size )

    def make_one_barrier( self, board_size: int )->None:
        '''
        create 1 'block' of barriers (2x2 tiles) at a random position
        includes check for complete overlap and increments barrierCound on success

        # NOTE realized I can eliminate this parameter wherever it is used
        :param board_size: int, size of board
        '''
        while(True):
            origin_tile, x, y = self.randomize_position()
            is_duplicate = origin_tile.set_to_barrier( True )
            if ( not is_duplicate ):
                break

        #once successfull barrier origin, add 1 to barrierCount
        self.set_barrier_count( self.get_barrier_count()+1 )

        # if barrier would overflow an edge, wrap overflow barrier tiles (set coord value = 0)
        if ( x+1 == board_size ):
            x2 = 0
        else:
            x2 = x+1
        if ( y+1 == board_size ):
            y2 = 0
        else:
            y2 = y+1

        # add remaining barrier tiles of the 2x2 barrier
        self.get_coord_tile(x2,y).set_to_barrier( False )        
        self.get_coord_tile(x2,y2).set_to_barrier( False )        
        self.get_coord_tile(x,y2).set_to_barrier( False )        

    def make_treasures( self, treasure_number: int )->bool:
        '''
        generate board treasures

        :param treasure_number: number of treasures to make
        :return: bool is_valid
        '''
        board_size = self.get_size()               
        try: 
            self.validate_treasure_number(treasure_number)
        except ValueError:
            raise
            # max_blocks = (board_size*board_size)*.05
            # if treasure_number <= 0:
            #     print( "must have at least 1 treasures, and no more than ", max_blocks)
            # else: 
            #     print("Too many treasures for board size, at current size, generate no more than ", max_blocks)
            #     print("increase board size, or decrease number of treasures")
            # return False
        except TypeError:
            raise
            # print(treasure_number + "is not a number")
            # return False
        else:            
            for i in range( treasure_number ):
                self.make_one_treasure()

    def make_one_treasure( self )->None:
        '''
        create 1 treasure at a random position
        includes check for previous tile contents and increments treasure_count on success
        '''
        board_size = self.get_size()
        while(True):
            x = random.randint(0, board_size-1)
            y = random.randint(0, board_size-1)
            treasure_tile = self.get_coord_tile(x,y)
            is_duplicate = treasure_tile.set_to_treasure( 1 )
            if ( not is_duplicate ):
                break

        #once successfull treasure, add 1 to treasure_count
        self.set_treasure_count( self.get_treasure_count() + 1 )

    def make_new_player( self )->Player:
        '''
        creates a new player and places it on a random empty tile

        :return: Player, the new player
        '''
        '''
        creates a new player and places it on a random empty tile

        :return: Player, the new player
        '''
        while True:
            tile, column, row = self.randomize_position()
            if tile.get_contents() == None:
                # place new player instance into contents
                new_player = tile.set_contents( Player( column, row, self ) )
                return new_player

# Setters and Getters
    def get_board( self )->list[list[Tile]]:
        '''
        returns the 2D array of board tiles

        :return: 2D array of tiles 
        '''
        return self.grid
    # no set_board() - instead, make_empty_board()

    def get_size( self )->int:
        '''
        get the number of tiles per side of the board
        Note: no setter, as changing would require re-generating the board

        :return: int, number of tiles per side
        '''
        return self.size    
    # no set_board_size() - only done at init

    def get_coord_tile( self, column: int, row: int )->Tile:
        '''
        returns tile for a specific 2D array position[row][column]

        :param row: index of row in board array
        :param column: index of tile in row array
        :return: Tile
        '''
        if self.check_on_board( column,row ):
            return self.get_board()[row][column]
    # no set_coord_contents() - only done at init

    def get_players( self )->list[Player]:
        '''
        returns all current players as a list

        :return: list[Player], list of all current players
        '''
        output = "Current players: "
        for player in self.players:
            output += (str)(player)
            output += ','
        print(output)
        return self.players
    #no set_players() - instead, make_new_player()

    def get_tile_count( self )->int:
        '''
        get number of tiles on the board

        :return: number of tiles in the board
        '''        
        return self.tile_count
    def set_tile_count( self, count: int )->None:
        '''
        set tile_count to value count

        :param count: number of tiles in the board
        '''
        self.tile_count = count

    def get_treasure_count( self )->int:
        '''
        get number of treasures on the board

        :return: number of treasures on the board
        ''' 
        return self.treasure_count
    def set_treasure_count( self, count: int )->None:
        '''
        set treasure_count to value count

        :param count: number of treasures on the board
        '''
        self.treasure_count = count

    def get_barrier_count( self )->int:
        '''
        get number of barrier blocks on the board

        :return: number of barrier blocks on the board
        '''         
        return self.barrierCount
    def set_barrier_count( self, count: int )->None:
        '''
        set barrierCount to value count

        :param count: number of barrier blocks (not tiles) on the board
        '''        
        self.barrierCount = count

# expanded setters
    def decrement_treasure_count( self ):
        self.treasure_count -= 1

    def randomize_position(self):
        '''
        get a random board position and return tile, if any

        :return: tile instance: Tile, x-coordinate: int, y-coordinate: int
        '''
        board_size = self.get_size()
        column = random.randint(0, board_size-1)
        row = random.randint(0, board_size-1)
        prev_tile = self.get_coord_tile( column, row )
        return prev_tile, column, row

    def place_in_random_empty( self, item_to_place ):
        '''
        Places an item in a random empty tile. Loops until successfully placed.

        :param item_to_place: item to place into the game Tile. Acceptable classes: Player, Barrier, Treasure
        Places an item in a random empty tile. Loops until successfully placed.

        :param item_to_place: item to place into the game Tile. Acceptable classes: Player, Barrier, Treasure
        '''
        while True:
            tile, _, _ = self.randomize_position()
            if tile.get_contents() == None:
                tile.set_contents( item_to_place )
                break

# Validation and checks
    def validate_size(self, size: int)->bool:
        '''
        Validates size parameter for the game board is an integer > 0 and <= 30
        Validates size parameter for the game board is an integer > 0 and <= 30

        :param size: int between [1,30], size of each side of the board (board is size x size)
        :return: bool, is_valid
        :return: bool, is_valid
        '''
        if not isinstance(size, int):
            raise TypeError("Size given is not an integer")
        elif ( not( 0 < size <= 30) ):
            raise ValueError("Size must be at least 5.")
        else:
            return True
        
    def validate_barrier_number (self, barrier_number: int)->bool:
        '''
        Validates barrier_number parameter is an integer > 0, and
        Does not occupy > 20% of the board

        :param barrier_number: int > 0 and < 20% of board, number of barrier blocks to make
        :return: bool, is_valid
        :return: bool, is_valid
        '''
        if not isinstance(barrier_number, int ):
            raise TypeError("Barrier_number given needs to be an integer")
        elif ( barrier_number < 1 ):
            raise ValueError("Must have 1 or more barriers")
        # barriers must be <= 20% of board; each barrier takes (up to) 4 tiles
        elif ( barrier_number*4 > ( self.get_tile_count() * .2 ) ):
            raise ValueError("Too many barriers. Either increase board size, or decrease barrier_number")
        else:
            return True

    def validate_treasure_number (self, treasure_number: int)->bool:
        '''
        Validates treasure_number parameter is an integer > 0, and
        Does not occupy > 5% of the board

        :param treasure_number: int > 0 and < 5% of board, number of treasures to make
        :return: bool, is_valid
        '''
        if not isinstance(treasure_number, int ):
            raise TypeError("treasure_number given needs to be an integer")
        elif ( treasure_number <= 0 ):
            raise ValueError("Cannot have negative treasures")
        # treasures must be <= 5% of board
        elif ( treasure_number > self.get_tile_count() * .05 ):
            raise ValueError("Too many treasures. Either increase board size, or decrease treasure_number")
        else:
            return True

    def check_on_board( self, column, row )->bool:
        '''
        checks if coordinates are within the gameboard


        :return: bool, isOnGameboard
        '''
        if ( 0 <= column < self.get_size() and 0 <= row < self.get_size() ):
            return True        
        else:
            return False

# Utility
    def report_player_scores(self):
        '''
        prints out the current player scores for all players
        '''
        '''
        prints out the current player scores for all players
        '''
        players = self.get_players()
        for player in players:
            print(f"player {player.get_name()}: score: {player.get_score()}")