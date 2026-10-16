import constants
import pytest
from Board import Board
from Player import Player
from Barrier import Barrier
from Treasure import Treasure
from Tile import Tile

# TODO
# [ ] test for:
#       [ ] every exception, 
#       [ ] every public method, and 
#       [ ] for normal game play

def set_monkeypatch( input_values, monkeypatch ):
    user_inputs = iter( input_values )
    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))

# ---------------------Testing Player---------------------------------
# def test_player_score():
#     b = Board(10,1,4)
#     # changed from original (row, column, board_size/board, initial score) 
#     # to: (column, row, board_size/board, initial score) for consistency w/ my code (x,y) order
#     p = Player(2, 1, b, 3) 

#     # testing: set, get, add score & get_coords()
#     assert p.get_coords() == (2,1)
#     assert p.get_score() == 3
#     p.add_score(10)
#     assert p.get_score() == 13
#     p.set_score(6)
#     assert p.get_score() == 6
#     p.move(constants.UP) #, constants.BLANK)
#     assert p.get_coords() == (2, 0)

# def test_player_multi_creation():
#     # testing: get_players(), get_player_count() and make_new_player() 
#     m = Board(5, 0, 1)
#     playerList = m.get_players()
#     p1 = playerList[0]

#     assert Player.get_player_count() == 1

#     p2 = m.make_new_player()
#     assert Player.get_player_count() == 2

#     Player.set_player_count( 8 )
#     assert Player.get_player_count() == 8

#     p3 = m.make_new_player()
#     assert Player.get_player_count() == 9
#     assert p3.get_name() == 9

#     assert p1.get_board() == m
#     assert p2.get_board() == m

#     # check name, symbol, print output
#     # there is no 'set name' or 'set symbol'
#     assert p1.get_name() == 1
#     assert p1.get_symbol() == "1"
#     assert str(p1) == "1"

#     assert p2.get_name() == 2
#     assert p2.get_symbol() == "2"
#     assert str(p2) == "2"

#     assert p3.get_name() == 9
#     assert p3.get_symbol() == "9"
#     assert str(p3) == "9"

# def test_player_multi_score():
#     m = Board(5, 0, 1)
#     playerList = m.get_players()
#     p1 = playerList[0]
#     p2 = m.make_new_player()

#     # testing score & score reporting for 2p
#     # no validate score, as set is always set by the program
#     assert p1.get_score() == 0
#     assert p2.get_score() == 0

#     p1.set_score(-30)
#     p2.set_score(83)
#     assert p1.get_score() == -30
#     assert p2.get_score() == 83

#     p1.add_score(30)
#     p2.add_score(10)
#     assert p1.get_score() == 0
#     assert p2.get_score() == 93

#     p2.add_score(-100)
#     assert p2.get_score() == -7

# def test_player_coords():
#     b = Board(10,1,4)
#     p = Player(2, 1, b, 3) 

#     # testing: coords set above correctly, and get_coords()
#     assert p.get_coords() == (2,1)

#     # testing: move & get_coords()
#     p.move(constants.UP) #, constants.BLANK)
#     assert p.get_coords() == (2, 0)

#     # testing standard initial player creation 
#     m = Board(5, 0, 1)
#     playerList = m.get_players()
#     p1 = playerList[0]

#     # clear coords to set to
#     b.get_coord_tile(2,1).clear_tile()
#     b.get_coord_tile(3,2).clear_tile()
#     # test: get & set coords
#     # only called by move, so no validation at this level
#     p1.set_coords(2,1)
#     assert p1.get_coords() == (2,1)
#     p1.set_coords(3,2)
#     assert p1.get_coords() == (3,2)

#     # test: validation of coords
#     assert p1.validate_coords( 0, 0 ) == True
#     assert p1.validate_coords( 3, 3 ) == True
#     assert p1.validate_coords( 4, 4 ) == True
#     with pytest.raises(ValueError):
#         p1.validate_coords( -1, 3 )
#     with pytest.raises(ValueError):
#         p1.validate_coords( -1, -1 )
#     with pytest.raises(ValueError):
#         p1.validate_coords( 3, -1 )
#     with pytest.raises(ValueError):
#         p1.validate_coords( 3, 11 )
#     with pytest.raises(ValueError):
#         p1.validate_coords( 11, 11 )
#     with pytest.raises(ValueError):
#         p1.validate_coords( 11, 3 )

# def test_Player_getMoveDir( monkeypatch ): # under 'player'cover
#     b = Board(5,0,1)
#     p1 = Player( 3,3,b )

#     set_monkeypatch(["a", "uu", 1, "D"], monkeypatch)
#     p1.get_move_direction( ) == constants.DOWN

#     set_monkeypatch(["U", "u", "D", "d", "L", "l", "R", "r"], monkeypatch)
#     assert p1.get_move_direction() == constants.UP
#     assert p1.get_move_direction() == constants.UP
#     assert p1.get_move_direction() == constants.DOWN
#     assert p1.get_move_direction() == constants.DOWN
#     assert p1.get_move_direction() == constants.LEFT
#     assert p1.get_move_direction() == constants.LEFT
#     assert p1.get_move_direction() == constants.RIGHT
#     assert p1.get_move_direction() == constants.RIGHT

# def test_player_move(monkeypatch): # under 'player'
#     b = Board(5,0,1)

#     # make sure that tiles are free to start
#     b.get_coord_tile(1,0).clear_tile()
#     b.get_coord_tile(1,1).clear_tile()
#     b.get_coord_tile(1,2).clear_tile()
#     b.get_coord_tile(0,0).clear_tile()
#     b.get_coord_tile(0,1).clear_tile()
#     b.get_coord_tile(0,2).clear_tile()
#     b.get_coord_tile(0,3).clear_tile()
#     b.get_coord_tile(0,4).clear_tile()
#     b.get_coord_tile(1,4).clear_tile()
#     b.get_coord_tile(2,4).clear_tile()
#     b.get_coord_tile(3,4).clear_tile()
#     b.get_coord_tile(4,4).clear_tile()
#     b.get_coord_tile(4,3).clear_tile()

#     # create objects to interact with
#     b1 = b.get_coord_tile( 1, 2 ).set_to_barrier(True) #col,row
#     t1 = b.get_coord_tile( 0, 0 ).set_to_treasure( 1 )

#     # specify player (2) location
#     p = Player(1, 1, b, 0)
#     assert p.get_coords() == (1,1)
#     assert p.get_score() == 0

#     # trying to move into a barrier (fails)
#     set_monkeypatch([ constants.DOWN ], monkeypatch)
#     assert p.get_coords() == (1,1)
#     p.move() 
#     assert p.get_coords() == (1,1)

#     # move up 1 works, up off board does not
#     set_monkeypatch([ constants.UP , constants.UP ], monkeypatch)
#     assert p.get_coords() == (1,1)
#     p.move()
#     assert p.get_coords() == (1,0)
#     p.move()
#     assert p.get_coords() == (1,0)

#     # moving into treasure: allows movement, adds to score, removes from board
#     set_monkeypatch([ constants.LEFT ], monkeypatch)
#     assert p.get_coords() == (1,0)
#     assert p.get_score() == 0
#     p.move() 
#     assert p.get_coords() == (0,0)
#     assert p.get_score() == 1

#     # moving off left side of board fails (move left succeeds already tested w/ treasure collect)
#     set_monkeypatch([ constants.LEFT ], monkeypatch)
#     assert p.get_coords() == (0,0)
#     p.move()
#     assert p.get_coords() == (0,0)

#     # move Down works, move off bottom of board does not
#     set_monkeypatch([ constants.DOWN ], monkeypatch)
#     assert p.get_coords() == (0,0)
#     p.move()
#     assert p.get_coords() == (0,1)
#     set_monkeypatch( [constants.DOWN]*4, monkeypatch)
#     p.move()
#     p.move()
#     p.move()
#     assert p.get_coords() == (0,4)
#     p.move() # off other end of board
#     assert p.get_coords() == (0,4)

#     # move Right works, move off right side does not
#     set_monkeypatch([ constants.RIGHT ], monkeypatch)
#     assert p.get_coords() == (0,4)
#     p.move()
#     assert p.get_coords() == (1,4)
#     set_monkeypatch( [constants.RIGHT]*4, monkeypatch)
#     p.move()
#     p.move()
#     p.move()
#     assert p.get_coords() == (4,4)
#     p.move() # off other end of board
#     assert p.get_coords() == (4,4)

#     set_monkeypatch([ constants.UP ], monkeypatch)
#     p.move()
#     assert p.get_coords() == (4,3)    

# # ---------------------Testing Barrier---------------------------------
# def test_barrier():
#     b = Board(10,1,4)

#     # test: Barrier class symbol set/get
#     assert Barrier.get_symbol() == "X"
#     Barrier.set_symbol("*")
#     assert Barrier.get_symbol() == "*"

#     # test: instanciation, set/get origin, outpu
#     bar1 = Barrier( True )
#     assert bar1.get_is_origin() == True
#     bar1.set_is_origin( False )
#     assert bar1.get_is_origin() == False
#     assert str( bar1 ) == "*"

#     bar2 = Barrier( False )
#     assert bar2.get_is_origin() == False
#     assert str( bar2 ) == "*"

#     #reset class & test instances follow
#     Barrier.set_symbol("X")
#     assert str( bar1 ) == "X"
#     assert str( bar2 ) == "X"

# # ---------------------Testing Treasure---------------------------------
# def test_treasure(capsys):
#     # Test: class symbol set/get
#     assert Treasure.get_symbol() == "$"
#     Treasure.set_symbol("&")
#     assert Treasure.get_symbol() == "&"

#     # Test init treasure value, output (matches class symbol)
#     t1 = Treasure( 10 )
#     t2 = Treasure( 1 )

#     assert t1.get_value() == 10
#     assert t2.get_value() == 1
#     assert str( t1 ) == "& (10)"
#     assert str( t2 ) == "& (1)"

#     t1.set_value( 2 )
#     assert t1.get_value() == 2
#     assert str( t1 ) == "& (2)"

#     #reset class symbol, test instances output follows
#     Treasure.set_symbol("$")
#     assert str( t1 ) == "$ (2)"
#     assert str( t2 ) == "$ (1)"

# def test_treasure_value():
#     t1 = Treasure( 10 )
#     assert t1.get_value() == 10

#     t1.set_value(2)
#     assert t1.get_value() == 2

#     with pytest.raises(ValueError, match='Treasure value -2 is not valid. Must be integer > 0'):
#         t1.set_value(-2)
#     with pytest.raises(TypeError, match='a is not an integer'):
#         t1.set_value("a")
#     with pytest.raises(TypeError, match='9 is not an integer'):
#         t1.set_value("9")

# def test_treasure_collect(capsys):
#     b = Board(10,0,4)
#     tile = b.get_coord_tile( 2,2 )
#     assert b.get_treasure_count() == 4
#     players = b.get_players()
#     p1 = players[0]
#     p2 = b.make_new_player()    

#     # set/get treasure as expected
#     tile.clear_tile() # clear
#     assert tile.get_contents() == None
#     tile.set_to_treasure( 5 ) #DOES NOT INCREMENT, occurs in calling funct
#     b.set_treasure_count( 5 )
#     assert isinstance( tile.get_contents(), Treasure)
    

#     # test collect : correct pre-collect values
#     assert isinstance( tile.get_contents(), Treasure)
#     assert tile.get_symbol() == "$"
#     assert b.get_treasure_count() == 5
#     assert p1.get_score() == 0
#     assert p2.get_score() == 0

#     # Test: output correct when collect
#     capsys.readouterr() # clear
#     tile.get_contents().collect_treasure( b, tile, p1 )
#     capture = capsys.readouterr().out.strip() # get output & clean
#     assert capture == "remaining treasures: 4\nplayer 1 collected: 5 treasure points."

#     assert tile.get_contents() == None # treasure removed
#     assert tile.get_symbol() == "_" # tile symbol reverted to empty
#     assert b.get_treasure_count() == 4 # treasure count decremented
#     assert p1.get_score() == 5 # player score increased by treasure value
#     assert p2.get_score() == 0

# ---------------------Testing Tile---------------------------------
def test_tile_init_setget_attr():
    t1 = Tile()

    # testing initialize correct
    assert t1.get_symbol() == "_"
    assert t1.get_contents() == None
    assert str( t1 ) == '_'

    # testing set/get symbol, contents, clear
    t1.set_symbol("%")
    assert t1.get_symbol() == "%"
    assert t1.get_contents() == None
    assert str( t1 ) == "%"

    t1.set_contents( Treasure(5) )
    assert t1.get_symbol() == "$"
    assert t1.get_contents().get_value() == 5
    assert isinstance( t1.get_contents(), Treasure )
    assert str( t1 ) == "$"

    t1.clear_tile()
    assert t1.get_symbol() == "_"
    assert t1.get_contents() == None
    assert str( t1 ) == "_"     

def test_tile_setgetcheck_contents(capsys):   
    b = Board(10,0,4)
    p1 = b.get_players()[0]
    tile = b.get_coord_tile( 2,2 )
    # clear target tile & confirm
    tile.clear_tile()
    assert tile.get_contents() == None
    assert tile.get_symbol() == "_"

    # Testing starts
    tile.set_to_barrier( True )
    assert tile.check_is_treasure() == False
    assert tile.check_if_barrier() == (True, True)
    assert tile.get_contents().get_is_origin() == True
    assert tile.check_empty() == False
    assert isinstance( tile.get_contents(), Barrier)
    assert tile.get_symbol() == "X"

    assert tile.set_to_barrier( True ) == True # (returning 'is duplicate' NOT 'is success')
    assert tile.set_to_barrier( False ) == False

    tile.clear_tile()
    assert tile.check_is_treasure() == False
    assert tile.check_if_barrier() == (False, False)
    assert tile.check_empty() == True
    assert tile.get_contents() is None
    assert tile.get_symbol() == "_"

    tile.set_to_barrier( False )
    assert tile.check_is_treasure() == False
    assert tile.check_if_barrier() == (True, False)
    assert tile.get_contents().get_is_origin() == False
    assert tile.check_empty() == False
    assert isinstance( tile.get_contents(), Barrier)

    assert tile.set_to_treasure(5) == True
    tile.clear_tile()

    tile.set_to_treasure( 5 )
    assert tile.check_is_treasure() == 5
    assert tile.check_if_barrier() == (False, False)
    assert tile.check_empty() == False
    assert isinstance( tile.get_contents(), Treasure)
    assert tile.get_symbol() == "$"

    tile.set_to_player( p1 ) #DOES NOT trigger collect, etc. Handled in calling function
    assert tile.check_is_treasure() == False
    assert tile.check_if_barrier() == (False, False)
    assert tile.check_empty() == False
    assert isinstance( tile.get_contents(), Player)
    assert tile.get_symbol() == 1
    assert str(tile) == "1"

# # # ---------------------Testing Board---------------------------------
# # def test_board(capsys):
# # #   [ ]  
# #     # -------testing validation--------
# #     # Size
# #     with pytest.raises(ValueError, match='Size must be at least 5.'):
# #         b = Board(0, 0, 0)
# #     with pytest.raises(TypeError, match='Size given is not an integer'):
# #         b = Board("a", 0, 0)

# #     # Barrier Number
# #     with pytest.raises(TypeError, match='Barrier_number given needs to be an integer'):
# #         b = Board(5, "a", 0)
# #     with pytest.raises(ValueError, match='Cannot have negative barriers'):
# #         b = Board(5, -5, 0)
# #     with pytest.raises(ValueError, match='Too many barriers. Either increase board size, or decrease barrier_number'):
# #         b = Board(5, 20, 0)

# #     # Treasure Number
# #     with pytest.raises(TypeError, match='treasure_number given needs to be an integer'):
# #         b = Board(5, 1, "a")
# #     with pytest.raises(ValueError, match='Cannot have negative treasures'):
# #         b = Board(5, 1, -5)
# #     with pytest.raises(ValueError, match='Too many treasures. Either increase board size, or decrease treasure_number'):
# #         b = Board(5, 1, 20)

# #     # check_on_board()
# #     b = Board(5,1,1)
# #     assert b.check_on_board( 11, 11 ) == False
# #     assert b.check_on_board( -1, -1 ) == False
# #     assert b.check_on_board( 11, 2 ) == False
# #     assert b.check_on_board( -1, 2 ) == False
# #     assert b.check_on_board( 2, 11 ) == False
# #     assert b.check_on_board( 2, -1 ) == False
# #     assert b.check_on_board( 5, 5 ) == False
# #     assert b.check_on_board( 0, 0 ) == True
# #     assert b.check_on_board( 2, 2 ) == True
# #     assert b.check_on_board( 4, 4 ) == True

# #     # -------testing board & player creation & output --------
# #     b = Board(5, 1, 1)
# #     boardOutputArr = (b.__str__()).replace("\n", "").replace("_", "").replace(" ", "").split("n", 1)
# #     boardOutput = boardOutputArr[0]
# #     assert boardOutput.count("X") == 4
# #     assert boardOutput.count("$") == 1
# #     assert boardOutput.count("1") == 1

# #     # make 2 barrier, 5 treasure, 1 player
# #     b = Board(10, 2, 5)
# #     boardOutputArr = (b.__str__()).replace("\n", "").replace("_", "").replace(" ", "").split("n", 1)
# #     boardOutput = boardOutputArr[0]
# #     assert 6 <= boardOutput.count("X") <= 2*4 
# #     assert boardOutput.count("$") == 5
# #     assert boardOutput.count("1") == 1

# #     # make 4 barrier, 5 treasure, 1 player
# #     b = Board(10, 4, 5)
# #     boardOutputArr = (b.__str__()).replace("\n", "").replace("_", "").replace(" ", "").split("n", 1)
# #     boardOutput = boardOutputArr[0]
# #     assert 10 <= boardOutput.count("X") <= 5*4 
# #     assert boardOutput.count("$") == 5
# #     assert boardOutput.count("1") == 1
# #     # test decrement
# #     b.decrement_treasure_count()
# #     assert b.get_treasure_count() == 4
# #     b.decrement_treasure_count()
# #     assert b.get_treasure_count() == 3
# #     b.decrement_treasure_count()
# #     assert b.get_treasure_count() == 2
# #     b.decrement_treasure_count()
# #     assert b.get_treasure_count() == 1
# #     b.decrement_treasure_count()
# #     assert b.get_treasure_count() == 0
# #     # because normally the component that calls decrement checks if there are any treasures left and ends 
# #     # the game if there is not, below should never *actually* happen in the program
# #     b.decrement_treasure_count()
# #     assert b.get_treasure_count() == -1 


# #     # make empty board (+1 player, +1treasure (minimum))
# #     m = Board(5, 0, 1)
# #     boardOutputArr = (m.__str__()).replace("\n", "").replace(" ", "").split("n", 1)
# #     boardOutput = boardOutputArr[0]
# #     assert boardOutput.count("_") == 23
# #     assert boardOutput.count("X") == 0
# #     assert boardOutput.count("$") == 1
# #     assert boardOutput.count("1") == 1
# #     # test adding second player
# #     p2 = m.make_new_player()
# #     boardOutputArr = (m.__str__()).replace("\n", "").replace(" ", "").split("n", 1)
# #     boardOutput = boardOutputArr[0]
# #     assert boardOutput.count("1") == 1
# #     assert boardOutput.count("2") == 1

# #     # getting all players through get_players() not written yet.
# #     # currently should return most *recently* created player
# #     capsys.readouterr()
# #     playerList = m.get_players()
# #     p1 = playerList[0]    
# #     capture = capsys.readouterr()
# #     assert capture.out.strip() == "Current players: 1, 2"
# #     assert playerList[1] == p2

# #     p1.set_score(-30)
# #     p2.set_score(83)
# #     capsys.readouterr()
# #     score = m.report_a_player_score( p2 )
# #     capture = capsys.readouterr()
# #     assert capture.out.strip() == "player 2 score: 83"

# #     score = m.report_a_player_score( p1 )
# #     capture = capsys.readouterr()
# #     assert capture.out.strip() == "player 1 score: -30"

# #     score = m.report_player_scores()
# #     capture = capsys.readouterr()
# #     assert capture.out.strip() == "Current players: 1, 2\nplayer 1 score: -30\nplayer 2 score: 83"

# # def test_barrier_increase_wrap_probability():
# #     b = Board(5,1,1)
# #     #using the make barriers func will trigger the count error bc validation
# #     b.make_one_barrier(5) 
# #     b.make_one_barrier(5)
# #     b.make_one_barrier(5)
# #     b.make_one_barrier(5)
# #     b.make_one_barrier(5)
# #     b.make_one_barrier(5)
# #     b.make_one_barrier(5)
# #     b.make_one_barrier(5)
# #     b.make_one_barrier(5)
# #     b.make_one_barrier(5)
# #     b.make_one_barrier(5)
# #     b.make_one_barrier(5)
# #     b.make_one_barrier(5)
