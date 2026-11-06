from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

BUF_SIZE = 1024
HOST = '127.0.0.1'
PORT = 12345

with socket(AF_INET, SOCK_STREAM) as sock:
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(1)
    print('Server:', sock.getsockname())
    sc, _ = sock.accept()
    with sc:
        print('Client:', sc.getpeername())
        data = sc.recv(BUF_SIZE)
        print(data)