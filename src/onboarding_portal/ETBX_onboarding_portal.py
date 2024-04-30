from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from ETBX_login_portal import LoginScreen
from kivymd.app import MDApp


'''
MainAppp class  builds application
'''
class MainApp(MDApp):
    def build(self):
        self.screen_manager = ScreenManager()
        login_screen = LoginScreen(name='login')
        self.screen_manager.add_widget(LoginScreen)
        return self.screen_manager
    
    def login(self, screen): 
        self.screen_manager.get_screen('login').login(screen)

if __name__ == '__main__':
    MainApp().run()

# from kivy.app import App
# from kivy.uix.screenmanager import ScreenManager, Screen
# from login import LoginScreen
# from signup import SignupScreen
# from kivymd.app import MDApp


# class MainApp(MDApp):
#     def build(self):
#         self.screen_manager = ScreenManager()
#         self.screen_manager.add_widget(LoginScreen(name='login'))
#         self.screen_manager.add_widget(SignupScreen(name='signup'))
#         return self.screen_manager

# if __name__ == '__main__':
#     MainApp().run()
