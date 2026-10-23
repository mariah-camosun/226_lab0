#!/usr/bin/python3.11
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from struct import pack, unpack
from threading import Thread, current_thread, Semaphore

lock = Semaphore()
total = 0 

def receive(sc, size): 
    data = b''
    while len(data) < size: # waits until right length
        curr_data = sc.recv(size - len(data))
        if curr_data == b'': #or connection closed
            return data
        data += curr_data

    return data

def add_to_total( sc ):
    global total
    with sc: 
        data = receive( sc, SHORT )
        if len(data) != SHORT:
            return
        unpacked_data = unpack( '!H' , data)[0]
        # print(currentThread)
        print( unpacked_data )
        with lock: # only 1 thread can access this section at a time
            total += unpacked_data
            total_copy = total # never lock the send
        sc.sendall( pack( '!Q', total_copy )) #yes, intentionally diff from abv
                    #best way of guarding the data

SHORT = 2
# BUF_SIZE = 1024
HOST = '127.0.0.1'
PORT = 12345

with socket(AF_INET, SOCK_STREAM) as sock: # TCP socket
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # Details later; not neccessary, makes debugging easier
    sock.bind((HOST, PORT)) # Claim messages sent to port "PORT"
    sock.listen(1) # Server only supports a single 3-way handshake at a time
    # print('Server:', sock.getsockname()) # Server IP and port
    while True: # forever
        
        sc, _ = sock.accept() # Wait until a connection is established
        # with sc: #wrong ; sc = client socket, sock = server (one that spawns the sc -think mothership), and then one sc for *each client*
        Thread(target=add_to_total, args=(sc,)).start()
            # add_to_total(sc)