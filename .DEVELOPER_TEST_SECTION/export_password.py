import hashlib
import os

def hash_string_with_salt(string, salt):
    hashed_string = hashlib.sha256(string.encode() + salt).hexdigest()
    return hashed_string

# Generate a random salt
salt = os.urandom(16)

# Hash the word "apple" with the generated salt
hashed_word = hash_string_with_salt("password", salt)

print("Hashed word (with salt):", hashed_word)
print("Salt:", salt.hex())
