from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
import sqlite3
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.clock import Clock

Builder.load_file('etbx_login_portal.kv')


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
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
    
    def login(self, screen_manager): 
            conn = sqlite3.connect('first_db.db')
            c = conn.cursor()	
            email = self.ids.email_input.text
            password = self.ids.password_input.text

            if email != '' and password != '':
                c.execute('SELECT password FROM customers WHERE email =?', [email])
                account = c.fetchone() 
                conn.close()  
                if account: 
                    if account[0] == password: 
                        print("Credentials Valid! Switching Screen")  
                        def switch_screen(dt):
                            app.root.screen_manager.current = 'signup'
                        print("Credentials Valid! Switching Screen")
                        Clock.schedule_once(switch_screen, 0.1)  
                        # popup = Popup(title='Test popup', content=Label(text='Login Successful'), auto_dismiss=False)
                        # popup.open()
                    else: 
                        popup = Popup(title='Test popup', content=Label(text='Invalid Password'), auto_dismiss=False)
                        popup.open()
                else:
                    popup = Popup(title='Test popup', content=Label(text='Invalid Email'), auto_dismiss=False)
                    popup.open()
            else: 
                popup = Popup(title='Test popup', content=Label(text='Please enter all the fields'), auto_dismiss=False)
                popup.open()         


