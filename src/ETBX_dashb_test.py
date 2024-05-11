# Only for tesitng purposes, skips the login process. Run this to test the UI of main dashbvoard!

from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.core.window import Window

from main_dashboard.ETBX_main_dashboard import MainDashboard
from main_dashboard.ETBx_scan_image import ScanImage
from main_dashboard.ETBX_view_records import ViewRecords
from main_dashboard.ETBX_scan_results import ScanResult


from kivymd.app import MDApp


class MainApp(MDApp):

    def build(self):
        Window.maximize()
        self.screen_manager = ScreenManager(transition=NoTransition())        
        self.screen_manager.add_widget(MainDashboard(name="main_dashb"))
        self.screen_manager.add_widget(ScanImage(name="scan_img"))
        self.screen_manager.add_widget(ViewRecords(name="view_rec"))
        self.screen_manager.add_widget(ScanResult(name="scan_result"))
        return self.screen_manager


if __name__ == "__main__":
    MainApp().run()


# helloo
