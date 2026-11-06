#!/usr/bin/python3.11

from socket import socket, AF_INET, SOCK_STREAM
from sys import argv
import main
import constants
import asyncio
from struct import pack, unpack

BUF_SIZE = 1024
HOST = '10.21.75.22'
PORT = 12345

def play_game( sock ):
    # get & output game board

    while (True):
        cmd = get_player_commands( sock ) #, board_size )
        direct_user_command( cmd, sock ) #, board_size  )
        get_reply()
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
        pass
    elif cmd == constants.UP:
        sock.sendall( pack ( constants.REG_PACK_FLAG, constants.UP_BIN ) )
    elif cmd == constants.DOWN:
        sock.sendall( pack ( constants.REG_PACK_FLAG, constants.DOWN_BIN ) )
    elif cmd == constants.LEFT:
        sock.sendall( pack ( constants.REG_PACK_FLAG, constants.LEFT_BIN ) )
    elif cmd == constants.RIGHT:
        sock.sendall( pack ( constants.REG_PACK_FLAG, constants.RIGHT_BIN ) )
    else:
        return
    # reply = get_move_reply()
    # print( reply )

'''
for interpretting the command - can look at the data can always get one bite
and that will tell what to do with the rest?

but cant manipulate the ...byte 'blob' until unpacked or decoded


----once get to threading
writing our own queue, but can import it.


'''
# def get_board():
#     # send request (already binary string)
#     sock.sendall( pack ( constants.REG_PACK_FLAG, constants.PRINT_CMD) )
#     return get_str()

# def show_server_board():
#     board = get_reply()
#     board_size = board.len()
#     board = prettify_board( board, board_size )
#     print( board, " size: ", board_size )
#     return board, board_size



def get_str( size ):    # recieve, decode & pass on
    string = sock.recv( size * size )
    decoded_reply = string.decode()
    return decoded_reply

def get_reply():
    reply, cmd = get_reply_cmd( )

    if cmd == constants.PRINT_BOARD_CMD:
        get_board( reply )

    if cmd == constants.SCORE_CMD:
        get_player_score( reply )

    if cmd == constants.DELTA_CMD:
        get_delta_opts( reply )
# maybe not the best way to handle this?
        print("delta no 2")
        reply_d2, cmd_d2 = get_reply_cmd( )
        get_delta_opts( reply_d2 )
        print("delta w score following")
        reply_score, cmd_score = get_reply_cmd( )
        get_player_score( reply_score )


def get_reply_cmd(  ):
    reply = sock.recv( constants.SHORT )
    reply = unpack(constants.REG_PACK_FLAG, reply)[0]
    cmd = reply >> ( constants.C_OPT_SMALL )

    print( reply, "bin: ", bin(reply) )
    print( cmd, "bin: ", bin(cmd) )
    return reply, cmd

def get_delta_opts( reply ):
    part2 = sock.recv( constants.SHORT )
    part2 = unpack(constants.REG_PACK_FLAG, part2)[0]
    print("p1:", bin(reply), ", p2:", bin(part2) )

    reply = reply << constants.BYTE_SIZE
    reply += part2
    print( "combo:", bin(reply))

    row = ( reply & constants.C_ROW_MASK ) >> constants.C_ROW_TAIL_SIZE
    col = ( reply & constants.C_COL_MASK ) >> constants.C_COL_TAIL_SIZE
    contents = ( reply & constants.TILE_MASK )
    print( "row:", row, ", col:", col, ", contents:", bin(contents))

def get_player_score( reply ):
        score = ( reply & constants.C_SIZE_MASK )
        print( "Player score:", score )

def get_board( reply ):
        size = ( reply & constants.C_SIZE_MASK ) >> constants.C_PRINT_TAIL_SIZE
        print("board size:", size)
        print( prettify_board( get_str( size ) ) ) 

# def get_move_reply():
    # delta1 = sock.recv( BUF_SIZE )
    # delta1 = unpack(constants.LONG_PACK_FLAG, delta1)[0]
    # print( bin(delta1) )

    # # NEED TO BE ABLE TO IDENTIFY COMMAND BEFORE DECODING
    # if ( reply << constants.b):

    # delta2 = sock.recv( BUF_SIZE )
    # delta2 = unpack(constants.LONG_PACK_FLAG, delta2)[0]
    # print( bin(delta2) )

    # score = sock.recv( BUF_SIZE )
    # score = unpack(constants.REG_PACK_FLAG, score)[0]
    # print( bin(score) )


# def get_response( ): #board_size ):
#     reply = sock.recv( BUF_SIZE )
#     # bits = reply.len()
#     if bits == 8: # recieve score cmd
#         data = main.unpack_data()
#         data = unpack(constants.REG_PACK_FLAG, reply)
#         # get_score()
#     elif bits == 16: # recieve delta cmd
#         data = unpack(constants.LONG_PACK_FLAG, reply)

    # elif bits >= board_size*board_size: #???? how pickup string....
    #        data = get_str()
    # else:
    #     print( "incorrect number of bits")
    
    # return data


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



def prettify_board( board, board_size ):
    newBoard = ''
    col_counter = 0
    for c in board:
        newBoard += c
        col_counter += 1
        if col_counter == board_size:
            newBoard += c
        else:
            newBoard += c
            newBoard += ' '            
    # for c in board:
    #     if c == '\n':
    #         newBoard += c
    #     else:
    #         newBoard += c
    #         newBoard += ' '
    return newBoard

sock = socket(AF_INET, SOCK_STREAM)
# with socket(AF_INET, SOCK_STREAM) as sock:
    # create connection
sock.connect(( HOST, PORT ))
# data = argv[1].encode('utf-8')

print( 'Client:', sock.getsockname())

play_game( sock )