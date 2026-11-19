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
        self.clients = []
        self.client_queues = {} # dictionary of clients & their queues

        self.set_server( start_server() )

    ####################### INITIALIZATION HELPERS #######################
    async def start_server(self):
        server = await start_server( self.new_client, self.HOST, self.PORT )
        await server.serve_forever()
        return server

    async def new_client( self, reader: StreamReader, writer: StreamWriter)-> None:
        to_client_queue = Queue()
        client_name = writer.get_extra_info('peername')
        print( "connected to client:", client_name)
        self.add_client({ client_name, reader, writer })
        client_cmd = create_task( self.receive_from_client( client_name, reader, writer ) )
        to_cli_task = create_task( self.send_to_client( to_client_queue, client_name, reader, writer ) )

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
    def __set_clients(self, client_array):
        self.clients = client_array

    def get_client_queues(self):
        return self.client_queues
    def set_client_queues(self, queue_array):
        self.client_queues = queue_array

    # ~~~~~~~~~~~~~~~~~~~~~~~ EXPANDED GETTERS & SETTERS ~~~~~~~~~~~~~~~~~~~~~~~
    def __add_client( self, new_client ):
        self.clients.append( new_client )

    # this one probably wont work right as written....
    def del_client( self, del_client ):
        self.clients.remove( del_client )

    #expect prob  w  .append & dictionary
    def __add_client_queue( self, new_client_queue ):
        self.client_queues.append( new_client_queue ) # dont think append works w dictionary...

    ####################### TRANSFER DATA #######################
    async def route_to_client_send_queue( self ):
        while True:
            client, cmd = await self.get_output_queue().get()

            if client is None:
                for client in self.get_client_queues().values():
                    client.put( cmd )
            elif client in self.get_client_queues():
                    self.client_queues[client].put(cmd)                
            else:
                # error? print? both? "client closed"


    # async def send_to_client( self, to_client_queue, client_name, reader, writer ):
    #     while True:
    #         cmd, writer = await self.output_queue.get()
    #         if writer:
    #             writer.write( cmd )
    #             await writer.drain()
    #     #         # send to only the one writer
    #         else:
    #             # this is not *entirely* how i'd want to do it....
    #             # separate client queues so that lag in one doesnt affect
    #             # the other would be better, but for now this will do
    #             # ... add iniv client queues and copy to them depending on if the command
    #             # is for one or both? the game itself doesnt see the server/clients directly
    #             # just the queue. or does async take care of this? hard to tell...
    #             # test with a sleep and prints to see!
    #             for client in self.get_clients():
    #                 name, reader, writer = client
    #                 writer.write( cmd )
    #                 await writer.drain()
    #             # send to both


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