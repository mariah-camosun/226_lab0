#!/usr/bin/python3.11
# from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
# from threading import Thread, current_thread, Semaphore
from asyncio import run, start_server, StreamReader, StreamWriter, Queue, create_task #, #open_connection
from struct import pack, unpack
# from queue import Queue
from Board import Board
# import sys
import constants
from Server import Server
import traceback

BUF_SIZE = 1 # in bytes
HOST = ''
PORT = 12345

# MIN_PACK_BYTES = 2
MAX_PLAYERS = 2

###########################  CLASS INTERACTIONS  ###########################
def new_board( num ):
    b = Board.new_max_board(num)
    show_board_and_scores(b)
    return b

def get_tile_details( board, player ):
        active_player = board.get_player( player )
        column, row = active_player.get_coords()
        tile_contains = board.get_coord_tile( column, row ).get_contents()

        return column, row, tile_contains

def show_board_and_scores(b):
    print( b )
    print( b.report_player_scores() )

###########################  SEND TO QUEUE   ###########################
async def send_board( server, board, client ):
    print("send board")
    board_size = board.get_size()
    out_cmd = constants.PRINT_BOARD | ( board_size << constants.S_PRINT_TAIL )
    packed_send_precmd = pack( constants.REG_PACK_FLAG, out_cmd)

    board_str = str( board )
    board_str = board_str.replace(" ", "").replace("\n", "").split("n", 1)
    board_str = board_str[0]

    data = packed_send_precmd + board_str.encode( 'utf-8' )
    print("send board data packed")
    print("send board pre-queue Queue contents:", list(server.get_output_queue()._queue))
    await queue_send_cmd( server, (data, client) )
    print("send board post-queue Queue contents:", list(server.get_output_queue()._queue))

async def send_delta( server, board, player_num, isSourse, client ):
    '''
    builds, packs, and sends the 'delta' command to the client.

    :param1: board object
    :param2: isSource - true if this delta is for the tile player was on, false
    if for the tile the player is going to.
    '''
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
    await queue_send_cmd( server, (data, None) )
    return data

async def send_score( server, board, client ):
    scoreOpt = (0b01) << ( 8 + 6 ) 
    p1_bits = board.get_player( 1 ).get_score() << (4 + 6)
    p2_bits = board.get_player( 2 ).get_score() << ( 6 )

    cmd_out = scoreOpt | p1_bits | p2_bits
    data = pack ( constants.LONG_PACK_FLAG, cmd_out )
    await queue_send_cmd( server, (data, None) )

async def queue_send_cmd( server, cmd_tupple ):
    await server.get_output_queue().put( cmd_tupple )

###########################  ROUTING  ###########################
async def process_action(server, board, data, client):
    # data = unpack( constants.REG_PACK_FLAG, data)[0]
    cmd = data >> (8-3)
    opt = (data & 0b00011110) >> 1
    # print('pre-bitshift:', data, bin(data), 'post-bitshift:', opt, bin(opt))
    # print("in process_action. cmd:", cmd, bin(cmd), opt, bin(opt))

    # print("cmd:", cmd, bin(cmd), "shifted >> 2:", cmd >> 2, bin(cmd >> 2))


    if cmd >> 2 == 0b1: # move
        # print("in if move")
        # print("player/'opt':", opt, bin)
        player = board.get_player( opt + 1 )
        await send_delta( server, board, opt + 1 , True, client )

        if ( cmd == (constants.UP_BIN_MIN) ): # move up
            player.move( constants.UP )
        elif ( cmd == (constants.DOWN_BIN_MIN) ): # move down
            player.move( constants.DOWN )     
        elif ( cmd == (constants.LEFT_BIN_MIN) ): # move left
            player.move( constants.LEFT )   
        elif ( cmd == (constants.RIGHT_BIN_MIN) ): # move right
            player.move( constants.RIGHT )
            
        await send_delta( server, board, opt + 1, False, client )
        await send_score( server, board, client )
        return # no need to send board
    elif cmd == 0b000: # create board
        print("in if create")
        board = new_board( opt, client )
    elif cmd == 0b001: # show board
        print("in if show board")
        pass
    else: # invalid cmd
        print("in if invalid cmd")
        return 
    
    await send_board( server, board, client )
    show_board_and_scores(board)
    return board

###########################  CONNECTION  ###########################
#----\/-----suitable for clientside---------------------------------------------------------------------------
# whoops, client out is only ever 1 byte - got server/cli out mixed up again
# async def process_cmd( raw_data, reader ):
#     data = unpack( constants.REG_PACK_FLAG, raw_data )[0]
#     if data == 0b00111100:
#         return data
#     else:
#         data_pt2 = await reader.read( BUF_SIZE ) 
#         data_pt2 = unpack( constants.REG_PACK_FLAG, data_pt2 )[0]
#         return ( data << constants.BYTE_SIZE | data_pt2 )

async def consume_game_commands( server, board, game_action_queue ): #, reader: StreamReader, writer: StreamWriter) -> None:
    '''
    consumes items in the game move queue
    '''
    try:
        while True:
            # get from queue; waits if empty
            action, client = await game_action_queue.get()
            print("starting processing of game command")
            print("queue item:", action, "for client:", client)

            #process # function also includes adding server response to out_queue
            await process_action(server, board, action, client) 
            print( "processed a board action")
    except Exception:
        traceback.print_exc()

async def main()->None:
    server = Server()
    board = new_board( 10 )
    game_actions_task = create_task( consume_game_commands(server, board, server.get_input_queue() ) )
    await server.start()

    
#         game_thread = Thread( target=handle_game_queue, args=(game_queue, board), daemon=True )            

    
    # client_tasks = [ create_task( get_client_requests( player_num ) ) for i in range( MAX_PLAYERS ) ]
    # game_actions = create_task( handle_game_queue() )
    # to_cli1_task = create_task( send_to_client( output_queue_cli1 ) )
    # to_cli2_task = create_task( send_to_client( output_queue_cli2 ) )


    # gather is wait for them to *finish* (lol nope; maybe if time setup closes)
    # await asyncio.gather( get_client_requests(), get_client_requests() );




run( main() )
    # with socket(AF_INET, SOCK_STREAM) as sock_listener: # TCP socket - REMOVED 'WITH' SO doesnt close at end of func
        # sock_listener = socket(AF_INET, SOCK_STREAM) # TCP socket - REMOVED 'WITH' SO doesnt close at end of func
        # sock_listener.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # Details later
        # sock_listener.bind((HOST, PORT)) # Claim messages sent to port "PORT"
        # sock_listener.listen(1) # Server only supports a single 3-way handshake at a time

        # print('Server:', sock_listener.getsockname()) # Server IP and port

        # client_threads = [] # contents are tupples: { thread, accepted_socket }

        # for i in range( MAX_PLAYERS ):
        #     sock_connector, _ = sock_listener.accept() # Wait until a connection is established
        #     print('Client:', sock_connector.getpeername()) # Client IP and port

            # client_threads.append( (cli_thread, sock_connector) )
            # cli_thread.start() 

        

        # game_thread.start()

        # sys.exit()

# main()