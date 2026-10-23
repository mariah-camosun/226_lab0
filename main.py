from Board import Board
    # TODO
    # [~] fix functions that pass in unneccessary variables (eg. Board.Boardsize)

# LAB 4
# Modify main.py so that
    # [x] it creates a 10 x 10 board with max barriers and treasures and 
            # [x] prints out the board and player score
    # [x] it accepts local TCP connections on port 12345
    #       [ ] and non-local 
    # [x] it prints out every received byte in hexadecimal form
    # [ ] it implements the protocol shown in the figures on the next page
            # [ ] if the create board command is received, a board of size x size is created with the maximum number of barriers and
                # treasures, and the entire board string is sent back to the client
            # [ ] if a motion command is received, the command is passed to the board, and two delta messages are sent back to the
                # client, representing the origin tile's index and value and then the destination tile's index and value; subsequently, the score
                # message is sent
    # [ ] it ignores incoming messages that do not comply with the protocol
    # [x] it closes the connection after every message
    # [ ] it prints out the board and score after every command is executed
    # [ ] it is refactored to use functions throughout
    # [ ] it does not cras

#!/usr/bin/python3.11
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from struct import pack, unpack
from threading import Thread, current_thread, Semaphore

BUF_SIZE = 1024
HOST = ''
PORT = 12345
SHORT = 2

total = 0

def recieve_data( sc, size ): # recieves data in bitecode format
    data = b''
    while len(data) < size:
        curr_data = sc.recv(size - len(data))
        if curr_data == b'': #closed connection
            return data
        data += curr_data
    return data

def add_to_total( sc ):
    global total
    with sc: 
        print('Client:', sc.getpeername()) # Client IP and port
        data = recieve_data( sc, SHORT )
        if len(data) != SHORT:
            return
        unpacked_data = unpack( '!H' , data)[0]
        # print(currentThread)
        # print( 'unpacked:', unpacked_data )
        as_hex = pack( '!I', unpacked_data )
        sc.sendall( as_hex )
        print( as_hex )

# def recieve_data(): # recieve in str format
#     data = sc.recv(BUF_SIZE) # recvfrom not needed since address known
#     decoded_data = data.decode('utf-8') # also doesnt work if nothing in ()

#     print('Bites recieved (hex), pre "decode":', data) 
#     print(decoded_data) 

#     sc.sendall(data) # Client IP and port implicit due to accept call

with socket(AF_INET, SOCK_STREAM) as sock: # TCP socket
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # Details later
    sock.bind((HOST, PORT)) # Claim messages sent to port "PORT"
    sock.listen(1) # Server only supports a single 3-way handshake at a time

    print('Server:', sock.getsockname()) # Server IP and port
    
    while True:
        sc, _ = sock.accept() # Wait until a connection is established
        # Thread(target=add_to_total, args=(sc,)).start()
        add_to_total( sc )

            # data = sc.recv(BUF_SIZE) # recvfrom not needed since address known
            # # print('Bites recieved (hex), pre "decode":', data) 
            # decoded_data = data.decode('utf-8') # also doesnt work if nothing in ()
            # # print(decoded_data) 

            # # interpret_data(data, decoded_data)

            # sc.sendall(data) # Client IP and port implicit due to accept call

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