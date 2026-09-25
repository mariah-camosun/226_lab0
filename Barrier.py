class Barrier:
    def __init__(self, posn):
        self.symbol = 'X'
        self.posn = posn # 'TL' = top left - 'marker' position

    def __str__(self):
        return f'{self.symbol}'