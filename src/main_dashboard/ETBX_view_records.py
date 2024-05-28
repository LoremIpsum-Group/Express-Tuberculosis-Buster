from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup

from kivymd.uix.button import MDRectangleFlatButton

from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout

from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.properties import ListProperty, StringProperty
from kivy.uix.recyclegridlayout import RecycleGridLayout

from fpdf import FPDF 

import io
from PIL import Image

import sqlite3

Builder.load_file("main_dashboard/maindash_kivy_files/etbx_view_rcrds.kv")
class ViewRecords(Screen):

    data_items = ListProperty([]) 
    current_patient_id = StringProperty("")  # To store the current patient ID

    
    def __init__(self, **kwargs):
        """
        Initializes an instance of the ETBX_view_records class.

        Parameters:
        - kwargs: Additional keyword arguments that can be passed to the parent class.

        Attributes:
        - conn: SQLite connection object used to connect to the database.
        - c: SQLite cursor object used to execute SQL statements.
        """
        super().__init__(**kwargs)
        
        conn = sqlite3.connect('src/components/view_record_main.db')
        c = conn.cursor()
        c.execute(
            """ 
            CREATE TABLE IF NOT EXISTS RESULTS (
                result_id INTEGER PRIMARY KEY, 
                patient_id INTEGER, 
                date_of_scan TEXT NOT NULL, 
                result TEXT NOT NULL,
                percentage REAL, 
                orig_image BLOB NOT NULL, 
                preproc_image BLOB NOT NULL, 
                grad_cam_image BLOB NOT NULL, 
                notes TEXT, 
                FOREIGN KEY(patient_id) REFERENCES PATIENT(patient_id)
            )
        """
        )

        conn.commit()
        conn.close()
    
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
        conn = sqlite3.connect('src/components/view_record_main.db')
        c = conn.cursor()
        search_input = self.ids.search_input.text

        if not search_input:
            self.ids.search_result_layout.clear_widgets()
            self.error_popup("Please fill-in the ID number of the patient")
            self.ids.search_result.text = ""
        elif not search_input.isdigit():
            self.ids.search_result_layout.clear_widgets()
            self.error_popup("Please enter a valid ID number")
            self.ids.search_result.text = ""
        else:
            self.ids.search_result.text = f"Records of Patient ID: {search_input}"
            c.execute("SELECT * FROM RESULTS WHERE patient_ID = ?", (search_input,))
            results = c.fetchall()
            if results:
                for result in results:
                    self.data_items.append(result)
                self.current_patient_id = search_input
            else:
                self.ids.search_result_layout.clear_widgets()
                self.error_popup("No ID found")
                self.ids.search_result.text = ""

        conn.close()
                
    def record_clicked(self, search_input):
        """
        Handle the event when a record is clicked.

        Parameters:
        - search_input (str): The search input to match against the records.

        Returns:
        None
        """

        for record in self.data_items:
            if record[1] == search_input:
                full_record = record
                res_id = full_record[0]

                self.manager.get_screen('patient_result').update_result(int(res_id))
                self.manager.current = 'patient_result'
                break
                    
    
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

       
    def result_popup(self, search_input):
        """
        Displays a popup window with options for the user to choose from.

        Args:
            search_input (str): The search input provided by the user.

        Returns:
            None
        """
        content = FloatLayout()
        label = Label(text="Please choose: ", size_hint=(1, 0.8), pos_hint={'x': 0, 'y': 0.2})
        self.popup = Popup(title='', content=content, auto_dismiss=False, size_hint=(0.4, 0.4))
        close_button = Button(text='X', size_hint=(0.1, 0.1), pos_hint={'right': 1, 'top': 1})
        close_button.bind(on_press=lambda instance: self.close_popup(instance))
        button_grid = GridLayout(cols=2, size_hint=(1, 0.2), pos_hint={'x': 0, 'y': 0})

        button1 = Button(text='Export Images')
        button1.bind(on_release=lambda instance: self.export_result(search_input))
        button1.bind(on_release=lambda instance: self.export_success())
        button1.bind(on_release=lambda instance: self.close_popup(instance))

        button2 = Button(text='View Result')
        button2.bind(on_release=lambda instance: self.record_clicked(search_input))
        button2.bind(on_release=lambda instance: self.close_popup(instance))

        button_grid.add_widget(button1)
        button_grid.add_widget(button2)
        content.add_widget(label)
        content.add_widget(close_button)
        content.add_widget(button_grid)
        self.popup.open()

    def export_success(self):
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
        content = BoxLayout(orientation='vertical')
        label = Label(text="Exported Successfully!")
        self.popup = Popup(title='', content=content, auto_dismiss=False, size_hint=(0.4, 0.4))
        close_button = Button(text='Close', on_press=lambda instance: self.close_popup(instance))
        content.add_widget(label)
        content.add_widget(close_button)
        self.popup.open()

    def export_result(self, search_input):
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

        conn = sqlite3.connect('src/components/view_record_main.db')
        c = conn.cursor()
        c.execute(
            """
            SELECT PATIENT.patient_ID, PATIENT.first_name, PATIENT.last_name, PATIENT.sex, PATIENT.age, PATIENT.address, 
            RESULTS.date_of_scan, RESULTS.result, RESULTS.percentage, RESULTS.notes, RESULTS.orig_image, RESULTS.preproc_image, RESULTS.grad_cam_image
            FROM PATIENT
            JOIN RESULTS ON PATIENT.patient_ID = RESULTS.patient_id
            WHERE PATIENT.patient_ID = ?
            """,
            (search_input,)
        )
        records = c.fetchall()
        
        if records:  
            for record in records:
                patient_ID = record[0]
                first_name = record[1]
                last_name = record[2]
                sex = record[3]
                age = record[4]
                address = record[5]
                date_of_scan = record[6]
                result = record[7]
                percentage = record[8]
                notes = record[9]
            
        pdf.cell(200, 10, f'Patient ID: {patient_ID}', ln=True)
        pdf.cell(200, 10, f'First Name: {first_name}', ln=True)
        pdf.cell(200, 10, f'Last Name: {last_name}', ln=True)
        pdf.cell(200, 10, f'Sex: {sex}', ln=True)
        pdf.cell(200, 10, f'Age: {age}', ln=True)
        pdf.cell(200, 10, f'Address: {address}', ln=True)
        pdf.cell(200, 10, f'Date of Scan: {date_of_scan}', ln=True)   
        pdf.cell(200, 10, f'Result: {result}', ln=True)
        pdf.cell(200, 10, f'Percentage: {percentage}', ln=True)
        pdf.cell(200, 10, f'Notes: {notes}', ln=True)

        pdf.output('assets/temp-img-location-per-view-records/patient_results.pdf')
        
        orig_image_bytes  = record[10]
        orig_image_stream = io.BytesIO(orig_image_bytes)
        orig_image = Image.open(orig_image_stream)
        orig_image.save('assets/temp-img-location-per-view-records/orig_image.jpg')
        
        preproc_image_bytes = record[11]
        preproc_image_stream = io.BytesIO(preproc_image_bytes)
        preproc_image = Image.open(preproc_image_stream)
        preproc_image.save('assets/temp-img-location-per-view-records/preproc_image.jpg')

        gradcam_image_bytes = record[12]
        gradcam_image_stream = io.BytesIO(gradcam_image_bytes)
        gradcam_image = Image.open(gradcam_image_stream)
        gradcam_image.save('assets/temp-img-location-per-view-records/gradcam_image.jpg')


    def close_popup(self, instance):
        """
        Closes the popup window.

        Parameters:
            instance (object): The instance of the button that triggered the event.

        Returns:
            None
        """
        self.popup.dismiss()
    
  
