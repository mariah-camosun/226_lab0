class Player:
    def __init__(self):
        self.num = 1
        self.symbol = (str)(self.num)

    def __str__(self):
        return f'{self.symbol}'