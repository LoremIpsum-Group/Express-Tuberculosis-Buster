from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton

from kivy.lang import Builder

class MyButton(MDRaisedButton):
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


class MainDashboard(MDApp):
    """
    The main dashboard of the application.

    This class represents the main dashboard of the application. It inherits from the `MDApp` class provided by the KivyMD library.

    Attributes:
        theme_cls (ThemeManager): The theme manager for the application.
        icon (str): The path to the application's icon file.

    Methods:
        build(): Builds the main dashboard user interface. Returns an MDScreen

    """

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        self.icon = "assets\lung-temporary-logo.ico"

        return Builder.load_file('m_dashb.kv')

MainDashboard().run()
