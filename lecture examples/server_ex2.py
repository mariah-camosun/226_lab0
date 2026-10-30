# #!/usr/bin/python3.11
# from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
# from struct import pack, unpack
# from threading import Thread, current_thread, Semaphore

# lock = Semaphore()
# total = 0 

# def receive(sc, size): 
#     data = b''
#     while len(data) < size: # waits until right length
#         curr_data = sc.recv(size - len(data))
#         if curr_data == b'': #or connection closed
#             return data
#         data += curr_data

#     return data

# # sending 0b00101010 er but in hex. as 0x2a
# def add_to_total( sc ):
#     with sc: 
#         data = receive( sc, 1 )
#         if len(data) != 1:
#             return
#         unpacked_data = unpack( '!B' , data)[0]

#         op = unpacked_data >> 6
#         num1 = unpacked_data >> 3 & 0b111 #need to remove operator
#         num2 = unpacked_data & 0b111 # take unpacked data, but fist? 3 get filtered out (num 1)
#         result = 0
#         if op == 0:
#             result = num1 + num2
#             print( op, '  ',  bin(num1), '  ', bin(num2))
#         elif op == 1:
#             result = num1 - num2
#         elif op == 2:
#             result = num1 * num2
#         else:
#             result = num1 // num2
#         print('Result = ', result)
#         sc.sendall( pack( '!Q', total_copy )) #yes, intentionally diff from abv
#                     #best way of guarding the data

# SHORT = 2
# # BUF_SIZE = 1024
# HOST = '127.0.0.1'
# PORT = 12345

# with socket(AF_INET, SOCK_STREAM) as sock: # TCP socket
#     sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # Details later; not neccessary, makes debugging easier
#     sock.bind((HOST, PORT)) # Claim messages sent to port "PORT"
#     sock.listen(1) # Server only supports a single 3-way handshake at a time
#     # print('Server:', sock.getsockname()) # Server IP and port
#     while True: # forever
        
#         sc, _ = sock.accept() # Wait until a connection is established
#         # with sc: #wrong ; sc = client socket, sock = server (one that spawns the sc -think mothership), and then one sc for *each client*
#         Thread(target=add_to_total, args=(sc,)).start()
#             # add_to_total(sc)