from kivy.uix.screenmanager import ScreenManager, NoTransition, FadeTransition
from kivy.core.window import Window
from kivy.config import Config

from main_dashboard.ETBX_main_dashboard import MainDashboard
from main_dashboard.ETBx_scan_image import ScanImage
from main_dashboard.ETBX_view_records import ViewRecords  
from main_dashboard.ETBX_manage_account import ManageAccount
from main_dashboard.ETBX_scan_results import ScanResult   
from main_dashboard.ETBX_view_records_patient import PatientResult  

from main_dashboard.ETBX_save_new import SaveNew
from main_dashboard.ETBX_save_existing import SaveExisting
from kivymd.app import MDApp

class MainApp(MDApp):
    Config.set('kivy', 'exit_on_escape', '0')
    def build(self):
        Window.maximize()
        self.screen_manager = ScreenManager(transition=NoTransition())
        self.screen_manager.add_widget(MainDashboard(name='main_menu'))
        self.screen_manager.add_widget(ScanImage(name='scan_img'))
        self.screen_manager.add_widget(ViewRecords(name='view_rec'))
        self.screen_manager.add_widget(ManageAccount(name='manage_account'))
        self.screen_manager.add_widget(ScanResult(name='scan_result'))
        self.screen_manager.add_widget(SaveNew(name='save_new'))
        self.screen_manager.add_widget(SaveExisting(name='save_existing'))
        self.screen_manager.add_widget(PatientResult(name='patient_result')) 

        return self.screen_manager

if __name__ == '__main__':
    MainApp().run()

