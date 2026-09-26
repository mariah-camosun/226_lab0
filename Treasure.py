class Treasure:
    symbol = '$'
    def __init__(self, treasureValue: int):
        self.setValue( treasureValue )

    def __str__(self):
        '''
        Returns the Treasure's symbol and value as a string
        :return: (str)(Treasure.symbol (self.value)) 
        '''        
        return f'{ self.getSymbol() } ({ self.getValue() })'
    @classmethod
    def getSymbol( cls )->str:
        '''
        Returns the Treasure symbol
        :return: Treasure.symbol 
        '''
        return cls.symbol

    @classmethod
    def setSymbol( cls, symbol: str ):
        '''
        set the symbol for Treasure class
        NOTE: symbol is for class, NOT per instance
        :param symbol: str, the symbol to represent a treasure tile 
        '''        
        cls.symbol = symbol

    def getValue( self )->int:
        '''
        get value of treasure item
        :return: self.value: int
        '''        
        return self.value
    
    def setValue( self, value: int ):
        '''
        set the value of a treasure object
        :param value: int, point value of treasure
        '''
        self.value = value