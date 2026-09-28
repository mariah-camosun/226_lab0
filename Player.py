class Player:
    # auto-increment name as player number
    # contain coors of player
    # contains player score
    # __str__ methd
    # add_score, get_score methods
    # move methd, takes a dir (UDLR) to chg player location if poss (otherwise ignored)
    # value error on: row, col, score negative; row col outside board
    def __init__(self):
        self.num = 1 # TO BE auto-incremented, for now this will hold place
        self.symbol = (str)(self.num)

    def __str__(self):
        return f'{self.symbol}'