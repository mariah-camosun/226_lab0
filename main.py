from Board import Board
b = Board(10,5,4)
print(b)
while ( b.getTreasureCount() > 0 ):
    players = b.getPlayers()
    players.move( )
    print(b)