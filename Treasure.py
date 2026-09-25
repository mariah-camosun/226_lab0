class Treasure:
    def __init__(self, treasureValue: int):
        self.symbol = '$'
        self.value = treasureValue

    def __str__(self):
        return f'{self.symbol} ({self.value})'