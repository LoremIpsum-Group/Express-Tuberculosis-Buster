from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

import sqlite3

import bcrypt

from kivy.lang import Builder

Builder.load_file("onboarding_portal/onboarding_kivy_files/etbx_signup.kv")

class SignupScreen(Screen):
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
        
        conn.commit()
        conn.close()

    def signup_button(self): 
        conn = sqlite3.connect('first_db.db')
        c = conn.cursor()   
        full_name = self.ids.full_name_input.text.strip()
        email = self.ids.email_input.text.strip()
        password = self.ids.password_input.text.strip()
        confirm_password = self.ids.confirm_password.text.strip()

        

        if not full_name or not email or not password or not confirm_password:
            self.show_popup('Please fill in all fields')
            
        else:
            if password == confirm_password:
                
                c.execute('SELECT * FROM users WHERE email = ?', (email,))
                result = c.fetchone()
                if result:
                    self.show_popup('Email already used')
                else:

                    #stores the password in hashed form
                    bytePwd = password.encode('utf-8')
                    mySalt = bcrypt.gensalt()
                    hash = bcrypt.hashpw(bytePwd, mySalt)

                    c.execute('INSERT INTO users (full_name, email, password) VALUES (?, ?, ?)', (full_name, email, hash))
                    conn.commit()
                    conn.close()
                    self.show_popup("Signup Success!")
                    
                    self.ids.full_name_input.text = ''
                    self.ids.email_input.text = ''
                    self.ids.password_input.text = ''
                    self.ids.confirm_password.text = ''
                    print(f"Hashed Password: {hash}") #testing hashed password
                    self.manager.current = 'login'
            else:
                self.show_popup('Passwords do not match')
                conn.close()
            

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

# transition movement 
# def change_screen(self, direct = None):
# 		if direct is not None:
# 			self.root.ids.screen_manager.current = 'login'
# 			self.root.ids.screen_manager.transition.direction = 'right'
# 			self.root.ids.email.text = ''
# 			self.root.ids.password.text = ''

# class ETBxApp(MDApp):
#     def build(self):
#         return Builder.load_file("etbx_signup.kv")
    
#     def login(self, *args):
#         print("Loggin In")
# ETBxApp().run()
