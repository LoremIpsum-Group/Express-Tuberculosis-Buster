import sqlite3

conn = sqlite3.connect('src/components/view_record_main.db')
cur = conn.cursor()

cur.execute(
    # FOR CREATING PATIENT TABLE
    # """
    # CREATE TABLE IF NOT EXISTS PATIENT (
    #         patient_ID INTEGER PRIMARY KEY,
    #         first_name TEXT,
    #         last_name TEXT,
    #         sex TEXT NOT NULL,
    #         age INTEGER,
    #         date_of_birth TEXT,
    #         address TEXT,
    #    
    #         UNIQUE(patient_ID)
    # )
    # """


    # FOR CREATING THE RESULTS TABLE
    # """ 
    #     CREATE TABLE IF NOT EXISTS RESULTS (
    #         result_id INTEGER PRIMARY KEY, 
    #         patient_id INTEGER, 
    #         date_of_scan TEXT NOT NULL, 
    #         result TEXT NOT NULL,
    #         percentage REAL, 
    #         orig_image BLOB NOT NULL, 
    #         preproc_image BLOB NOT NULL, 
    #         grad_cam_image BLOB NOT NULL, 
    #         notes TEXT, 
    #         FOREIGN KEY(patient_id) REFERENCES PATIENT(patient_id)
    #     )
    # """

    # FOR DELETING TABLES
    # """
    #     DROP TABLE PATIENT;
    # """

    #! FOR TESTING PURPOSES
    # """
    #     CREATE TABLE IF NOT EXISTS TEST2 (
        
    #             image_id INTEGER PRIMARY KEY, 
    #             img BLOB
    #     )
    # """

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

# cur.execute("SELECT img FROM TEST2 WHERE image_id = 1")
# data = cur.fetchone()[0]

# with open('retrieved_image.jpg', 'wb') as file:
#     file.write(data)

# conn.commit()
# conn.close()