#!/usr/bin/python3.11
from socket import socket, AF_INET, SOCK_STREAM
from traceback import format_exc

HOST = '127.0.0.1'
PORT = 12345

def echo(host, port):
    sock = socket(AF_INET, SOCK_STREAM)
    try:
        sock.connect((host, port))
        while True:
            data = input()
            sock.sendall(data.encode('utf-8'))
    except Exception as e:
        print(e)
        print(format_exc())
    sock.close()
echo(HOST, PORT)