from Board import Board
    # TODO
    # [~] fix functions that pass in unneccessary variables (eg. Board.Boardsize)

# LAB 4
# Modify main.py so that
    # ??? [ ] it creates a 10 x 10 board with max barriers and treasures and 
            # ??? [ ] prints out the board and player score
    # [x] it accepts local TCP connections on port 12345
    #       [ ] and non-local 
    # [x] it prints out every received byte in hexadecimal form
    # [ ] it implements the protocol shown in the figures on the next page
            # [x] if the create board command is received, a board of size x size is created with the maximum number of barriers and treasures, 
                # [x] and the entire board string is sent back to the client
            # [ ] if a motion command is received, the command is passed to the board, and two delta messages are sent back to the
                # client, representing the origin tile's index and value and then the destination tile's index and value; subsequently, the score
                # message is sent
    # [~] it ignores incoming messages that do not comply with the protocol
    # [ ] it closes the connection after every message
    # [ ] it prints out the board and score after every command is executed
    # [ ] it is refactored to use functions throughout
    # [ ] it does not crash

#!/usr/bin/python3.11
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from struct import pack, unpack
from threading import Thread, current_thread, Semaphore

BUF_SIZE = 1024
HOST = ''
PORT = 12345
SHORT = 1 # num bytes
# CMD_LEN = [1,2] # num bytes

def recieve_buffer_data( sc, size ): # recieves data in bitecode format
    data = b''
    while len(data) < size:
        curr_data = sc.recv(size - len(data))
        if curr_data == b'': #closed connection
            print('closing connection')
            return data
        data += curr_data
    return data

def unpack_data( sc ):
    print('Client:', sc.getpeername()) # Client IP and port
    data = recieve_buffer_data( sc, SHORT )
    # print( "length of data", len(data), "short", SHORT )

    # check correct length, fix, or ignore by size.
    if ( len(data) != SHORT ): # not in CMD_LEN:
        return
    # elif ( len( data ) < SHORT ): # if recieved < required number bytes, pad 
    data = data.rjust( 2, b'\x00' )
    print( data )

    # requires length to be correct!            
    # print( "recieved data (pre-unpack):", data ) # prints as recieved, in hex format
    unpacked_data = unpack( '!H' , data)[0]
    # print( "server data (unpacked):", unpacked_data ) # prints binary number as decimal
    return unpacked_data

def interpret_bin( data ):
    print( " entered interpret", "Data is:", data, ", in binary:", bin(data))
    # testing first three bits
    cmd = data >> 5
    print( "cmd",  cmd, "opt", bin( (data << 3) >> 3 ) )

    # if first three unset, create board, of size 'opt'
    if ( cmd == 0 ):
        opt = ( data << 3 ) >> 4
        b = Board.new_max_board( opt )
        print( b.get_barrier_count(), b.get_treasure_count(), b.get_tile_count() )
        print( "cmd",  cmd, "opt", bin(opt), opt )
        print( b )
    #otherwise its a move command, direction is one of 4
    else:
        if ( ( cmd & 2**2 > 0 ) and ( cmd & 2**1 > 0 ) ): # 111
            print( "move right")
        elif ( ( cmd & 2**2 > 0 ) and ( cmd & 2**1 == 0 ) ): # 110
            print( "move left")
        elif ( ( cmd & 2**2 == 0 ) and ( cmd & 2**1 > 0 ) ): # 101
            print( "move down")
        elif ( ( cmd & 2**2 == 0 ) and ( cmd & 2**1 == 0 ) ): # 100
            print( "move up")
    return b


        
def send_data( unpacked_data ):
        # pack as unsigned int, and send to client
        as_hex = pack( '!H', unpacked_data )
        sc.sendall( as_hex )
        print( "send to client data (packed into bits):", as_hex )

with socket(AF_INET, SOCK_STREAM) as sock: # TCP socket
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # Details later
    sock.bind((HOST, PORT)) # Claim messages sent to port "PORT"
    sock.listen(1) # Server only supports a single 3-way handshake at a time

    print('Server:', sock.getsockname()) # Server IP and port
    
    while True:
        sc, _ = sock.accept() # Wait until a connection is established
        # Thread(target=add_to_total, args=(sc,)).start()
        with sc: 
            data = unpack_data( sc )
            b = interpret_bin( data )
            send_data( data )
            sc.sendall( str(b).encode('utf-8') )

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