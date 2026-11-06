# ========== UDP  CLIENT ==========

from socket import socket, AF_INET, SOCK_DGRAM
from sys import argv
from cryptography.fernet import Fernet

BUF_SIZE = 1024
HOST = '127.0.0.1'
PORT = 65432

f = Fernet(b'X8qnkzU_BuaiIiwF5OMva1jQzw5_ACEK9hwZfDm6yRU=')

if len(argv) != 2:
    print(argv[0] + ' message')
    exit()

with socket(AF_INET, SOCK_DGRAM) as sock:
    data = argv[1].encode('utf-8')
    encrypted = f.encrypt(data)

    sock.sendto(encrypted, (HOST, PORT))