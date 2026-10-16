from Board import Board
    # TODO
    # [x] rework Tile.setBarrierTile() -- too much duplication
    # [ ] update draw.io class diagram to contain all functions
    # [x] should probably rename the Player.get/set etc from number to name (not technically a req't)
    # [~] fix functions that pass in unneccessary variables (eg. Board.Boardsize)
    # [x] CHANGE EVERYTHING to snake case (function names, variables)

# LAB 4
# Modify main.py so that
    # [x] it creates a 10 x 10 board with max barriers and treasures and 
            # [x] prints out the board and player score
    # [ ] it accepts local and non-local TCP connections on port 12345
    # [ ] it prints out every received byte in hexadecimal form
    # [ ] it implements the protocol shown in the figures on the next page
            # [ ] if the create board command is received, a board of size x size is created with the maximum number of barriers and
                # treasures, and the entire board string is sent back to the client
            # [ ] if a motion command is received, the command is passed to the board, and two delta messages are sent back to the
                # client, representing the origin tile's index and value and then the destination tile's index and value; subsequently, the score
                # message is sent
    # [ ] it ignores incoming messages that do not comply with the protocol
    # [ ] it closes the connection after every message
    # [ ] it prints out the board and score after every command is executed
    # [ ] it is refactored to use functions throughout
    # [ ] it does not cras

#!/usr/bin/python3.11
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
BUF_SIZE = 1024
HOST = ''
PORT = 12345

with socket(AF_INET, SOCK_STREAM) as sock: # TCP socket
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # Details later
    sock.bind((HOST, PORT)) # Claim messages sent to port "PORT"
    sock.listen(1) # Server only supports a single 3-way handshake at a time
    print('Server:', sock.getsockname()) # Server IP and port
    while True:
        sc, _ = sock.accept() # Wait until a connection is established
        with sc:
            print('Client:', sc.getpeername()) # Client IP and port
            data = sc.recv(BUF_SIZE) # recvfrom not needed since address known
            decoded_data = data.decode()
            print(decoded_data)
            sc.sendall(data) # Client IP and port implicit due to accept call

b = Board(10,5,5)
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print(b)
while ( b.get_treasure_count() > 0 ):
    b.report_player_scores()

    players = b.get_players()
    for player in players:
        player.move( )
    print(b)
    
b.report_player_scores()
print("No more treasure to collect!")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")