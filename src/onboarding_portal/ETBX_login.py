from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
import sqlite3

from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

Builder.load_file('etbx_login.kv')

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        conn = sqlite3.connect('first_db.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS users (  
                id INTEGER PRIMARY KEY,
                full_name TEXT NOT NULL, 
                email TEXT NOT NULL,
                password TEXT NOT NULL)
                """)

        # c.execute(
        #             '''
        #             INSERT INTO users (full_name, email, password)
        #             VALUES ("richard", "doctor", "apple")
        #             '''
        #         )
        conn.commit()
        conn.close()
    
    def login_button(self): 
        conn = sqlite3.connect('first_db.db')
        c = conn.cursor()   
        email = self.ids.email_input.text
        password = self.ids.password_input.text

        if email != '' and password != '':
            c.execute('SELECT password FROM users WHERE email =?', [email])
            account = c.fetchone() 
            conn.close()  
            if account: 
                if account[0] == password: 
                    self.manager.current = 'signup'
                    self.ids.email_input.text = ''
                    self.ids.password_input.text = ''
                    
                else: 
                    self.show_popup('Invalid Password')
            else:
                self.show_popup('Invalid Email')
        else: 
            self.show_popup('Please enter all the fields')

    def show_popup(self, message):
        content = BoxLayout(orientation='vertical')
        label = Label(text=message)
        close_button = Button(text='Close', on_press=self.dismiss_popup)
        content.add_widget(label)
        content.add_widget(close_button)
        self.popup = Popup(title='Test popup', content=content, auto_dismiss=False, size_hint=(0.4, 0.4))
        self.popup.open()

    def dismiss_popup(self, instance):
        self.popup.dismiss()
