from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

import sqlite3


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
        full_name = self.ids.full_name_input.text
        email = self.ids.email_input.text
        password = self.ids.password_input.text
        confirm_password = self.ids.confirm_password.text

        if not full_name or not email or not password or not confirm_password:
            self.show_popup('Please fill in all fields')
            
        else:
            if password == confirm_password:
                
                c.execute('SELECT * FROM users WHERE email = ?', (email,))
                result = c.fetchone()
                if result:
                    self.show_popup('Email already used')
                else:
                    c.execute('INSERT INTO users (full_name, email, password) VALUES (?, ?, ?)', (full_name, email, password))
                    conn.commit()
                    conn.close()
                    self.show_popup("Signup Success!")
                    
                    self.ids.full_name_input.text = ''
                    self.ids.email_input.text = ''
                    self.ids.password_input.text = ''
                    self.ids.confirm_password.text = ''

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
