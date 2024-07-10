from kivy.uix.screenmanager import Screen   
from kivy.lang import Builder
from tkinter import filedialog
import tkinter as tk
# Temporary for popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout

from src.components.core_functions import (
    resource_path, 
    check_image,
    Image,
    io,
    base64,
    np,
    cv2,
    dicom_processor as dcmp,
    os
)

is_dicom = None 
dicom_image = None 

class DicomFile:
    def __init__(self):
        self.file_path = None 

dicom_file = DicomFile()

Builder.load_file(resource_path("src\\main_dashboard\\maindash_kivy_files\\etbx_scan_img.kv"))
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
            file_path = resource_path(file_path)
            self.put_image(file_path)

            if self.is_dicom_file(file_path):
                image = dcmp.extract_image(file_path) # np.ndarray
                image = cv2.resize(image, (512, 512))
                image = Image.fromarray((image). astype(np.uint8))
                if os.path.isfile(resource_path("dicom_image.png")): 
                    os.remove(resource_path("dicom_image.png"))
                image.save(resource_path("dicom_image.png"))
                faulty_img = check_image(resource_path("dicom_image.png"))
            else:    
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
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.dcm;*.dicom")])
        root.destroy()  
        if not file_path:
            pass
        else: 
            return resource_path(file_path)

    def put_image(self, file_path):
        global dicom_file_path, is_dicom, dicom_image 

        if file_path:
            if self.is_dicom_file(file_path):
                dicom_file.file_path = file_path
                image = dcmp.extract_image(file_path) # np.ndarray
                image = cv2.resize(image, (512, 512))
                image = Image.fromarray((image). astype(np.uint8))
                self.image.source = self.img_string(image)
                is_dicom = True 
            else:            
                self.image.source = file_path
                is_dicom = False
             
     

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
        if resource_path(self.image.source) == resource_path("assets/jpg.png"):
            self.show_warning_popup("Please load an image first.")
            return

        if is_dicom:
            image_path = resource_path("dicom_image.png")
        else:
            image_path = resource_path(self.image.source)
        self.manager.current = 'scan_result'
        print(image_path)
        self.manager.get_screen('scan_result').update_result(image_path, is_dicom)

    def loading_screen(self, dt):
        """
        Future loading screen, still figuring out how.
        """
        pass

    def img_string(self, image):
        """
        Changes the displayed image based on the selected instance. In-depth procedure:
        1. Save PIL Image to BytesIO object. A BytesIO object is like a file object, but it resides in memory instead of being saved to disk.
        2. Retrieve the contents of the BytesIO object as a bytes string using the `getvalue` method.
        3. Encode the bytes string into base64 format. Base64 encoding is a way of converting binary data into text format, which is needed because `img.source` expects a string.
        4. Convert the string into a data URL by adding the prefix 'data:image/png;base64,'. A data URL is a URI scheme that allows you to include data in-line in web pages as if they were external resources.
        """
        with io.BytesIO() as output:
            image.save(output, format="PNG")
            contents = output.getvalue()

        img_data = base64.b64encode(contents).decode('ascii')
        return 'data:image/png;base64,' + img_data 
   

    def is_dicom_file(self, file_path):
        return file_path.endswith('.dcm') or file_path.endswith('.dicom')

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

    def logout(self, instance):
        self.popup.dismiss()
        self.manager.current = 'login'

    def logout_popup(self):
        """
        Displays a popup with a given message and a close button.

        Parameters:
        - message (str): The message to be displayed in the popup.

        Returns:
        None
        """
        content = BoxLayout(orientation='vertical')
        label = Label(text="Are you sure you want to logout?")
        confirm_button = Button(text="Confirm", on_press=self.logout)
        close_button = Button(text='Close', on_press=self.close_popup)
        content.add_widget(label)
        content.add_widget(confirm_button)

        content.add_widget(close_button)
        self.popup = Popup(title='', content=content, auto_dismiss=False, size_hint=(0.4, 0.4))
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
