import constants
import pytest
from Board import Board
from Player import Player

def test_player():
    b = Board(10,0,4)

    p = Player(2, 1, b, 3) #column row (x,y), og given code was row column
    assert p.get_coords() == (2,1)
    assert p.get_score() == 3
    p.add_score(10)
    assert p.get_score() == 13
    p.move(constants.UP) #, constants.BLANK)
    assert p.get_coords() == (2, 0)

def test_board():
    with pytest.raises(ValueError, match='Size must be at least 5.'):
        b = Board(0, 0, 0)