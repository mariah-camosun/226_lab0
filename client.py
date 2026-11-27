#!/usr/bin/python3.11
from socket import socket, AF_INET, SOCK_STREAM
from sys import argv
import game.treasureweb.game.gameProg.constants as constants
from struct import pack, unpack
from asyncio import run, open_connection, create_task, gather, Queue, to_thread
import traceback
import game.treasureweb.game.gameProg.constants as constants

BUF_SIZE = 1024
HOST = '10.21.75.22' # mine
# HOST = '10.21.75.50' # bbcli
# HOST = '10.21.75.14' # Felix
# HOST = '10.21.75.16' #
PORT = 12345

###########################  SUB CLASS USER INPUT  ###########################
class User_Input:
    '''
    Class for collecting user input from the command line
    '''

    def __init__(self):
        '''
        initialize instance of User_Input & its' queue
        '''
        self.cmd_queue = Queue()

    def get_cmd_queue(self):
        '''
        gets and returns the command queue of player commands
        :return: Queue, player commands
        '''
        return self.cmd_queue

    async def queue_player_commands(self): #, board_size ):    
        '''
        Prompt user for command: print or move direction.
        Repeat until a valid option is entered

        :return: str, command letter
        '''
        prompt_command()
        while (True):
            try:
                command = await to_thread( input, "" )   
                self.validate_command( command.upper() )
            except ValueError:
                print(f"Invalid entry, choose one of: P, U, D, L, R") # will also accept lower case
                continue
            else:
                try:
                    await self.cmd_queue.put( command.upper() )
                except Exception:
                    print('problem sending command')
                    return

    def validate_command( self, cmd ):
        '''
        Checks if command is one of the valid options
        :param cmd: str, command
        :return: bool, True if valid, else raises an error
        '''
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
###########################  SUB CLASS ENDS  ###########################



###########################  SEND CMDS   ###########################
async def send_command( cmd, player, writer ):
    '''
    formats and sends collected player commands to server

    :param cmd: string, player command as input format
    :param player: int, player number
    :param writer: Streamwriter of server/client connection
    '''
    if cmd == constants.PRINT:
        try:
            writer.write( pack ( constants.REG_PACK_FLAG, constants.C_PRINT_CMD ) )
            await writer.drain()
        except Exception:
            print('server disconnected')
            return
    elif ( cmd == constants.UP or cmd == constants.DOWN or cmd == constants.LEFT or cmd == constants.RIGHT):
        dir = ''
        if cmd == constants.UP:
            dir = constants.UP_BIN_MIN
        elif cmd == constants.DOWN:
            dir = constants.DOWN_BIN_MIN
        elif cmd == constants.LEFT:
            dir = constants.LEFT_BIN_MIN
        elif cmd == constants.RIGHT:
            dir = constants.RIGHT_BIN_MIN

        try:
            await send_move_cmd( dir, player, writer )
        except Exception:
            print('server disconnected')
            return
    else:
        return

async def send_move_cmd( cmd, player, writer ):
    '''
    formats and sends move commands to server

    :param cmd: int, player command converted to protocol numbers
    :param player: int, player number (per board player)
    :param writer: Streamwriter of server/client connection
    '''
    cmd = cmd << constants.C_MOVE_TAIL
    pl_cmd = (player - 1) << constants.C_MOVE_P_SHIFT
    complete_cmd = cmd | pl_cmd
    try:
        writer.write( pack ( constants.REG_PACK_FLAG, complete_cmd ) )
        await writer.drain()
    except Exception:
        print('server disconnected')
        return

def prompt_command():
    print( "\nChoose one of: re-print board (p), or move up(u), down(d), left(l), right(r)" )

###########################  ROUTING  ###########################
async def direct_reply( data, reader ):
    '''
    directs actions depending on command recieved

    :param data: packed incoming command
    :param reader: Streamreader of server/client connection
    '''    
    temp_data = unpack( constants.REG_PACK_FLAG, data )[0]
    cmd = temp_data >> ( constants.BYTE_SIZE - constants.S_CMD_SIZE )
    if cmd == constants.PRINT_BOARD_CMD:
        await get_board( temp_data, reader )
        return

    elif cmd == constants.S_SCORE_CMD or cmd == constants.DELTA_CMD:
        data_pt2 = await reader.read( 1 ) # read remaining 1 byte of commands
        data_pt2 = unpack( constants.REG_PACK_FLAG, data_pt2 )[0]
        full_cmd = ( temp_data << constants.BYTE_SIZE | data_pt2 )
        if cmd == constants.DELTA_CMD:
            await handle_delta(full_cmd)
        else:
            await handle_score(full_cmd)

###########################  RECIEVE CMDS  ###########################
async def handle_delta( reply ):
    '''
    breaks down and interprets delta commands *recieved* from server

    :param reply: unpacked server command
    :returns tupple: int row index, int column index, int contents cmd number 
    '''
    row = ( reply & constants.S_ROW_MASK ) >> constants.S_ROW_TAIL_SIZE
    col = ( reply & constants.S_COL_MASK ) >> constants.S_COL_TAIL_SIZE
    contents = ( reply & constants.TILE_MASK )
    print( 'delta: row:', (row), 'col:', (col), 'contents', bin(contents) )
    return row, col, contents

async def handle_score( reply ):
    '''
    breaks down and interprets score commands *recieved* from server

    :param reply: unpacked server command
    :returns tupple: int player 1 score, int player 2 score 
    '''    
    p1_score = reply >> ( constants.SCORE_BIT_CT + constants.S_SCORE_TAIL )
    p1_score = p1_score & constants.P1_SCORE_MASK
    p2_score = reply >> ( constants.S_SCORE_TAIL )
    p2_score = p2_score & constants.P2_SCORE_MASK
    # print('player 1 score:', bin(p1_score), 'player 2 score:', bin(p2_score))
    print('player 1 score:', p1_score)
    print('player 2 score:', p2_score)
    prompt_command()
    return p1_score, p2_score    

async def get_board( reply, reader ):
    '''
    breaks down and interprets show/print board commands *recieved* from server

    :param reply: unpacked server command
    :param reader: Streamreader of server/client connection
    :returns string: board string
    '''
    size = ( reply & constants.S_PRINT_OPT_MASK ) >> constants.S_PRINT_TAIL
    try:
        data = await reader.read( size * size )
    except Exception:
        print('server disconnected')
        return
    board = data.decode()
    print( prettify_board( board, size ) )
    prompt_command()
    return board

def prettify_board( board, board_size ):
    '''
    transforms the raw board string recieved from the server to a prettier 
    format for displaying in terminal
    :param board: Board, the active board
    :param board_size: int, size of the board
    :returns string: 'pretty' version of string
    '''
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
async def recieve_server_cmds( reader ):
        '''
        task to wait for incoming server commands

        :param reader: Streamreader of server/client connection
        '''
        while (True):
            try:
                reply = await reader.read(1) # read only first byte of command
                await direct_reply( reply, reader )
                
            except Exception:
                print('server disconnected')
                return

async def send_user_command( input, player, writer ):
    '''
    task to recieve user commands from user command queue and send them to server

    :param input: Queue the input queue of player commands
    :param player: int, player number (per board counting, 1 indexed)
    :param writer: Streamwriter of server/client connection
    '''
    try:
        while (True):
            cmd = await input.get_cmd_queue().get()
            await send_command( cmd, player, writer )
    except Exception:
        print('server disconnected')
    
async def setup():
    '''
    checks that client has chosen a player number, or else returns an error. 
    Then sets up and runs player client
    sends initial print board command
    '''
    try:
        player = int(argv[1])
    except:
        print( 'Missing player number argument, enter 1 or 2' )
        return

    try:
        reader, writer = await open_connection( HOST, PORT)
        input = User_Input()
        
        get_cmd_task = create_task( input.queue_player_commands() )
        listener_task = create_task( recieve_server_cmds( reader ))
        send_cmd_task = create_task( send_user_command(input, player, writer))
        try:
            await send_command( constants.PRINT, player, writer )
        except Exception:
            print('server disconnected')
        await gather( get_cmd_task, send_cmd_task, listener_task)
    except Exception:
        print( 'problem seting up')
        return

run( setup() )