#!/usr/bin/python3.11

from socket import socket, AF_INET, SOCK_STREAM
from sys import argv
import main
import constants
import asyncio
from struct import pack, unpack

BUF_SIZE = 2
HOST = '10.21.75.22'
PORT = 12345

def request_board():
    # send request (already binary string)
    main.send_cmd(sock, constants.PRINT_CMD, '!B')
    
    # recieve, decode & interpret data
    reply = sock.recv( BUF_SIZE )
    print( reply )
    # decoded_reply = reply.decode()
    unpacked = unpack( '!H', reply )
    print('Reply:', unpacked)
    return unpacked    

sock = socket(AF_INET, SOCK_STREAM)
# with socket(AF_INET, SOCK_STREAM) as sock:
    # create connection
sock.connect(( HOST, PORT ))
print( 'Client:', sock.getsockname())

board = request_board()