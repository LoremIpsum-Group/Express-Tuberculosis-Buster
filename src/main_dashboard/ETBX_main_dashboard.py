from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton # not currently used
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition

from kivy.lang import Builder

class MyButton(MDRaisedButton): #not currently used
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


class MainMenu(Screen):
    pass


class ScanImage(Screen):
    
    pass


class ViewRecords(Screen):
    pass


class ManageUsers(Screen):
    pass


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
        Builder.load_file("m_dashb_2.kv")

        self.screen_manager = ScreenManager(transition=NoTransition())
        self.screen_manager.add_widget(MainMenu(name="main_menu"))
        self.screen_manager.add_widget(ScanImage(name="scan_img"))
        self.screen_manager.add_widget(ViewRecords(name="view_rec"))
        self.screen_manager.add_widget(ManageUsers(name="manage_users"))

        return self.screen_manager


def run_main_dashboard():
    """
    Runs the main dashboard of the application. For simple integration when switching panels
    """
    MainDashboard().run()

if __name__ == "__main__":
    run_main_dashboard()
