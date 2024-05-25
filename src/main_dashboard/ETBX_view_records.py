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

import sqlite3

Builder.load_file("main_dashboard/maindash_kivy_files/etbx_view_rcrds.kv")
class ViewRecords(Screen):

    data_items = ListProperty([]) 
    current_patient_id = StringProperty("")  # To store the current patient ID

    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        conn = sqlite3.connect('src/components/view_record_main.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS main_table (  
                result_ID INTEGER,
                patient_ID INTEGER PRIMARY KEY,
                date_of_scan TEXT,
                result TEXT, 
                percentage TEXT, 
                UNIQUE(patient_ID))
                """)
        
        # c.execute("DROP TABLE main_table") 
        #dummy records for testing
        c.execute(
                    '''
                    INSERT OR IGNORE INTO main_table (result_ID, patient_ID, date_of_scan, result, percentage)
                    VALUES ("1728", 1106, "2021-1-1-", "Non-TB", "0.00"),
                           ("1729", 1106, "2021-2-1", "Tuberculosis", "75.00"),
                           ("1730", 1106, "2021-3-1-", "Non-TB", "49.00");
                    '''
                )
        conn.commit()
        conn.close()
    
    def search_button (self): 
        self.data_items.clear()
        conn = sqlite3.connect('src/components/view_record_main.db') 
        c = conn.cursor()
        search_input = self.ids.search_input.text

        if not search_input:
            self.ids.search_result_layout.clear_widgets()
            self.error_popup("Please fill-in the ID number of the patient")
            self.ids.search_result.text =""

        elif not search_input.isdigit():
            self.ids.search_result_layout.clear_widgets()
            self.error_popup("Please enter a valid ID number")
            self.ids.search_result.text =""

        #testing of multiple clickable tables per match result
        else:
            self.ids.search_result.text = f"Records of Patient ID: {search_input}"
            c.execute("SELECT result, date_of_scan, patient_ID FROM RESULTS WHERE patient_ID = ?", (search_input,))
            results = c.fetchall()

            if results:  
                for result in results:
                    self.data_items.append((result[0], result[1], result[2])) 
                self.current_patient_id = search_input
            else:
                self.ids.search_result_layout.clear_widgets()
                self.ids.search_result.text ="No ID found"
        
        conn.close()
                
    # def record_clicked(self, patient_id):
    #     conn = sqlite3.connect('src/components/view_record_main.db')
    #     c = conn.cursor()
    #     c.execute("SELECT * FROM RESULTS WHERE patient_ID = ?", (patient_id,))
    #     record = c.fetchone()
    #     conn.close()
        
    #     if record:
    #         message = f"Result ID: {record[0]}\n  Patient ID: {record[1]}\n  Date of Scan: {record[2]}\n  Result: {record[3]}\n  Percentage: {record[4]} "
    #         self.error_popup(message)
    #     else:
    #         self.error_popup("Record not found")
    
    #popup for invalid inputs 
    def error_popup(self, message):
        content = BoxLayout(orientation='vertical')
        label = Label(text=message)
        self.popup = Popup(title= '', content=content, auto_dismiss=False, size_hint=(0.4, 0.4))
        close_button = Button(text='Close', on_press=lambda instance: self.close_popup(instance))
        content.add_widget(label)
        content.add_widget(close_button)
        self.popup.open()

       
    #popup for search results
    def result_popup(self, patient_id):
        content = FloatLayout()
        label = Label(text="Please choose: ", size_hint=(1, 0.8), pos_hint={'x': 0, 'y': 0.2})
        self.popup = Popup(title='', content=content, auto_dismiss=False, size_hint=(0.4, 0.4))
        close_button = Button(text='X', size_hint=(0.1, 0.1), pos_hint={'right': 1, 'top': 1})
        close_button.bind(on_press=lambda instance: self.close_popup(instance))
        button_grid = GridLayout(cols=2, size_hint=(1, 0.2), pos_hint={'x': 0, 'y': 0})

        button1 = Button(text='Export Images')
        #button1.bind(on_release=lambda instance: self.record_clicked(patient_id))

        button2 = Button(text='View Result')
        button2.bind(on_release=lambda instance: self.record_clicked(patient_id))

        button_grid.add_widget(button1)
        button_grid.add_widget(button2)
        content.add_widget(label)
        content.add_widget(close_button)
        content.add_widget(button_grid)
        self.popup.open()

    def close_popup(self, instance):
        self.popup.dismiss()
    
  
