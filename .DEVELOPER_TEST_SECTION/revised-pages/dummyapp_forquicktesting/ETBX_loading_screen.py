# ETBX_loading_screen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

class LoadingScreen(Screen):
    def __init__(self, **kwargs):
        super(LoadingScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.label = Label(text="[b]Express Tuberculosis Buster[/b]\nis loading. Please Wait. . .", font_size=Window.width*0.05, markup=True, color = (0, 128/255, 1, 1))  
        self.layout.add_widget(self.label)
        self.add_widget(self.layout)
        Window.bind(size=self._update_font_size)

    def _update_font_size(self, instance, value):
        self.label.font_size = value[0]*0.05 
