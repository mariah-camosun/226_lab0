#!/usr/bin/python3.11

from socket import socket, AF_INET, SOCK_STREAM
from sys import argv
import main
import constants
import asyncio
from struct import pack, unpack

BUF_SIZE = 1024
# DELTA_BUF_SIZE = 
# DISPLAY_BUF_SIZE = 
HOST = '10.21.75.22'
PORT = 12345

# global board_size
# board_size = 10

def play_game( sock ):
    # get & output game board


    while (True):
        cmd = get_player_commands( sock ) #, board_size )
        direct_user_command( cmd, sock ) #, board_size  )
        get_response()
        # print updated board
        # print updated score

def get_player_commands( sock ): #, board_size ):    
    '''
    Prompt user for command: print or move direction.
    Repeat until a valid option is entered

    :return: str, command letter
    '''
    while (True):
        try:
            command = input( "Choose one of: re-print board (p), or move up(u), down(d), left(l), right(r)" )
            print(f"command entered: {command}")            
            validate_command( command )
        except ValueError:
            print(f"Invalid entry, choose one of: P, U, D, L, R") # will also accept lower case
            # raise
            continue
        else:
            return direct_user_command( command.upper(), sock ) #, board_size )

def validate_command( cmd ):
    if isinstance( cmd, int):
        raise ValueError
    else:
        cmd = cmd.upper()

        if not ( cmd == constants.PRINT or cmd == constants.UP or 
                cmd == constants.DOWN or cmd == constants.LEFT or 
                cmd == constants.RIGHT ):
            raise ValueError                
        else:
            return True

def direct_user_command( cmd, sock ): #, board_size  ):
    if cmd == constants.PRINT:
        get_board()
    elif cmd == constants.UP:
        sock.sendall( pack ( constants.REG_PACK_FLAG, constants.UP_BIN ) )
        get_move_reply()
    elif cmd == constants.DOWN:
        sock.sendall( pack ( constants.REG_PACK_FLAG, constants.DOWN_BIN ) )
    elif cmd == constants.LEFT:
        sock.sendall( pack ( constants.REG_PACK_FLAG, constants.LEFT_BIN ) )
    elif cmd == constants.RIGHT:
        sock.sendall( pack ( constants.REG_PACK_FLAG, constants.RIGHT_BIN ) )
    else:
        return
    reply = get_move_reply()
    # print( reply )

'''
for interpretting the command - can look at the data can always get one bite
and that will tell what to do with the rest?

but cant manipulate the ...byte 'blob' until unpacked or decoded


----once get to threading
writing our own queue, but can import it.


'''
def get_board():
    # send request (already binary string)
    sock.sendall( pack ( constants.REG_PACK_FLAG, constants.PRINT_CMD) )
    return get_str()

def show_server_board():
    board = get_board()
    board_size = board.len()
    board = prettify_board( board )
    print( board )

def get_move_reply():
    delta1 = sock.recv( BUF_SIZE )
    delta1 = unpack(constants.LONG_PACK_FLAG, delta1)[0]
    print( bin(delta1) )

    delta2 = sock.recv( BUF_SIZE )
    delta2 = unpack(constants.LONG_PACK_FLAG, delta2)[0]
    print( bin(delta2) )

    score = sock.recv( BUF_SIZE )
    score = unpack(constants.REG_PACK_FLAG, score)[0]
    print( bin(score) )


def get_response( ): #board_size ):
    reply = sock.recv( BUF_SIZE )
    # bits = reply.len()
    if bits == 8: # recieve score cmd
        data = main.unpack_data()
        data = unpack(constants.REG_PACK_FLAG, reply)
        # get_score()
    elif bits == 16: # recieve delta cmd
        data = unpack(constants.LONG_PACK_FLAG, reply)

    # elif bits >= board_size*board_size: #???? how pickup string....
    #        data = get_str()
    else:
        print( "incorrect number of bits")
    
    return data


# def get_delta():
#     reply = get_response()

#     unpacked = unpack('!H', reply)
#     return unpacked

# def get_score():
#     reply = get_response()

#     unpacked = unpack('!B', reply)
#     return unpacked

# def get_cmd():
#     reply = get_response()

#     unpacked = main.unpack_data( reply )
#     return unpacked

def get_str():    # recieve, decode & pass on
    reply = get_response()

    decoded_reply = reply.decode()
    return decoded_reply

def prettify_board( board ):
    newBoard = ''
    for c in board:
        if c == '\n':
            newBoard += c
        else:
            newBoard += c
            newBoard += ' '
    return newBoard

sock = socket(AF_INET, SOCK_STREAM)
# with socket(AF_INET, SOCK_STREAM) as sock:
    # create connection
sock.connect(( HOST, PORT ))
# data = argv[1].encode('utf-8')

print( 'Client:', sock.getsockname())

play_game( sock )