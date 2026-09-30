class Treasure:
    symbol = '$'
    def __init__(self, treasureValue: int)->None:
        '''
        initialize new treasure item, set value to treasureValue
        :param treasureValue: int, point value of treasure item
        '''
        self.setValue( treasureValue )

    def __str__(self)->str:
        '''
        Returns the Treasure's symbol and value as a string
        :return: (str)(Treasure.symbol (self.value)) 
        '''        
        return f'{ self.getSymbol() } ({ self.getValue() })'

# setters and getters
# Class variables
    @classmethod
    def getSymbol( cls )->str:
        '''
        Returns the Treasure symbol
        :return: str, Treasure.symbol 
        '''
        return cls.symbol

    @classmethod
    def setSymbol( cls, symbol: str )->None:
        '''
        set the symbol for Treasure class
        NOTE: symbol is for class, NOT per instance
        :param symbol: str, the symbol to represent a treasure tile 
        '''        
        cls.symbol = symbol

# instance variables
    def getValue( self )->int:
        '''
        get point value of treasure item
        :return: self.value: int, point value of treasure
        '''        
        return self.value
    
    def setValue( self, value: int )->None:
        '''
        set the point value of a treasure object
        :param value: int, point value of treasure
        '''
        try: 
            self.validateTreasureValue( value )
        except TypeError as details:
            print(f"{value} is not an integer: {details}")
        except ValueError as details:
            print(f"Treasure value {value} is not valid. Must be integer > 0: {details}")
        else:
            self.value = value           

# Validation and Checks
    def validateTreasureValue(self, value)->bool:
        if type( value )!=int:
            raise TypeError
        elif ( value <= 0):
            raise ValueError
        else:
            return True