from Board import Board
b = Board(10,5,4)
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print(b)
while ( b.getTreasureCount() > 0 ):
    players = b.getPlayers()
    for player in players:
        player.move( )
    print(b)
    
print("No more treasure to collect!")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")