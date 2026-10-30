#!/usr/bin/python3.11

from socket import socket, AF_INET, SOCK_STREAM
from sys import argv
import main
import constants

BUF_SIZE = 2
HOST = '10.21.75.22'
PORT = 65432

def request_board():
    # send request (already binary string)
    main.send_cmd(sock, constants.PRINT_CMD, '!B')
    
    # recieve, decode & interpret data
    reply = sock.recv( BUF_SIZE )
    decoded_reply = reply.decode()
    print('Reply:', decoded_reply)
    return decoded_reply    

with socket(AF_INET, SOCK_STREAM) as sock:
    # create connection
    sock.connect(( HOST, PORT ))
    print( 'Client:', sock.getsockname())

    board = request_board()