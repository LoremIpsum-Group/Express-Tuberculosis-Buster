from kivy.uix.screenmanager import Screen   
from kivy.lang import Builder
from tkinter import filedialog
import tkinter as tk

Builder.load_file("main_dashboard/maindash_kivy_files/etbx_scan_img.kv")
class ScanImage(Screen):
    def __init__(self, **kwargs):
        super(ScanImage, self).__init__(**kwargs)
        self.image = self.ids.image

    def load_image(self):
        file_path = self.file_dialog()
        if file_path:
            self.put_image(file_path)

    def file_dialog(self):
        root = tk.Tk()
        root.withdraw()  
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        root.destroy()  
        return file_path

    def put_image(self, file_path):
        if file_path:
            self.image.source = file_path

    #pindot process mag-gogo to, tapos display result. 
    def process_image(self):
        # Path to the image you want to predict on
        image_path = self.image.source
        self.manager.current = 'scan_result'
        self.manager.get_screen('scan_result').update_result(image_path)

    def loading_screen(self, dt):
        pass