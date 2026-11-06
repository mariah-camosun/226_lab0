#!/usr/bin/python3.11

from socket import socket, AF_INET, SOCK_STREAM
from sys import argv
import main
import constants
import asyncio
from struct import pack, unpack

BUF_SIZE = 1024
# HOST = '10.21.75.22' # mine
HOST = '10.21.75.14'
PORT = 12345

def play_game( sock ):
    # get & output game board

    while (True):
        cmd = get_player_commands( sock ) #, board_size )
        send_user_command( cmd, sock ) #, board_size  )
        direct_reply()
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
            return send_user_command( command.upper(), sock ) #, board_size )

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

def send_user_command( cmd, sock ): #, board_size  ):
    if cmd == constants.PRINT:
        sock.sendall( pack ( constants.REG_PACK_FLAG, constants.C_PRINT_CMD ) )
    elif cmd == constants.UP:
        send_move_cmd( constants.UP_BIN_MIN )       
    elif cmd == constants.DOWN:
        send_move_cmd( constants.DOWN_BIN_MIN )
    elif cmd == constants.LEFT:
        send_move_cmd( constants.LEFT_BIN_MIN )
    elif cmd == constants.RIGHT:
        send_move_cmd( constants.RIGHT_BIN_MIN )
    else:
        return
    # reply = get_move_reply()
    # print( reply )

def send_move_cmd( cmd ):
    cmd = cmd << constants.C_MOVE_TAIL
    print("sending:", bin(cmd))
    print("sending-packed:", pack ( constants.REG_PACK_FLAG, cmd ))
    sock.sendall( pack ( constants.REG_PACK_FLAG, cmd ) )

'''
for interpretting the command - can look at the data can always get one bite
and that will tell what to do with the rest?

but cant manipulate the ...byte 'blob' until unpacked or decoded


----once get to threading
writing our own queue, but can import it.
'''
# def get_board():
#     # send request (already binary string)
#     sock.sendall( pack ( constants.REG_PACK_FLAG, constants.C_PRINT_CMD) )
#     return get_str()

# def show_server_board():
#     board = direct_reply()
#     board_size = board.len()
#     board = prettify_board( board, board_size )
#     print( board, " size: ", board_size )
#     return board, board_size

def direct_reply():
    reply, cmd = get_reply_cmd( )

    if cmd == constants.PRINT_BOARD_CMD:
        get_board( reply )

    if cmd == constants.SCORE_CMD:
        print("score, reply:", reply)
        print("entered score")
        get_player_score( reply )
        handle_delta( reply )

    if cmd == constants.DELTA_CMD:
        handle_delta( reply )

def get_reply_cmd(  ):
    reply = sock.recv( constants.SHORT )
    print( "reply-packed: ", reply)#bin(reply) )
    reply = unpack(constants.REG_PACK_FLAG, reply)[0]
    print( "reply-unpacked: ", reply, bin(reply) )
    cmd = reply >> ( constants.BYTE_SIZE - constants.S_CMD_SIZE )

    print( "reply:", reply, "bin: ", bin(reply) )
    print( "cmd:", cmd, "bin: ", bin(cmd) )
    return reply, cmd

def get_str( size ):    # recieve, decode & pass on
    string = sock.recv( size * size )
    decoded_reply = string.decode()
    return decoded_reply

def handle_delta( reply ):
    print("delta, reply:", reply)
    get_delta_opts( reply )
# maybe not the best way to handle this?
    print("delta no 2")
    reply_d2, cmd_d2 = get_reply_cmd( )
    get_delta_opts( reply_d2 )
    print("delta w score following")
    reply_score, cmd_score = get_reply_cmd( )
    get_player_score( reply_score )

def get_delta_opts( reply ):
    part2 = sock.recv( constants.SHORT )
    part2 = unpack(constants.REG_PACK_FLAG, part2)[0]
    print("p1:", bin(reply), ", p2:", bin(part2) )

    reply = reply << constants.BYTE_SIZE
    reply += part2
    print( "combo:", bin(reply))

    row = ( reply & constants.S_ROW_MASK ) >> constants.S_ROW_TAIL_SIZE
    col = ( reply & constants.S_COL_MASK ) >> constants.S_COL_TAIL_SIZE
    contents = ( reply & constants.TILE_MASK )
    print( "row:", row, ", col:", col, ", contents:", bin(contents))

def get_player_score( reply ):
        score = ( reply & constants.S_SCORE_MASK ) >> constants.S_SCORE_TAIL
        print( "Player score:", score )

def get_board( reply ):
        size = ( reply & constants.S_PRINT_OPT_MASK ) >> constants.S_PRINT_TAIL
        print("board size:", size)
        board = get_str( size )
        print( board )
        # print( prettify_board( board, size ) ) 

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
# create connection
sock.connect(( HOST, PORT ))
# data = argv[1].encode('utf-8')

print( 'Client:', sock.getsockname())

play_game( sock )

