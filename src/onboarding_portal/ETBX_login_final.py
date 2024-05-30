from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

Builder.load_file('src/onboarding_portal/onboarding_kivy_files/etbx_login_final.kv')

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    
    def login_button(self): 
        username_input = self.ids.username_input.text
        password_input = self.ids.password_input.text

        if username_input != '' and password_input != '':
            if username_input == "doctor" and password_input == "apple":
                self.manager.current = 'main_menu'
                print("Login Successful")
            
            elif username_input != "doctor":
                self.show_popup('Invalid Username')
            
            elif password_input != "apple":
                self.show_popup('Invalid Password')

            elif username_input != "doctor" and password_input != "apple":
                self.show_popup('Invalid Username and Password')

        else:
            self.show_popup('Please enter all the fields')

    def forgot_password(self):
        self.ids.username_input.clear_widgets()
        self.ids.password_input.clear_widgets()
        self.forgot_password_popup('Please contact: Venz Salvatierra \nContact Number: 09123456789 \nEmail: venz@gmail.commie')

    
    def forgot_password_popup(self, message):
        content = BoxLayout(orientation='vertical')
        label = Label(text=message)
        close_button = Button(text='Close', on_press=self.dismiss_popup)
        content.add_widget(label)
        content.add_widget(close_button)
        self.popup = Popup(title='', content=content, auto_dismiss=False, size_hint=(0.4, 0.4))
        self.popup.open()
         

    def show_popup(self, message):
        content = BoxLayout(orientation='vertical')
        label = Label(text=message)
        close_button = Button(text='Close', on_press=self.dismiss_popup)
        content.add_widget(label)
        content.add_widget(close_button)
        self.popup = Popup(title='', content=content, auto_dismiss=False, size_hint=(0.4, 0.4))
        self.popup.open()

    def dismiss_popup(self, instance):
        self.popup.dismiss()
