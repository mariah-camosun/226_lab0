#!/usr/bin/python3.11
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread, current_thread, Semaphore
from struct import pack, unpack
from queue import Queue
from Board import Board
import constants

BUF_SIZE = 1
HOST = ''
PORT = 12345

MIN_PACK_BYTES = 2
MAX_PLAYERS = 2

'''
----once get to threading
writing our own queue, but can import it.
'''
game_queue = Queue()
output_queue = Queue()

###########################  NEW BOARD   ###########################
def new_board( num ):
    b = Board.new_max_board(num)
    show_board_and_scores(b)
    return b

###########################  CLASS INTERACTIONS  ###########################
def get_tile_details( board, player ):
        active_player = board.get_player( player )
        column, row = active_player.get_coords()
        tile_contains = board.get_coord_tile( column, row ).get_contents()

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
            sc.close()
            return #data
        data += curr_data

    return data

###########################  SEND CMDS   ###########################
def queue_show_board( board ):
    board_size = board.get_size()
    cmd = constants.PRINT_BOARD | ( board_size << constants.S_PRINT_TAIL )
    packed_send_precmd = pack( constants.REG_PACK_FLAG, cmd)

    board_str = str( board )
    board_str = board_str.replace(" ", "").replace("\n", "").split("n", 1)
    board_str = board_str[0]

    output_queue.put( packed_send_precmd + board_str.encode( 'utf-8' ) )
    
def queue_delta( board, player_num, isSourse ):
    '''
    builds, packs, and sends the 'delta' command to the client.

    :param1: board object
    :param2: isSource - true if this delta is for the tile player was on, false
    if for the tile the player is going to.
    '''
    print("entered send delta")
    column, row, prev_content = get_tile_details( board, player_num )
    row = row << constants.S_ROW_TAIL_SIZE
    column = column << constants.S_COL_TAIL_SIZE

    delta = 0

    if ( isSourse == True ):
        delta = constants.DELTA | row | column | constants.BLANK
    elif player_num == 1:
        delta = constants.DELTA | row | column | constants.PLAYER1
    else:
        delta = constants.DELTA | row | column | constants.PLAYER2

    data = pack( constants.LONG_PACK_FLAG, int(delta) )
    output_queue.put( data )

def queue_score( board ):
    scoreOpt = (0b01) << ( 8 + 6 ) 
    p1_bits = board.get_player( 1 ).get_score() << (4 + 6)
    p2_bits = board.get_player( 2 ).get_score() << ( 6 )

    cmd_out = scoreOpt | p1_bits | p2_bits
    output_queue.put( pack ( constants.LONG_PACK_FLAG, cmd_out ) )

###########################  ROUTING  ###########################
def direct_request( cmd_byte, board ):
    # recieve print board cmd
    if ( cmd_byte == int(constants.C_PRINT_CMD) ):
        queue_show_board( board )
    else:
        # get cmd portion of split cmd bits from remaining opt bits (via bitshifting)
        cmd = cmd_byte >> ( constants.BYTE_SIZE - constants.C_CMD_SIZE )
    
        # recieve create board command
        if ( cmd == int(constants.CREATE_BOARD_MIN) ):
            size = ( cmd_byte & constants.C_SIZE_MASK ) # size = 4 bits, convert cmd bits to 0, using bitmask
            size = size >> ( constants.C_CREATE_TAIL ) # cut off trailing 0 not part of opt

            board = new_board( size )
            queue_show_board( board )

        #otherwise its a move command, direction is one of 4
        else:
            player_byte = cmd_byte & 0b00000010 
            player_byte = player_byte >> ( 1 )
            player = board.get_player( player_byte + 1 )

            queue_delta( board, player_byte + 1 , True )

            if ( cmd == (constants.UP_BIN_MIN) ):
                player.move( constants.UP )
            elif ( cmd == (constants.DOWN_BIN_MIN) ):
                player.move( constants.DOWN )     
            elif ( cmd == (constants.LEFT_BIN_MIN) ):
                player.move( constants.LEFT )   
            elif ( cmd == (constants.RIGHT_BIN_MIN) ):
                player.move( constants.RIGHT )

            queue_delta( board, player_byte + 1, False )
            queue_score( board )
    show_board_and_scores(board) 
    return board

###########################  CONNECTION  ###########################
def receive_from_client( sock, thread_name ):
    # print('Client:', sock.getpeername()) # Client IP and port
    with sock: 
        while (True):
            raw_data = recieve_buffer_data( sock, constants.SHORT )
            if raw_data == b'':
                print( "did socket close?", sock.getpeername() )
            else:
                data = unpack( constants.REG_PACK_FLAG, raw_data )[0]
                print("unpacked raw data from client (to game_queue)", thread_name, ":", data, bin(data))

                game_queue.put( data ) 

def handle_game_queue(game_queue, board):
    # print('started handle game queue')
    while True:
            cmd = game_queue.get()
            board = direct_request( cmd, board )

def send_to_client( client_threads ):
    # print("started/entered send to client")

    prev_is_show_board = False
    curr_is_show_board = False

    while True:
        data = output_queue.get()
        prev_is_show_board = curr_is_show_board

        if (unpack( '!B', data ) >> 6) == 0:
            curr_is_show_board = True
        else:
            curr_is_show_board = False

        # if both prev and curr send are 'show board' dont send
        if not ( prev_is_show_board == True and curr_is_show_board == True):
            for client in client_threads:
                cli, sock_connector = client
                try:
                    sock_connector.sendall( data )
                    print("sent data", data, "to client", cli)
                except OSError:
                    print('socket was closed pre-maturely')

def main():
    sock_listener = socket(AF_INET, SOCK_STREAM) # TCP socket - REMOVED 'WITH' SO doesnt close at end of func
    sock_listener.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # Details later
    sock_listener.bind((HOST, PORT)) # Claim messages sent to port "PORT"
    sock_listener.listen(1) # Server only supports a single 3-way handshake at a time

    print('Server:', sock_listener.getsockname()) # Server IP and port

    client_threads = [] # contents are tupples: { thread, accepted_socket }

    for i in range( MAX_PLAYERS ):
        sock_connector, _ = sock_listener.accept() # Wait until a connection is established

        cli_thread = ( Thread(target=receive_from_client, args=(sock_connector,)) )
        client_threads.append( (cli_thread, sock_connector) )
        cli_thread.start() 

    
    out_thread = Thread( target=send_to_client, args=(client_threads,) )
    out_thread.start()

    board = new_board( 10 )
    game_thread = Thread( target=handle_game_queue, args=(game_queue, board) )
    game_thread.start()
    return sock_listener

server_socket = main()