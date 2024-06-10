import os, sqlite3
from cryptography.fernet import Fernet

if not os.path.exists("secret.key"):
            key = Fernet.generate_key()
            with open("secret.key", "wb") as key_file:
                key_file.write(key)
else:
    with open("secret.key", "rb") as key_file:
        key = key_file.read()

conn = sqlite3.connect('.DEVELOPER_TEST_SECTION\hash.db')
cur = conn.cursor()

cur.execute(
        """
        CREATE TABLE IF NOT EXISTS PATIENT (
        patient_ID INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT)""")
conn.commit()
conn.close()

patient_id = int(input("enter patient ID:"))
first_name = input("enter first name:")
last_name = input("enter last name:")

cipher_suite = Fernet(key) 
encrypted_first_name = cipher_suite.encrypt(first_name.encode())
encrypted_last_name = cipher_suite.encrypt(last_name.encode())


conn = sqlite3.connect('.DEVELOPER_TEST_SECTION\hash.db')
cur = conn.cursor()
cur.execute("INSERT INTO PATIENT (patient_ID, first_name, last_name) VALUES (?, ?, ?)", (patient_id, encrypted_first_name, encrypted_last_name))
conn.commit()
conn.close()
