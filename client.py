#!/usr/bin/python3.11

from socket import socket, AF_INET, SOCK_STREAM
from sys import argv
import constants
import time
from struct import pack, unpack
from threading import Thread, current_thread, Semaphore
from struct import pack, unpack
from queue import Queue

import constants

BUF_SIZE = 1024
# HOST = '10.21.75.22' # mine
HOST = '10.21.75.50' # bbcli
# HOST = '10.21.75.14' # Felix
# HOST = '10.21.75.16' #
PORT = 12345

###########################  ROUTING  ###########################
def direct_reply():
    reply, cmd = get_cmd( )

    if cmd == constants.PRINT_BOARD_CMD:
        board = get_board( reply )
        

    # if cmd == constants.SCORE_CMD:
    #     print("score, reply:", reply)
    #     print("entered score")
    #     get_player_score( reply )
    #     handle_delta( reply )

    elif cmd == constants.DELTA_CMD:
        handle_delta( reply )
    elif cmd == constants.SCORE_CMD:
        handle_score( reply )
    else:
        print('unknown command')

###########################  SEND CMDS   ###########################
def get_player_commands(): #, board_size ):    
    '''
    Prompt user for command: print or move direction.
    Repeat until a valid option is entered

    :return: str, command letter
    '''
    while (True):
        try:
            command = input( "Choose one of: re-print board (p), or move up(u), down(d), left(l), right(r)\n" )
            # print(f"command entered: {command}")            
            validate_command( command )
        except ValueError:
            print(f"Invalid entry, choose one of: P, U, D, L, R") # will also accept lower case
            continue
        else:
            return command.upper() #, board_size )

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

def send_user_cmd( sock ):
    send_user_command( sock )

def send_user_command( sock ):
    while (True):
        cmd = get_player_commands() #, board_size )

        send_command( cmd, sock )

def send_command( cmd, sock ): #, board_size  ):
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

def send_move_cmd( cmd ):
    cmd = cmd << constants.C_MOVE_TAIL
    pl_cmd = (player - 1) << constants.C_MOVE_P_SHIFT
    complete_cmd = cmd | pl_cmd
    print( 'sending: cmd lead', bin(cmd), 'player', bin(pl_cmd), 'complete', bin(complete_cmd) )
    sock.sendall( pack ( constants.REG_PACK_FLAG, complete_cmd ) )

###########################  RECIEVE CMDS  ###########################
def get_cmd():
    reply = sock.recv( constants.SHORT )
    reply = unpack(constants.REG_PACK_FLAG, reply)[0]
    cmd = reply >> ( constants.BYTE_SIZE - constants.S_CMD_SIZE )
    # print('cmd', cmd, bin(cmd))
    if cmd == 0b01 or cmd == 0b10:
        # print('\nentered if cmd score or delta')
        pt2 = sock.recv( constants.SHORT )
        pt2 = unpack(constants.REG_PACK_FLAG, pt2)[0]
        # print('pt2:', pt2a, pt2, bin(pt2))
        # print('reply preshift', bin(reply))
        reply = reply << constants.BYTE_SIZE
        # print('reply shifted', bin(reply), 'pt2:', bin(pt2))
        reply = reply | pt2
        # print('reply compl', bin(reply))
    # print("\ncmd in rec'd:", bin(reply), "cmd:", bin(cmd))
    return reply, cmd

def get_large_reply_cmd(  ):
    reply = sock.recv( constants.SHORT )
    # print( "reply-packed: ", reply)#bin(reply) )
    reply = unpack(constants.REG_PACK_FLAG, reply)[0]
    # print( "reply-unpacked: ", reply, bin(reply) )
    cmd = reply >> ( constants.BYTE_SIZE - constants.S_CMD_SIZE )

    reply2 = sock.recv( constants.SHORT )
    # print( "reply2-packed: ", reply2)#bin(reply) )
    reply2 = unpack(constants.REG_PACK_FLAG, reply2)[0]
    # print( "reply2-unpacked: ", reply2, bin(reply2) )    

    # print( "reply:", reply, "bin: ", bin(reply) )
    # print( "reply2:", reply2, "bin: ", bin(reply2) )
    # print( "cmd:", cmd, "bin: ", bin(cmd) )
    mega_score = reply << constants.BYTE_SIZE | reply2
    # print('mega-score:', mega_score)
    return reply, cmd

def handle_delta( reply ):
    # print('delta reply all', bin(reply))
    row = ( reply & constants.S_ROW_MASK ) >> constants.S_ROW_TAIL_SIZE
    col = ( reply & constants.S_COL_MASK ) >> constants.S_COL_TAIL_SIZE
    contents = ( reply & constants.TILE_MASK )
    # print( 'cmd recd:', bin(reply), '\n', 'delta: row:', bin(row), 'col:', bin(col), 'contents', bin(contents) )
    print( 'delta: row:', (row), 'col:', (col), 'contents', bin(contents) )

def handle_score( reply ):
    print('scsore reply all', bin(reply))
    p1_score = reply >> ( 6 + 4 )
    p1_score = p1_score & 0b001111
    p2_score = reply >> ( 6 )
    p2_score = p2_score & 0b0000001111
    print('player 1 score:', bin(p1_score), 'player 2 score:', bin(p2_score))
    print('player 1 score:', p1_score, 'player 2 score:', p2_score)
    return p1_score, p2_score    

    # get_cmd() #just clears the buffer, doesnt actually add to score... not implementing large score yet

def get_delta_opts( reply ):
    part2 = sock.recv( constants.SHORT )
    part2 = unpack(constants.REG_PACK_FLAG, part2)[0]
    # print("p1:", bin(reply), ", p2:", bin(part2) )

    reply = reply << constants.BYTE_SIZE
    reply += part2
    # print( "combo:", bin(reply))

    row = ( reply & constants.S_ROW_MASK ) >> constants.S_ROW_TAIL_SIZE
    col = ( reply & constants.S_COL_MASK ) >> constants.S_COL_TAIL_SIZE
    contents = ( reply & constants.TILE_MASK )
    # print( "row:", row, ", col:", col, ", contents:", bin(contents))

def get_player_score( reply ):
        score = ( reply & constants.S_SCORE_MASK ) >> constants.S_SCORE_TAIL
        print("score", score)
        # mega_score = score >> constants.BYTE_SIZE
        # print("megascore", mega_score)

        print( "Player score:", score )
        # print( "Player score:", mega_score )

def get_board( reply ):
    size = ( reply & constants.S_PRINT_OPT_MASK ) >> constants.S_PRINT_TAIL
    data = sock.recv( size * size )
    board = data.decode()
    print( prettify_board( board, size ) )
    return board

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

###########################  CONNECTION  ###########################
def play_game( sock ):
    while (True):
        cmd = get_player_commands() #, board_size )
        send_user_command( cmd, sock ) #, board_size  )
        direct_reply()

def recieve_server_cmds( sock ):
     while (True):
        #  print('entered rec server cmds')
         direct_reply()
         print( "Choose one of: re-print board (p), or move up(u), down(d), left(l), right(r)\n" )
         

try:
    player = int(argv[1])
except:
    print( 'Missing player number argument, enter 1 or 2' )
else:
    # initial connect, print, and disconnect
    # with socket(AF_INET, SOCK_STREAM) as sock:
    #     sock = socket(AF_INET, SOCK_STREAM)
    #     # create connection
    #     sock.connect(( HOST, PORT ))
    #     sock.sendall( pack ( constants.REG_PACK_FLAG, constants.C_PRINT_CMD ) )
    #     reply, cmd = get_cmd()
    #     get_board(reply)

    with socket(AF_INET, SOCK_STREAM) as sock:
        sock = socket(AF_INET, SOCK_STREAM)
        # create connection
        sock.connect(( HOST, PORT ))

        print( 'Client:', sock.getsockname())
        # action_out_thread = Thread( target=send_user_cmd, args=(sock,) )
        in_thread = Thread( target=recieve_server_cmds, args=(sock,) )

        # action_out_thread.start()
        in_thread.start()

        send_command( constants.PRINT, sock )
        # time.sleep(0.2)
        send_user_command( sock )
        # send_user_cmd( sock )

        # play_game( sock )