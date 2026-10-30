# from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
# from struct import unpack

# BUF_SIZE = 8
# DLAG = '!Q'
# HOST = ''
# PORT = 12345
# QUEUE_SIZE = 1 

# SHORT = 2

# sum = 0

# def sum_bits( num ):
#     first4 = num[0].tostring() + num[1].tostring() +num[2].tostring() +num[3].tostring()
#     last4 = num[-4].tostring() + num[-3].tostring() +num-[2].tostring() +num[-1].tostring()
#     return first4 + last4

# def receive(sc, size):
#     data = b''
#     while len(data < size):
#         curr_data = sc.recv(size - len(data))
#         if curr_data == b'':
#             return data
#         data += curr_data
#     return data

# # def add_4bits_sum(sc):
# #     global sum
# #     with sc: 
# #         data = receive( sc, SHORT )
# #         if len(data) != SHORT:
# #             return
# #         unpacked_data = unpack( '!Q', data)[0]
# #         sum_bits(  unpacked_data )
# #         sum += unpacked_data
# #         # convert from chars and then send that? no 'string' in flags in notes
# #         sc.sendall( pack( '!C', sum) )

# receive(sc, BUF_SIZE)

# with socket(AF_INET, SOCK_STREAM) as sock:
#     sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
#     sock.bind((HOST, PORT))
#     sock.listen( QUEUE_SIZE )
#     while True: # while up and running
#         try:
#             sc, _ = sock.accept()
#             with sc:
#                 data=sc.rcv(sc, BUF_SIZE)
#                 unpacked_data = unpack( FLAG, data)[0]
#                 ttl = 0
#                 # Add first four bits and last four bits of every bite
#                 num = unpacked_data & 0xf
#                 print(i, hex(num))
#                 ttl += num
#                 unpacked_data = unpacked_data >> 4 #bitshift 4
#             reply = str(ttl).encode()
#             sc.sendall......

#                 # decoded_data = data.decode()
#                 # sc.sendall(data)