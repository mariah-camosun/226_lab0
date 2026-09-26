class Barrier:
    symbol = 'X' # Symbol should be the same for 'origin' and 'non-origin' tiles
    def __init__( self, isOrigin: bool ):
        '''
        Creates a new barrier instance
        :param isOrigin: boolean, is this barrier segment the 'origin' or inital point of the barrier
        '''
        self.setIsOrigin( isOrigin ) # 'origin' is top left, 'initial' point of the barrier

    def __str__( self ):
        '''
        Returns the Barrier's symbol as a string
        :return: (str)(Barrier.symbol)
        '''
        return f'{ self.getBarrierSymbol() }'

    def getIsOrigin( self ):
        '''
        get value of param: isOrigin
        :return: isOrigin: bool
        '''
        return self.isOrigin

    def setIsOrigin( self, isOrigin: bool ):
        '''
        set value of param: isOrigin
        :param isOrigin: bool, is this tile the reference point for the barrier grid
        '''
        self.isOrigin = isOrigin

    @classmethod
    def getSymbol(cls):
        '''
        get the symbol for Barrier class
        :return: Barrier.symbol
        '''
        return cls.symbol

    @classmethod
    def setSymbol( cls, symbol ):
        '''
        set the symbol for Barrier class
        NOTE: symbol is for class, NOT per instance
        :param symbol: str, the symbol to represent a barrier tile 
        '''
        cls.symbol = symbol