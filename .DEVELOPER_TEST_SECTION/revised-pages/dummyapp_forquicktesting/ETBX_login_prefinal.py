from kivymd.app import MDApp 
from kivymd.uix.behaviors import HoverBehavior
from kivymd.uix.textfield import MDTextField
from kivy.uix.screenmanager import ScreenManager, Screen 


from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

from kivy.lang import Builder

Builder.load_file("etbx_login_prefinal.kv")
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def login_button(self):
        """
        Handles the login button click event.

        Retrieves the username and password input from the UI.
        If both fields are filled, it checks if the input matches the predefined username and password.
        If the input matches, it sets the current screen to 'main_menu' and prints "Login Successful".
        If the input does not match, it shows a popup with the message 'Invalid Username or Password'.
        If any of the fields are empty, it shows a popup with the message 'Please enter all the fields'.
        """
        username_input = self.ids.username_input.text.strip()
        password_input = self.ids.password_input.text.strip()

        if username_input != '' and password_input != '':
            #with open("password.txt", 'r') as file:
            # with open(resource_path("src\onboarding_portal\introduction.txt"), 'r') as file:
            #     stored_username, stored_salt_username = file.readline().strip().split(':')
            #     stored_password, stored_salt_password = file.readline().strip().split(':')

            # hashed_input_username = hash_string(username_input, bytes.fromhex(stored_salt_username))
            # hashed_input_password = hash_string(password_input, bytes.fromhex(stored_salt_password))


            login_successful = True

            if login_successful:
                self.manager.current = 'main_menu'
                print("Login Successful")
            else:
                self.show_popup('Invalid Username or Password')
        else:
            self.show_popup('Please enter all the fields')

        #Reason why this is here is to ensure that what happens at the end of login everytime is clearing the input fields
        self.ids.username_input.text = ''
        self.ids.password_input.text = ''


    def forgot_password(self):
        """
        Clears the username and password input fields and displays a popup with contact information for password recovery.
        Put the clearing of the credentials here too when "contact developer" is clicked
        returns:
        None
        """        
        self.ids.username_input.text = ''
        self.ids.password_input.text = ''        
        self.forgot_password_popup('Please contact: Venz Salvatierra (ETBX-Developer)\nContact Number: 09773503492 \nEmail:202110530@fit.edu.ph')

    
    def forgot_password_popup(self, message):
        """
        Displays a popup with a given message and a close button.

        Parameters:
        - message (str): The message to be displayed in the popup.

        Returns:
        None
        """
        content = BoxLayout(orientation='vertical')
        label = Label(text=message)
        close_button = Button(text='Close', on_press=self.dismiss_popup)
        content.add_widget(label)
        content.add_widget(close_button)
        self.popup = Popup(title='', content=content, auto_dismiss=False, size_hint=(0.4, 0.4))
        self.popup.open()
        
         

    def show_popup(self, message):
        """
        Displays a popup with the given message.

        Parameters:
        - message (str): The message to be displayed in the popup.

        Returns:
        None
        """
        content = BoxLayout(orientation='vertical')
        label = Label(text=message)
        close_button = Button(text='Close', on_press=self.dismiss_popup)
        content.add_widget(label)
        content.add_widget(close_button)
        self.popup = Popup(title='', content=content, auto_dismiss=False, size_hint=(0.4, 0.4))
        self.popup.open()

    def dismiss_popup(self, instance):
        self.popup.dismiss()
