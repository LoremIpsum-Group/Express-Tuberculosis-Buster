from kivy.uix.screenmanager import ScreenManager, FadeTransition, NoTransition
from ETBX_login import LoginScreen
from ETBX_signup import SignupScreen
from kivymd.app import MDApp

class MainApp(MDApp):
    def build(self):
        self.screen_manager = ScreenManager(transition=NoTransition())
        self.screen_manager.add_widget(LoginScreen(name='login'))
        self.screen_manager.add_widget(SignupScreen(name='signup'))
        return self.screen_manager

if __name__ == '__main__':
    MainApp().run()
