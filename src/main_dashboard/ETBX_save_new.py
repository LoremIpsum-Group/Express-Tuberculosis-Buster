from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.app import App
from kivy.metrics import dp 


from kivymd.uix.pickers import MDDatePicker
from main_dashboard.ETBX_scan_results import scan_result

import sqlite3
import datetime

Builder.load_file("main_dashboard/save_new.kv")
class SaveNew(Screen): 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        conn = sqlite3.connect('src/components/view_record_main.db')
        cur = conn.cursor()

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS PATIENT (
                    patient_ID INTEGER PRIMARY KEY,
                    first_name TEXT,
                    last_name TEXT,
                    sex TEXT NOT NULL,
                    age INTEGER,
                    date_of_birth TEXT,
                    address TEXT,
                    UNIQUE(patient_ID)
            )
            
            """
        )

        conn.commit()
        conn.close()
    

    def show_date_picker(self, focus):
        if not focus:
            return
        
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_date_picker_save, on_cancel=self.on_date_picker_cancel)
        date_dialog.pos = [
            self.ids.birthdate.center_x - date_dialog.width / 2,
            self.ids.birthdate.center_y - (date_dialog.height + dp(32))
        ]
        
        date_dialog.open()
       
    
    def on_date_picker_save(self, instance, value, date_range):
        self.ids.birthdate.text = value.strftime("%Y-%m-%d")
    
    def on_date_picker_cancel(self, instance, value):
        self.ids.field.focus = False

    def save_record(self):
        patient_id = self.ids.patient_id.text 
        first_name = self.ids.first_name.text
        last_name = self.ids.last_name.text
        age = int(self.ids.age.text)
        birthdate = self.ids.birthdate.text
        address = self.ids.address.text
        scan_date = datetime.datetime.now().strftime("%Y-%m-%d")

        if (self.ids.male.active):
            sex = 'Male'
        elif (self.ids.female.active):
            sex = 'Female'
        
        with open(scan_result.orig_img, 'rb') as file:
            xray_orig = file.read()

        conn = sqlite3.connect("src/components/view_record_main.db")
        cur = conn.cursor()
        
        cur.execute(
            f"""
            INSERT INTO PATIENT (patient_ID, first_name, last_name, sex, age, date_of_birth, address)
            VALUES ({patient_id}, '{first_name}', '{last_name}', '{sex}', {age}, '{birthdate}', '{address}');
            """
        )

        cur.execute(
            """
            INSERT INTO RESULTS (patient_ID, date_of_scan, result, percentage, orig_image, preproc_image, grad_cam_image, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (patient_id, scan_date, scan_result.results, scan_result.percentage, 
             xray_orig, scan_result.preproc_img, scan_result.gradcam_img, 
             scan_result.notes)
        )

        conn.commit()
        conn.close()

