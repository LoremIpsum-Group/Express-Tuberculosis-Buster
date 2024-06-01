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
        """
        Loads an image from a file path selected using a file dialog.
        If a file path is selected, the image is displayed using the put_image method.
        """
        file_path = self.file_dialog()
        if file_path:
            self.put_image(file_path)

    def file_dialog(self):
        """
        Opens a file dialog to select an image file.

        Returns:
            str: The path of the selected image file.
        """
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
        """
        Process the image and update the scan result screen.

        This method is responsible for switching to the scan_results screen
        while also sending the relevant image path
        of the image that is to be predicted upon.

        It retrieves the image path from the `image.source` attribute
        and sets the current screen to 'scan_result'. It then calls the `update_result` method
        of the 'scan_result' screen to update the result with the image path.

        Parameters:
        None

        Returns:
        None
        """
        image_path = self.image.source
        self.manager.current = 'scan_result'
        self.manager.get_screen('scan_result').update_result(image_path)

    def loading_screen(self, dt):
        """
        Future loading screen, still figuring out how.
        """
        pass