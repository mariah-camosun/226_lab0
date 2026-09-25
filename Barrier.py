class Barrier:
    def __init__(self, isOrigin: bool):
        self.symbol = 'X'
        self.isOrigin = isOrigin # 'origin' is top left, 'initial' point of the barrier

    def __str__(self):
        if (self.isOrigin==True):
            return f'O' 
        else:
            return f'{self.symbol}'