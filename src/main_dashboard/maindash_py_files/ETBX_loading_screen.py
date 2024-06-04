# ETBX_loading_screen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class LoadingScreen(Screen):
    def __init__(self, **kwargs):
        super(LoadingScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.label = Label(text="ETBX Loading. Please Wait. . .", font_size='80sp', color = (0, 128/255, 1, 1))  
        self.layout.add_widget(self.label)
        self.add_widget(self.layout)
