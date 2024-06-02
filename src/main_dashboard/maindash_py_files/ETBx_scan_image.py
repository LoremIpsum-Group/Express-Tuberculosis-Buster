from kivy.uix.screenmanager import Screen   
from kivy.lang import Builder
from tkinter import filedialog
import tkinter as tk

# Temporary for popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout

from components.core_functions import check_image

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

        faulty_img = check_image(file_path)
        self.show_warning_popup(faulty_img[1])

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

    # pindot process mag-gogo to, tapos display result.
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

    def show_warning_popup(self, message):
        """
        Displays a popup with the given message.

        Parameters:
        - message (str): The message to be displayed in the popup.

        Returns:
        None
        """
        content = BoxLayout(orientation="vertical")
        label = Label(text=message)
        close_button = Button(text="Close", on_press=self.close_popup)
        content.add_widget(label)
        content.add_widget(close_button)
        self.popup = Popup(
            title="", content=content, auto_dismiss=False, size_hint=(0.4, 0.4)
        )
        self.popup.open()

    def close_popup(self, instance):
        """
        Closes the popup window.

        Parameters:
        - instance: The instance of the button that triggered the event.

        Returns:
        None
        """
        self.popup.dismiss()
