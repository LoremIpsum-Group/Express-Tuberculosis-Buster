import hashlib
import os

def generate_salt():
    return os.urandom(16)

def hash_string(string, salt):
    hashed_string = hashlib.sha256(string.encode() + salt).hexdigest()
    return hashed_string

salt_username = generate_salt()
hashed_username = hash_string("doctor", salt_username)

salt_password = generate_salt()
hashed_password = hash_string("apple", salt_password)

with open("password.txt", "w") as file:
    file.write(hashed_username + ':' + salt_username.hex() + '\n')
    file.write(hashed_password + ':' + salt_password.hex())
