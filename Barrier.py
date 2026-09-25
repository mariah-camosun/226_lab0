class Barrier:
    def __init__(self):
        self.symbol = 'X'
        self.posn = "TL" #top left - 'marker' position
        self.makeBarrierGrid()

    def __str__(self):
        return f'{self.symbol}'

    def makeBarrierGrid(  ):
        # take the bard position of barrier marker
        # make TR (@Board[x+1][y])
        # make BL (@Board [x][y+1])
        # make BR (@Board [x+1][y+1])
        pass
