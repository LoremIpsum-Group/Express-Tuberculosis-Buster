from kivymd.app import MDApp 
from kivymd.uix.behaviors import HoverBehavior
from kivymd.uix.textfield import MDTextField
from kivy.uix.screenmanager import ScreenManager, Screen 

from kivy.lang import Builder

from ETBX_login_prefinal import LoginScreen
from ETBX_main_dashboard import MainDashboard
from ETBx_scan_image import ScanImage
from ETBX_view_records import ViewRecords 

class TestApp(MDApp):
    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(LoginScreen(name='login'))
        screen_manager.add_widget(MainDashboard(name='main_menu'))
        screen_manager.add_widget(ScanImage(name="scan_img"))
        screen_manager.add_widget(ViewRecords(name="view_rec"))


        return screen_manager

if __name__ == '__main__':
    TestApp().run()

