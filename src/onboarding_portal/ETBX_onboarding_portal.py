from kivymd.app import MDApp 
from kivymd.uix.behaviors import HoverBehavior
from kivymd.uix.textfield import MDTextField


import sqlite3
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label

class ETBxApp(MDApp):
    def build(self):
            conn = sqlite3.connect('first_db.db')
            c = conn.cursor()
            c.execute("""CREATE TABLE IF NOT EXISTS customers (  
                    email TEXT,
                    password TEXT)
                """)

            #default user
            c.execute(
                    '''
                    INSERT INTO customers (email, password)
                    VALUES ("doctor", "apple")
                    '''
                )
            conn.commit()
            conn.close()
            return Builder.load_file('etbx.kv') 
	
    def login(self): 
            conn = sqlite3.connect('first_db.db')
            c = conn.cursor()	
            email = self.root.ids.email_input.text
            password = self.root.ids.password_input.text

            if email != '' and password != '':
                c.execute('SELECT password FROM customers WHERE email =?', [email])
                account = c.fetchone() 
                conn.close()  
                if account: 
                    if account[0] == password: 
                        popup = Popup(title='Test popup', content=Label(text='Login Successful'), auto_dismiss=False)
                        popup.open()
                    else: 
                        popup = Popup(title='Test popup', content=Label(text='Invalid Password'), auto_dismiss=False)
                        popup.open()
                else:
                    popup = Popup(title='Test popup', content=Label(text='Invalid Email'), auto_dismiss=False)
                    popup.open()
            else: 
                popup = Popup(title='Test popup', content=Label(text='Please enter all the fields'), auto_dismiss=False)
                popup.open() 
    




ETBxApp().run()
