class Barrier:
# Requirements
# 
# ~~~ Part C ~~~ 
# [x] add detailed header comments to ALL methods 
# [ ] make sure ALL instance variables of classes not accessed directly by outside code
# [x] abv re-perspective. This class does NOT directly access any outside instance variables
#          - eg. bad: board.player.row += 1
#          - instead: board.move('D'), which will in turn call self.player.move('D')

    symbol = 'X' # Symbol should be the same for all tiles, including 'origin' and 'non-origin' types
    def __init__( self, isOrigin: bool )->None:
        '''
        Creates a new barrier instance (not block), occupies 1 tile

        :param isOrigin: bool, is this barrier the 'origin' or inital segment of the barrier
        '''
        self.setIsOrigin( isOrigin ) # 'origin' is top left, 'initial' point of the barrier

    def __str__( self )->str:
        '''
        Returns the Barrier's symbol as a string.

        :return: (str)(Barrier.symbol)
        '''
        return f'{ self.getSymbol() }'

# Getters and Setters
# class variables
    @classmethod
    def getSymbol(cls)->str:
        '''
        get the symbol for Barrier class

        :return: str, Barrier.symbol
        '''
        return cls.symbol

    @classmethod
    def setSymbol( cls, symbol: str )->None:
        '''
        set the symbol for Barrier class
        NOTE: symbol is for class, NOT per instance

        :param symbol: str, the symbol for a barrier tile 
        '''
        cls.symbol = symbol

# instance variables
    def getIsOrigin( self )->bool:
        '''
        get value of param: isOrigin

        :return: isOrigin: bool, is this the 'origin' barrier tile for it's block
        '''
        return self.isOrigin

    def setIsOrigin( self, isOrigin: bool )->None:
        '''
        set value of param: isOrigin

        :param isOrigin: bool, is this the 'origin' barrier tile for it's block
        '''
        self.isOrigin = isOrigin