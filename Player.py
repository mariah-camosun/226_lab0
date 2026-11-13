from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Board import Board
    from Tile import Tile
    from Treasure import Treasure    

class Player:
    player_count = 0

    def __init__(self, column:int, row:int, game_board, initial_score = 0)->None:
        '''
        create a new Player instance

        :param column: int, the x-position of the player
        :param row: int, the y-position of the player
        :param game_board: the game_board the player is on
        :param initial_score: int, starting score for player. Defaults to 0
        '''
        self.increment_player_count()
        self.name = self.get_player_count()
        self.symbol = (str)(self.name)
        self.score = initial_score
        self.row = row
        self.column = column
        self.game_board = game_board

    def __str__(self)->str:
        '''
        returns the symbol (number) for the player instance

        :return: str, player symbol (number)
        '''
        return f'{self.symbol}'

# Getters & Setters
    # Class variables: (player count)
    @classmethod
    def get_player_count( cls )->int:
        '''
        returns the total number of players

        :return: int, number of players
        '''
        return cls.player_count
    @classmethod
    def set_player_count( cls, count:int )->None:
        '''
        sets the player count to the number passed in

        :param count: int, number of current players
        '''
        cls.player_count = count

    # Instance Variables: (name, symbol, score, column, row, game_board)
    def get_name(self)->int:
        '''
        returns the name of this player instance

        :return: str, player name
        '''
        return self.name
    # no set_name() - only done at init

    def get_symbol(self)->str:
        '''
        returns the symbol of this player's instance

        :return: str, player symbol
        '''
        return self.symbol
    # no setPlayerSymbol() - only done at init

    def get_score( self )->int:
        '''
        returns the current score for this player instance

        :return: int, player score
        '''        
        return self.score
    def set_score( self, score:int ):
        '''
        changes this player's score to the number passed in

        :param score: int, new player score        
        '''
        self.score = score

    def get_coords( self )->tuple[int, int]:
        '''
        returns the current game_board coordinates of this player

        :return: tupple[int, int], column coordiante, row coordinate
        '''
        return self.column, self.row
    def set_coords( self, column:int, row:int)->None:
        '''
        sets the values for player coordinates to the given column and row

        :param column: int, x-position of player
        :param row: int, y-position of player
        '''
        self.column = column
        self.row = row

    def get_board( self )->list[list[Tile]]:
        '''
        returns the game_board the player is on

        :return: list[list[Tile]], the game_board containing the player
        '''
        return self.game_board
    # no set_board() - only done at init

# Extended Setters
    @classmethod
    def increment_player_count( cls )->None:
        '''
        icreases the player count by 1
        '''        
        cls.player_count += 1
     
    def add_score( self, add_score:int )->int:
        '''
        adds add_score to this player's score and returns updated score

        :param add_score: int, points to add to player score
        :return: int, player score after update
        '''
        self.score += add_score
        return self.score

# Validation
    def validate_direction( self, direction: str )->bool:
        '''
        validates the entered string is allowed

        :param direction: str, direction to move the player in
        :return: bool, is_valid
        '''
        if ( direction == "U" or direction == "D" or direction == "L" or direction == "R" ):
            return True
        else:
            raise ValueError

    def validate_coords( self, row:int, column:int)->bool:
        '''
        validates that coordinates (row and column) are both within the valid range (>= 0, < board size)

        :return: bool, is_valid for BOTH row and column coordinates
        '''
        board_size = self.get_board().get_size()
        if ( 0 <= row < board_size and 0 <= column < board_size ):
            return True
        else: 
            raise ValueError

# Move
    def get_move_direction( self )->str:
        '''
        Prompt user for direction to move in and check for validity

        :return: str, direction to move
        '''
        while True:
            direction = input(f"Move player {self.get_symbol()}: \nEnter a direction (U-up D-down L-left R-right) to move: ")
            print(f"direction value entered: {direction}")

            if isinstance( direction, int):
                print(f"Choose one of: U, D, L, R")
                continue
                # raise TypeError
            
            try:
                direction = direction.upper()
                is_valid = self.validate_direction( direction )
            # except TypeError as details:
            #     print(f"Choose one of: U, D, L, R") # will also accept lower case
            #     raise
            except ValueError as details:
                print(f"Choose one of: U, D, L, R") # will also accept lower case
                # raise
                continue
            else:
                return direction

    def move( self, direction=None )->None: # direction not a param, as includes user prompt
        '''
        Move the current player instance. Includes prompting and validation.
        Checks contents of target tile, and moves or not as appropriate.
        '''
        if direction==None:
            direction = self.get_move_direction() # direction moving
        board = self.get_board()
        x,y = self.get_coords() # coordinates of initial position
        old_tile = board.get_coord_tile( x,y ) # initial position tile

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

        # if x2 or y2 are outside the game_board bounds, return, otherwise continue checking
        try:
            are_coords_valid = self.validate_coords( x2, y2 )
        except ValueError as details:
            print(f"Coordinates [{x2},{y2}] are outside the game board")
            return
        else:
            target_tile = board.get_coord_tile( x2,y2 ) # tile to move to
            is_barrier, _ = target_tile.check_if_barrier()
            is_treasure = target_tile.check_is_treasure()
            is_player = target_tile.check_is_player()
            if is_barrier or is_player: 
            # or target_tile.checkTilePlayer(): #Second check doesnt actually exist yet
                print(f"entered tile is barrier or player: {target_tile.get_contents()}")
                return
            elif ( is_treasure ): # 0 evals to false,
                treasure = target_tile.get_contents()
                treasure.collect_treasure( board, target_tile, self )
            # else empty is only alternative (unspecified), 
            # no movement blocks then Given ALREADY PREVIOUSLY checked in bounds into
            # all successful move intos use the following code hence outside the if block
            target_tile.set_to_player( self )
            self.set_coords( x2, y2 )
            old_tile.clear_tile()