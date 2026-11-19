#!/usr/bin/python3.11
# from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
# from threading import Thread, current_thread, Semaphore
from asyncio import run, start_server, StreamReader, StreamWriter, Queue, create_task #, #open_connection
from struct import pack, unpack
# from queue import Queue
from Board import Board
# import sys
import constants

class Server:
    # class variables ( same for everybody )
    BUF_SIZE = 1 # in bytes
    HOST = ''
    PORT = 12345

    MIN_PACK_BYTES = 2
    MAX_PLAYERS = 2

    # member functions
    def __init__(self):

        game_queue = Queue()
        output_queue = Queue()        

        self.set_server( start_server() )


    async def start_server():
        server = await start_server( new_client, cls.HOST, cls.PORT )
        await server.serve_forever()
        return server



async def new_client( reader: StreamReader, writer: StreamWriter)-> None:
    to_client_queue = Queue()
    client_name = writer.get_extra_info('peername')
    print( "connected to client:", client_name)
    client_cmd = create_task( receive_from_client( client_name, reader, writer ) )
    to_cli_task = create_task( send_to_client( to_client_queue, client_name, reader, writer ) )
