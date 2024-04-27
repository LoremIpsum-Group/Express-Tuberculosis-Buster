from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton

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

        screen = MDScreen()

        button1 = MyButton(
                text="Hello, This is the first button",
                pos_hint={"x": 0, "center_y": 0.7},
        )

        button2 = MyButton(
                text="Hello, This is the second button",
                pos_hint={"x": 0, "center_y": 0.6},
        )

        button3 = MyButton(
                text="Hello, This is the third button",
                pos_hint={"x": 0, "center_y": 0.5},
        )

        screen.add_widget(button1)
        screen.add_widget(button2)
        screen.add_widget(button3)
        return screen

MainDashboard().run()
