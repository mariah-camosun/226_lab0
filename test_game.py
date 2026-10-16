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

def test_player():
    b = Board(10,1,4)

    p = Player(2, 1, b, 3) #column row (x,y), og given code was row column
    assert p.get_coords() == (2,1)
    assert p.get_score() == 3
    p.add_score(10)
    assert p.get_score() == 13
    p.set_score(6)
    assert p.get_score() == 6
    p.move(constants.UP) #, constants.BLANK)
    assert p.get_coords() == (2, 0)

    # testing score & score reporting
    # no validate score, as set is always set by the program
    m = Board(5, 0, 1)
    assert Player.get_player_count() == 1

    playerList = m.get_players()
    p1 = playerList[0]
    p2 = m.make_new_player()
    assert Player.get_player_count() == 2
    assert p1.get_score() == 0
    assert p2.get_score() == 0

    p1.set_score(-30)
    p2.set_score(83)
    assert p1.get_score() == -30
    assert p2.get_score() == 83

    p1.add_score(30)
    p2.add_score(10)
    assert p1.get_score() == 0
    assert p2.get_score() == 93
    p2.add_score(-100)
    assert p2.get_score() == -7

    #only called by move, so no validation at this level
    p1.set_coords(2,1)
    assert p1.get_coords() == (2,1)
    assert p1.validate_coords( 0, 0 ) == True
    assert p1.validate_coords( 3, 3 ) == True
    assert p1.validate_coords( 4, 4 ) == True
    with pytest.raises(ValueError):
        p1.validate_coords( -1, 3 )
    with pytest.raises(ValueError):
        p1.validate_coords( -1, -1 )
    with pytest.raises(ValueError):
        p1.validate_coords( 3, -1 )
    with pytest.raises(ValueError):
        p1.validate_coords( 3, 11 )
    with pytest.raises(ValueError):
        p1.validate_coords( 11, 11 )
    with pytest.raises(ValueError):
        p1.validate_coords( 11, 3 )

    #no set name, symbol
    assert p1.get_name() == 1
    assert p1.get_symbol() == "1"
    assert str(p1) == "1"

    assert p2.get_name() == 2
    assert p2.get_symbol() == "2"
    assert str(p2) == "2"

    Player.set_player_count( 99 )
    assert Player.get_player_count() == 99 
    Player.set_player_count( 2 )

    assert p1.get_board() == m
    assert p2.get_board() == m

    # test movement

def set_monkeypatch( input_values, monkeypatch ):
    user_inputs = iter( input_values )
    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))

def test_getMovePlayer( monkeypatch ): # under 'player'cover
    b = Board(5,0,1)
    p1 = Player( 3,3,b )

    set_monkeypatch(["a", "uu", 1, "D"], monkeypatch)
    p1.get_move_direction( ) == "D"

    set_monkeypatch(["U", "u", "D", "d", "L", "l", "R", "r"], monkeypatch)
    assert p1.get_move_direction() == "U"
    assert p1.get_move_direction() == "U"
    assert p1.get_move_direction() == "D"
    assert p1.get_move_direction() == "D"
    assert p1.get_move_direction() == "L"
    assert p1.get_move_direction() == "L"
    assert p1.get_move_direction() == "R"
    assert p1.get_move_direction() == "R"

def test_movePlayer(monkeypatch): # under 'player'
    b = Board(5,0,1)

    # make sure that tiles are free to start
    b.get_coord_tile(0,0).clear_tile()
    b.get_coord_tile(0,1).clear_tile()
    b.get_coord_tile(0,2).clear_tile()
    b.get_coord_tile(0,3).clear_tile()
    b.get_coord_tile(0,4).clear_tile()
    b.get_coord_tile(1,4).clear_tile()
    b.get_coord_tile(2,4).clear_tile()
    b.get_coord_tile(3,4).clear_tile()
    b.get_coord_tile(4,4).clear_tile()

    # activeTile
    b1 = b.get_coord_tile( 1, 2 ).set_to_barrier(True) #col,row
    t1 = b.get_coord_tile( 0, 0 ).set_to_treasure( 1 )

    p = Player(1, 1, b, 0) #column row (x,y), og given code was row column 
    assert p.get_coords() == (1,1)
    assert p.get_score() == 0

    p.move( "D" ) # trying to move into a barrier
    assert p.get_coords() == (1,1)

    p.move( "U" )
    assert p.get_coords() == (1,0)
    p.move( "U" ) # moving up off the board
    assert p.get_coords() == (1,0)

    p.move( "L" ) # moving into treasure. includes test that it collects
    assert p.get_coords() == (0,0)
    assert p.get_score() == 1
    p.move( "L" ) # attempting to move off board
    assert p.get_coords() == (0,0)

    p.move( "D" )
    assert p.get_coords() == (0,1)
    p.move( "D" )
    p.move( "D" )
    p.move( "D" )
    assert p.get_coords() == (0,4)
    p.move( "D" ) # off other end of board
    assert p.get_coords() == (0,4)

    p.move( "R" )
    assert p.get_coords() == (1,4)
    p.move( "R" )
    p.move( "R" )
    p.move( "R" )
    assert p.get_coords() == (4,4)
    p.move( "R" ) # off other end of board
    assert p.get_coords() == (4,4)

    set_monkeypatch(["u"], monkeypatch)
    p.move()
    assert p.get_coords() == (4,3)    

def test_barrier():
    b = Board(10,1,4)

    assert Barrier.get_symbol() == "X"
    Barrier.set_symbol("*")
    assert Barrier.get_symbol() == "*"

    bar1 = Barrier( True )
    assert bar1.get_is_origin() == True
    bar1.set_is_origin( False )
    assert bar1.get_is_origin() == False
    assert str( bar1 ) == "*"

    bar2 = Barrier( False )
    assert bar2.get_is_origin() == False
    assert str( bar2 ) == "*"

    #reset
    Barrier.set_symbol("X")
    assert str( bar1 ) == "X"
    assert str( bar2 ) == "X"

def test_barrier_increase_wrap_probability():
    b = Board(5,1,1)
    #using the make barriers func will trigger the count error bc validation
    b.make_one_barrier(5) 
    b.make_one_barrier(5)
    b.make_one_barrier(5)
    b.make_one_barrier(5)
    b.make_one_barrier(5)
    b.make_one_barrier(5)
    b.make_one_barrier(5)
    b.make_one_barrier(5)
    b.make_one_barrier(5)
    b.make_one_barrier(5)
    b.make_one_barrier(5)
    b.make_one_barrier(5)
    b.make_one_barrier(5)

def test_treasure(capsys):
    assert Treasure.get_symbol() == "$"
    Treasure.set_symbol("&")
    assert Treasure.get_symbol() == "&"

    t1 = Treasure( 10 )
    t2 = Treasure( 1 )

    assert t1.get_value() == 10
    assert t2.get_value() == 1
    assert str( t1 ) == "& (10)"
    assert str( t2 ) == "& (1)"

    #reset
    Treasure.set_symbol("$")
    assert str( t1 ) == "$ (10)"
    assert str( t2 ) == "$ (1)"

    t1.set_value(2)
    assert t1.get_value() == 2
    with pytest.raises(ValueError, match='Treasure value -2 is not valid. Must be integer > 0'):
        t1.set_value(-2)
    with pytest.raises(TypeError, match='a is not an integer'):
        t1.set_value("a")
    with pytest.raises(TypeError, match='9 is not an integer'):
        t1.set_value("9")

    #Testing collect 
    b = Board(10,0,4)
    tile = b.get_coord_tile( 2,2 )
    tile.set_to_treasure( 5 ) #DOES NOT INCLUDE INCREMENT
    b.set_treasure_count( 5 ) 
    t3 = tile.get_contents()

    assert isinstance( t3, Treasure)
    capsys.readouterr()
    players = b.get_players()
    p1 = players[0]
    t3.collect_treasure( b, tile, p1 )
    capture = capsys.readouterr()

    assert capture.out.strip() == "Current players: 1\nremaining treasures: 4\nplayer 1 collected: 5 treasure points."

    assert tile.get_contents() == None
    assert tile.get_symbol() == "_"
    assert b.get_treasure_count() == 4
    assert p1.get_score() == 5

def test_tile(capsys):
    t1 = Tile()
    
    assert t1.get_symbol() == "_"
    t1.set_symbol("'")
    assert t1.get_symbol() == "'"

    #Testing check contents 
    b = Board(10,0,4)
    tile = b.get_coord_tile( 2,2 )
    tile.clear_tile()
    p1 = b.get_players()[0]

    assert str( tile ) == '_'
    tile.set_symbol("%")
    assert tile.get_symbol() == '%'
    assert str( tile ) == '%'

    tile.set_contents( p1 )
    assert tile.get_contents() == p1
    tile.clear_tile()

    tile.set_to_barrier( True )
    assert tile.check_is_treasure() == False
    assert tile.check_if_barrier() == (True, True)
    assert tile.check_empty() == False
    assert isinstance( tile.get_contents(), Barrier)
    assert tile.get_symbol() == "X"

    # with pytest.raises(ValueError, match='Treasure value -2 is not valid. Must be integer > 0'):
    assert tile.set_to_barrier( True ) == True
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

    tile.set_to_player( p1 ) #does not trigger a collect or anything else, just teh sets
    assert tile.check_is_treasure() == False
    assert tile.check_if_barrier() == (False, False)
    assert tile.check_empty() == False
    assert isinstance( tile.get_contents(), Player)
    assert tile.get_symbol() == 1
    assert str(tile) == "1"

def test_board(capsys):
#   [ ]  
    # -------testing validation--------
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

    # check_on_board()
    b = Board(5,1,1)
    assert b.check_on_board( 11, 11 ) == False
    assert b.check_on_board( -1, -1 ) == False
    assert b.check_on_board( 11, 2 ) == False
    assert b.check_on_board( -1, 2 ) == False
    assert b.check_on_board( 2, 11 ) == False
    assert b.check_on_board( 2, -1 ) == False
    assert b.check_on_board( 5, 5 ) == False
    assert b.check_on_board( 0, 0 ) == True
    assert b.check_on_board( 2, 2 ) == True
    assert b.check_on_board( 4, 4 ) == True

    # -------testing board & player creation & output --------
    b = Board(5, 1, 1)
    boardOutputArr = (b.__str__()).replace("\n", "").replace("_", "").replace(" ", "").split("n", 1)
    boardOutput = boardOutputArr[0]
    assert boardOutput.count("X") == 4
    assert boardOutput.count("$") == 1
    assert boardOutput.count("1") == 1

    # make 2 barrier, 5 treasure, 1 player
    b = Board(10, 2, 5)
    boardOutputArr = (b.__str__()).replace("\n", "").replace("_", "").replace(" ", "").split("n", 1)
    boardOutput = boardOutputArr[0]
    assert 6 <= boardOutput.count("X") <= 2*4 
    assert boardOutput.count("$") == 5
    assert boardOutput.count("1") == 1

    # make 4 barrier, 5 treasure, 1 player
    b = Board(10, 4, 5)
    boardOutputArr = (b.__str__()).replace("\n", "").replace("_", "").replace(" ", "").split("n", 1)
    boardOutput = boardOutputArr[0]
    assert 10 <= boardOutput.count("X") <= 5*4 
    assert boardOutput.count("$") == 5
    assert boardOutput.count("1") == 1
    # test decrement
    b.decrement_treasure_count()
    assert b.get_treasure_count() == 4
    b.decrement_treasure_count()
    assert b.get_treasure_count() == 3
    b.decrement_treasure_count()
    assert b.get_treasure_count() == 2
    b.decrement_treasure_count()
    assert b.get_treasure_count() == 1
    b.decrement_treasure_count()
    assert b.get_treasure_count() == 0
    # because normally the component that calls decrement checks if there are any treasures left and ends 
    # the game if there is not, below should never *actually* happen in the program
    b.decrement_treasure_count()
    assert b.get_treasure_count() == -1 


    # make empty board (+1 player, +1treasure (minimum))
    m = Board(5, 0, 1)
    boardOutputArr = (m.__str__()).replace("\n", "").replace(" ", "").split("n", 1)
    boardOutput = boardOutputArr[0]
    assert boardOutput.count("_") == 23
    assert boardOutput.count("X") == 0
    assert boardOutput.count("$") == 1
    assert boardOutput.count("1") == 1
    # test adding second player
    p2 = m.make_new_player()
    boardOutputArr = (m.__str__()).replace("\n", "").replace(" ", "").split("n", 1)
    boardOutput = boardOutputArr[0]
    assert boardOutput.count("1") == 1
    assert boardOutput.count("2") == 1

    # getting all players through get_players() not written yet.
    # currently should return most *recently* created player
    capsys.readouterr()
    playerList = m.get_players()
    p1 = playerList[0]    
    capture = capsys.readouterr()
    assert capture.out.strip() == "Current players: 1, 2"
    assert playerList[1] == p2

    p1.set_score(-30)
    p2.set_score(83)
    capsys.readouterr()
    score = m.report_a_player_score( p2 )
    capture = capsys.readouterr()
    assert capture.out.strip() == "player 2 score: 83"

    score = m.report_a_player_score( p1 )
    capture = capsys.readouterr()
    assert capture.out.strip() == "player 1 score: -30"

    score = m.report_player_scores()
    capture = capsys.readouterr()
    assert capture.out.strip() == "Current players: 1, 2\nplayer 1 score: -30\nplayer 2 score: 83"

    