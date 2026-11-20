#!/usr/bin/python3.11
# from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
# from threading import Thread, current_thread, Semaphore
from asyncio import run, start_server, StreamReader, StreamWriter, Queue, create_task #, #open_connection
from struct import pack, unpack
# from queue import Queue
from Board import Board
# import sys
import constants
'''
Server class that will connect to specified number of clients and hand off commands to a 
input_queue, and will accept commands from an output_queue and send those to clients 
(if unspecified, broadcast, otherwise to specified client)
'''
class Server:
    # MIN_PACK_BYTES = 2
    # member functions
    def __init__(self, BUF_SIZE = 1, HOST = '', PORT = 12345, MAX_CLIENTS = 2):
        self.BUF_SIZE = BUF_SIZE
        self.HOST = HOST
        self.PORT = PORT
        self.MAX_CLIENTS = MAX_CLIENTS

        self.input_queue = Queue()
        self.output_queue = Queue()
        self.clients = {}
        self.clients_connected = 0 # all-time, not current!

        create_task( self.route_to_client_send_queue(), name="game-out-to-cli-queues" )

    ####################### INITIALIZERS #######################
    async def start(self):
        self.set_server( await start_server( self.new_client, self.HOST, self.PORT, reuse_address=True) )
        await self.server.serve_forever()

    async def new_client( self, reader: StreamReader, writer: StreamWriter)-> None:
        client_name = writer.get_extra_info('peername')
        print( "connected to client:", client_name)
        self.add_client(client_name, reader, writer, Queue()) # creates & records a new queue per client
        client_cmd = create_task( self.receive_from_client( client_name ), name=f"{client_name}-IN" )
        to_cli_task = create_task( self.send_to_client( client_name ), name=f"{client_name}-OUT" )

    ####################### GETTERS & SETTERS #######################
    def get_input_queue(self):
        return self.input_queue

    def get_output_queue(self):
        return self.output_queue

    def get_BUF_SIZE(self):
        return self.BUF_SIZE

    def get_server(self):
        return self.server
    def set_server(self, server):
        self.server = server

    def get_clients(self):
        return self.clients
    def set_clients(self, client_array):
        self.clients = client_array

    def get_clients_connected(self):
        return self.clients_connected
    
    # ~~~~~~~~~~~~~~~~~~~~~~~ EXPANDED GETTERS & SETTERS ~~~~~~~~~~~~~~~~~~~~~~~
    def add_client( self, client_name, reader, writer, cli_queue ):
        self.clients_connected += 1
        self.clients[client_name] = {
            "id": self.get_clients_connected(),
            "reader": reader,
            "writer": writer,
            "queue": cli_queue
        }

    # this one probably wont work right as written....
    def del_client( self, del_client ):
        return self.clients.pop( del_client )

    def get_a_client_queue(self, client_name):
        return self.clients[client_name]["queue"]

    def get_a_client_info(self, client_name):
        return self.clients.get( client_name )

    def get_all_clients_names(self):
        return list( self.get_clients().keys() )

    def get_all_clients_info(self):
        return list( self.get_clients().values() )

    ####################### TRANSFER DATA #######################
    async def route_to_client_send_queue( self ):
        while True:
            cmd, client = await self.get_output_queue().get()
            print("attempting route from board-out to to-client queues")

            if client is None:
                for client in self.get_all_clients_info():
                    await client['queue'].put( cmd )
            else:
                await self.get_a_client_queue( client ).put(cmd)
   #                              
                # error? print? both? "client closed"

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

    async def receive_from_client( self, client_name ) -> None:
        '''
        get client requests and passes them to handler to proccess, queues processed cmd
        '''
        reader = self.get_a_client_info( client_name )['reader']
        # manual_print = pack( constants.REG_PACK_FLAG, constants.C_PRINT_CMD)
        # await self.input_queue.put( (constants.C_PRINT_CMD, client_name) )

        # print("manually put print board when client connected")

        # get raw data
        while True:
            raw_data = await reader.read( self.BUF_SIZE )
            print("raw data recieved:", raw_data)

            if raw_data:
                data = unpack( constants.REG_PACK_FLAG, raw_data )[0]
            else:
                self.del_client(client_name)
                print(f"client {client_name} disconnected")
                break
          
            print( "client:", client_name, "raw data recieved:", raw_data, "unpacked:", data, bin(data) )

            await self.input_queue.put( (data, client_name) )
            print("put cmd into input queue")

    async def send_to_client(self, client_name):
        queue = self.get_a_client_info( client_name )['queue']
        writer = self.get_a_client_info( client_name )['writer']
        
        while True:
            cmd = await queue.get()
            print("got cmd from to-client queue of", client_name)
            # buffer get
            writer.write( cmd )
            await writer.drain()