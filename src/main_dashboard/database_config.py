import sqlite3

conn = sqlite3.connect('src/components/test.db')
cur = conn.cursor()

cur.execute(
    # """
    # CREATE TABLE IF NOT EXISTS PATIENT (
    #         patient_ID INTEGER PRIMARY KEY,
    #         first_name TEXT,
    #         last_name TEXT,
    #         sex TEXT NOT NULL,
    #         age INTEGER,
    #         date_of_birth TEXT,
    #         address TEXT,
    #         image BLOB
    #         UNIQUE(patient_ID)
    # )
    # """

    """
        CREATE TABLE IF NOT EXISTS TEST2 (
        
                image_id INTEGER PRIMARY KEY, 
                img BLOB
        )
    """
)


# with open('src\main_dashboard\student_img.jpg', 'rb') as file:
#     image_data = file.read()
#     cur.execute(
#         """
#         INSERT INTO TEST2 (image_id, img) 
#         VALUES (?, ?);  
#         """,
#         (1, image_data)
#     )

cur.execute("SELECT img FROM TEST2 WHERE image_id = 1")
data = cur.fetchone()[0]

with open('retrieved_image.jpg', 'wb') as file:
    file.write(data)

conn.commit()
conn.close()