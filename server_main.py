#!/usr/bin/python3.11
from asyncio import run, create_task #open_connection
from struct import pack
from Board import Board
import constants
from Server import Server
import traceback

BUF_SIZE = 1 # in bytes
HOST = ''
PORT = 12345

MAX_PLAYERS = 2

INITIAL_BOARD_SIZE = 10

###########################  CLASS INTERACTIONS  ###########################
def new_board( num ):
    '''
    creates new board of num size and (if not commented out) shows it on server
    :return: Board, the created board
    '''
    b = Board.new_max_board(num)
    show_board_and_scores(b)
    return b

def get_tile_details( board, player ):
    '''
    get and return the details for the tile the player is on

    :param board: Board, the active board
    :param player: Player, the player moving (on the tile)
    :returns: (int, int, Class) tupple
    '''
    active_player = board.get_player( player )
    column, row = active_player.get_coords()
    tile_contains = board.get_coord_tile( column, row ).get_contents()

    return column, row, tile_contains

def show_board_and_scores(b):
    print( b )
    print( b.report_player_scores() )

###########################  SEND TO QUEUE   ###########################
async def send_board( server, board, client ):
    '''
    send the board string to the client machine
    :param server: Server, instance of the running server 
    :param board: Board, board the game is played on
    :param client: string, client name
    '''
    board_size = board.get_size()
    out_cmd = constants.PRINT_BOARD | ( board_size << constants.S_PRINT_TAIL )
    packed_send_precmd = pack( constants.REG_PACK_FLAG, out_cmd)

    board_str = str( board )
    board_str = board_str.replace(" ", "").replace("\n", "").split("n", 1)
    board_str = board_str[0]

    data = packed_send_precmd + board_str.encode( 'utf-8' )
    try:
        await queue_send_cmd( server, (data, client) )
    except Exception:
        # print(f"problem queueing board")
        return

async def send_delta( server, board, player_num, isSourse ):
    '''
    builds, packs, and queues the 'delta' command to the client.

    :param server: Server, instance of the running server 
    :param board: Board, board the game is played on
    :param player_num: int, player number ( as seen by the board, not the player number command)
    :param isSource: bool - true if this delta is for the tile player was on, false
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
    try:
        await queue_send_cmd( server, (data, None) )
        return data
    except Exception:
        # print("problem queueing delta")
        return

async def send_score( server, board ):
    '''
    send the score for both players
    :param server: Server, instance of the running server 
    :param board: Board, board the game is played on
    '''
    scoreOpt = (constants.S_SCORE_CMD) << ( constants.SCORE_BIT_CT*2 + constants.S_SCORE_TAIL ) 
    p1_bits = board.get_player( 1 ).get_score() << (constants.SCORE_BIT_CT + constants.S_SCORE_TAIL)
    p2_bits = board.get_player( 2 ).get_score() << ( constants.S_SCORE_TAIL )

    cmd_out = scoreOpt | p1_bits | p2_bits
    data = pack ( constants.LONG_PACK_FLAG, cmd_out )
    try:
        await queue_send_cmd( server, (data, None) )
    except Exception:
        # print("problem queueing score")
        return

async def queue_send_cmd( server, cmd_tupple ):
    '''
    Queues the sent in command to the server's outgoing queue, NOT the client
    queues
    :param server: Server, instance of the running server
    :param cmd_tupple: packed command, client name as a tupple
    '''
    await server.get_output_queue().put( cmd_tupple )
        
###########################  ROUTING  ###########################
async def process_action(server, board, data, client):
    '''
    takes the unpacked command from the client, makes the action described, 
    and queues up the outgoing response command
    :param server: Server, instance of the running server 
    :param board: Board, board the game is played on
    :param data: unpacked command recieved (first byte) 
    :param client: string, client name
    :returns: Board, board the game is played on, with any changes
    '''
    cmd = data >> ( constants.BYTE_SIZE - constants.C_CMD_SIZE )
    opt = (data & constants.C_OPT_MASK) >> 1

    if ( cmd >> (constants.C_CMD_SIZE - 1) == constants.C_MOVE_CROPPED ) : # move
        player = board.get_player( opt + 1 )
        await send_delta( server, board, opt + 1 , True )

        if ( cmd == (constants.UP_BIN_MIN) ): # move up
            player.move( constants.UP )
        elif ( cmd == (constants.DOWN_BIN_MIN) ): # move down
            player.move( constants.DOWN )     
        elif ( cmd == (constants.LEFT_BIN_MIN) ): # move left
            player.move( constants.LEFT )   
        elif ( cmd == (constants.RIGHT_BIN_MIN) ): # move right
            player.move( constants.RIGHT )
            
        show_board_and_scores(board)
        await send_delta( server, board, opt + 1, False )
        await send_score( server, board )
        return # no need to send board
    elif cmd == constants.CREATE_BOARD_MIN: # create board
        board = new_board( opt, client )
    elif cmd == constants.SHOW_BOARD_MIN: # show board
        pass
    else: # invalid cmd
        return 
    
    await send_board( server, board, client )
    show_board_and_scores(board)
    return board

###########################  CONNECTION  ###########################
async def consume_game_commands( server, board, game_action_queue ): #, reader: StreamReader, writer: StreamWriter) -> None:
    '''
    consumes items in the game move queue
    :param server: Server, instance of the running server 
    :param board: Board, board the game is played on
    :param game_action_queue: Queue, the game's queue of incoming commands to process
    '''
    try:
        while True:
            # get from queue; waits if empty
            action, client = await game_action_queue.get()
            print( 'command recieved:', hex( action ))

            #process # function also includes adding server response to out_queue
            await process_action(server, board, action, client) 
    except Exception:
        # traceback.print_exc()
        return

async def main()->None:
    '''
    setup and run the game server
    '''
    server = Server()
    board = new_board( INITIAL_BOARD_SIZE )
    game_actions_task = create_task( consume_game_commands(server, board, server.get_input_queue() ) )
    await server.start()

run( main() )