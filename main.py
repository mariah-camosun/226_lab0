from Board import Board
# Requirements
# [ ] contains only: import; b = Board( 10,5,4 ); print(b)
#       [ ] unclear if section B (Player Class added) can then incl more here
# [ ] run mult times to confirm that:
#       [ ] 4 treasures randomly assigned
#       [ ] 5 barriers randomly assigned - can parially overlap, wrap edges
# [ ] conf program still runs : PRE ADDING PLAYER 1 - find commit
# [ ] commit & push to GitHub, share w instructor
# [ ] CHANGE EVERYTHING to snake case (function names, variables)

# ~~~ Part C ~~~ 'Complete the game'
# repeatedly:
#       [ ] print out board
#       [ ] prompt user for direction
#       [ ] on error, print error message, AND continue prompting
#### ~~~ ~~~ while in the 'main, repeatedly' section, look more like move rules, cloned there ~~~ ~~~
####       [ ] if given tile contains treasure, 
####               [ ] replace treasure with blank
####               [ ] add 1 to the Player's score
####       [ ] if the player would move into a barrier or off the board, do not move

# ~~~ Part C ~~~ 
# general/copy to all [x] copy reqts to ea class
# [ ] add detailed header comments to ALL methods 
# [ ] make sure ALL instance variables of classes not accessed directly by outside code
# [x] abv re-perspective. This class does NOT directly access any outside instance variables
#          - eg. bad: board.player.row += 1
#          - instead: board.move('D'), which will in turn call self.player.move('D')

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