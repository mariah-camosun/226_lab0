#!/usr/bin/python3.11

from cryptography.fernet import Fernet
key = Fernet.generate_key()
print(key)

f = Fernet(key)


encrypted = f.encrypt(b"Hello World")
print(encrypted)


decrypted = f.decrypt(encrypted)
print(decrypted)