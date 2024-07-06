import os, sqlite3
from cryptography.fernet import Fernet
import sqlite3

patient_id = int(input("enter patient ID:"))

with open("secret.key", "rb") as key_file:
    key = key_file.read()
    cipher_suite = Fernet(key)

    conn = sqlite3.connect('.DEVELOPER_TEST_SECTION\hash.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM PATIENT WHERE patient_ID = ?", (patient_id,))
    results = cur.fetchall()
    for row in results:
        print("Patient ID: ", row[0])
        print("First Name: ", cipher_suite.decrypt(row[1]).decode())
        print("Last Name: ", cipher_suite.decrypt(row[2]).decode())
        print("Patient ID: ", row[0])
        print("First Name: ", row[1])
        print("Last Name: ", row[2])



     #c.execute("SELECT * FROM RESULTS WHERE patient_ID = ?", (search_input,))