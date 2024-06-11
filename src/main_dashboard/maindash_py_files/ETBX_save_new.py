from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label 
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from src.main_dashboard.maindash_py_files.ETBX_scan_results import scan_result

from cryptography.fernet import Fernet #new 

from src.components.core_functions import (
    resource_path,
    io,
    np,
    Image,
    sqlite3,
    datetime,
    os #new 
)



Builder.load_file(resource_path("src\\main_dashboard\\maindash_kivy_files\\save_new.kv"))
class SaveNew(Screen): 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Generate a key and save it to a file
        # if not os.path.exists("supersecret.key"):
        #     key = Fernet.generate_key()
        #     with open("supersecret.key", "wb") as key_file:
        #         key_file.write(key)
        # else:
        #     with open("supersecret.key", "rb") as key_file:
        #         key = key_file.read()


        # if not os.path.exists("supersecret.key"):
        #     key = Fernet.generate_key() 
        #     with open("supersecret.key", "wb") as key_file:
        #         key_file.write(key)
        # else:
        #     with open("supersecret.key", "rb") as key_file:
        #         key = key_file.read()

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

    def save_record(self, instance):
        self.close(instance)
        if not self.entries_valid():
            return 
        
        # #testing the encryption
        # if not os.path.exists("supersecret.key"):
        #     key = Fernet.generate_key() 
        #     with open("supersecret.key", "wb") as key_file:
        #         key_file.write(key)
        # else:
        #     with open("supersecret.key", "rb") as key_file:
        #         key = key_file.read()

        patient_id = self.ids.patient_id.text 
        first_name = self.ids.first_name.text
        last_name = self.ids.last_name.text
        birthdate = self.ids.birthdate.text
        current_date = datetime.datetime.now()
        age = (current_date - datetime.datetime.strptime(birthdate, "%Y/%m/%d")).days // 365
        address = self.ids.address.text
        scan_date = current_date.strftime("%Y-%m-%d")

        if (self.ids.male.active):
            sex = 'Male'
        elif (self.ids.female.active):
            sex = 'Female'

        # patient_id = self.ids.patient_id.text 
        # first_name = self.ids.first_name.text.encode() #testing the encryption
        # last_name = self.ids.last_name.text.encode() #.encode()#testing the encryption
        # birthdate = self.ids.birthdate.text.encode() ##testing the encryption
        # birthdate_str = birthdate.decode() # Decode birthdate back to a string
        # current_date = datetime.datetime.now()
        # age = str((current_date - datetime.datetime.strptime(birthdate_str, "%Y/%m/%d")).days // 365).encode()
        # address = self.ids.address.text.encode()#testing the encryption
        # scan_date = current_date.strftime("%Y-%m-%d").encode()

        # if (self.ids.male.active):
        #     sex = 'Male'.encode() #testing the encryption
        # elif (self.ids.female.active):
        #     sex = 'Female'.encode() #testing the encryption

        #end of test
        with open(scan_result.orig_img, 'rb') as file:
            xray_orig = file.read()

        preproc_img = Image.fromarray(((1.0 - scan_result.preproc_img) * 255).astype(np.uint8))
        preproc_img.convert('L')

        preproc_img_io = io.BytesIO()
        preproc_img.save(preproc_img_io, format='PNG')
        preproc_img_bytes = preproc_img_io.getvalue()  

        # gradcam_img = Image.fromarray((scan_result.gradcam_img).astype(np.uint8))
        gradcam_img =  scan_result.gradcam_img
        gradcam_img.convert("RGB")

        gradcam_img_io = io.BytesIO()
        gradcam_img.save(gradcam_img_io, format='PNG')
        gradcam_img_bytes = gradcam_img_io.getvalue()  

        conn = sqlite3.connect(resource_path("src\\components\\view_record_main.db"))
        cur = conn.cursor()

        cur.execute("SELECT patient_id FROM PATIENT where patient_id = ?", (patient_id,))

        if cur.fetchone():
            self.ids.patient_id.text = "Patient ID already exists!"
            self.ids.patient_id.error = True
            return 
        
        # cipher_suite = Fernet(key)

        # #Encrypt the personal information
        # encrypted_first_name = cipher_suite.encrypt(first_name)
        # encrypted_last_name = cipher_suite.encrypt(last_name)
        # encrypted_birthdate = cipher_suite.encrypt(birthdate)
        # encrypted_sex = cipher_suite.encrypt(sex)
        # encrypted_address = cipher_suite.encrypt(address)
        # encrypted_age = cipher_suite.encrypt(age)



        cur.execute(
            f"""
            INSERT INTO PATIENT (patient_ID, first_name, last_name, sex, age, date_of_birth, address)
            VALUES ({patient_id}, '{first_name}', '{last_name}', '{sex}', {age}, '{birthdate}', '{address}');
            """
        )

        cur.execute(
            """
            INSERT INTO RESULTS (patient_ID, date_of_scan, result, 
                percentage, orig_image, preproc_image, grad_cam_image, notes, misclassified)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (patient_id, scan_date, scan_result.results, scan_result.percentage, 
             xray_orig, preproc_img_bytes, gradcam_img_bytes, 
             self.manager.get_screen('scan_result').ids.notes.text,
             self.manager.get_screen('scan_result').ids.misclassified.active)
        )

        # cur.execute(
        #     """
        #     INSERT INTO PATIENT (patient_ID, first_name, last_name, sex, age, date_of_birth, address)
        #     VALUES (?, ?, ?, ?, ?, ?, ?);
        #     """,
        # (patient_id, encrypted_first_name, encrypted_last_name, encrypted_sex, encrypted_age, encrypted_birthdate, encrypted_address)
        # )


        # encrypted_result = cipher_suite.encrypt(scan_result.results.encode())
        # encrypted_percentage = cipher_suite.encrypt(str(scan_result.percentage).encode())
        # encrypted_orig_image = cipher_suite.encrypt(xray_orig)
        # encrypted_preproc_image = cipher_suite.encrypt(preproc_img_bytes)
        # encrypted_gradcam_image = cipher_suite.encrypt(gradcam_img_bytes)
        # encrypted_notes = cipher_suite.encrypt(self.manager.get_screen('scan_result').ids.notes.text.encode())
        # encrypted_misclassified = cipher_suite.encrypt(str(self.manager.get_screen('scan_result').ids.misclassified.active).encode())

        # cur.execute(
        #     """
        #     INSERT INTO RESULTS (patient_ID, date_of_scan, result, 
        #         percentage, orig_image, preproc_image, grad_cam_image, notes, misclassified)
        #     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        #     """,
        #     (patient_id, scan_date, encrypted_result, encrypted_percentage, 
        #     encrypted_orig_image, encrypted_preproc_image, encrypted_gradcam_image, 
        #     encrypted_notes, encrypted_misclassified)
        # )

        #end of test

        if cur.lastrowid is not None:
            self.clear_fields() 
            self.manager.get_screen('save_existing').ids.patient_search_result.clear_widgets()
            self.manager.get_screen('save_existing').ids.patient_search_result.add_widget(
                Label(text="[b]Search Patient ID to save[/b]", 
                      pos_hint={'center_x': 0.5, 'center_y': 0.5},
                      color=(0, 0, 0, 1), markup=True)
            )
            conn.commit()
            conn.close()
            self.show_popup()

    def clear_fields(self):
        self.ids.patient_id.text = ''
        self.ids.first_name.text = ''
        self.ids.last_name.text = ''
        self.ids.birthdate.text = ''
        self.ids.address.text = ''
        self.ids.male.active = False
        self.ids.female.active = False
        self.manager.get_screen('scan_result').ids.notes.text = ''
        self.manager.get_screen('scan_result').ids.misclassified.active = False

    # display a popup after successfully saving the record
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
        self.popup.open()

    def close_popup(self, instance):
        self.popup.dismiss()
        self.manager.current = 'scan_img'

    def close(self, instance):
        self.popup.dismiss()

    def confirm_save_popup(self):
        if not self.entries_valid():
            return 

        content = BoxLayout(orientation='vertical')
        with content.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=content.size, pos=content.pos)
        content.bind(size=self._update_rect, pos=self._update_rect)
        content.add_widget(Label(
            text="[b]Saving scan result to patient\nDo you want to proceed?[/b]", 
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

        # content.add_widget(Button(text="Close", on_press=self.close_popup))

        self.popup = Popup(title='Confirm Action', content=content, size_hint=(0.4, 0.4),
            separator_color=(0,0,0,0), background_color=(0, 0, 1, 0.5),auto_dismiss=False)
        self.popup.open()

    def entries_valid(self):
        valid = True 
        try:
            birthdate = datetime.datetime.strptime(self.ids.birthdate.text, "%Y/%m/%d")

            if not self.is_valid_age(birthdate):
                self.ids.birthdate.text = 'Must be 15 and above'
                self.ids.birthdate.error = True
                valid = False

            if not self.is_valid_year(birthdate):
                self.ids.birthdate.text = "Year must not be lesser than 1900"
                self.ids.birthdate.error = True
                valid = False
                
            if not self.ids.patient_id.text.isdigit():
                self.ids.patient_id.text = "Invalid patient ID"
                self.ids.patient_id.error = True
                valid = False 

            if not self.ids.first_name.text:
                self.ids.first_name.text = "Required"
                self.ids.first_name.error = True
                valid = False

            if not self.ids.last_name.text:
                self.ids.last_name.text = "Required"
                self.ids.last_name.error = True
                valid = False

            # checks if sex is not selected
            if not any([self.ids.male.active, self.ids.female.active]):
                valid = False 

            return valid

        except ValueError:
            self.ids.birthdate.text = "Invalid date format"
            self.ids.birthdate.error = True
            return False

    def is_valid_age(self, birthdate): 
        """
            Checks if birthdate is 15 years or older 
        """
        return ((datetime.datetime.now() - birthdate).days // 365) >= 15
    
    def is_valid_year(self, birthdate):
        """
        Checks if year is not lesser than 1900
        """
        return birthdate.year >= 1900
    

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_focus_notes(self,instance, value):
        if value:
            pass
        else:
            instance.text = instance.text 
