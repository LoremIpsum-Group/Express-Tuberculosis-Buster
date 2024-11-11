from kivy.core.window import Window
from kivymd.uix.button import MDRaisedButton # not currently used
from kivy.uix.screenmanager import Screen

#from src.components.core_functions import resource_path

from kivy.lang import Builder

#! Resource Path 
#Builder.load_file(resource_path("src\\main_dashboard\\maindash_kivy_files\\etbx_main_dashb.kv"))

Builder.load_file("etbx_main_dashb.kv")
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
    pass

