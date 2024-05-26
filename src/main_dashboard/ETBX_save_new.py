from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.app import App
from kivy.metrics import dp 
from kivy.uix.popup import Popup
from kivy.uix.label import Label 
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.pickers import MDDatePicker
from kivy.graphics import Color, Rectangle
from main_dashboard.ETBX_scan_results import scan_result

import sqlite3
import datetime

from components.core_functions import (
    io,
    np,
    Image
)


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

        preproc_img = Image.fromarray(((1.0 - scan_result.preproc_img) * 255).astype(np.uint8))
        preproc_img.convert('L')

        preproc_img_io = io.BytesIO()
        preproc_img.save(preproc_img_io, format='PNG')
        preproc_img_bytes = preproc_img_io.getvalue()  # This is your image in PNG format, stored in memory

        gradcam_img = Image.fromarray((scan_result.gradcam_img).astype(np.uint8))
        gradcam_img.convert("RGB")

        gradcam_img_io = io.BytesIO()
        gradcam_img.save(gradcam_img_io, format='PNG')
        gradcam_img_bytes = gradcam_img_io.getvalue()  # This is your image in PNG format, stored in memory

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
             xray_orig, preproc_img_bytes, gradcam_img_bytes, scan_result.notes)
        )
        
        if cur.lastrowid is not None:
            self.clear_fields() 

            conn.commit()
            conn.close()
            self.show_popup()
 
    def clear_fields(self):
        self.ids.patient_id.text = ''
        self.ids.first_name.text = ''
        self.ids.last_name.text = ''
        self.ids.age.text = ''
        self.ids.birthdate.text = ''
        self.ids.address.text = ''
        self.manager.get_screen('scan_result').ids.notes.text = ''

        
    def show_popup(self):
        content = BoxLayout(orientation='vertical')
        with content.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=content.size, pos=content.pos)
         
        content.bind(size=self._update_rect, pos=self._update_rect)
        content.add_widget(Label(text="[b]Record saved successfully![/b]", color=(0, 0, 1, 1), markup=True))
        content.add_widget(Button(text="Close", 
            background_color=(0, 0, 1, 1), background_normal='',
            on_press=self.close_popup))
        self.popup = Popup(title='Success', content=content, size_hint=(0.4, 0.4), auto_dismiss=False)
        self.popup.open()
    
    def close_popup(self, instance):
        self.popup.dismiss()
        self.manager.current = 'scan_img'
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

