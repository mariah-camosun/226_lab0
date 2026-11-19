#!/usr/bin/python3.11
# from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
# from threading import Thread, current_thread, Semaphore
from asyncio import run, start_server, StreamReader, StreamWriter, Queue, create_task #, #open_connection
from struct import pack, unpack
# from queue import Queue
from Board import Board
# import sys
import constants

BUF_SIZE = 1 # in bytes
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
clients = []

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

###########################  RECIEVE CMDS  ###########################
# def recieve_buffer_data( sc, size ): # recieves data in bitecode format
#     data = b''
#     while len(data) < size:
#         curr_data = sc.recv(size - len(data)) # recvfrom not needed since address known
#         if curr_data == b'': #closed connection
#             print('closing connection')
#             sc.close()
#             sys.exit()
#             return #data
#         data += curr_data

#     return data

# def receive_from_client( sock ):
    with sock:
        try:
            while (True):
                raw_data = recieve_buffer_data( sock, constants.SHORT )
                if raw_data == b'' or raw_data == None:
                    print( "Connection was closed" )
                    sock.close()
                    sys.exit()
                    return
                else:
                    data = unpack( constants.REG_PACK_FLAG, raw_data )[0]
                    # await game_queue.put( data )
        except ConnectionResetError:
            print('Connection reset by peer')
            sock.close()
            sys.exit()
            return

###########################  SEND TO QUEUE   ###########################
async def queue_show_board( board, writer ):
    board_size = board.get_size()
    cmd = constants.PRINT_BOARD | ( board_size << constants.S_PRINT_TAIL )
    packed_send_precmd = pack( constants.REG_PACK_FLAG, cmd)

    board_str = str( board )
    board_str = board_str.replace(" ", "").replace("\n", "").split("n", 1)
    board_str = board_str[0]

    await output_queue.put( { packed_send_precmd + board_str.encode( 'utf-8' ), writer } )
    
async def queue_delta( board, player_num, isSourse ):
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
    await output_queue.put( { data, } )

async def queue_score( board ):
    scoreOpt = (0b01) << ( 8 + 6 ) 
    p1_bits = board.get_player( 1 ).get_score() << (4 + 6)
    p2_bits = board.get_player( 2 ).get_score() << ( 6 )

    cmd_out = scoreOpt | p1_bits | p2_bits
    await output_queue.put( { pack ( constants.LONG_PACK_FLAG, cmd_out ), } )

###########################  ROUTING  ###########################
def direct_request( cmd_byte, reader, writer, board ):
    if ( cmd_byte == int(constants.C_PRINT_CMD) ):
        queue_show_board( board, writer )
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
def handle_game_queue(game_queue, board):
    while True:
            cmd_data, reader, writer = game_queue.get()
            board = direct_request( cmd_data, reader, writer, board )

async def send_to_client( to_client_queue, client_name, reader, writer ):
    # pass
    # prev_is_show_board = False
    # curr_is_show_board = False

    while True:
        cmd, writer = await output_queue.get()
        if writer:
            writer.write( cmd )
            await writer.drain()
    #         # send to only the one writer
        else:
            pass
            # send to both


    #             for client in client_threads:
    #                 cli, sock_connector = client
    #                 try:
    #                     # try:
    #                     #     # udata = unpack( '!H', data )
    #                     #     # print( 'sending:', data, bin(udata) )
    #                     # except:
    #                     #     # print( 'sending:', data )
    #                     sock_connector.sendall( data )
    #                 except OSError:
    #                     print('socket was closed pre-maturely')
    #                     sys.exit()

async def receive_from_client( client_name, reader, writer ) -> None:
    '''
    get client requests and passes them to handler to proccess, queues processed cmd
    '''
    # get raw data
    while True:
        raw_data = await reader.read( BUF_SIZE )
        data = unpack( constants.REG_PACK_FLAG, raw_data )[0]
        print( "client:", client_name, "raw data recieved:", raw_data, "unpacked:", data, bin(data) )
        await game_queue.put( {data, reader, writer} )

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

async def new_client( reader: StreamReader, writer: StreamWriter)-> None:
    to_client_queue = Queue()
    client_name = writer.get_extra_info('peername')
    print( "connected to client:", client_name)
    client_cmd = create_task( receive_from_client( client_name, reader, writer ) )
    to_cli_task = create_task( send_to_client( to_client_queue, client_name, reader, writer ) )
 


    # abv includes processing and queueing (convert it to cmds) 
    # break down?
        # process 
        # queue it
    # await queue.put( processed_cmd )
    # print( "queued client command" )

async def consume_game_commands( reader: StreamReader, writer: StreamWriter) -> None:
    '''
    consumes items in the game move queue
    '''
    while True:
        # get from queue; waits if empty
        action = await game_queue.get()

        #process
        direct_request()

        #mark complete
        game_queue.task_done()
        print( "processed a board action")

        # put response in output queue
        await output_queue_cli1.put()
        await output_queue_cli2.put()
        print( "queued output")

# async def send_to_client(client)->None:
#     while True:
        
#         # get from queue, if nothing, wait
#         out = await output_queue.get()

#         # send
#         send_to_clients()

#         # mark complete
#         output_queue.task_done()
#         print("sent output command")


# main 

#     data = await reader.readline()
#     message = data.decode()

#             cli_thread = ( Thread(target=receive_from_client, args=(sock_connector,) ))
#         out_thread = Thread( target=send_to_client, args=(client_threads,), daemon=True )
#         # out_thread.start()

#         board = new_board( 10 )
#         game_thread = Thread( target=handle_game_queue, args=(game_queue, board), daemon=True )            


async def main()->None:

# game_queue = Queue()
# output_queue_cli1 = Queue()
# output_queue_cli2 = Queue()

    # start tcp server
    server = await start_server( new_client, HOST, PORT )
    await server.serve_forever()

    
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

main()