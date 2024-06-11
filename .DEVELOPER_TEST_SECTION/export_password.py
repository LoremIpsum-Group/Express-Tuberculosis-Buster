# import hashlib
# import os
# #from src.onboarding_portal.ETBX_login_final import hash_string


# def hash_string_with_salt(string, salt):
#     hashed_string = hashlib.sha256(string.encode() + salt).hexdigest()
#     return hashed_string

# # Generate a random salt
# salt = os.urandom(16)

# # Hash the word "apple" with the generated salt
# hashed_word = hash_string_with_salt('password', salt)

# with open('hashed_word.txt', "w") as file:
#     file.write(hashed_word + ':' + salt.hex())

def caesar_encrypt(string, shift):
    encrypted_string = ''.join(chr((ord(char) - 97 + shift) % 26 + 97) for char in string)
    return encrypted_string

shift = 3

encrypted_word = caesar_encrypt('password', shift)

with open('encrypted_word.txt', "w") as file:
    file.write(encrypted_word)

