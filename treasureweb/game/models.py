from django.db import models

# Create your models here.

# Tile Model : row, column, value
class Tile(models.Model):
    row=models.IntegerField()
    col=models.IntegerField()
    value=models.IntegerField()

    def __str__(self):
        return f'({self.row},{self.col}) is {self.value}'

# Player Model : name, row, column, score
class Player(models.Model):
    name=models.CharField(max_length=1)
    row=models.IntegerField()
    col=models.IntegerField()
    score=models.IntegerField()

    def __str__(self):
        return f'{self.name} @ ({self.row},{self.col})'

    @classmethod
    def create_player_at(cls, name, row, col):
        model = cls(name=name, row=row, col=col, score=0)
        model.full_clean()
        return model