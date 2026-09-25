class Barrier:
    def __init__(self, isOrigin: bool):
        self.isOrigin = isOrigin # 'origin' is top left, 'initial' point of the barrier
        if (self.isOrigin==True):
            self.symbol = 'O' 
        else:
            self.symbol = 'X'

    def __str__(self):
        return f'{self.symbol}'