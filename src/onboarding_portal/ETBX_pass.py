from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

class ScreenOne(Screen):
    pass

class ScreenTwo(Screen):
    pass 

class WindowManager(ScreenManager):
    pass


class ETBxApp(MDApp):
    def build(self):
        return Builder.load_file("onboarding_portal/onboarding_kivy_files/etbx_pass.kv")
    

ETBxApp().run()
