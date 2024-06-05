from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.core.window import Window
from kivy.config import Config
from kivy.clock import Clock
from kivymd.icon_definitions import md_icons

from src.main_dashboard.maindash_py_files.ETBX_loading_screen import LoadingScreen
from src.onboarding_portal.ETBX_login_final import LoginScreen
from src.main_dashboard.maindash_py_files.ETBX_main_dashboard import MainDashboard
from src.main_dashboard.maindash_py_files.ETBX_scan_results import ScanResult
from src.main_dashboard.maindash_py_files.ETBX_save_existing import SaveExisting
from src.main_dashboard.maindash_py_files.ETBx_scan_image import ScanImage
from src.main_dashboard.maindash_py_files.ETBX_save_new import SaveNew
from src.main_dashboard.maindash_py_files.ETBX_view_records import ViewRecords
from src.main_dashboard.maindash_py_files.ETBX_view_records_patient import PatientResult

from src.components.core_functions.resource_path import resource_path

from kivymd.app import MDApp

SOFTWARE_VERSION = '1.0'

class MainApp(MDApp):
    Config.set('kivy', 'exit_on_escape', '0')
    Window.minimum_width, Window.minimum_height = (800, 600)
    def build(self):
            """
            Builds the user interface by creating and configuring the screen manager.
            
            Returns:
                ScreenManager: The configured screen manager object.
            """
            
            Window.maximize()
            self.title = "Express Tuberculosis Buster v" + SOFTWARE_VERSION 
            self.screen_manager = ScreenManager(transition=NoTransition())

            self.screen_manager.add_widget(LoadingScreen(name='loading'))

            self.screen_manager.add_widget(LoginScreen(name='login'))
            self.screen_manager.add_widget(MainDashboard(name='main_menu'))
            self.screen_manager.add_widget(ScanImage(name='scan_img'))
            self.screen_manager.add_widget(ViewRecords(name='view_rec'))
            self.screen_manager.add_widget(ScanResult(name='scan_result'))
            self.screen_manager.add_widget(SaveNew(name='save_new'))
            self.screen_manager.add_widget(SaveExisting(name='save_existing'))
            self.screen_manager.add_widget(PatientResult(name='patient_result')) 

            Clock.schedule_once(self.load_models, 7) #lmaoooo

            return self.screen_manager

    def load_models(self, dt):
        """
        Loads the machine learning models for classification and segmentation.

        Args:
            dt: The datetime object representing the current date and time.

        Returns:
            None
        """

        from src.components.core_functions import load_model_efficientNet, load_model_unet

        self.model_classifier = load_model_efficientNet(resource_path('assets\\ml-model\\efficientnetB3_V0_7_11.h5'))
        self.model_segmentation = load_model_unet(resource_path('assets\\ml-model\\unet_V0_1_7.h5'))

        scan_result_screen = self.screen_manager.get_screen('scan_result')
        scan_result_screen.model_classifier = self.model_classifier
        scan_result_screen.model_segmentation = self.model_segmentation

        self.screen_manager.current = 'login'

if __name__ == '__main__':
    MainApp().run()
