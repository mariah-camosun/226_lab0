import constants
import pytest
from Board import Board
from Player import Player

def test_player():
    b = Board(10,1,4)

    p = Player(2, 1, b, 3) #column row (x,y), og given code was row column
    assert p.get_coords() == (2,1)
    assert p.get_score() == 3
    p.add_score(10)
    assert p.get_score() == 13
    p.move(constants.UP) #, constants.BLANK)
    assert p.get_coords() == (2, 0)

def test_board():
    # Size
    with pytest.raises(ValueError, match='Size must be at least 5.'):
        b = Board(0, 0, 0)
    with pytest.raises(TypeError, match='Size given is not an integer'):
        b = Board("a", 0, 0)

    # Barrier Number
    with pytest.raises(TypeError, match='Barrier_number given needs to be an integer'):
        b = Board(5, "a", 0)
    with pytest.raises(ValueError, match='Cannot have negative barriers'):
        b = Board(5, -5, 0)
    with pytest.raises(ValueError, match='Too many barriers. Either increase board size, or decrease barrier_number'):
        b = Board(5, 20, 0)

    # Treasure Number
    with pytest.raises(TypeError, match='treasure_number given needs to be an integer'):
        b = Board(5, 1, "a")
    with pytest.raises(ValueError, match='Cannot have negative treasures'):
        b = Board(5, 1, -5)
    with pytest.raises(ValueError, match='Too many treasures. Either increase board size, or decrease treasure_number'):
        b = Board(5, 1, 20)    