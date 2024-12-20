from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout 
from kivy.uix.label import Label
from kivy.uix.button import Button 
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from src.main_dashboard.maindash_py_files.ETBX_scan_results import scan_result

from src.components.core_functions import (
    resource_path,
    io,
    np,
    Image,
    sqlite3,
    datetime,
    os
)

Builder.load_file(resource_path("src\\main_dashboard\\maindash_kivy_files\\save_existing.kv"))
class SaveExisting(Screen): 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.patient_info_layout = None
        self.no_patient_layout = None
    
        conn = sqlite3.connect(resource_path('src\\components\\view_record_main.db'))
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

            conn = sqlite3.connect(resource_path('src\\components\\view_record_main.db'))
            cur = conn.cursor()
            cur.execute("SELECT * FROM PATIENT WHERE patient_ID = ?", (int(patient_id),))
            result = cur.fetchone()
            conn.close()

            if result: 
                self.display_patient(result)
            else:
                self.no_patient()
    
    def display_patient(self, patient):
        self.ids.patient_search_result.clear_widgets()
        self.ids.save_button.disabled = False
        patient_id = patient[0]
        patient_name = patient[1] + " " + patient[2]
        patient_sex = patient[3]
        patient_age = patient[4]
        patient_birthdate = patient[5]

        patient_info_content1 = BoxLayout(orientation='horizontal')
        name_label = Label(text=f'Name:\n{patient_name}', color=(0,0,0,1))
        age_label = Label(text=f'Age:\n{patient_age}', color=(0,0,0,1))
        patient_info_content1.add_widget(name_label)
        patient_info_content1.add_widget(age_label)

        patient_info_content2 = BoxLayout(orientation='horizontal')
        sex_label = Label(text=f'Sex:\n{patient_sex}', color=(0,0,0,1))
        birthdate_label = Label(text=f'Birthdate:\n{patient_birthdate}', color=(0,0,0,1))
        patient_info_content2.add_widget(sex_label)
        patient_info_content2.add_widget(birthdate_label)

        self.ids.patient_search_result.add_widget(patient_info_content1)
        self.ids.patient_search_result.add_widget(patient_info_content2)
  

    
    # display no patient layout when patient ID does not exist
    def no_patient(self):
        self.ids.save_button.disabled = True
        self.ids.patient_search_result.clear_widgets()
        self.ids.patient_search_result.add_widget(Label(
            text=f"No Patient ID - {self.ids.patient_id.text.strip()} Found! Please check the Patient ID and try again.",
            color=(1,0,0,1)
        ))

    
    def save_record(self, instance):
        self.close(instance)
        patient_id = self.ids.patient_id.text
        scan_date = datetime.datetime.now().strftime("%Y-%m-%d")
        is_misclassified = self.manager.get_screen('scan_result').ids.misclassified

        # convert images to BLOB for storage
        with open(scan_result.orig_img, 'rb') as file:
            xray_orig = file.read()

        preproc_img = Image.fromarray(((1.0 - scan_result.preproc_img) * 255).astype(np.uint8))
        preproc_img.convert('L')

        preproc_img_io = io.BytesIO()
        preproc_img.save(preproc_img_io, format='PNG')
        preproc_img_bytes = preproc_img_io.getvalue()  

        # gradcam_img = Image.fromarray((scan_result.gradcam_img).astype(np.uint8))
        # gradcam_img.convert("RGB")
        gradcam_img = scan_result.gradcam_img

        gradcam_img_io = io.BytesIO()
        gradcam_img.save(gradcam_img_io, format='PNG')
        gradcam_img_bytes = gradcam_img_io.getvalue()  
    
        conn = sqlite3.connect(resource_path("src\\components\\view_record_main.db"))
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO RESULTS (patient_ID, date_of_scan, result, percentage, 
                orig_image, preproc_image, grad_cam_image, notes, misclassified)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (patient_id, scan_date, scan_result.results, scan_result.percentage, 
             xray_orig, preproc_img_bytes, gradcam_img_bytes, 
             self.manager.get_screen('scan_result').ids.notes.text,
             self.manager.get_screen('scan_result').ids.misclassified.active)
        )

        conn.commit()
        conn.close()
        self.show_popup()
        self.ids.patient_id.text = ''
        self.manager.get_screen('scan_result').ids.notes.text = ''
        self.manager.get_screen('scan_result').ids.misclassified.active = False

    def show_popup(self):
        content = BoxLayout(orientation='vertical', padding=10)
        with content.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=content.size, pos=content.pos)
         
        content.bind(size=self._update_rect, pos=self._update_rect)
        content.add_widget(Label(text="[b]Record saved successfully![/b]", color=(0, 0, 1, 1), markup=True))
        content.add_widget(Button(text="Close", 
            background_color=(0, 0, 1, 1), background_normal='',
            size_hint_y=0.2, pos_hint={'center_x': 0.50, 'center_y': 0.10}, on_press=self.close_popup))
        self.popup = Popup(title='Success', content=content, size_hint=(0.4, 0.4), auto_dismiss=False)
        if os.path.isfile(resource_path("dicom_image.png")):
            # Remove the file
            os.remove(resource_path("dicom_image.png"))
        self.popup.open()
    

    def confirm_save_popup(self):

        content = BoxLayout(orientation='vertical')
        with content.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=content.size, pos=content.pos)
        content.bind(size=self._update_rect, pos=self._update_rect)
        content.add_widget(Label(
            text="[b]Saving scan result to patient record\nDo you want to proceed?[/b]", 
            color=(0, 0, 1, 1), markup=True))
        
        inner_content = BoxLayout(orientation='horizontal',
            spacing=10, padding=10, size_hint_y=0.3)

        confirm_btn = Button(text='Confirm',
            background_color=(0, 0, 1, 1), background_normal='',
            on_press=self.save_record)
        
        cancel_btn = Button(text='Cancel',
            background_color=(0, 0, 1, 1), background_normal='',
            on_press= self.close)
        
        inner_content.add_widget(confirm_btn)
        inner_content.add_widget(cancel_btn)
        content.add_widget(inner_content)

        
        #content.add_widget(Button(text="Close", on_press=self.close_popup))
        
        self.popup = Popup(title='Confirm Action', content=content, size_hint=(0.4, 0.4),
            separator_color=(0,0,0,0), background_color=(0, 0, 1, 0.5),auto_dismiss=False)
        self.popup.open()


    def close(self, instance):
        self.popup.dismiss()

    def close_popup(self, instance):
        self.popup.dismiss()
        self.ids.patient_search_result.clear_widgets()
        self.ids.save_button.disabled = True
        self.ids.patient_search_result.add_widget(
            Label(text="[b]Search Patient ID to save[/b]", 
                  pos_hint={'center_x': 0.5, 'center_y': 0.5},
                  color=(0, 0, 0, 1), markup=True)
        )
        self.manager.current = 'scan_img'


    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
