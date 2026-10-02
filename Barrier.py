class Barrier:
    # Symbol is the same for all tiles, including 'origin' and 'non-origin' types
    symbol = 'X' 

    def __init__( self, is_origin: bool )->None:
        '''
        Creates a new barrier instance (not block), occupies 1 tile

        :param is_origin: bool, is this barrier the 'origin' or inital segment of the barrier
        '''
        self.set_is_origin( is_origin ) # 'origin' is top left, 'initial' point of the barrier

    def __str__( self )->str:
        '''
        Returns the Barrier's symbol as a string.

        :return: (str)(Barrier.symbol)
        '''
        return f'{ self.get_symbol() }'

# Getters and Setters
# class variables
    @classmethod
    def get_symbol(cls)->str:
        '''
        get the symbol for Barrier class

        :return: str, Barrier.symbol
        '''
        return cls.symbol

    @classmethod
    def set_symbol( cls, symbol: str )->None:
        '''
        set the symbol for Barrier class
        NOTE: symbol is for class, NOT per instance

        :param symbol: str, the symbol for a barrier tile 
        '''
        cls.symbol = symbol

# instance variables
    def get_is_origin( self )->bool:
        '''
        get value of param: is_origin

        :return: is_origin: bool, is this the 'origin' barrier tile for it's block
        '''
        return self.is_origin

    def set_is_origin( self, is_origin: bool )->None:
        '''
        set value of param: is_origin

        :param is_origin: bool, is this the 'origin' barrier tile for it's block
        '''
        self.is_origin = is_origin