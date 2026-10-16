from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Board import Board
    from Tile import Tile
    from Player import Player  

class Treasure:
    symbol = '$'
    
    def __init__(self, treasure_value: int)->None:
        '''
        initialize new treasure item, set value to treasure_value

        :param treasure_value: int, point value of treasure item
        '''
        self.set_value( treasure_value )

    def __str__(self)->str:
        '''
        Returns the Treasure's symbol and value as a string
        
        :return: (str)(Treasure.symbol (self.value)) 
        '''        
        return f'{ self.get_symbol() } ({ self.get_value() })'

# setters and getters
# Class variables
    @classmethod
    def get_symbol( cls )->str:
        '''
        Returns the Treasure symbol
        
        :return: str, Treasure.symbol 
        '''
        return cls.symbol

    @classmethod
    def set_symbol( cls, symbol: str )->None:
        '''
        set the symbol for Treasure class
        NOTE: symbol is for class, NOT per instance
        
        :param symbol: str, the symbol to represent a treasure tile 
        '''        
        cls.symbol = symbol

# instance variables
    def get_value( self )->int:
        '''
        get point value of treasure item
        
        :return: self.value: int, point value of treasure
        '''        
        return self.value
    
    def set_value( self, value: int )->None:
        '''
        set the point value of a treasure object
        
        :param value: int, point value of treasure
        '''
        try: 
            self.validate_value( value )
        except TypeError as details:
            print(f"{value} is not an integer")
            raise TypeError(f"{value} is not an integer")
        except ValueError as details:
            print(f"Treasure value {value} is not valid. Must be integer > 0")
            raise ValueError(f"Treasure value {value} is not valid. Must be integer > 0")
        else:
            self.value = value           

# Validation and Checks
    def validate_value(self, value)->bool:
        '''
        checks that the point value of the treasure item is valid
        raises errors if it is not

        :param value: int, points value of the treasure
        :return: bool, isValid
        '''
        if type( value )!=int:
            raise TypeError
        elif ( value <= 0):
            raise ValueError
        else:
            return True

# utility
    def collect_treasure( self, board:Board, tile:Tile, player:Player )->None:
        '''
        Collects the treasure on the tile and adds value to player score

        :param board: Board, gameboard holding the treasure and player
        :param tile: Tile, containing the treasure item to be collected
        :param player: Player, player collecting the treasure
        '''
        treasure_value = self.get_value()
        player.add_score( treasure_value )
        tile.clear_tile()
        board.decrement_treasure_count()
        print(f"remaining treasures: {board.get_treasure_count()}")
        print(f"player {player.get_name()} collected: {treasure_value} treasure points.")