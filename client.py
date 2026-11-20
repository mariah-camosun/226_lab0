#!/usr/bin/python3.11

from socket import socket, AF_INET, SOCK_STREAM
from sys import argv
import constants
import time
from struct import pack, unpack
# from threading import Thread, current_thread, Semaphore
from struct import pack, unpack
# from queue import Queue
from asyncio import run, open_connection, create_task, gather, Queue, to_thread
import traceback

import constants

BUF_SIZE = 1024
# HOST = '10.21.75.22' # mine
HOST = '10.21.75.50' # bbcli
# HOST = '10.21.75.14' # Felix
# HOST = '10.21.75.16' #
PORT = 12345

###########################  SUB CLASS USER INPUT  ###########################
class User_Input:
    def __init__(self):
        self.cmd_queue = Queue()

    def get_cmd_queue(self):
        return self.cmd_queue

    async def get_player_commands(self): #, board_size ):    
        '''
        Prompt user for command: print or move direction.
        Repeat until a valid option is entered

        :return: str, command letter
        '''
        print("\nChoose one of: re-print board (p), or move up(u), down(d), left(l), right(r)")
        while (True):
            try:
                command = await to_thread( input, "" )   
                self.validate_command( command.upper() )
            except ValueError:
                print(f"Invalid entry, choose one of: P, U, D, L, R") # will also accept lower case
                continue
            else:
                await self.cmd_queue.put( command.upper() )

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
    if cmd == constants.PRINT:
        writer.write( pack ( constants.REG_PACK_FLAG, constants.C_PRINT_CMD ) )
        await writer.drain()
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

        await send_move_cmd( dir, player, writer )
    else:
        return

async def send_move_cmd( cmd, player, writer ):
    cmd = cmd << constants.C_MOVE_TAIL
    pl_cmd = (player - 1) << constants.C_MOVE_P_SHIFT
    complete_cmd = cmd | pl_cmd
    writer.write( pack ( constants.REG_PACK_FLAG, complete_cmd ) )
    await writer.drain()

###########################  ROUTING  ###########################
async def direct_reply( data, reader ):
    temp_data = unpack( constants.REG_PACK_FLAG, data )[0]
    cmd = temp_data >> ( constants.BYTE_SIZE - constants.S_CMD_SIZE )
    if cmd == 0b00:
        await get_board( temp_data, reader )
        return

    elif cmd == 0b01 or cmd == 0b10:
        data_pt2 = await reader.read( 1 )
        data_pt2 = unpack( constants.REG_PACK_FLAG, data_pt2 )[0]
        full_cmd = ( temp_data << constants.BYTE_SIZE | data_pt2 )
        if cmd == 0b10:
            await handle_delta(full_cmd)
        else:
            await handle_score(full_cmd)

###########################  RECIEVE CMDS  ###########################
async def handle_delta( reply ):
    row = ( reply & constants.S_ROW_MASK ) >> constants.S_ROW_TAIL_SIZE
    col = ( reply & constants.S_COL_MASK ) >> constants.S_COL_TAIL_SIZE
    contents = ( reply & constants.TILE_MASK )
    print( 'delta: row:', (row), 'col:', (col), 'contents', bin(contents) )
    return row, col, contents

async def handle_score( reply ):
    p1_score = reply >> ( 6 + 4 )
    p1_score = p1_score & 0b001111
    p2_score = reply >> ( 6 )
    p2_score = p2_score & 0b0000001111
    # print('player 1 score:', bin(p1_score), 'player 2 score:', bin(p2_score))
    print('player 1 score:', p1_score)
    print('player 2 score:', p2_score)
    print( "\nChoose one of: re-print board (p), or move up(u), down(d), left(l), right(r)" )
    return p1_score, p2_score    

async def get_board( reply, reader ):
    size = ( reply & constants.S_PRINT_OPT_MASK ) >> constants.S_PRINT_TAIL
    data = await reader.read( size * size )
    board = data.decode()
    print( prettify_board( board, size ) )
    print( "\nChoose one of: re-print board (p), or move up(u), down(d), left(l), right(r)" )
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
async def recieve_server_cmds( reader ):
        while (True):
            try:
                reply = await reader.read(1)
                await direct_reply( reply, reader )
                
            except Exception:
                pass
                # traceback.print_exc()

async def send_user_command( input, player, writer ):
    while (True):
        cmd = await input.get_cmd_queue().get()
        await send_command( cmd, player, writer )

async def setup( player ):
    reader, writer = await open_connection( HOST, PORT)
    input = User_Input()
    
    get_cmd_task = create_task( input.get_player_commands() )
    send_cmd_task = create_task( send_user_command(input, player, writer))
    listener_task = create_task( recieve_server_cmds( reader ))
    await gather( get_cmd_task, send_cmd_task, listener_task)

###########################  Main  ###########################
def main():
    try:
        player = int(argv[1])
    except:
        print( 'Missing player number argument, enter 1 or 2' )
    else:
        run( setup( player ) )

run( main() )