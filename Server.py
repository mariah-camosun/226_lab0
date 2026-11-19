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
    def __init__(self, BUF_SIZE = 1, HOST = '', PORT = 12345, MAX_PLAYERS = 2):
        self.BUF_SIZE = BUF_SIZE
        self.HOST = HOST
        self.PORT = PORT
        self.MAX_PLAYERS = MAX_PLAYERS

        self.input_queue = Queue()
        self.output_queue = Queue()
        self.clients = {}

    ####################### INITIALIZERS #######################
    async def start(self):
        self.__set_server( await start_server( self.new_client, self.HOST, self.PORT) )
        await self.server.serve_forever()

    async def new_client( self, reader: StreamReader, writer: StreamWriter)-> None:
        client_name = writer.get_extra_info('peername')
        print( "connected to client:", client_name)
        self.__add_client(client_name, reader, writer, Queue()) # creates & records a new queue per client
        client_cmd = create_task( self.receive_from_client( client_name, reader, writer ), name=f"{client_name}-IN" )
        to_cli_task = create_task( self.route_to_client_send_queue(), name=f"{client_name}-OUT" )

    ####################### GETTERS & SETTERS #######################
    def get_input_queue(self):
        return self.input_queue

    def get_output_queue(self):
        return self.output_queue

    def get_BUF_SIZE(self):
        return self.BUF_SIZE

    def get_server(self):
        return self.server
    def __set_server(self, server):
        self.server = server

    def get_clients(self):
        return self.clients
    def __set_clients(self, client_array):
        self.clients = client_array

    # ~~~~~~~~~~~~~~~~~~~~~~~ EXPANDED GETTERS & SETTERS ~~~~~~~~~~~~~~~~~~~~~~~
    def __add_client( self, client_name, reader, writer, cli_queue ):
        self.clients[client_name] = {
            "reader": reader,
            "writer": writer,
            "queue": cli_queue
        }

    # this one probably wont work right as written....
    def __del_client( self, del_client ):
        return self.clients.pop( del_client )

    def get_a_client_queue(self, client_name):
        return self.clients[client_name]["queue"]

    def get_a_client_info(self, client_name):
        client_info = self.clients.get( client_name )
        if client_info:
            reader, writer, queue = client_info

    ####################### TRANSFER DATA #######################
    async def route_to_client_send_queue( self ):
        while True:
            client, cmd = await self.get_output_queue().get()

            if client is None:
                for client in self.get_client_queues().values():
                    client.put( cmd )
            elif client in self.get_client_queues():
                    self.client_queues[client].put(cmd)
    #           prev abv was:
    #         elif:
    #             # this is not *entirely* how i'd want to do it....
    #             # separate client queues so that lag in one doesnt affect
    #             # the other would be better, but for now this will do
    #             # ... add iniv client queues and copy to them depending on if the command
    #             # is for one or both? the game itself doesnt see the server/clients directly
    #             # just the queue. or does async take care of this? hard to tell...
    #             # test with a sleep and prints to see!
    #             for client in self.get_clients():  # send to both  
    #                 name, reader, writer = client
    #                 writer.write( cmd )
    #                 await writer.drain()
    #                              
            else:
                pass
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

    async def receive_from_client( self, client_name, reader, writer ) -> None:
        '''
        get client requests and passes them to handler to proccess, queues processed cmd
        '''
        # get raw data
        while True:
            raw_data = await reader.read( self.BUF_SIZE )
            data = unpack( constants.REG_PACK_FLAG, raw_data )[0]
            print( "client:", client_name, "raw data recieved:", raw_data, "unpacked:", data, bin(data) )
            await self.input_queue.put( {data, reader, writer} )


# async def send_to_client(client)->None:
#     while True:
        
#         # get from queue, if nothing, wait
#         out = await output_queue.get()

#         # send
#         send_to_clients()

#         # mark complete
#         output_queue.task_done()
#         print("sent output command")