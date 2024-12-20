from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup

from kivymd.uix.button import MDRectangleFlatButton

from kivy.graphics import Color, Rectangle

from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout

from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.properties import ListProperty, StringProperty
from kivy.uix.recyclegridlayout import RecycleGridLayout

from fpdf import FPDF 

import io, os, pyzipper
from PIL import Image

from cryptography.fernet import Fernet, InvalidToken #for encryption

from getpass import getpass

import sqlite3

# from src.components.core_functions import (
#     resource_path,
#     FPDF,
#     io,
#     Image,
#     sqlite3
# )


Builder.load_file("etbx_view_rcrds.kv")
class ViewRecords(Screen):

    data_items = ListProperty([]) 
    current_patient_id = StringProperty("")  # To store the current patient ID

    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # conn = sqlite3.connect(resource_path('src\\components\\view_record_main.db'))
        # c = conn.cursor()
        # c.execute(
        #     """ 
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
        #         misclassified BOOLEAN,
        #         FOREIGN KEY(patient_id) REFERENCES PATIENT(patient_id)
        #     )
        # """
        # )

        # conn.commit()
        # conn.close()
    
    def search_button(self):
        """
        Perform a search based on the input ID number and display the corresponding records.

        This method clears the data_items list, connects to the 'view_record_main.db' database,
        retrieves the search input from the search_input text input field, and performs the following checks:
        
        - If the search input is empty, it clears the search_result_layout and displays an error message.
        - If the search input is not a valid ID number, it clears the search_result_layout and displays an error message.
        - If the search input is valid, it displays the search result and retrieves the records from the database
          for the specified patient ID. If records are found, it appends them to the data_items list and sets
          the current_patient_id to the search input. If no records are found, it clears the search_result_layout
          and displays an error message.

        After performing the search, the method closes the database connection.

        Parameters:
        - self: The instance of the class.

        Returns:
        - None
        """
        self.data_items.clear()
        conn = sqlite3.connect(resource_path('src\\\components\\view_record_main.db'))
        c = conn.cursor()
        search_input = self.ids.search_input.text
        

        #testing the encryption
        # with open("secret.key", "rb") as key_file:
        #     key = key_file.read()
        
        # cipher_suite = Fernet(key)

        if not search_input:
            self.ids.search_result_layout.clear_widgets()
            self.error_popup("Please fill-in the ID number of the patient")
            self.ids.search_result.text = ""
            self.ids.result_label.text = ""
            self.ids.date_label.text = ""
        elif not search_input.isdigit():
            self.ids.search_result_layout.clear_widgets()
            self.error_popup("Please enter a valid ID number")
            self.ids.search_result.text = ""
        else:
            self.ids.search_result.text = f"Records of Patient ID: {search_input}"
            c.execute("SELECT * FROM RESULTS WHERE patient_ID = ?", (search_input,))
            results = c.fetchall()
            self.ids.result_label.text = "Result"
            self.ids.date_label.text = "Date of Scan"
            #start of test here
            if results:
                for result in results:
                    self.data_items.append(result)
                self.current_patient_id = search_input
            else:
                self.ids.search_result_layout.clear_widgets()
                self.error_popup("No ID found")
                self.ids.search_result.text = ""
                self.ids.result_label.text = ""
                self.ids.date_label.text = ""

            # if results:
            #     for result in results:
            #         #self.data_items.append(result)
            #         try:
            #             result_id = result[0]
            #             patient_id = result[1]
            #             decrypted_date_of_scan = cipher_suite.decrypt(result[2]).decode()
            #             decrypted_result = cipher_suite.decrypt(result[3]).decode()
            #             decrypted_percentage = cipher_suite.decrypt(result[4]).decode()
            #             decrypted_orig_image = cipher_suite.decrypt(result[5]).decode()
            #             decrypted_preproc_image = cipher_suite.decrypt(result[6]).decode()
            #             decrypted_grad_cam_image = cipher_suite.decrypt(result[7]).decode()
            #             decrypted_notes = cipher_suite.decrypt(result[8]).decode()
            #             decrypted_misclassified = cipher_suite.decrypt(result[9]).decode()

                        
                        


            #             self.data_items.append(result_id, patient_id, decrypted_date_of_scan, decrypted_result, decrypted_percentage, 
            #                    decrypted_orig_image, 
            #                    decrypted_preproc_image, decrypted_grad_cam_image, decrypted_notes, decrypted_misclassified)
            #         except InvalidToken:
            #             print("Invalid token. Please check the token and try again.")
            #         except Exception as e:
            #             print("An error occurred: ", str(e))
            #     self.current_patient_id = search_input
            # else:
            #     self.ids.search_result_layout.clear_widgets()
            #     self.error_popup("No ID found")
            #     self.ids.search_result.text = ""
            #     self.ids.result_label.text = ""
            #     self.ids.date_label.text = ""
        #end of test
        conn.close()
                
    def record_clicked(self, search_input, index):
        """
        Handle the event when a record is clicked.

        Parameters:
        - search_input (str): The search input to match against the records.

        Returns:
        None
        """

        # for record in self.data_items:
        #     if record[1] == search_input:
        #         full_record = record
        #         res_id = full_record[0]

        #         self.manager.get_screen('patient_result').update_result(int(res_id))
        #         self.manager.current = 'patient_result'
        #         break
        
        records = [record for record in self.data_items if record[1] == search_input]
        if index < len(records):
            full_record = records[index]
            res_id = full_record[0]

            self.manager.get_screen('patient_result').update_result(int(res_id))
            self.manager.current = 'patient_result'

    
    def logout(self, instance):
        self.popup.dismiss()
        self.manager.current = 'login'

    def logout_popup(self):
        """
        Displays a popup with a given message and a close button.

        Parameters:
        - message (str): The message to be displayed in the popup.

        Returns:
        None
        """
        content = BoxLayout(orientation='vertical')
        label = Label(text="Are you sure you want to logout?")
        confirm_button = Button(text="Confirm", on_press=self.logout)
        close_button = Button(text='Close', on_press=self.close_popup)
        content.add_widget(label)
        content.add_widget(confirm_button)
        
        content.add_widget(close_button)
        self.popup = Popup(title='', content=content, auto_dismiss=False, size_hint=(0.4, 0.4))
        self.popup.open()
    
    def error_popup(self, message):
        """
        Displays an error popup with the given message.

        Parameters:
        - message (str): The error message to be displayed.

        Returns:
        - None
        """
        content = BoxLayout(orientation='vertical')
        label = Label(text=message)
        self.popup = Popup(title='', content=content, auto_dismiss=False, size_hint=(0.4, 0.4))
        close_button = Button(text='Close', on_press=lambda instance: self.close_popup(instance))
        content.add_widget(label)
        content.add_widget(close_button)
        self.popup.open()

       
    def result_popup(self, search_input, index):
        """
        Displays a popup window with options for the user to choose from.

        Args:
            search_input (str): The search input provided by the user.

        Returns:
            None
        """
        record = self.data_items[index]

        content = FloatLayout()
        with content.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=content.size, pos=content.pos)
        content.bind(size=self._update_rect, pos=self._update_rect)
        label = Label(text="Please choose: ", color=(0,0,1,1), size_hint=(1, 0.8), pos_hint={'x': 0, 'y': 0.2})
        self.popup = Popup(title='', content=content, auto_dismiss=False, size_hint=(0.4, 0.4))
        close_button = Button(text='X', size_hint=(0.1, 0.1),
             background_color=(1, 0, 0, 1), background_normal='', pos_hint={'right': 1, 'top': 1})
        close_button.bind(on_press=lambda instance: self.close_popup(instance))
        button_grid = GridLayout(cols=2, size_hint=(1, 0.2), pos_hint={'x': 0, 'y': 0}, padding=10, spacing=10)

        button1 = Button(text='Export Result', background_color=(0, 0, 1, 1), background_normal='')
        button1.bind(on_release=lambda instance: self.export_result(search_input, index))
        button1.bind(on_release=lambda instance: self.export_success(search_input))
        button1.bind(on_release=lambda instance: self.close_popup(instance))

        button2 = Button(text='View Result', background_color=(0, 0, 1, 1), background_normal='')
        button2.bind(on_release=lambda instance: self.record_clicked(search_input, index))
        button2.bind(on_release=lambda instance: self.close_popup(instance))

        button_grid.add_widget(button1)
        button_grid.add_widget(button2)
        content.add_widget(label)
        content.add_widget(close_button)
        content.add_widget(button_grid)
        self.popup.open()

   
    def export_success(self, patient_ID):
        """
        Displays a popup message indicating successful export.

        This method creates a popup window with a label displaying the message
        "Exported Successfully!" and a close button. The popup window remains
        open until the close button is pressed.

        Parameters:
        - self: The instance of the class.

        Returns:
        - None
        """
        content = FloatLayout()
        with content.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=content.size, pos=content.pos)
        content.bind(size=self._update_rect, pos=self._update_rect)
        #label = Label(text="Exported Successfully here: \n" + resource_path(f'Exported-Results\\patient_results_{patient_ID}.pdf'), color=(0,0,1,1))
        label = Label(
            text="Exported Successfully here: \n" + resource_path(f'Exported-Results'),
            color=(0,0,1,1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(1, None),  # Allow the label to expand horizontally
            height=50,  # Or whatever height you want the label to have
            text_size=(self.popup.width, None),  # Set the width of the text box to the width of the popup
            halign='center',  # Center the text horizontally
            valign='center'  # Center the text vertically
        )
        self.popup = Popup(title='', content=content, auto_dismiss=False, size_hint=(0.4, 0.4))
        close_button = Button(text='Close', background_color=(1, 0, 0, 1), background_normal='',
            size_hint=(1, 0.2), pos_hint={'center_x': 0.50, 'center_y': 0.10}, on_press=lambda instance: self.close_popup(instance))
        content.add_widget(label)
        content.add_widget(close_button)
        self.popup.open()
        

    def export_result(self, search_input, index):
        """
        Export the result of a patient's record to a PDF file and save associated images.

        Args:
            search_input (str): The patient ID used to search for the record.

        Returns:
            None
        """
        pdf = FPDF('P', 'mm', 'Letter')
        pdf.add_page()
        pdf.set_font('times', 'B', 16)

        conn = sqlite3.connect(resource_path('src\\components\\view_record_main.db'))
        c = conn.cursor()
        c.execute(
            """
            SELECT PATIENT.patient_ID, PATIENT.first_name, PATIENT.last_name, PATIENT.sex, PATIENT.age, PATIENT.address, 
            RESULTS.date_of_scan, RESULTS.result, RESULTS.percentage, RESULTS.notes, RESULTS.orig_image, RESULTS.preproc_image, RESULTS.grad_cam_image, RESULTS.misclassified, RESULTS.result_id
            FROM PATIENT
            JOIN RESULTS ON PATIENT.patient_ID = RESULTS.patient_id
            WHERE PATIENT.patient_ID = ?
            """,
            (int(search_input),)
        )
        records = c.fetchall()
        
        # records = [record for record in self.data_items if record[1] == search_input]
        # if index < len(records):
        #     full_record = records[index]
        #     patient_ID = full_record[0]
        #     first_name = full_record[1]
        #     last_name = full_record[2]
        #     sex = full_record[3]
        #     age = full_record[4]
        #     address = full_record[5]
        #     date_of_scan = full_record[6]
        #     result = full_record[7]
        #     percentage = full_record[8]
        #     notes = full_record[9]
        #     misclassified = full_record [13]

        #default working 
        # if records:  
        #     for record in records:
                # patient_ID = record[0]
                # first_name = record[1]
                # last_name = record[2]
                # sex = record[3]
                # age = record[4]
                # address = record[5]
                # date_of_scan = record[6]
                # result = record[7]
                # percentage = record[8]
                # notes = record[9]
                # misclassified = record [13]
                #result_ID = record[14]

        if records:
            full_record = records[index]
            patient_ID = full_record[0]
            first_name = full_record[1]
            last_name = full_record[2]
            sex = full_record[3]
            age = full_record[4]
            address = full_record[5]
            date_of_scan = full_record[6]
            result = full_record[7]
            percentage = full_record[8]
            notes = full_record[9]
            misclassified = full_record [13]
            result_ID = full_record[14] #Ttry
                
        if misclassified == True: 
            misclassified = "True"
        else:
            misclassified = "False"    

        #os.makedirs(resource_path(f'Exported-Results\\orig_image_{patient_ID}\\result_id{result_ID}'), exist_ok=True)

        
        orig_image_bytes  = full_record[10]
        orig_image_stream = io.BytesIO(orig_image_bytes)
        orig_image = Image.open(orig_image_stream)
        
        #raises an error when an image is 8 bit 


        orig_image.convert('RGB').save(resource_path(f'Exported-Results\\orig_image_{patient_ID}_result_id{result_ID}.png'))

        preproc_image_bytes = full_record[11]
        preproc_image_stream = io.BytesIO(preproc_image_bytes)
        preproc_image = Image.open(preproc_image_stream)
        preproc_image.save(resource_path(f'Exported-Results\\preproc_image_{patient_ID}_result_id{result_ID}.png'))

        gradcam_image_bytes = full_record[12]
        gradcam_image_stream = io.BytesIO(gradcam_image_bytes)
        gradcam_image = Image.open(gradcam_image_stream)
        gradcam_image.save(resource_path(f'Exported-Results\\heatmap_{patient_ID}_result_id{result_ID}.png'))


        '''
        This part generates a PDF report for a patient's record, including information such as patient ID, name, sex, age, address,
        date of scan, result, percentage, notes, and misclassification. It also saves the original image and Grad-CAM image associated
        with the record.
        '''
        pdf.set_font('times', 'B', 20)
        #pdf.cell(0, 10, '[Hospital Name]', ln=True, align='C')
        pdf.cell(0, 10, 'Report of Tuberculosis Screening', ln=True, align='C')
        pdf.ln(20)  

        pdf.set_font('times', '', 16)
        pdf.cell(95, 10, f'Patient ID: {patient_ID}')
        pdf.cell(95, 10, f'Date of Scan: {date_of_scan}', ln=True)
        pdf.cell(95, 10, f'First Name: {first_name}')
        pdf.cell(95, 10, f'Last Name: {last_name}', ln=True)
        pdf.cell(95, 10, f'Sex: {sex}')
        pdf.cell(95, 10, f'Age: {age}', ln=True)
        pdf.cell(0, 10, f'Address: {address}', ln=True)
        pdf.ln(5)  

        pdf.cell(95, 10, f'Result: {result}')
        pdf.cell(95, 10, f'Model Prediction %: {percentage}', ln=True)
        pdf.cell(0, 10, f'Did system Misclassify: {misclassified}', ln=True)
        pdf.ln(5)  

        pdf.cell(0, 10, 'Notes:', ln=True)
        pdf.multi_cell(0, 10, notes)

        pdf.ln(80)
        pdf.set_font('times', '', 16)
        pdf.cell(0, 10, 'Attending Physician:', ln=True)
        pdf.cell(0, 10, 'Name: _________________________', ln=True)
        pdf.cell(0, 10, 'Signature: _____________________', ln=True)

        pdf.add_page()
        pdf.set_font('times', 'B', 20)
        pdf.cell(0, 20, 'Original Image', 0, 1, 'C')
        pdf.image(resource_path(f'Exported-Results\\orig_image_{patient_ID}_result_id{result_ID}.png'), x=0, y=30, w=pdf.w, h=pdf.h-30)

        pdf.add_page()
        pdf.set_font('times', 'B', 20)
        pdf.cell(0, 20, 'Heatmap image', 0, 1, 'C')
        pdf.image(resource_path(f'Exported-Results\\heatmap_{patient_ID}_result_id{result_ID}.png'), x=0, y=30, w=pdf.w, h=pdf.h-30)

        pdf.output(resource_path(f'Exported-Results\\patient_results_{patient_ID}_result_id{result_ID}.pdf'))
       
        # Create an encrypted zip file
        #secret_password = b'password'
        
        #encrypted password
        # with open('hashed_word.txt', 'r') as file:
        #     hashed_password, salt = file.read().split(':')
        #     secret_password = bytes.fromhex(hashed_password)
        #     print("password: " , secret_password)

        with open(resource_path('src\main_dashboard\encrypted_word.txt'),'r') as file:
            encrypted_word = file.read()
            decrypted_word = ''.join(chr((ord(char) - 97 - 3) % 26 + 97) for char in encrypted_word).encode()

        with pyzipper.AESZipFile(resource_path(f'Exported-Results\\patient_results_{patient_ID}_result_id{result_ID}.zip'), 'w', compression=pyzipper.ZIP_LZMA) as zf:

            zf.setpassword(decrypted_word)
            zf.setencryption(pyzipper.WZ_AES, nbits =128)
            zf.write(f'Exported-Results\\patient_results_{patient_ID}_result_id{result_ID}.pdf')

            zf.write(f'Exported-Results\\orig_image_{patient_ID}_result_id{result_ID}.png')
           
            zf.write(f'Exported-Results\\preproc_image_{patient_ID}_result_id{result_ID}.png')
           
            zf.write(f'Exported-Results\\heatmap_{patient_ID}_result_id{result_ID}.png')
        
        # Remove the unencrypted files
        os.remove(resource_path(f'Exported-Results\\patient_results_{patient_ID}_result_id{result_ID}.pdf'))
       
        os.remove(resource_path(f'Exported-Results\\orig_image_{patient_ID}_result_id{result_ID}.png'))
       
        os.remove(resource_path(f'Exported-Results\\preproc_image_{patient_ID}_result_id{result_ID}.png'))

        os.remove(resource_path(f'Exported-Results\\heatmap_{patient_ID}_result_id{result_ID}.png'))




    def close_popup(self, instance):
        """
        Closes the popup window.

        Parameters:
            instance (object): The instance of the button that triggered the event.

        Returns:
            None
        """
        self.popup.dismiss()
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
  
