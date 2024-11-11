from kivy.core.window import Window
from kivymd.uix.button import MDRaisedButton # not currently used
from kivy.uix.screenmanager import Screen

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup

from src.components.core_functions import resource_path

from kivy.lang import Builder

Builder.load_file(resource_path("src\\main_dashboard\\maindash_kivy_files\\etbx_main_dashb.kv"))
class MyButton(MDRaisedButton): # CURRENTLY ONLY USED FOR THE TEMPORARY LOGOUT BUTTON, for removal if ever
    """
    A custom button class that changes the system cursor to 'hand' when the mouse is over the button.

    Inherits from MDRaisedButton. This means all instantiations of this button are designed like this.
    Adjustable in the future

    Attributes:
        None

    Methods:
        __init__(self, **kwargs): Initializes the MyButton object.
        on_mouseover(self, window, pos): Changes the system cursor to 'hand' when the mouse is over the button.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouseover)

    def on_mouseover(self, window, pos):
        if self.collide_point(*pos):
            Window.set_system_cursor('hand')
        else:
            Window.set_system_cursor('arrow')



class MainDashboard(Screen):
    def logout(self, instance):
        self.popup.dismiss()
        self.manager.current = 'login'

    def logout_popup(self):
        """
        Displays a popup with a given message and a close button.

        Parameters:
        - message (str): The message to be displayed in the popup.

        Returns:
        None
        """
        content = BoxLayout(orientation='vertical')
        label = Label(text="Are you sure you want to logout?")
        confirm_button = Button(text="Confirm", on_press=self.logout)
        close_button = Button(text='Close', on_press=self.close_popup)
        content.add_widget(label)
        content.add_widget(confirm_button)

        content.add_widget(close_button)
        self.popup = Popup(title='', content=content, auto_dismiss=False, size_hint=(0.4, 0.4))
        self.popup.open()

    def close_popup(self, instance):
        """
        Closes the popup window.

        Parameters:
        - instance: The instance of the button that triggered the event.

        Returns:
        None
        """
        self.popup.dismiss()
