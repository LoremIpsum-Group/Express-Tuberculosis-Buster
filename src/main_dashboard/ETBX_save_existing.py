from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout 
from kivy.uix.label import Label
from kivy.uix.button import Button 
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from main_dashboard.ETBX_scan_results import scan_result

import sqlite3 
import datetime 

from components.core_functions import (
    io,
    np,
    Image
)

Builder.load_file("main_dashboard/save_existing.kv")
class SaveExisting(Screen): 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.patient_info_layout = None
        self.no_patient_layout = None
        self.save_record_btn = Button(
            text="Save Record", 
            background_normal='',
            background_color=(0, 0, 1, 1),
            on_press=self.save_record,
            size_hint_x=0.06,
            size_hint_y=0.06,
            pos_hint={'center_x': 0.5, 'center_y': 0.25}
        )
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
    
    def search_record(self):
        patient_id = self.ids.patient_id.text.strip()
        
        if not patient_id or not patient_id.isdigit():
            self.ids.patient_id.error = True
        else:
            self.ids.patient_id.error = False

            conn = sqlite3.connect('src/components/view_record_main.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM PATIENT WHERE patient_ID = ?", (int(patient_id),))
            result = cur.fetchone()
            conn.close()

            if result: 
                self.display_patient(result)
            else:
                self.no_patient()
    
    def display_patient(self, patient):
        if self.patient_info_layout:
            self.remove_widget(self.patient_info_layout)
            self.remove_widget(self.save_record_btn)
        elif self.no_patient_layout:
            self.remove_widget(self.no_patient_layout)
            self.remove_widget(self.save_record_btn)

        patient_id = patient[0]
        patient_name = patient[1] + " " + patient[2]
        patient_sex = patient[3]
        patient_age = patient[4]
        patient_birthdate = patient[5]
        patient_info_layout = Builder.load_file('src/main_dashboard/patient_info_layout.kv')
        self.add_widget(patient_info_layout)

        if self.save_record_btn.parent:
            self.save_record_btn.parent.remove_widget(self.save_record_btn)

        self.add_widget(self.save_record_btn)
        patient_info_layout.ids.header.text = f'Patient ID - {patient_id}'
        patient_info_layout.ids.patient_name.text += patient_name
        patient_info_layout.ids.patient_sex.text += patient_sex
        patient_info_layout.ids.patient_age.text += f'{patient_age}'
        patient_info_layout.ids.patient_birthdate.text += patient_birthdate
    
    # display no patient layout when patient ID does not exist
    def no_patient(self):
        if self.save_record_btn.parent:
            self.save_record_btn.parent.remove_widget(self.save_record_btn)

        if self.patient_info_layout:
            self.remove_widget(self.patient_info_layout)
           
        elif self.no_patient_layout:
            self.remove_widget(self.no_patient_layout)
         

        no_patient_layout = Builder.load_file('src/main_dashboard/no_patient.kv')
        self.add_widget(no_patient_layout)

    
    def save_record(self, instance):
        patient_id = self.ids.patient_id.text
        scan_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
        # convert images to BLOB for storage
        with open(scan_result.orig_img, 'rb') as file:
            xray_orig = file.read()

        preproc_img = Image.fromarray(((1.0 - scan_result.preproc_img) * 255).astype(np.uint8))
        preproc_img.convert('L')

        preproc_img_io = io.BytesIO()
        preproc_img.save(preproc_img_io, format='PNG')
        preproc_img_bytes = preproc_img_io.getvalue()  

        gradcam_img = Image.fromarray((scan_result.gradcam_img).astype(np.uint8))
        gradcam_img.convert("RGB")

        gradcam_img_io = io.BytesIO()
        gradcam_img.save(gradcam_img_io, format='PNG')
        gradcam_img_bytes = gradcam_img_io.getvalue()  
    
        conn = sqlite3.connect("src/components/view_record_main.db")
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO RESULTS (patient_ID, date_of_scan, result, percentage, orig_image, preproc_image, grad_cam_image, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (patient_id, scan_date, scan_result.results, scan_result.percentage, 
             xray_orig, preproc_img_bytes, gradcam_img_bytes, scan_result.notes)
        )

        conn.commit()
        conn.close()
        self.show_popup()
        self.ids.patient_id.text = ''

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

    def clear_layout(self):
        
        if self.save_record_btn.parent:
            self.save_record_btn.parent.remove_widget(self.save_record_btn)

        if self.patient_info_layout:
            self.remove_widget(self.patient_info_layout)
           
        elif self.no_patient_layout:
            self.remove_widget(self.no_patient_layout)
        
        self.patient_info_layout = None
        self.no_patient_layout = None

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size