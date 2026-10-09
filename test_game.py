# import constants
import pytest
from Board import Board
from Player import Player

def test_player():
    b = Board(10,0,4)

    p = Player(1, 2, b, 3)
    assert p.get_coords() == (1, 2)
    assert p.get_score() == 3
    p.add_score(10)
    assert p.get_score() == 13
    p.move(constants.UP) #, constants.BLANK)
    assert p.get_coords() == (0, 2)

# def test_board():
#     with pytest.raises(ValueError, match='Size must be at least 5.'):
#     b = Board(0, 0, 0)