from Board import Board
    # TODO
    # [x] rework Tile.setBarrierTile() -- too much duplication
    # [ ] update draw.io class diagram to contain all functions
    # [x] should probably rename the Player.get/set etc from number to name (not technically a req't)
    # [~] fix functions that pass in unneccessary variables (eg. Board.Boardsize)
    # [x] CHANGE EVERYTHING to snake case (function names, variables)

b = Board(10,5,4)
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print(b)
while ( b.get_treasure_count() > 0 ):
    players = b.get_players()
    for player in players:
        player.move( )
    print(b)
    
print("No more treasure to collect!")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")