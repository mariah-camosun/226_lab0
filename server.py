from queue import Queue
from Board import Board
import constants


#!/usr/bin/python3.11
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from struct import pack, unpack
from threading import Thread, current_thread, Semaphore

BUF_SIZE = 1
HOST = ''
PORT = 12345

MIN_PACK_BYTES = 2
MAX_PLAYERS = 2



'''
----once get to threading
writing our own queue, but can import it.
'''
###########################  NEW BOARD   ###########################
def new_board( num ):
    b = Board.new_max_board(num)
    show_board_and_scores(b)
    return b

###########################  CLASS INTERACTIONS  ###########################
def get_tile_details( board ):
        active_player = board.get_player(1)
        column, row = active_player.get_coords()
        tile_contains = board.get_coord_tile( column, row ).get_contents()
        # print( "getTileDetails: col, row", column, row)

        return column, row, tile_contains

def show_board_and_scores(b):
    print( b )
    print( b.report_player_scores() )

###########################  RECIEVE CMDS  ###########################
def recieve_buffer_data( sc, size ): # recieves data in bitecode format
    data = b''
    while len(data) < size:
        curr_data = sc.recv(size - len(data)) # recvfrom not needed since address known
        if curr_data == b'': #closed connection
            print('closing connection')
            return data
        data += curr_data

    return data

###########################  SEND CMDS   ###########################
def send_board( board ):
    # print("entered send_board")
    build_send_board_pre_cmd( board.get_size() )

    board_str = str( board )
    # print(board_str)
    board_str = board_str.replace(" ", "").replace("\n", "").split("n", 1)
    board_str = board_str[0]
    # print( board_str )
    output_queue.put( board_str.encode( 'utf-8' ) )
    # sc.sendall( board_str.encode( 'utf-8' ) )

def build_send_board_pre_cmd( board_size ):
    cmd = constants.PRINT_BOARD | ( board_size << constants.S_PRINT_TAIL )
    # print("board meta command:", bin(cmd))
    output_queue.put( pack( constants.REG_PACK_FLAG, cmd) )
    # sc.sendall( pack( constants.REG_PACK_FLAG, cmd))

def handle_output_queue( output_queue, cmd ):
    pass

def send_delta( board, isSourse ):
    '''
    builds, packs, and sends the 'delta' command to the client.

    :param1: board object
    :param2: isSource - true if this delta is for the tile player was on, false
    if for the tile the player is going to.
    '''
    column, row, prev_content = get_tile_details( board )
    # print( "Send Delta: row, column:", row, column, "in bin", bin(row), bin(column))
    row = row << constants.S_ROW_TAIL_SIZE
    column = column << constants.S_COL_TAIL_SIZE

    if ( isSourse == True ):
        delta = constants.DELTA | row | column | constants.BLANK
    else:
        delta = constants.DELTA | row | column | constants.PLAYER
    # print( bin(delta))
    sc.sendall( pack( constants.LONG_PACK_FLAG, int(delta) ) )

def send_score( scoreOpt ):
    # print( "entered send score, score data:", scoreOpt, bin(scoreOpt))
    # scoreOpt = score & 0b001111 # make sure score is only component of cmd that is the 4 bit score sequence
    scoreOpt = scoreOpt << (constants.S_SCORE_TAIL) # add 2 0s at the end to padd to correct position
    fullCmd = (constants.SCORE) | scoreOpt
    megaCmd = fullCmd << constants.BYTE_SIZE

    # print ( "score data: ", scoreOpt, bin(scoreOpt), "cmd: ", fullCmd, bin(fullCmd), " opt: " )
    # sc.sendall( pack ( constants.REG_PACK_FLAG, fullCmd ) ) # Client IP and port implicit due to accept call
    sc.sendall( pack ( constants.LONG_PACK_FLAG, megaCmd ) ) # Client IP and port implicit due to accept call
    
    # main.send_str( sc, '\n' )

###########################  ROUTING  ###########################
def direct_request( cmd_byte, board ):
    # print( "Entered direct." )
    # print( "Data in:", cmd_byte, bin(cmd_byte))

    # recieve print board cmd
    if ( cmd_byte == int(constants.C_PRINT_CMD) ):
        # print("in print board")
        
        send_board( board )
    else:
        # print( "else not print board cmd" )
        # get cmd portion of split cmd bits from remaining opt bits (via bitshifting)
        # print( "recieved command:", cmd_byte, bin(cmd_byte) )
        cmd = cmd_byte >> ( constants.BYTE_SIZE - constants.C_CMD_SIZE )
        # print( cmd )
    
        # recieve create board command
        if ( cmd == int(constants.CREATE_BOARD_MIN) ):
            # print("in create board")
            # print("cmd: ", cmd, bin(cmd) )
            # opt represents board size, in 4 bits
            opt = ( cmd_byte & constants.C_SIZE_MASK ) # convert cmd bits to 0, using bitmask
            # print("opt: ", opt, bin(opt) )
            opt = opt >> ( constants.C_CREATE_TAIL ) # cut off trailing 0 not part of opt
            # print("opt: ", opt, bin(opt) )
            # print( "cmd:",  cmd, bin(cmd), " opt:", opt, bin( opt ) )

            board = Board.new_max_board( opt )
            # print( "board" )
            # print( board.__str__() )
            print( board )

            send_board( board )
            player = board.get_player( 1 )
            send_score( player.get_score() )

        # recieve ??? need to clean this one up
        # elif ( cmd >> ( constants.C_CMD_SIZE -1 ) != 1 ):
        #         print("entered print board? I think?")
        #         return board

        #otherwise its a move command, direction is one of 4
        else:
            # print( " in move command" )
            send_delta( board, True )
            player = board.get_player( 1 )
            # print( bin(cmd) )
            # cmd = cmd << ( constants.C_MOVE_TAIL )
            # print( bin(cmd) )

            if ( cmd == (constants.UP_BIN_MIN) ):
                # print("entered up")
                player.move( constants.UP )
            elif ( cmd == (constants.DOWN_BIN_MIN) ):
                player.move( constants.DOWN )     
            elif ( cmd == (constants.LEFT_BIN_MIN) ):
                player.move( constants.LEFT )   
            elif ( cmd == (constants.RIGHT_BIN_MIN) ):
                player.move( constants.RIGHT )

            # print("exited move direction section")
            send_delta( board, False )
            send_score( player.get_score() )
        # print("exited else move section")
    # print("tail of direct")
    show_board_and_scores(board) 
    return board

###########################  CONNECTION  ###########################
def receive_from_client( sock, thread_name, game_queue ):
    
    print('Client:', sock.getpeername()) # Client IP and port
    # print("entered connect_player")
    with sock: 
        while (True):
            # print( "entered socket, while true (always wait/loop) ")
            raw_data = recieve_buffer_data( sock, constants.SHORT )
            print(raw_data)
            if raw_data == '':
                print("Player", thread_name + 1, "Connection Closed")
            else:
                # print( "rawdata - handle connection", raw_data )
                data = unpack( constants.REG_PACK_FLAG, raw_data )[0]

                # print( "data, connection: ", data )
                # print( "recieved (hex):", hex( data ))

                game_queue.put( data ) 
                # direct_request( data, board )

def handle_game_queue(game_queue, board):
    while True:
        if not game_queue.empty():
            cmd = game_queue.get()
            direct_request( cmd, board )
            # need something to lock the queue while being accessed? 
            # only 1 thread for the board (using get) so should be fine?
            # but what about the output_queue?

# sock_connector, thread_counter, output_queue, board
def send_to_client( sock_connector, output_queue, board ):
    data = output_queue.get()
    sock_connector.sendall( data.encode( 'utf-8' ) )

# def handle_connection( sc, thread_name, board ):
#     print('Client:', sc.getpeername()) # Client IP and port
#     # print("entered handle connection")
#     with sc: 
#         while (True):
#             # print( "entered socket, while true (always wait/loop) ")
#             raw_data = recieve_buffer_data( sc, constants.SHORT )
#             # print(raw_data)
#             if raw_data == '':
#                 print("Connection Closed")
#             else:
#                 # print( "rawdata - handle connection", raw_data )
#                 data = unpack( constants.REG_PACK_FLAG, raw_data )[0]

#                 # print( "data, connection: ", data )
#                 # print( "recieved (hex):", hex( data ))

#                 board = direct_request( data, board )

def main():
    with socket(AF_INET, SOCK_STREAM) as sock_listener: # TCP socket
        sock_listener.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # Details later
        sock_listener.bind((HOST, PORT)) # Claim messages sent to port "PORT"
        sock_listener.listen(1) # Server only supports a single 3-way handshake at a time

        print('Server:', sock_listener.getsockname()) # Server IP and port

        board = new_board( 10 )
        game_queue = Queue()
        output_queue = Queue()
    
        # print( board )

        # while True:
        game_thread = Thread( target=handle_game_queue, args=(game_queue, board) )
        game_thread.start()

        from_client_threads = []
        to_client_threads = []
        thread_counter = 0
        for i in range( MAX_PLAYERS ):
            sock_connector, _ = sock_listener.accept() # Wait until a connection is established
            from_client_threads.append( Thread(target=receive_from_client, args=(sock_connector, thread_counter, game_queue)) )
            to_client_threads.append( Thread(target=send_to_client, args=(sock_connector, thread_counter, output_queue, board)) )
            thread_counter += 1
            from_client_threads[-1].start() 
            to_client_threads[-1].start() 

output_queue = Queue()
main()