from socket import socket, AF_INET, SOCK_STREAM
from sys import argv

BUF_SIZE = 1024
HOST = '127.0.0.1'
PORT = 12345

if len(argv) != 2:
    print(argv[0] + ' message')
    exit()

with socket(AF_INET, SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    print('Client:', sock.getsockname())
    data = argv[1].encode('utf-8')
    sock.sendall(data)