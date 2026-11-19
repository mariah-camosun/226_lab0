from django.db import models

# Create your models here.
class Player( models.Model):
    tag = models.CharField(max_length=1) # data field; NOT the primary key!
    row = models.IntegerField() 
    col = models.IntegerField()

    def __str__(self):
        return f'{self.tag} @({self.row}, {self.col})' # not neccessary unless doing debugging, shows up in admin

    @classmethod
    def create_player(cls, tag, row, col):
        model=cls(tag=tag, row=row, col=col)
        model.full_clean()
        return model