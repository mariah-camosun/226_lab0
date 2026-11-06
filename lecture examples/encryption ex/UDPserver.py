# ========== UDP  SERVER ==========

from socket import socket, AF_INET, SOCK_DGRAM
from cryptography.fernet import Fernet

BUF_SIZE = 1024
HOST = ''
PORT = 65432

f = Fernet(b'X8qnkzU_BuaiIiwF5OMva1jQzw5_ACEK9hwZfDm6yRU=')

with socket(AF_INET, SOCK_DGRAM) as sock:
    sock.bind((HOST, PORT))
    data, address = sock.recvfrom(BUF_SIZE)

    decrypted = f.decrypt(data)
    text = data.decode('utf-8')
    
    source_ip, source_port = address
    print(f'IP: {source_ip} Port: {source_port} Message: {decrypted}')