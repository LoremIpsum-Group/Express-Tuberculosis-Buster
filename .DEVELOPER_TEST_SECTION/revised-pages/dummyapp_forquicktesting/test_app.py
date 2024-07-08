from kivymd.app import MDApp 
from kivymd.uix.behaviors import HoverBehavior
from kivymd.uix.textfield import MDTextField
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition

from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock

from ETBX_loading_screen import LoadingScreen
from ETBX_login_prefinal import LoginScreen
from ETBX_main_dashboard import MainDashboard
from ETBx_scan_image import ScanImage
from ETBX_view_records import ViewRecords
from ETBX_scan_results import ScanResult

class TestApp(MDApp):
    def build(self):
        Window.maximize()
        self.screen_manager = ScreenManager(transition=NoTransition())
        self.screen_manager.add_widget(LoadingScreen(name="loading"))

        Clock.schedule_once(self.transition_to_login, 5)  # 5 seconds delay to simulate loading stuff

        self.screen_manager.add_widget(LoginScreen(name="login"))
        self.screen_manager.add_widget(MainDashboard(name="main_menu"))
        self.screen_manager.add_widget(ScanImage(name="scan_img"))
        self.screen_manager.add_widget(ScanResult(name="scan_result"))
        self.screen_manager.add_widget(ViewRecords(name="view_rec"))

        return self.screen_manager

    def transition_to_login(self, *args):
        # Transition to the login screen after simulating loading
        self.screen_manager.current = 'login'

if __name__ == '__main__':
    TestApp().run()
