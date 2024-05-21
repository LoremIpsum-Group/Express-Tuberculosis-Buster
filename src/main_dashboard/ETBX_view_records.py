from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup

from kivymd.uix.button import MDRectangleFlatButton

#tkinter popup
# from tkinter import *
# from tkinter import ttk
# win = Tk()


import sqlite3

Builder.load_file("main_dashboard/maindash_kivy_files/etbx_view_rcrds.kv")
class ViewRecords(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        conn = sqlite3.connect('src/components/view_record_main.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS main_table (  
                result_ID INTEGER,
                patient_ID INTEGER,
                date_of_scan TEXT,
                result TEXT, 
                percentage TEXT, 
                UNIQUE(patient_ID, date_of_scan, result, percentage))
                """)
        
        # working table but keeps on adding
        # c.execute("""CREATE TABLE IF NOT EXISTS main_table (  
        #         result_ID INTEGER NOT NULL,
        #         patient_ID INTEGER NOT NULL,
        #         date_of_scan TEXT NOT NULL,
        #         result TEXT NOT NULL, 
        #         percentage TEXT NOT NULL)
        #         """)
        
        c.execute(
                    '''
                    INSERT OR IGNORE INTO main_table (result_ID, patient_ID, date_of_scan, result, percentage)
                    VALUES ("1728", "1106", "2021-1-1-", "Non-TB", "0.00"),
                           ("1729", "1106", "2021-2-1", "Tuberculosis", "75.00"),
                           ("1730", "1106", "2021-3-1-", "Non-TB", "49.00");
                    '''
                )


        conn.commit()
        conn.close()
    
    def search_button (self): 
        conn = sqlite3.connect('src/components/view_record_main.db') 
        c = conn.cursor()
        search_input = self.ids.search_input.text

        if not search_input:
            self.show_popup("Please fill-in the ID number of the patient")

        elif not search_input.isdigit():
            self.show_popup("Please enter a valid ID number")


        #testing of multiple clickable tables per match result
        else:
            c.execute("SELECT result, date_of_scan FROM main_table WHERE patient_ID = ?", (search_input,))
            results = c.fetchall()
            if results:
                for result in results:

                    button = MDRectangleFlatButton(
                        text=f"Result: {result[0]:<20} Date of Scan: {result[1]}\n\n",
                        theme_text_color="Custom",
                        text_color=[0, 0, 0, 1],
                        size_hint=(0.3, 0.1)
                    )

                    self.ids.search_result_layout.add_widget(button)

                   
            else:
                no_results_label = Label(text="No ID found")
                self.ids.search_result_layout.add_widget(no_results_label)


        #working code 
        # else:
        #     c.execute("SELECT result, date_of_scan FROM main_table WHERE patient_ID = ?", (search_input,))
        #     results = c.fetchall()
        #     if results:
        #         self.ids.search_result.text =""
        #         for result in results:
        #             self.ids.search_result.text += f"Result: {result[0]:<20} Date of Scan: {result[1]}\n\n"
        #     else:
        #         self.ids.search_result.text ="No ID found"              
        #         #if want popup style na warning
        #         # self.show_popup("No ID found")
    
    
    
    
    #tkinter popup
    # def open_popup(self):
    #     top= Toplevel(win)
    #     top.geometry("750x250")
    #     top.title("Child Window")
    #     Label(top, text= "Select from the two", font=('Mistral 18 bold')).place(x=150,y=80)
       
       

    def show_popup(self, message):
        content = BoxLayout(orientation='vertical')
        label = Label(text=message)
        close_button = Button(text='Close', on_press=self.dismiss_popup)
        content.add_widget(label)
        content.add_widget(close_button)
        self.popup = Popup(title= '', content=content, auto_dismiss=False, size_hint=(0.4, 0.4))
        self.popup.open()

    def dismiss_popup(self, instance):
        self.popup.dismiss()    

   


# win.mainloop()


    #pass

    #plain text result
    # def search_button (self): 
    #     conn = sqlite3.connect('src/components/view_record_main.db') 
    #     c = conn.cursor()
    #     search_input = self.ids.search_input.text

    #     if not search_input:
    #         self.show_popup("Please fill-in the ID number of the patient")

    #     elif not search_input.isdigit():
    #         self.show_popup("Please enter a valid ID number")

    #     else:
    #         c.execute("SELECT result, date_of_scan FROM main_table WHERE patient_ID = ?", (search_input,))
    #         results = c.fetchall()
    #         if results:
    #             self.ids.search_result.text =""
    #             for result in results:
    #                 self.ids.search_result.text += f"Result: {result[0]:<20} Date of Scan: {result[1]}\n\n"
    #         else:
    #             self.ids.search_result.text ="No ID found"                
    #             # self.show_popup("No ID found")
