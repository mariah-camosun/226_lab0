#!/usr/bin/python3.11
from socket import socket, AF_INET, SOCK_STREAM, IPPROTO_TCP, SOL_SOCKET, SO_KEEPALIVE, TCP_KEEPCNT, TCP_KEEPIDLE, TCP_KEEPINTVL
from traceback import format_exc

PORT = 12345
def echo(port):
    sock = socket(AF_INET, SOCK_STREAM)

    try:
        print('Enabling Keep Alive')
        sock.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
        n = 5
        print('Starting idle check after', n, 'seconds')
        sock.setsockopt(IPPROTO_TCP, TCP_KEEPIDLE, n)
        n = 10
        print('Continuing to ping every', n, 'seconds')
        sock.setsockopt(IPPROTO_TCP, TCP_KEEPINTVL, n)
        n = 3
        print('Deeming connection to be disconnected after', n, 'fails')
        sock.setsockopt(IPPROTO_TCP, TCP_KEEPCNT, n)
    except:
        print(f'*** Failed to set attribute; terminating program')
        return
    try:
        sock.bind(('localhost', port))
        sock.listen(1)
        sc, name = sock.accept()
        while True:
            data = sc.recv(1)
            if data == b'':
                break
            print(data)
    except Exception as e:
        print(e)
        print(format_exc())
    sock.close()
echo(PORT)