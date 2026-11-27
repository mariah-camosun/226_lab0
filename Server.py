#!/usr/bin/python3.11
# from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
# from threading import Thread, current_thread, Semaphore
from asyncio import run, start_server, StreamReader, StreamWriter, Queue, create_task #, #open_connection
from struct import pack, unpack
# from queue import Queue
from game.treasureweb.game.gameProg.Board import Board
# import sys
import game.treasureweb.game.gameProg.constants as constants
'''
Server class that will connect to specified number of clients and hand off commands to a 
input_queue, and will accept commands from an output_queue and send those to clients 
(if unspecified, broadcast, otherwise to specified client)

command interpretation is handled by main program
server instances must be created, and then '.start()'ed to run 
'''
    # MIN_PACK_BYTES = 2
    # member functions
class Server:

    def __init__(self, BUF_SIZE = 1, HOST = '', PORT = 12345, MAX_CLIENTS = 2):
        '''
        initializes server instance variables and task to route from a single out-going
        queue to per-client queues.

        :param BUF_SIZE: int, buffer size in bytes. default 1
        :param HOST: str, host server ip. default ''
        :param PORT: int, host server port. default 12345
        :param MAX_CLIENTS: maximum intended simultaneous clients. default 2
        '''
        self.BUF_SIZE = BUF_SIZE
        self.HOST = HOST
        self.PORT = PORT
        self.MAX_CLIENTS = MAX_CLIENTS

        self.input_queue = Queue()
        self.output_queue = Queue()
        self.clients = {}
        self.clients_connected = 0 # all-time per instance, not current!

    #~##################### INITIALIZERS #######################
    async def start(self):
        '''
        sets up and starts the server listener task. Sets to always open, quickly makes closed ports re-available.
        '''
        self.task_to_cli_queue = create_task( self.route_to_client_send_queue(), name="game-out-to-cli-queues" )
        try:
            self.set_server( await start_server( self.new_client, self.HOST, self.PORT, reuse_address=True) )
            await self.server.serve_forever()
        except Exception:
            # print(f'server not running')
            return

    async def new_client( self, reader: StreamReader, writer: StreamWriter)-> None:
        '''
        sets up a tasks (listening and ourgoing queues) for each client when it connects
        and adds the needed client information to the internal client dictionary

        :param reader: asyncio reader (listener component) for the new client
        :param writer: asyncio writer (sender component) for the new client
        '''
        try:
            client_name = writer.get_extra_info('peername')
            print('new client:', client_name)
        except Exception:
            print("problem connecting client")
            return

        try:            
            client_info = self.add_client(client_name, reader, writer, Queue()) # creates & records a new queue per client
            client_info['from_cli_task'] = create_task( self.receive_from_client( client_name ), name=f"{client_name}-IN" )
            client_info['to_cli_task'] = create_task( self.send_to_client( client_name ), name=f"{client_name}-OUT" )
        except Exception:
            self.del_client( client_name )

    #~##################### GETTERS & SETTERS #######################
    def get_input_queue(self):
        '''
        gets & returns the server instance's input queue
        :return: Queue, input queue 
        '''
        return self.input_queue

    def get_output_queue(self):
        '''
        gets & returns the *server instance's* output queue.
        One per server. Commands to be routed to appropriate client queues.
        :return: Queue, output queue
        '''
        return self.output_queue

    def get_BUF_SIZE(self):
        '''
        gets the server buffer size ( or more accurately, the number of bytes 
        it expects declarative command portion to be)
        :return: int, 'buffer' size in bytes
        '''
        return self.BUF_SIZE

    def get_server(self):
        '''
        returns the contents of the self.server variable - possibly redundant/unneeded code
        leftover from other things. Haven't confirmed.
        :return: Server type? reference to server task
        '''
        return self.server

    def set_server(self, server):
        '''
        sets self.server variable to reference to the server - possibly redundant/unneeded code
        leftover from other things. Haven't confirmed.
        :param server: Server type? return of server task
        '''
        self.server = server

    def get_clients(self):
        '''
        gets and returns the client dictionary of currently connected clients
        keys are client_name, with value a nested dictionary of per client information:
            id (int), reader, writer, queue
        :return: dictionary of connected clients  
        '''
        return self.clients

    def get_clients_connected(self):
        '''
        gets and returns the total number of clients that have connected to 
        this server instance
        :return: int, total clients connections made
        '''
        return self.clients_connected
    
    # ~~~~~~~~~~~~~~~~~~~~~~~ EXPANDED GETTERS & SETTERS ~~~~~~~~~~~~~~~~~~~~~~~
    def add_client( self, client_name, reader, writer, cli_queue ):
        '''
        adds a single client to the client dictionary (self.clients)
        :param client_name: string, client name
        :param reader: Streamreader for client
        :param writer: Streamwriter for client
        :param cli_queue: Queue, outgoing queue for this client
        :returns dictionary: the contents of the client_name key
        '''
        self.clients_connected += 1
        self.clients[client_name] = {
            "id": self.get_clients_connected(),
            "reader": reader,
            "writer": writer,
            "queue": cli_queue
        }
        return self.clients[client_name]

    def del_client( self, del_client ):
        '''
        removes specified client from the client dictionary
        :param del_client: string, name of client to be removed
        :return: dictionary, client dictionary (values) of removed client
        '''
        try:
            deleted = self.clients.pop( del_client )
            if not deleted:
                return
            
            writer = deleted['writer']
            if writer:
                writer.close()

            deleted['from_cli_task'].cancel()
            deleted['to_cli_task'].cancel()

            print(f'client {del_client} disconnected')
            return deleted
        except Exception:
            print(f"problem disconnecting {del_client}")
            return           

    def get_a_client_info(self, client_name):
        '''
        gets and return the information dictionary of a specified client
        :param client_name: dictionary, client to find information of
        :return: dictionary, client information
        '''
        try:
            return self.clients.get( client_name )
        except Exception:
            self.del_client(client_name)
            return    

    def get_a_client_queue(self, client_name):
        '''
        gets and returns the queue of a specified client
        :param client_name: string, name of client
        :return: Queue, outgoing queue for specified client 
        '''
        try:
            return self.clients[client_name]["queue"]
        except Exception:
            # print(f"client {client_name} disconnected")
            return

    def get_all_clients_names(self):
        '''
        gets and returns a list of all current client names
        :return: list of client names (keys of client dictionary)
        '''
        return list( self.get_clients().keys() )

    def get_all_clients_info(self):
        '''
        gets and returns a list of all current clients' information
        :return: list of dictionaries of client information
        '''
        return list( self.get_clients().values() )

    #~##################### TRANSFER DATA #######################
    async def route_to_client_send_queue( self ):
        '''
        moves commands in outgoing queue to client queues. Client queue
        decided by contents in second half of command tupple, client name
        if none, sends to all clients
        '''
        try:
            while True:
                cmd, client = await self.get_output_queue().get()

                if client is None:
                    for client in self.get_all_clients_info():
                        await client['queue'].put( cmd )
                else:
                    await self.get_a_client_queue( client ).put(cmd)
        except Exception:
            # print( "cancelled task" )
            return

    async def receive_from_client( self, client_name ) -> None:
        '''
        get client requests, unpacks, and queues unpacked cmd. Only revieces 
        comds of exactly set 'buffer' size. Removes client from dictionary 
        if disconnected.
        :param client_name: string, client name of relevant client
        '''
        try:
            reader = self.get_a_client_info( client_name )['reader']
        except Exception:
            self.del_client(client_name)
            return

        try:
            while True:
                raw_data = await reader.read( self.BUF_SIZE )

                try:
                    data = unpack( constants.REG_PACK_FLAG, raw_data )[0]
                except Exception:
                    self.del_client(client_name)
                    break

                await self.input_queue.put( (data, client_name) )
        except Exception:
            self.del_client(client_name)
            return

    async def send_to_client(self, client_name):
        '''
        takes commands in *client specific* outgoing queue and sends to client
        :param client_name: string, client name of relevant client
        '''
        try:
            queue = self.get_a_client_info( client_name )['queue']
            writer = self.get_a_client_info( client_name )['writer']
        except Exception:
            self.del_client( client_name )
            return
        try:
            while True:
                cmd = await queue.get()
                writer.write( cmd )
                await writer.drain()
        except Exception:
            self.del_client( client_name )
            return