#!/usr/bin/python3.11

from socket import socket, AF_INET, SOCK_STREAM
from sys import argv
import main
import constants
import asyncio
from struct import pack, unpack

BUF_SIZE = 1024
# HOST = '10.21.75.22' # mine
# HOST = '10.21.75.14' # Felix
HOST = '10.21.75.16' #
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

def get_large_reply_cmd(  ):
    reply = sock.recv( constants.SHORT )
    print( "reply-packed: ", reply)#bin(reply) )
    reply = unpack(constants.REG_PACK_FLAG, reply)[0]
    print( "reply-unpacked: ", reply, bin(reply) )
    cmd = reply >> ( constants.BYTE_SIZE - constants.S_CMD_SIZE )

    reply2 = sock.recv( constants.SHORT )
    print( "reply2-packed: ", reply2)#bin(reply) )
    reply2 = unpack(constants.REG_PACK_FLAG, reply2)[0]
    print( "reply2-unpacked: ", reply2, bin(reply2) )    

    print( "reply:", reply, "bin: ", bin(reply) )
    print( "reply2:", reply2, "bin: ", bin(reply2) )
    print( "cmd:", cmd, "bin: ", bin(cmd) )
    mega_score = reply << constants.BYTE_SIZE | reply2
    print('mega-score:', mega_score)
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
    get_reply_cmd() #just clears the buffer, doesnt actually add to score... not implementing large score yet
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
        print("score", score)
        # mega_score = score >> constants.BYTE_SIZE
        # print("megascore", mega_score)

        print( "Player score:", score )
        # print( "Player score:", mega_score )

def get_board( reply ):
        size = ( reply & constants.S_PRINT_OPT_MASK ) >> constants.S_PRINT_TAIL
        print("board size:", size)
        board = get_str( size )
        print( board )
        print( "\n")
        print( prettify_board( board, size ) ) 

def prettify_board( board, board_size ):
    newBoard = ''
    col_counter = 0
    for c in board:
        newBoard += c
        col_counter += 1
        if col_counter == board_size:
            newBoard += '\n'
            col_counter = 0
        else:
            newBoard += ' '            
    return newBoard

with socket(AF_INET, SOCK_STREAM) as sock:
    sock = socket(AF_INET, SOCK_STREAM)
    # create connection
    sock.connect(( HOST, PORT ))
    # data = argv[1].encode('utf-8')

    print( 'Client:', sock.getsockname())
    sock.sendall( pack ( constants.REG_PACK_FLAG, constants.C_PRINT_CMD ) )
    reply, cmd = get_reply_cmd()
    get_board(reply)


with socket(AF_INET, SOCK_STREAM) as sock:
    sock = socket(AF_INET, SOCK_STREAM)
    # create connection
    sock.connect(( HOST, PORT ))
    # data = argv[1].encode('utf-8')

    print( 'Client:', sock.getsockname())
    play_game( sock )

