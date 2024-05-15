# Only for tesitng purposes, skips the login process. Run this to test the UI of main dashbvoard!

from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.core.window import Window

from main_dashboard.ETBX_main_dashboard import MainDashboard
from main_dashboard.ETBx_scan_image import ScanImage
from main_dashboard.ETBX_view_records import ViewRecords
from main_dashboard.ETBX_manage_account import ManageAccount

from onboarding_portal.ETBX_login import LoginScreen

from kivymd.app import MDApp


class MainApp(MDApp):

    def build(self):
        Window.maximize()
        self.screen_manager = ScreenManager(transition=FadeTransition())        
        self.screen_manager.add_widget(MainDashboard(name="main_dashb"))
        self.screen_manager.add_widget(ScanImage(name="scan_img"))
        self.screen_manager.add_widget(ViewRecords(name="view_rec"))
        self.screen_manager.add_widget(ManageAccount(name="manage_account")) 
        self.screen_manager.add_widget(LoginScreen(name="login"))
        return self.screen_manager


if __name__ == "__main__":
    MainApp().run()


# helloo
