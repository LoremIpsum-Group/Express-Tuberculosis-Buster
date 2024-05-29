from kivy.uix.screenmanager import Screen   
from kivy.lang import Builder
from kivymd.uix.button import MDRaisedButton   
from kivy.properties import NumericProperty
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from main_dashboard.ETBX_full_view import xray_full_app

from components.core_functions import (
    load_model_efficientNet,
    load_model_unet,
    segment_image,
    predict,
    get_gradCAM,
    sqlite3,
    io,
    plt,
    np,
    Image,
    base64
)

import sqlite3
class ScanResultData: 
    """
        A class that stores information about results of scanned X-ray 
        for database storage 
    """

    def __init__(self):
        self.results = None 
        self.percentage = None 
        self.orig_img = None 
        self.preproc_img = None
        self.gradcam_img = None 
        self.notes = None 
        self.is_misclassified = None

scan_result = ScanResultData() 

# Load the trained model
model_classifier = load_model_efficientNet('assets/ml-model/efficientnetB3_V0_6_1.h5')
model_segmentation = load_model_unet('assets/ml-model/unet_V0_1_3.h5')

Builder.load_file("main_dashboard/maindash_kivy_files/etbx_scan_res.kv")

scan_results = ScanResultData()
class ScanResult(Screen):
    """
    Represents a screen for displaying scan results.

    Attributes:
        None

    Methods:
        update_result(image_path): Updates the scan result with the provided image path.
        change_img(instance): Changes the displayed image based on the selected instance.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        conn = sqlite3.connect('src/components/view_record_main.db')
        c = conn.cursor()
        c.execute(
            """ 
            CREATE TABLE IF NOT EXISTS RESULTS (
                result_id INTEGER PRIMARY KEY, 
                patient_id INTEGER, 
                date_of_scan TEXT NOT NULL, 
                result TEXT NOT NULL,
                percentage REAL, 
                orig_image BLOB NOT NULL, 
                preproc_image BLOB NOT NULL, 
                grad_cam_image BLOB NOT NULL, 
                notes TEXT, 
                misclassified BOOLEAN, 
                FOREIGN KEY(patient_id) REFERENCES PATIENT(patient_id)
            )
        """
        )
        
        conn.commit()
        conn.close()

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
        pass
    
    def update_result(self, image_path):
        """
        Updates the scan result with the provided image path.

        Args:
            image_path (str): The path to the image file.

        Returns:
            None
        """
        global xray_orig, xray_orig_resized, superimposed_img, masked_image
        xray_orig = image_path
        self.ids.res_img.source = xray_orig
        self.ids.x_ray.md_bg_color = (0.1, 0.5, .9, 1)
        self.ids.x_ray.text_color = (1, 1, 1, 1)

        # !CORE FUNCTIONALITIES - START
        # Get segmented/masked image
        xray_orig_resized, masked_image, mask_result = segment_image(
             model_segmentation, image_path
        )

        # Get Score from segmented image
        predicted_class, predicted_score = predict(model_classifier, masked_image)

        # Superimpose heatmap of segmented image onto original image
        superimposed_img = get_gradCAM(model_classifier, xray_orig_resized, masked_image)

        # !CORE FUNCTIONALITIES - end
        # *DEBUGGING PURPOSES, removable any time
        # preprocessed_img = get_img_array_OLD(masked_image)
        # predicted_class, predicted_score = predict(model_classifier, preprocessed_img)
        # superimposed_img = get_gradCAM_NONSEGMENTED(model_classifier, original_image)
        # * Replace here the image you want to display, temporary ONLY!!!!!
        # Good results: normal 2551, tuberculosis 640


        bar_color = None
        if (predicted_score <= 25):
            bar_color = (0, 1, 0, 1)
        elif (predicted_score <= 49):
            bar_color = (1, 1, 0, 1)
        elif (predicted_score <= 74):
            bar_color = (1, 0.5, 0, 1)
        else:
            bar_color = (1, 0, 0, 1)

        self.percentage = int(predicted_score)
        self.percentage_color = bar_color
        self.ids.result_classnPerc.text = predicted_class + ": " +str(predicted_score) + " %\n segmented datatype: " + str(masked_image.dtype)

        scan_result.results = predicted_class
        scan_result.percentage = predicted_score
        scan_result.orig_img = xray_orig
        scan_result.preproc_img = masked_image 
        scan_result.gradcam_img = superimposed_img
        scan_result.notes = self.ids.notes.text

    def change_img(self, instance):
        white = (1, 1, 1, 1)  # Default color
        blue = (0.1, 0.5, .9, 1)  # Pressed color

        # Reset all buttons to default color
        self.ids.x_ray.md_bg_color = white
        self.ids.x_ray.text_color = blue
        self.ids.pre_proc.md_bg_color = white
        self.ids.pre_proc.text_color = blue
        self.ids.grad_cam.md_bg_color = white
        self.ids.grad_cam.text_color = blue

        # Change the pressed button's color
        instance.md_bg_color = blue
        instance.text_color = white

        if instance == self.ids.x_ray:
            self.ids.res_img.source = xray_orig
            pass

        elif instance == self.ids.grad_cam:
            img = Image.fromarray((superimposed_img) .astype(np.uint8))
            img = img.convert("RGB")            
                     
            self.ids.res_img.source = self.img_string(img)  
            pass 

        elif instance == self.ids.pre_proc: 
            img = Image.fromarray(((1.0 - masked_image) * 255).astype(np.uint8))
            img = img.convert('L')
            

            self.ids.res_img.source = self.img_string(img) 

        else:
            pass

    def back_button(self):
        white = (1, 1, 1, 1)  # Default color
        blue = (0.1, 0.5, .9, 1)  # Pressed color

        self.ids.x_ray.md_bg_color = white
        self.ids.x_ray.text_color = blue
        self.ids.pre_proc.md_bg_color = white
        self.ids.pre_proc.text_color = blue
        self.ids.grad_cam.md_bg_color = white
        self.ids.grad_cam.text_color = blue

        self.show_popup()
        
        pass


    def full_view(self):
        xrayPath = xray_orig_resized
        supIM = superimposed_img

        xray_full_app(xrayPath, supIM)
        pass

    def show_popup(self):
        content = BoxLayout(orientation='vertical')
        with content.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=content.size, pos=content.pos)
        content.bind(size=self._update_rect, pos=self._update_rect)
        content.add_widget(Label(
            text="[b]Are you sure you want to go back?\nScan Results will be lost[/b]!", 
            color=(0, 0, 1, 1), markup=True))
        
        inner_content = BoxLayout(orientation='horizontal',
            spacing=10, padding=10, size_hint_y=0.3)

        confirm_btn = Button(text='Confirm',
            background_color=(0, 0, 1, 1), background_normal='',
            on_press= self.confirm)
        
        cancel_btn = Button(text='Cancel',
            background_color=(0, 0, 1, 1), background_normal='',
            on_press= self.close_popup)
        
        inner_content.add_widget(confirm_btn)
        inner_content.add_widget(cancel_btn)
        content.add_widget(inner_content)

        
        #content.add_widget(Button(text="Close", on_press=self.close_popup))
        
        self.popup = Popup(title='Confirm Action', content=content, size_hint=(0.4, 0.4),
            separator_color=(0,0,0,0), background_color=(0, 0, 1, 0.5),auto_dismiss=False)
        self.popup.open()
    
    def confirm(self, instance):
        save_new_screen = self.manager.get_screen('save_new')
        save_existing_screen = self.manager.get_screen('save_existing')
        save_new_screen.ids.patient_id.text = ''
        save_new_screen.ids.first_name.text = ''
        save_new_screen.ids.last_name.text = ''
        save_new_screen.ids.birthdate.text = ''
        save_new_screen.ids.address.text = ''
        save_new_screen.ids.male.active = False
        save_new_screen.ids.female.active = False
        self.manager.get_screen('scan_result').ids.notes.text = ''
        self.ids.misclassified.active = False
        self.manager.get_screen('save_existing').ids.patient_id.text = ''
        self.manager.get_screen('save_existing').ids.patient_search_result.clear_widgets()
        self.manager.get_screen('save_existing').ids.patient_search_result.add_widget(
                Label(text="[b]Search Patient ID to save[/b]", 
                      pos_hint={'center_x': 0.5, 'center_y': 0.5},
                      color=(0, 0, 0, 1), markup=True)
        )
        self.manager.current = 'scan_img'
        self.popup.dismiss()
        
    def close_popup(self, instance):
        self.popup.dismiss()
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
   
