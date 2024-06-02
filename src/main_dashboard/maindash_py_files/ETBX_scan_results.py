from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivymd.uix.button import MDRaisedButton
from kivy.properties import NumericProperty
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from main_dashboard.maindash_py_files.ETBX_full_view import xray_full_app


from components.core_functions import (
    check_image,
    crop_resize_image,
    segment_imageV2,
    check_segmented_img,
    classify_image,
    make_gradcam_heatmap,
    superimpose_heatmap,

    last_conv_layer_name,
    sqlite3,
    io,
    plt,
    np,
    Image,
    base64,
)

import sqlite3

class ScanResultData:
    def __init__(self):
        self.results = None
        self.percentage = None
        self.orig_img = None
        self.preproc_img = None
        self.gradcam_img = None
        self.notes = None
        self.is_misclassified = None

scan_result = ScanResultData()

Builder.load_file("main_dashboard/maindash_kivy_files/etbx_scan_res.kv")

class ScanResult(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_classifier = None
        self.model_segmentation = None

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

        #! START Core functionalities
        faulty_img = check_image(image_path)
        if not faulty_img[0]:
            # * Cropping and resizing image
            cropped_img = crop_resize_image(image_path)
            # * Segmentation part
            xray_orig_resized, masked_image, mask_result = segment_imageV2(
                self.model_segmentation,
                cropped_img,
                img_shape=(512, 512),
                threshold=120,
            )
            # * Check if segmentation is successful
            segment_bad = check_segmented_img(masked_image, mask_result)

            # WEAKLY APPLIED CHECKING. FOR FUTURE, TRY TO INCORPORATE POPUP
            if not segment_bad[0]:
                self.show_warning_popup(segment_bad[1])  # Displays all good so far

            else:                
                self.show_warning_popup(segment_bad[1]) # Displays waht check_segmented_img returns in the components folder

            # * Classification part
            predicted_class, predicted_score, raw = classify_image(self.model_classifier, masked_image)

            # * GradCAM part, do not include Cl;assification ==Non tuberculosis if want to mimic actual flow of program
            if predicted_class == "Tuberculosis" or predicted_class == "Non-Tuberculosis":
                # ? genearte gradcam of segmented image, but superimpose it onto original img (not yet cropped)
                heatmap = make_gradcam_heatmap(
                    masked_image, self.model_classifier, last_conv_layer_name
                )
                print(f"heatmap shape and datatype: {heatmap.shape} | {heatmap.dtype}")
                superimposed_img = superimpose_heatmap(masked_image, heatmap)

        #! END Core Functionalities

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
        self.ids.result_classnPerc.text = predicted_class + ": " +str(predicted_score)

        scan_result.results = predicted_class
        scan_result.percentage = predicted_score
        scan_result.orig_img = xray_orig
        scan_result.preproc_img = masked_image
        scan_result.gradcam_img = superimposed_img
        scan_result.notes = self.ids.notes.text

    def change_img(self, instance):
        """
        Change the displayed image based on the selected instance.

        Parameters:
            instance (kivy.uix.button.Button): The button instance that triggered the image change.

        Returns:
            None
        """

        white = (1, 1, 1, 1)
        blue = (0.1, 0.5, .9, 1)

        self.ids.x_ray.md_bg_color = white
        self.ids.x_ray.text_color = blue
        self.ids.pre_proc.md_bg_color = white
        self.ids.pre_proc.text_color = blue
        self.ids.grad_cam.md_bg_color = white
        self.ids.grad_cam.text_color = blue

        instance.md_bg_color = blue
        instance.text_color = white

        if instance == self.ids.x_ray:
            self.ids.res_img.source = xray_orig
        elif instance == self.ids.grad_cam:
            # img = Image.fromarray((superimposed_img).astype(np.uint8))
            img = superimposed_img
            # img = img.convert("RGB")
            self.ids.res_img.source = self.img_string(img)
        elif instance == self.ids.pre_proc:
            img = Image.fromarray(((1.0 - masked_image) * 255).astype(np.uint8))
            img = img.convert('L')
            self.ids.res_img.source = self.img_string(img)

    def full_view(self):
        """
        Sends float32 images to a separate python file which displays them side by side
        so that the images can be inspected and reviewed.
        """
        xrayPath = xray_orig_resized
        supIM = superimposed_img
        xray_full_app(xrayPath, supIM)

    def back_button(self):
        """
        Displays a popup window when pressing the back button
        with a confirmation message and buttons for confirming or canceling an action.
        """
        content = BoxLayout(orientation='vertical')
        with content.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=content.size, pos=content.pos)
        content.bind(size=self._update_rect, pos=self._update_rect)
        content.add_widget(Label(
            text="[b]Are you sure you want to go back?\nScan Results will be lost[/b]!",
            color=(0, 0, 1, 1), markup=True))

        inner_content = BoxLayout(orientation='horizontal', spacing=10, padding=10, size_hint_y=0.3)
        confirm_btn = Button(text='Confirm', background_color=(0, 0, 1, 1), background_normal='', on_press=self.confirm)
        cancel_btn = Button(text='Cancel', background_color=(0, 0, 1, 1), background_normal='', on_press=self.close_popup)
        inner_content.add_widget(confirm_btn)
        inner_content.add_widget(cancel_btn)
        content.add_widget(inner_content)

        self.popup = Popup(title='Confirm Action', content=content, size_hint=(0.4, 0.4),
            separator_color=(0,0,0,0), background_color=(0, 0, 1, 0.5), auto_dismiss=False)
        self.popup.open()

    def confirm(self, instance):
        """
        Resets the screen and navigates to the 'scan_img' screen after confirming an action from the popup.

        Args:
            instance: The instance of the button that triggered the confirmation.

        Returns:
            None
        """
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
        white = (1, 1, 1, 1)
        blue = (0.1, 0.5, .9, 1)

        self.ids.x_ray.md_bg_color = white
        self.ids.x_ray.text_color = blue
        self.ids.pre_proc.md_bg_color = white
        self.ids.pre_proc.text_color = blue
        self.ids.grad_cam.md_bg_color = white
        self.ids.grad_cam.text_color = blue

        self.manager.current = 'scan_img'
        self.popup.dismiss()

    def close_popup(self, instance):
        """
        Closes the popup window.

        Parameters:
        - instance: The instance of the button that triggered the event.

        Returns:
        None
        """
        self.popup.dismiss()

    def _update_rect(self, instance, value):
        """
        Update the position and size of the rectangle based on the given instance.

        Parameters:
        - instance: The instance whose position and size will be used to update the rectangle.
        - value: The new value for the instance.

        Returns:
        None
        """
        self.rect.pos = instance.pos
        self.rect.size = instance.size

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

