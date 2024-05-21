from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.app import App
from kivy.metrics import dp 

from kivymd.app import MDApp

from kivymd.uix.pickers import MDDatePicker

class SaveNew(MDApp): 
    
    def show_date_picker(self, focus):
        if not focus:
            return
        
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_date_picker_save, on_cancel=self.on_date_picker_cancel)
        date_dialog.pos = [
            self.root.ids.field.center_x - date_dialog.width / 2,
            self.root.ids.field.center_y - (date_dialog.height + dp(32))
        ]
        
        date_dialog.open()
    
    def on_date_picker_save(self, instance, value, date_range):
        self.root.ids.field.text = value.strftime("%Y-%m-%d")
    
    def on_date_picker_cancel(self, instance, value):
        self.root.ids.field.focus = False

    #pass

SaveNew().run()